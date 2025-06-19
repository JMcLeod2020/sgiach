# ==============================================================================
# SGIACH COMPREHENSIVE INTEGRATION - COMPLETE IMPLEMENTATION
# SkyeBridge Consulting & Developments Inc.
# Professional Engineering Platform Enhancement
# Jeff McLeod, P.Eng - Technical Lead
# ==============================================================================

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import json
import math
from datetime import datetime, date
from enum import Enum
import pandas as pd
import requests
import asyncio

# ==============================================================================
# ENHANCED DATA MODELS
# ==============================================================================

class ValidationStatus(str, Enum):
    MUNICIPAL = "municipal"
    PARTIAL = "partial" 
    PENDING = "pending"
    NONE = "none"

class InfrastructureStatus(str, Enum):
    AVAILABLE = "available"
    EXTENSION_REQUIRED = "extension-required"
    MAJOR_INFRASTRUCTURE = "major-infrastructure"
    PRIVATE_SYSTEM = "private-system"

class Municipality(str, Enum):
    EDMONTON = "edmonton"
    CALGARY = "calgary"
    LEDUC = "leduc"
    ST_ALBERT = "st_albert"
    STRATHCONA = "strathcona"
    PARKLAND = "parkland"

class PropertyCoordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class UtilityConnection(BaseModel):
    utility_type: str
    distance: str
    status: InfrastructureStatus
    connection_cost: str
    authority: str
    timeline: str
    details: str
    coordinates: PropertyCoordinates

class AmenityFeature(BaseModel):
    amenity_type: str
    name: str
    distance: str
    status: str
    impact: str
    validation: ValidationStatus
    coordinates: PropertyCoordinates

class MunicipalValidation(BaseModel):
    municipality: Municipality
    last_updated: date
    next_review: date
    amenity_data: Dict[str, Any]
    research_schedule: Dict[str, str]

class InfrastructureAssessment(BaseModel):
    utilities: List[UtilityConnection]
    total_cost_min: float
    total_cost_max: float
    development_timeline: str
    readiness_level: str

class PropertyAnalysisRequest(BaseModel):
    address: str
    coordinates: PropertyCoordinates
    municipality: Municipality
    property_type: str
    size_hectares: float
    zoning: str
    analysis_type: str = "comprehensive"

class EnhancedPropertyDataModel(BaseModel):
    # Basic Property Information
    address: str
    coordinates: PropertyCoordinates
    municipality: Municipality
    zoning: str
    size_hectares: float
    
    # Financial Analysis (Enhanced with Market Ranges)
    land_value_base: float
    land_value_range: Dict[str, float]  # min, max, optimistic, conservative
    construction_costs: Dict[str, float]  # base, min, max
    soft_costs: Dict[str, float]  # base, min, max
    
    # Municipal Validation Data
    municipal_validation: MunicipalValidation
    amenity_features: List[AmenityFeature]
    amenity_score: float
    amenity_multiplier: float
    
    # Infrastructure Assessment
    infrastructure: InfrastructureAssessment
    utility_connections: List[UtilityConnection]
    infrastructure_risks: List[str]
    
    # Professional Engineering Assessment
    engineering_constraints: List[str]
    development_feasibility: str
    professional_validation_required: bool
    professional_notes: Optional[str] = None
    
    # Analysis Metadata
    analysis_date: datetime
    analysis_version: str = "2.0"
    analyst: str = "Sgiach Platform"
    
class PropertyMappingResponse(BaseModel):
    property_data: EnhancedPropertyDataModel
    map_features: Dict[str, List[Dict]]
    distance_matrix: Dict[str, str]
    professional_summary: Dict[str, Any]

# ==============================================================================
# ENHANCED SGIACH API APPLICATION
# ==============================================================================

app = FastAPI(
    title="Sgiach Professional Development Analysis Platform",
    description="Municipal-Level Property Development Analysis with Professional Engineering Oversight",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for mapping components
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==============================================================================
# MUNICIPAL VALIDATION DATABASE
# ==============================================================================

MUNICIPAL_VALIDATION_DB = {
    Municipality.EDMONTON: {
        "population": "1,010,899",
        "area": "684 km²",
        "last_updated": "2025-06-18",
        "next_review": "Q3 2025",
        "amenities": {
            "transit": {
                "validation": ValidationStatus.MUNICIPAL,
                "impact": "Complex: -value <274m, +27-99% multifamily 274m-1600m",
                "multiplier_range": {"min": -0.02, "max": 0.05},
                "data_source": "REIN Transportation Effect Report 2018",
                "next_study": "Q3 2025 - Valley Line impact assessment"
            },
            "parks": {
                "validation": ValidationStatus.PENDING,
                "impact": "North America's largest urban park system",
                "multiplier_range": {"min": 0.01, "max": 0.08},
                "data_source": "International research pending local validation",
                "next_study": "Q3 2025 - River Valley proximity impact study"
            },
            "schools": {
                "validation": ValidationStatus.PENDING,
                "impact": "Edmonton Public + Catholic school districts",
                "multiplier_range": {"min": 0.03, "max": 0.12},
                "data_source": "UK research pending local validation",
                "next_study": "Q4 2025 - School district boundary impact assessment"
            }
        }
    },
    Municipality.LEDUC: {
        "population": "33,032", 
        "area": "42.9 km²",
        "last_updated": "2025-06-18",
        "next_review": "Q4 2025",
        "amenities": {
            "employment": {
                "validation": ValidationStatus.PARTIAL,
                "impact": "Edmonton International Airport employment hub",
                "multiplier_range": {"min": 0.02, "max": 0.05},
                "data_source": "Employment statistics + anecdotal evidence",
                "next_study": "Q3 2026 - Employment center proximity study"
            }
        }
    },
    Municipality.STRATHCONA: {
        "population": "104,570",
        "area": "1,179 km²", 
        "last_updated": "2025-06-18",
        "next_review": "Q4 2025",
        "amenities": {
            "industrial": {
                "validation": ValidationStatus.PARTIAL,
                "impact": "Industrial Heartland - petrochemical hub",
                "multiplier_range": {"min": 0.05, "max": 0.15},
                "data_source": "Economic development data + employment statistics",
                "next_study": "Q2 2026 - Industrial proximity impact assessment"
            }
        }
    }
}

# ==============================================================================
# INFRASTRUCTURE COST DATABASE
# ==============================================================================

INFRASTRUCTURE_COSTS = {
    "urban_infill": {
        "water": {"min": 3500, "max": 8500, "status": InfrastructureStatus.AVAILABLE},
        "sewer": {"min": 4200, "max": 9800, "status": InfrastructureStatus.AVAILABLE},
        "electrical": {"min": 2500, "max": 6000, "status": InfrastructureStatus.AVAILABLE},
        "gas": {"min": 1800, "max": 4500, "status": InfrastructureStatus.AVAILABLE},
        "internet": {"min": 0, "max": 500, "status": InfrastructureStatus.AVAILABLE}
    },
    "suburban_greenfield": {
        "water": {"min": 45000, "max": 85000, "status": InfrastructureStatus.EXTENSION_REQUIRED},
        "sewer": {"min": 125000, "max": 200000, "status": InfrastructureStatus.MAJOR_INFRASTRUCTURE},
        "electrical": {"min": 35000, "max": 65000, "status": InfrastructureStatus.EXTENSION_REQUIRED},
        "gas": {"min": 25000, "max": 45000, "status": InfrastructureStatus.AVAILABLE},
        "internet": {"min": 2000, "max": 8000, "status": InfrastructureStatus.EXTENSION_REQUIRED}
    },
    "rural_acreage": {
        "water": {"min": 15000, "max": 35000, "status": InfrastructureStatus.PRIVATE_SYSTEM},
        "sewer": {"min": 18000, "max": 45000, "status": InfrastructureStatus.PRIVATE_SYSTEM},
        "electrical": {"min": 45000, "max": 125000, "status": InfrastructureStatus.EXTENSION_REQUIRED},
        "gas": {"min": 8000, "max": 15000, "status": InfrastructureStatus.PRIVATE_SYSTEM},
        "internet": {"min": 1500, "max": 5000, "status": InfrastructureStatus.EXTENSION_REQUIRED}
    }
}

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def calculate_distance(coord1: PropertyCoordinates, coord2: PropertyCoordinates) -> float:
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Earth's radius in km
    lat1, lon1 = math.radians(coord1.lat), math.radians(coord1.lng)
    lat2, lon2 = math.radians(coord2.lat), math.radians(coord2.lng)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return distance

def format_distance(distance_km: float) -> str:
    """Format distance for display"""
    if distance_km < 1:
        return f"{int(distance_km * 1000)}m"
    else:
        return f"{distance_km:.1f}km"

def determine_property_classification(municipality: Municipality, zoning: str, size: float) -> str:
    """Determine property classification for infrastructure costing"""
    if municipality == Municipality.EDMONTON and size < 0.5:
        return "urban_infill"
    elif size > 5.0:
        return "rural_acreage"
    else:
        return "suburban_greenfield"

def calculate_amenity_multiplier(municipality: Municipality, amenity_features: List[AmenityFeature]) -> float:
    """Calculate overall amenity multiplier based on municipal validation data"""
    if municipality not in MUNICIPAL_VALIDATION_DB:
        return 1.0
    
    total_multiplier = 1.0
    municipal_data = MUNICIPAL_VALIDATION_DB[municipality]
    
    for feature in amenity_features:
        if feature.amenity_type in municipal_data["amenities"]:
            amenity_data = municipal_data["amenities"][feature.amenity_type]
            if amenity_data["validation"] == ValidationStatus.MUNICIPAL:
                # Use validated multipliers
                distance_km = float(feature.distance.replace('km', '').replace('m', '').replace(',', '')) 
                if 'm' in feature.distance:
                    distance_km = distance_km / 1000
                
                # Apply distance-based multiplier (closer = higher impact)
                if distance_km < 0.5:
                    multiplier = amenity_data["multiplier_range"]["max"]
                elif distance_km < 2.0:
                    multiplier = (amenity_data["multiplier_range"]["max"] + amenity_data["multiplier_range"]["min"]) / 2
                else:
                    multiplier = amenity_data["multiplier_range"]["min"]
                
                total_multiplier += multiplier
    
    return min(total_multiplier, 1.20)  # Cap at 20% premium

def assess_infrastructure_costs(property_classification: str) -> InfrastructureAssessment:
    """Calculate comprehensive infrastructure costs"""
    if property_classification not in INFRASTRUCTURE_COSTS:
        property_classification = "suburban_greenfield"
    
    costs = INFRASTRUCTURE_COSTS[property_classification]
    total_min = sum(cost["min"] for cost in costs.values())
    total_max = sum(cost["max"] for cost in costs.values())
    
    # Determine timeline based on most complex requirement
    max_complexity = max(cost["status"] for cost in costs.values())
    if max_complexity == InfrastructureStatus.AVAILABLE:
        timeline = "2-6 weeks"
        readiness = "Immediate"
    elif max_complexity == InfrastructureStatus.EXTENSION_REQUIRED:
        timeline = "3-8 months"
        readiness = "Extension Required"
    elif max_complexity == InfrastructureStatus.MAJOR_INFRASTRUCTURE:
        timeline = "8-15 months"
        readiness = "Major Development"
    else:
        timeline = "6-12 weeks"
        readiness = "Private Systems"
    
    return InfrastructureAssessment(
        utilities=[],  # Will be populated separately
        total_cost_min=total_min,
        total_cost_max=total_max,
        development_timeline=timeline,
        readiness_level=readiness
    )

# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {
        "status": "healthy", 
        "service": "sgiach-api",
        "version": "2.0.0",
        "features": ["mapping", "municipal-validation", "infrastructure-assessment"]
    }

@app.post("/property/comprehensive-analysis", response_model=PropertyMappingResponse)
async def comprehensive_property_analysis(request: PropertyAnalysisRequest):
    """
    Comprehensive property analysis with mapping, municipal validation, and infrastructure assessment
    """
    try:
        # Determine property classification
        property_classification = determine_property_classification(
            request.municipality, request.zoning, request.size_hectares
        )
        
        # Get municipal validation data
        municipal_data = MUNICIPAL_VALIDATION_DB.get(request.municipality, {})
        municipal_validation = MunicipalValidation(
            municipality=request.municipality,
            last_updated=datetime.strptime(municipal_data.get("last_updated", "2025-06-18"), "%Y-%m-%d").date(),
            next_review=municipal_data.get("next_review", "Q4 2025"),
            amenity_data=municipal_data.get("amenities", {}),
            research_schedule={}
        )
        
        # Generate amenity features (sample data - would integrate with real APIs)
        amenity_features = generate_sample_amenities(request.coordinates, request.municipality)
        
        # Calculate amenity multiplier
        amenity_multiplier = calculate_amenity_multiplier(request.municipality, amenity_features)
        
        # Assess infrastructure
        infrastructure = assess_infrastructure_costs(property_classification)
        utility_connections = generate_utility_connections(request.coordinates, property_classification)
        
        # Calculate financial ranges with market variability
        base_land_value = estimate_base_land_value(request.municipality, request.size_hectares)
        land_value_range = {
            "base": base_land_value,
            "min": base_land_value * 0.85,  # -15% for market conditions
            "max": base_land_value * 1.15,  # +15% for market conditions
            "optimistic": base_land_value * 0.90,  # -10% for best case
            "conservative": base_land_value * 1.10   # +10% for worst case
        }
        
        construction_costs = calculate_construction_costs(request.size_hectares, property_classification)
        soft_costs = calculate_soft_costs(construction_costs["base"])
        
        # Determine if professional validation required
        professional_validation_required = (
            infrastructure.total_cost_max > 100000 or
            property_classification == "rural_acreage" or
            request.size_hectares > 5.0
        )
        
        # Create comprehensive property data model
        property_data = EnhancedPropertyDataModel(
            address=request.address,
            coordinates=request.coordinates,
            municipality=request.municipality,
            zoning=request.zoning,
            size_hectares=request.size_hectares,
            land_value_base=base_land_value,
            land_value_range=land_value_range,
            construction_costs=construction_costs,
            soft_costs=soft_costs,
            municipal_validation=municipal_validation,
            amenity_features=amenity_features,
            amenity_score=calculate_amenity_score(amenity_features),
            amenity_multiplier=amenity_multiplier,
            infrastructure=infrastructure,
            utility_connections=utility_connections,
            infrastructure_risks=assess_infrastructure_risks(property_classification),
            engineering_constraints=assess_engineering_constraints(request.municipality, property_classification),
            development_feasibility=assess_development_feasibility(infrastructure, amenity_multiplier),
            professional_validation_required=professional_validation_required,
            analysis_date=datetime.now(),
            analyst="Sgiach Platform v2.0"
        )
        
        # Generate map features
        map_features = generate_map_features(request.coordinates, property_classification, request.municipality)
        
        # Calculate distance matrix
        distance_matrix = calculate_distance_matrix(request.coordinates, map_features)
        
        # Professional summary
        professional_summary = generate_professional_summary(property_data)
        
        return PropertyMappingResponse(
            property_data=property_data,
            map_features=map_features,
            distance_matrix=distance_matrix,
            professional_summary=professional_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/mapping/interactive/{municipality}")
async def get_interactive_map(municipality: Municipality):
    """
    Get interactive mapping interface for specific municipality
    """
    return HTMLResponse(content=generate_interactive_map_html(municipality))

@app.get("/municipal/validation-status/{municipality}")
async def get_municipal_validation_status(municipality: Municipality):
    """
    Get current municipal validation status and research schedule
    """
    municipal_data = MUNICIPAL_VALIDATION_DB.get(municipality)
    if not municipal_data:
        raise HTTPException(status_code=404, detail="Municipality data not found")
    
    return {
        "municipality": municipality,
        "validation_status": municipal_data,
        "research_schedule": {
            "Q3_2025": ["Edmonton Valley Line LRT impact", "River Valley parks proximity"],
            "Q4_2025": ["School district impact assessment", "Satellite municipality validation"],
            "Q1_2026": ["Healthcare facility proximity", "Regional transit connectivity"],
            "Q2_2026": ["Industrial Heartland employment", "Airport employment impact"],
            "Q3_2026": ["Recreational amenity impact", "Rural county analysis"]
        }
    }

@app.post("/professional/validation-request")
async def request_professional_validation(
    property_data: EnhancedPropertyDataModel,
    validation_type: str,
    background_tasks: BackgroundTasks
):
    """
    Request professional engineering validation for complex analysis
    """
    validation_request = {
        "request_id": f"VAL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "property_address": property_data.address,
        "validation_type": validation_type,
        "complexity_score": calculate_complexity_score(property_data),
        "estimated_cost": estimate_validation_cost(validation_type, property_data),
        "estimated_timeline": estimate_validation_timeline(validation_type),
        "professional_reviewer": "Jeff McLeod, P.Eng",
        "status": "requested",
        "priority": "standard"
    }
    
    # Add background task to notify professional team
    background_tasks.add_task(notify_professional_team, validation_request)
    
    return {
        "message": "Professional validation requested",
        "validation_request": validation_request,
        "next_steps": [
            "Professional review within 24 hours",
            "Detailed scope confirmation",
            "Engineering analysis completion",
            "Professional report delivery"
        ]
    }

# ==============================================================================
# HELPER FUNCTIONS (Sample Implementations)
# ==============================================================================

def generate_sample_amenities(coordinates: PropertyCoordinates, municipality: Municipality) -> List[AmenityFeature]:
    """Generate sample amenity features - would integrate with real APIs"""
    sample_amenities = []
    
    if municipality == Municipality.EDMONTON:
        sample_amenities = [
            AmenityFeature(
                amenity_type="transit",
                name="Central LRT Station",
                distance="420m",
                status="excellent",
                impact="+1.5% property value (validated)",
                validation=ValidationStatus.MUNICIPAL,
                coordinates=PropertyCoordinates(lat=coordinates.lat + 0.002, lng=coordinates.lng + 0.003)
            ),
            AmenityFeature(
                amenity_type="park",
                name="River Valley Park System",
                distance="650m",
                status="excellent", 
                impact="Premium location factor",
                validation=ValidationStatus.PENDING,
                coordinates=PropertyCoordinates(lat=coordinates.lat - 0.005, lng=coordinates.lng + 0.001)
            )
        ]
    
    return sample_amenities

def generate_utility_connections(coordinates: PropertyCoordinates, classification: str) -> List[UtilityConnection]:
    """Generate utility connection data based on property classification"""
    connections = []
    costs = INFRASTRUCTURE_COSTS.get(classification, {})
    
    for utility_type, cost_data in costs.items():
        distance = "15m" if classification == "urban_infill" else "500m+" if classification == "suburban_greenfield" else "Private system"
        
        connections.append(UtilityConnection(
            utility_type=utility_type,
            distance=distance,
            status=cost_data["status"],
            connection_cost=f"${cost_data['min']:,} - ${cost_data['max']:,}",
            authority=get_utility_authority(utility_type),
            timeline=get_utility_timeline(cost_data["status"]),
            details=get_utility_details(utility_type, cost_data["status"]),
            coordinates=PropertyCoordinates(
                lat=coordinates.lat + (hash(utility_type) % 100 - 50) / 10000,
                lng=coordinates.lng + (hash(utility_type) % 100 - 50) / 10000
            )
        ))
    
    return connections

def estimate_base_land_value(municipality: Municipality, size_hectares: float) -> float:
    """Estimate base land value - simplified calculation"""
    base_rates = {
        Municipality.EDMONTON: 250000,  # per hectare
        Municipality.CALGARY: 280000,
        Municipality.LEDUC: 180000,
        Municipality.ST_ALBERT: 220000,
        Municipality.STRATHCONA: 160000
    }
    
    base_rate = base_rates.get(municipality, 200000)
    return base_rate * size_hectares

def calculate_construction_costs(size_hectares: float, classification: str) -> Dict[str, float]:
    """Calculate construction costs with market variability"""
    base_cost_per_hectare = {
        "urban_infill": 800000,
        "suburban_greenfield": 600000,
        "rural_acreage": 400000
    }
    
    base = base_cost_per_hectare.get(classification, 600000) * size_hectares
    
    return {
        "base": base,
        "min": base * 0.85,  # -15% for favorable conditions
        "max": base * 1.20   # +20% for challenging conditions
    }

def calculate_soft_costs(construction_base: float) -> Dict[str, float]:
    """Calculate soft costs as percentage of construction"""
    base_percentage = 0.15  # 15% of construction
    base = construction_base * base_percentage
    
    return {
        "base": base,
        "min": base * 0.90,  # -10% for streamlined approvals
        "max": base * 1.15   # +15% for complex approvals
    }

def get_utility_authority(utility_type: str) -> str:
    """Get utility authority based on type"""
    authorities = {
        "water": "EPCOR Water Services",
        "sewer": "EPCOR Water Services",
        "electrical": "EPCOR Distribution",
        "gas": "ATCO Gas",
        "internet": "Multiple providers"
    }
    return authorities.get(utility_type, "Municipal Authority")

def get_utility_timeline(status: InfrastructureStatus) -> str:
    """Get timeline based on infrastructure status"""
    timelines = {
        InfrastructureStatus.AVAILABLE: "2-4 weeks",
        InfrastructureStatus.EXTENSION_REQUIRED: "3-8 months",
        InfrastructureStatus.MAJOR_INFRASTRUCTURE: "8-15 months",
        InfrastructureStatus.PRIVATE_SYSTEM: "6-10 weeks"
    }
    return timelines.get(status, "To be determined")

def get_utility_details(utility_type: str, status: InfrastructureStatus) -> str:
    """Get utility-specific details"""
    if status == InfrastructureStatus.AVAILABLE:
        return f"Municipal {utility_type} service readily available"
    elif status == InfrastructureStatus.EXTENSION_REQUIRED:
        return f"{utility_type.title()} main extension required"
    elif status == InfrastructureStatus.MAJOR_INFRASTRUCTURE:
        return f"Major {utility_type} infrastructure development required"
    else:
        return f"Private {utility_type} system required"

def calculate_amenity_score(amenity_features: List[AmenityFeature]) -> float:
    """Calculate overall amenity score"""
    if not amenity_features:
        return 5.0
    
    total_score = 0
    for feature in amenity_features:
        if feature.validation == ValidationStatus.MUNICIPAL:
            score = 9.0
        elif feature.validation == ValidationStatus.PARTIAL:
            score = 7.0
        elif feature.validation == ValidationStatus.PENDING:
            score = 6.0
        else:
            score = 4.0
        
        total_score += score
    
    return min(total_score / len(amenity_features), 10.0)

def assess_infrastructure_risks(classification: str) -> List[str]:
    """Assess infrastructure risks based on property classification"""
    risks = {
        "urban_infill": [
            "Aging infrastructure may require upgrades",
            "Limited space for utility connections",
            "Coordination with existing services required"
        ],
        "suburban_greenfield": [
            "Major infrastructure extensions required",
            "Developer responsible for system costs", 
            "Complex servicing due to topography",
            "Extended development timeline"
        ],
        "rural_acreage": [
            "Private systems require ongoing maintenance",
            "Soil conditions critical for septic systems",
            "High electrical extension costs",
            "Limited emergency service response"
        ]
    }
    return risks.get(classification, ["Standard development risks"])

def assess_engineering_constraints(municipality: Municipality, classification: str) -> List[str]:
    """Assess engineering constraints requiring P.Eng oversight"""
    base_constraints = [
        "Geotechnical analysis required for foundation design",
        "Municipal development permit process",
        "Environmental assessment for sensitive areas"
    ]
    
    if classification == "rural_acreage":
        base_constraints.extend([
            "Private well water quality testing",
            "Septic system soil percolation testing",
            "Electrical service capacity analysis"
        ])
    elif classification == "suburban_greenfield":
        base_constraints.extend([
            "Infrastructure extension engineering",
            "Stormwater management design",
            "Traffic impact assessment"
        ])
    
    return base_constraints

def assess_development_feasibility(infrastructure: InfrastructureAssessment, amenity_multiplier: float) -> str:
    """Assess overall development feasibility"""
    if infrastructure.total_cost_max > 200000:
        if amenity_multiplier > 1.10:
            return "Challenging but viable with premium location"
        else:
            return "High infrastructure costs require careful analysis"
    elif infrastructure.total_cost_max > 50000:
        return "Moderate development complexity"
    else:
        return "Straightforward development opportunity"

def generate_map_features(coordinates: PropertyCoordinates, classification: str, municipality: Municipality) -> Dict[str, List[Dict]]:
    """Generate map features for visualization"""
    # This would integrate with real mapping APIs
    return {
        "utilities": [],
        "amenities": [],
        "services": [],
        "boundaries": []
    }

def calculate_distance_matrix(coordinates: PropertyCoordinates, map_features: Dict) -> Dict[str, str]:
    """Calculate distance matrix for all features"""
    # Simplified implementation
    return {"sample_feature": "1.2km"}

def generate_professional_summary(property_data: EnhancedPropertyDataModel) -> Dict[str, Any]:
    """Generate professional engineering summary"""
    return {
        "total_development_cost": property_data.land_value_base + property_data.infrastructure.total_cost_max,
        "professional_validation_required": property_data.professional_validation_required,
        "key_risks": property_data.infrastructure_risks[:3],
        "development_timeline": property_data.infrastructure.development_timeline,
        "engineering_recommendation": "Professional P.Eng review recommended for complex infrastructure requirements"
    }

def calculate_complexity_score(property_data: EnhancedPropertyDataModel) -> float:
    """Calculate complexity score for validation pricing"""
    base_score = 1.0
    
    if property_data.infrastructure.total_cost_max > 100000:
        base_score += 1.0
    if property_data.size_hectares > 5.0:
        base_score += 0.5
    if len(property_data.engineering_constraints) > 5:
        base_score += 0.5
    
    return min(base_score, 3.0)

def estimate_validation_cost(validation_type: str, property_data: EnhancedPropertyDataModel) -> float:
    """Estimate professional validation cost"""
    base_costs = {
        "engineering": 3500,
        "market": 2500,
        "comprehensive": 7500
    }
    
    base_cost = base_costs.get(validation_type, 5000)
    complexity_multiplier = calculate_complexity_score(property_data)
    
    return base_cost * complexity_multiplier

def estimate_validation_timeline(validation_type: str) -> str:
    """Estimate validation timeline"""
    timelines = {
        "engineering": "3-5 business days",
        "market": "2-3 business days", 
        "comprehensive": "5-7 business days"
    }
    return timelines.get(validation_type, "3-5 business days")

async def notify_professional_team(validation_request: Dict):
    """Background task to notify professional team of validation request"""
    # Implementation would send email/notification to Jeff McLeod, P.Eng
    print(f"Professional validation requested: {validation_request['request_id']}")

def generate_interactive_map_html(municipality: Municipality) -> str:
    """Generate interactive map HTML with Leaflet.js"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sgiach Property Mapping - {municipality.title()}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
        <style>
            #map {{ height: 600px; width: 100%; }}
            .legend {{ background: white; padding: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Property Analysis Map - {municipality.title()}</h1>
        <div id="map"></div>
        <div class="legend">
            <h4>Legend</h4>
            <p>🏠 Property Location</p>
            <p>💧 Utilities</p>
            <p>🏫 Amenities</p>
            <p>🚑 Emergency Services</p>
        </div>
        <script>
            var map = L.map('map').setView([53.5444, -113.4909], 12);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            
            // Add markers for utilities, amenities, etc.
            L.marker([53.5444, -113.4909]).addTo(map)
                .bindPopup('Property Location<br/>Professional analysis available');
        </script>
    </body>
    </html>
    """

# ==============================================================================
# MAIN APPLICATION STARTUP
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
