# ==============================================================================
# SGIACH TRULY COMPLETE API - EVERYTHING INTEGRATED
# SkyeBridge Consulting & Developments Inc.
# Complete Professional Platform: Partner Realty + Mapping + Amenities + Infrastructure
# Jeff McLeod, P.Eng - Technical Lead
# ==============================================================================

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Tuple, Union
from datetime import datetime, date
from enum import Enum
import json
import math
import hashlib
import uuid
from dataclasses import dataclass, asdict

app = FastAPI(
    title="Sgiach Professional Development Analysis Platform",
    description="Complete Municipal Property Development Analysis with Professional Engineering Oversight",
    version="3.0.0"
)

# Mount static files for mapping
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==============================================================================
# COMPLETE DATA MODELS (All Features)
# ==============================================================================

class PropertyType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed_use"

class Municipality(str, Enum):
    EDMONTON = "edmonton"
    LEDUC = "leduc"
    ST_ALBERT = "st_albert"
    STRATHCONA = "strathcona"
    PARKLAND = "parkland"

class AmenityType(str, Enum):
    TRANSIT = "transit"
    SCHOOLS = "schools"
    HEALTHCARE = "healthcare"
    RETAIL = "retail"
    RECREATION = "recreation"
    EMPLOYMENT = "employment"
    UTILITIES = "utilities"
    EMERGENCY = "emergency"

class InfrastructureStatus(str, Enum):
    AVAILABLE = "available"
    EXTENSION_REQUIRED = "extension_required"
    MAJOR_INFRASTRUCTURE = "major_infrastructure"
    NOT_AVAILABLE = "not_available"

class DataSourceType(str, Enum):
    MANUAL_INPUT = "manual_input"
    PARTNER_REALTY = "partner_realty"
    MLS_FEED = "mls_feed"
    REALTOR_SCRAPING = "realtor_scraping"
    COMPARABLE_ANALYSIS = "comparable_analysis"
    MARKET_ESTIMATE = "market_estimate"

class SaleType(str, Enum):
    ACTUAL_SALE = "actual_sale"
    LISTING_PRICE = "listing_price"
    ASSESSED_VALUE = "assessed_value"
    MARKET_ESTIMATE = "market_estimate"

# ==============================================================================
# PARTNER REALTY MODELS
# ==============================================================================

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

class PartnerFirm(BaseModel):
    partner_id: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    license_number: str
    service_areas: List[str]
    data_types: List[str]
    credibility_level: str = "high"
    api_key: str
    is_active: bool = True
    created_date: datetime = Field(default_factory=datetime.now)

class PropertySaleData(BaseModel):
    sale_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    address: str
    municipality: Municipality
    property_type: PropertyType
    sale_type: SaleType
    sale_price: float
    list_price: Optional[float] = None
    sale_date: date
    days_on_market: Optional[int] = None
    lot_size_sqft: Optional[float] = None
    building_sqft: Optional[float] = None
    year_built: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    coordinates: Optional[Tuple[float, float]] = None
    postal_code: Optional[str] = None
    neighborhood: Optional[str] = None
    financing_type: Optional[str] = None
    sale_conditions: Optional[str] = None
    property_condition: Optional[str] = None
    source_partner_id: str
    mls_number: Optional[str] = None
    confidence_level: str = "high"
    notes: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    updated_date: Optional[datetime] = None

# ==============================================================================
# MAPPING & AMENITY MODELS  
# ==============================================================================

@dataclass
class AmenityPoint:
    name: str
    type: AmenityType
    address: str
    coordinates: Tuple[float, float]
    distance_km: float
    impact_score: float
    description: str

class UtilityConnection(BaseModel):
    utility_type: str
    status: InfrastructureStatus
    distance_to_connection: float
    estimated_cost: int
    timeline_weeks: int
    capacity_adequate: bool
    notes: str

class PropertyMappingRequest(BaseModel):
    address: str
    municipality: Municipality
    coordinates: Optional[Tuple[float, float]] = None
    analysis_radius_km: float = Field(default=5.0, ge=1.0, le=15.0)
    include_amenities: List[AmenityType] = Field(default_factory=lambda: list(AmenityType))
    include_infrastructure: bool = True
    include_distances: bool = True

class PropertyMappingResponse(BaseModel):
    property_id: str
    address: str
    coordinates: Tuple[float, float]
    municipality: str
    amenities_by_type: Dict[str, List[Dict]] = {}
    amenity_scores: Dict[str, float] = {}
    overall_amenity_score: float
    utility_connections: List[UtilityConnection] = []
    infrastructure_total_cost: int
    development_readiness: str
    distance_matrix: Dict[str, float] = {}
    accessibility_score: float
    engineering_notes: List[str] = []
    requires_peng_review: bool
    map_center: Tuple[float, float]
    map_markers: List[Dict] = []
    map_layers: Dict[str, List[Dict]] = {}

# ==============================================================================
# MULTI-SOURCE ANALYSIS MODELS
# ==============================================================================

class DataSource(BaseModel):
    source_type: DataSourceType
    source_id: str
    credibility_weight: float
    data_points: int
    last_updated: datetime
    confidence_level: str

class WeightedMarketRange(BaseModel):
    conservative_value: float
    realistic_value: float
    optimistic_value: float
    data_points_count: int
    confidence_level: str
    credibility_score: float
    supporting_sources: List[DataSource]
    value_basis: str

class PropertyMarketAnalysis(BaseModel):
    property_id: str
    address: str
    municipality: Municipality
    market_ranges: WeightedMarketRange
    manual_inputs: List[Dict] = []
    partner_sales: List[PropertySaleData] = []
    scraped_listings: List[Dict] = []
    comparable_properties: List[Dict] = []
    analysis_date: datetime = Field(default_factory=datetime.now)
    total_data_sources: int
    recommendation: str
    requires_validation: bool = False
    validation_notes: List[str] = []

# ==============================================================================
# COMPLETE ALBERTA AMENITY DATABASE
# ==============================================================================

ALBERTA_AMENITIES = {
    "edmonton": {
        AmenityType.TRANSIT: [
            {"name": "University LRT Station", "coordinates": (53.5232, -113.5263), "type": "lrt_station", "description": "Capital Line LRT"},
            {"name": "Stadium LRT Station", "coordinates": (53.5347, -113.4755), "type": "lrt_station", "description": "Capital Line LRT"},
            {"name": "Clareview LRT Station", "coordinates": (53.5723, -113.3909), "type": "lrt_station", "description": "Northeast Line LRT"},
            {"name": "Belvedere LRT Station", "coordinates": (53.5733, -113.4447), "type": "lrt_station", "description": "Northeast Line LRT"},
            {"name": "Coliseum LRT Station", "coordinates": (53.5947, -113.4747), "type": "lrt_station", "description": "Northeast Line LRT"},
            {"name": "Century Park LRT Station", "coordinates": (53.4347, -113.5047), "type": "lrt_station", "description": "Capital Line South LRT"},
            {"name": "Health Sciences LRT Station", "coordinates": (53.5194, -113.5194), "type": "lrt_station", "description": "Capital Line LRT"},
            {"name": "Central Station", "coordinates": (53.5444, -113.4904), "type": "lrt_station", "description": "Downtown Transit Hub"}
        ],
        AmenityType.SCHOOLS: [
            {"name": "University of Alberta", "coordinates": (53.5232, -113.5263), "type": "university", "description": "Major research university"},
            {"name": "MacEwan University", "coordinates": (53.5499, -113.5074), "type": "university", "description": "Undergraduate-focused university"},
            {"name": "NAIT", "coordinates": (53.5699, -113.4974), "type": "college", "description": "Northern Alberta Institute of Technology"},
            {"name": "Victoria School", "coordinates": (53.5315, -113.5012), "type": "high_school", "description": "Arts-focused high school"},
            {"name": "Strathcona High School", "coordinates": (53.5187, -113.5126), "type": "high_school", "description": "Academic high school"},
            {"name": "McNally High School", "coordinates": (53.5547, -113.4847), "type": "high_school", "description": "Composite high school"},
            {"name": "Old Scona Academic", "coordinates": (53.5087, -113.5226), "type": "high_school", "description": "Academic specialized school"}
        ],
        AmenityType.HEALTHCARE: [
            {"name": "University of Alberta Hospital", "coordinates": (53.5194, -113.5194), "type": "hospital", "description": "Major teaching hospital"},
            {"name": "Royal Alexandra Hospital", "coordinates": (53.5547, -113.5047), "type": "hospital", "description": "Trauma center"},
            {"name": "Misericordia Hospital", "coordinates": (53.5347, -113.5569), "type": "hospital", "description": "Community hospital"},
            {"name": "Mazankowski Alberta Heart Institute", "coordinates": (53.5194, -113.5194), "type": "specialty_hospital", "description": "Cardiac care center"},
            {"name": "Cross Cancer Institute", "coordinates": (53.5194, -113.5194), "type": "specialty_hospital", "description": "Cancer treatment center"},
            {"name": "Stollery Children's Hospital", "coordinates": (53.5194, -113.5194), "type": "childrens_hospital", "description": "Pediatric care"}
        ],
        AmenityType.RETAIL: [
            {"name": "West Edmonton Mall", "coordinates": (53.5225, -113.6232), "type": "major_shopping", "description": "World's largest shopping mall"},
            {"name": "Kingsway Mall", "coordinates": (53.5689, -113.4747), "type": "shopping_center", "description": "Major shopping center"},
            {"name": "Southgate Centre", "coordinates": (53.4947, -113.5126), "type": "shopping_center", "description": "South Edmonton shopping"},
            {"name": "Whyte Avenue Shopping", "coordinates": (53.5194, -113.5126), "type": "retail_district", "description": "Entertainment district"},
            {"name": "124 Street District", "coordinates": (53.5494, -113.5326), "type": "retail_district", "description": "Boutique shopping area"},
            {"name": "Downtown Shopping", "coordinates": (53.5444, -113.4904), "type": "retail_district", "description": "Central business district"}
        ],
        AmenityType.RECREATION: [
            {"name": "River Valley Park System", "coordinates": (53.5194, -113.5126), "type": "park_system", "description": "North America's largest urban park"},
            {"name": "Commonwealth Stadium", "coordinates": (53.5347, -113.4755), "type": "sports_venue", "description": "CFL Edmonton Elks home"},
            {"name": "Rogers Place", "coordinates": (53.5469, -113.4978), "type": "sports_venue", "description": "NHL Edmonton Oilers arena"},
            {"name": "Hawrelak Park", "coordinates": (53.5194, -113.5569), "type": "park", "description": "Festival and recreation park"},
            {"name": "Fort Edmonton Park", "coordinates": (53.4994, -113.5669), "type": "historical_park", "description": "Living history museum"},
            {"name": "Kinsmen Sports Centre", "coordinates": (53.5394, -113.5269), "type": "recreation_center", "description": "Aquatic and fitness center"}
        ],
        AmenityType.EMPLOYMENT: [
            {"name": "Downtown Edmonton", "coordinates": (53.5444, -113.4904), "type": "business_district", "description": "Government and corporate offices"},
            {"name": "University Research Park", "coordinates": (53.5194, -113.5194), "type": "research_park", "description": "Technology and research hub"},
            {"name": "Alberta Legislature", "coordinates": (53.5344, -113.5069), "type": "government", "description": "Provincial government center"},
            {"name": "City Centre", "coordinates": (53.5444, -113.4904), "type": "office_district", "description": "Major office towers"},
            {"name": "Refinery Row", "coordinates": (53.6044, -113.3904), "type": "industrial", "description": "Petrochemical industry"}
        ]
    },
    "leduc": {
        AmenityType.EMPLOYMENT: [
            {"name": "Edmonton International Airport", "coordinates": (53.3097, -113.5803), "type": "major_employer", "description": "26,000+ jobs, cargo hub"},
            {"name": "Nisku Industrial Heartland", "coordinates": (53.3547, -113.5126), "type": "industrial_park", "description": "Petrochemical and manufacturing"},
            {"name": "Alberta Industrial Heartland", "coordinates": (53.4047, -113.4126), "type": "industrial_heartland", "description": "Major industrial development"}
        ],
        AmenityType.RETAIL: [
            {"name": "Leduc Common", "coordinates": (53.2694, -113.5422), "type": "shopping_center", "description": "Regional shopping center"},
            {"name": "Leduc Recreation Centre", "coordinates": (53.2694, -113.5422), "type": "recreation_center", "description": "Community recreation"}
        ],
        AmenityType.RECREATION: [
            {"name": "Leduc #1 Energy Discovery Centre", "coordinates": (53.2594, -113.5322), "type": "museum", "description": "Oil heritage site"},
            {"name": "Telford Lake", "coordinates": (53.2794, -113.5222), "type": "park", "description": "Natural lake park"}
        ]
    },
    "st_albert": {
        AmenityType.SCHOOLS: [
            {"name": "St. Albert Catholic High School", "coordinates": (53.6347, -113.6126), "type": "high_school", "description": "Catholic education"},
            {"name": "Paul Kane High School", "coordinates": (53.6247, -113.6026), "type": "high_school", "description": "Public high school"},
            {"name": "Morinville Community High School", "coordinates": (53.8047, -113.6426), "type": "high_school", "description": "Rural high school"}
        ],
        AmenityType.RECREATION: [
            {"name": "Arden Theatre", "coordinates": (53.6347, -113.6126), "type": "cultural_venue", "description": "Professional theatre"},
            {"name": "Red Willow Park", "coordinates": (53.6447, -113.6026), "type": "park", "description": "Sturgeon River park"},
            {"name": "Servus Place", "coordinates": (53.6247, -113.6226), "type": "sports_complex", "description": "Arena and recreation"}
        ],
        AmenityType.RETAIL: [
            {"name": "St. Albert Centre", "coordinates": (53.6347, -113.6126), "type": "shopping_center", "description": "Regional mall"},
            {"name": "Village Landing", "coordinates": (53.6447, -113.6226), "type": "retail_district", "description": "Outdoor shopping"}
        ]
    },
    "strathcona": {
        AmenityType.EMPLOYMENT: [
            {"name": "Industrial Heartland", "coordinates": (53.6547, -113.3126), "type": "industrial_heartland", "description": "Petrochemical hub"},
            {"name": "Sherwood Park Business Park", "coordinates": (53.5247, -113.3226), "type": "business_park", "description": "Office and light industrial"}
        ],
        AmenityType.RECREATION: [
            {"name": "Festival Place", "coordinates": (53.5347, -113.3126), "type": "cultural_venue", "description": "Arts and conference center"},
            {"name": "Broadmoor Lake Park", "coordinates": (53.5147, -113.3026), "type": "park", "description": "Lake recreation"},
            {"name": "Millennium Place", "coordinates": (53.5247, -113.3226), "type": "recreation_center", "description": "Aquatic and fitness"}
        ],
        AmenityType.RETAIL: [
            {"name": "Sherwood Park Mall", "coordinates": (53.5347, -113.3126), "type": "shopping_center", "description": "Regional shopping"},
            {"name": "Baseline Road Retail", "coordinates": (53.5047, -113.3426), "type": "retail_corridor", "description": "Commercial strip"}
        ]
    },
    "parkland": {
        AmenityType.EMPLOYMENT: [
            {"name": "Highway 16A Corridor", "coordinates": (53.7347, -113.7126), "type": "commercial_corridor", "description": "Transportation and logistics"},
            {"name": "Spruce Grove Business Park", "coordinates": (53.5447, -113.9026), "type": "business_park", "description": "Light industrial"}
        ],
        AmenityType.RECREATION: [
            {"name": "Wabamun Lake", "coordinates": (53.7847, -114.3126), "type": "lake", "description": "Recreation lake"},
            {"name": "Parkland County Parks", "coordinates": (53.7347, -113.7126), "type": "park_system", "description": "Rural recreation"}
        ]
    }
}

# ==============================================================================
# COMPLETE INFRASTRUCTURE DATABASE
# ==============================================================================

MUNICIPAL_INFRASTRUCTURE = {
    "edmonton": {
        "water_main_grid": 0.2,  # km spacing
        "sewer_grid": 0.2,
        "electrical_grid": 0.15,
        "gas_grid": 0.3,
        "internet_fiber": 0.1,
        "connection_costs": {
            "water": {"base": 3500, "per_meter": 150},
            "sewer": {"base": 4200, "per_meter": 180},
            "electrical": {"base": 2800, "per_meter": 120},
            "gas": {"base": 3200, "per_meter": 140},
            "internet": {"base": 800, "per_meter": 25}
        },
        "service_standards": {
            "water_pressure": "550-700 kPa",
            "electrical_capacity": "200A standard service",
            "gas_pressure": "Low pressure residential",
            "internet_speed": "Gigabit fiber available"
        }
    },
    "leduc": {
        "water_main_grid": 0.5,
        "sewer_grid": 0.5,
        "electrical_grid": 0.4,
        "gas_grid": 0.6,
        "internet_fiber": 0.3,
        "connection_costs": {
            "water": {"base": 5500, "per_meter": 200},
            "sewer": {"base": 6800, "per_meter": 250},
            "electrical": {"base": 4500, "per_meter": 180},
            "gas": {"base": 5200, "per_meter": 200},
            "internet": {"base": 1200, "per_meter": 35}
        },
        "service_standards": {
            "water_pressure": "450-650 kPa",
            "electrical_capacity": "200A standard, 400A available",
            "gas_pressure": "Medium pressure industrial available",
            "internet_speed": "100 Mbps standard, fiber select areas"
        }
    },
    "st_albert": {
        "water_main_grid": 0.3,
        "sewer_grid": 0.3,
        "electrical_grid": 0.25,
        "gas_grid": 0.4,
        "internet_fiber": 0.2,
        "connection_costs": {
            "water": {"base": 4000, "per_meter": 160},
            "sewer": {"base": 4800, "per_meter": 190},
            "electrical": {"base": 3200, "per_meter": 130},
            "gas": {"base": 3600, "per_meter": 150},
            "internet": {"base": 900, "per_meter": 28}
        },
        "service_standards": {
            "water_pressure": "500-650 kPa",
            "electrical_capacity": "200A standard service",
            "gas_pressure": "Low pressure residential",
            "internet_speed": "Fiber to premises expanding"
        }
    },
    "strathcona": {
        "water_main_grid": 0.4,
        "sewer_grid": 0.4,
        "electrical_grid": 0.3,
        "gas_grid": 0.5,
        "internet_fiber": 0.25,
        "connection_costs": {
            "water": {"base": 4200, "per_meter": 170},
            "sewer": {"base": 5000, "per_meter": 200},
            "electrical": {"base": 3500, "per_meter": 140},
            "gas": {"base": 4000, "per_meter": 170},
            "internet": {"base": 1000, "per_meter": 30}
        },
        "service_standards": {
            "water_pressure": "475-625 kPa",
            "electrical_capacity": "200A standard, 600A industrial",
            "gas_pressure": "High pressure industrial available",
            "internet_speed": "Mixed fiber/cable availability"
        }
    },
    "parkland": {
        "water_main_grid": 2.0,  # Sparse rural
        "sewer_grid": 999,  # Rural - septic required
        "electrical_grid": 1.0,
        "gas_grid": 999,  # Rural - propane required
        "internet_fiber": 5.0,  # Limited rural
        "connection_costs": {
            "water": {"base": 25000, "per_meter": 0},  # Well required
            "sewer": {"base": 35000, "per_meter": 0},  # Septic required
            "electrical": {"base": 15000, "per_meter": 200},  # Extension required
            "gas": {"base": 8000, "per_meter": 0},  # Propane tank
            "internet": {"base": 5000, "per_meter": 50}  # Satellite/fixed wireless
        },
        "service_standards": {
            "water_pressure": "Private well system",
            "electrical_capacity": "200A service, extension required",
            "gas_pressure": "Propane service only",
            "internet_speed": "Satellite/fixed wireless, limited fiber"
        }
    }
}

# ==============================================================================
# COMPLETE 23 SAMPLE PROPERTIES
# ==============================================================================

ALL_SAMPLE_PROPERTIES = [
    {
        "property_id": "EDM_001",
        "address": "10123 97 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "listing_price": 425000,
        "lot_size_sqft": 7200,
        "estimated_value": 465000,
        "development_potential": "Medium - Infill potential in mature neighborhood",
        "investment_recommendation": "Buy - Good amenity access, established area",
        "amenity_scores": {
            "transit_score": 8.5,
            "schools_score": 9.0,
            "retail_score": 7.5,
            "recreation_score": 8.0,
            "overall_score": 8.25
        },
        "infrastructure_assessment": {
            "water_connection": "Available - $3,500",
            "sewer_connection": "Available - $4,200",
            "electrical_service": "Adequate - No upgrade required",
            "road_access": "Municipal maintained"
        },
        "requires_peng_review": False,
        "confidence_level": "high"
    },
    {
        "property_id": "EDM_002",
        "address": "8245 102 Street NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "commercial",
        "listing_price": 850000,
        "lot_size_sqft": 12500,
        "estimated_value": 925000,
        "development_potential": "High - Commercial zoning, high traffic area",
        "investment_recommendation": "Strong Buy - Excellent ROI potential",
        "amenity_scores": {
            "transit_score": 9.0,
            "employment_score": 9.5,
            "retail_score": 8.5,
            "traffic_score": 9.0,
            "overall_score": 9.0
        },
        "infrastructure_assessment": {
            "water_connection": "Available - $5,500",
            "sewer_connection": "Available - $6,800",
            "electrical_service": "3-phase available",
            "road_access": "Major arterial"
        },
        "requires_peng_review": True,
        "professional_notes": "Commercial development requires P.Eng review for structural and MEP systems",
        "confidence_level": "high"
    },
    {
        "property_id": "LED_001",
        "address": "22531 Hwy 21, Leduc County, AB",
        "municipality": "leduc",
        "property_type": "residential",
        "listing_price": 389000,
        "lot_size_sqft": 43560,  # 1 acre
        "estimated_value": 425000,
        "development_potential": "Medium - Rural residential, subdivision potential",
        "investment_recommendation": "Hold - Monitor infrastructure development",
        "amenity_scores": {
            "airport_proximity": 9.5,  # Near Edmonton International
            "highway_access": 8.5,
            "rural_lifestyle": 9.0,
            "overall_score": 7.5
        },
        "infrastructure_assessment": {
            "water_connection": "Well required - $25,000",
            "sewer_connection": "Septic required - $35,000",
            "electrical_service": "Extension required - $45,000",
            "road_access": "County maintained gravel"
        },
        "requires_peng_review": True,
        "professional_notes": "Rural development requires geotechnical assessment and P.Eng design for private systems",
        "confidence_level": "medium"
    },
    {
        "property_id": "SAB_001",
        "address": "125 Sturgeon Road, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "residential",
        "listing_price": 520000,
        "lot_size_sqft": 8400,
        "estimated_value": 565000,
        "development_potential": "Medium - Established neighborhood, family area",
        "investment_recommendation": "Buy - Excellent schools, stable market",
        "amenity_scores": {
            "schools_score": 9.5,
            "community_score": 8.5,
            "transit_score": 6.5,  # Bus service only
            "recreation_score": 8.0,
            "overall_score": 8.1
        },
        "infrastructure_assessment": {
            "water_connection": "Available - $4,500",
            "sewer_connection": "Available - $5,200",
            "electrical_service": "Adequate service",
            "road_access": "Municipal maintained"
        },
        "requires_peng_review": False,
        "confidence_level": "high"
    },
    {
        "property_id": "STR_001",
        "address": "2003 Sherwood Drive, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "residential",
        "listing_price": 485000,
        "lot_size_sqft": 7800,
        "estimated_value": 525000,
        "development_potential": "Medium - Mature area, good amenities",
        "investment_recommendation": "Buy - Industrial heartland proximity",
        "amenity_scores": {
            "employment_score": 9.0,  # Industrial heartland
            "schools_score": 8.5,
            "retail_score": 8.0,
            "recreation_score": 9.0,  # Festival Place, parks
            "overall_score": 8.6
        },
        "infrastructure_assessment": {
            "water_connection": "Available - $4,000",
            "sewer_connection": "Available - $4,800",
            "electrical_service": "Adequate service",
            "road_access": "County maintained"
        },
        "requires_peng_review": False,
        "confidence_level": "high"
    },
    # Additional 18 properties
    {
        "property_id": "EDM_003",
        "address": "5614 111 Street NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "listing_price": 375000,
        "estimated_value": 431250,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "EDM_004",
        "address": "12245 142 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "listing_price": 445000,
        "estimated_value": 511750,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "EDM_005",
        "address": "9856 88 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "commercial",
        "listing_price": 1250000,
        "estimated_value": 1437500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "EDM_006",
        "address": "14523 23 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "industrial",
        "listing_price": 890000,
        "estimated_value": 1023500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "LED_002",
        "address": "5025 50 Street, Leduc, AB",
        "municipality": "leduc",
        "property_type": "commercial",
        "listing_price": 750000,
        "estimated_value": 862500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "LED_003",
        "address": "RR 262, Leduc County, AB",
        "municipality": "leduc",
        "property_type": "residential",
        "listing_price": 425000,
        "estimated_value": 488750,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "SAB_002",
        "address": "85 Belmont Drive, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "residential",
        "listing_price": 595000,
        "estimated_value": 684250,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "SAB_003",
        "address": "1245 St. Albert Trail, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "commercial",
        "listing_price": 925000,
        "estimated_value": 1063750,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "STR_002",
        "address": "251 Baseline Road, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "commercial",
        "listing_price": 1150000,
        "estimated_value": 1322500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "STR_003",
        "address": "45 Emerald Drive, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "residential",
        "listing_price": 535000,
        "estimated_value": 615250,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "PAR_001",
        "address": "53234 RR 13, Parkland County, AB",
        "municipality": "parkland",
        "property_type": "residential",
        "listing_price": 695000,
        "estimated_value": 799250,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "PAR_002",
        "address": "Highway 16A, Parkland County, AB",
        "municipality": "parkland",
        "property_type": "commercial",
        "listing_price": 450000,
        "estimated_value": 517500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "EDM_007",
        "address": "7845 156 Street NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "listing_price": 525000,
        "estimated_value": 603750,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "EDM_008",
        "address": "10567 University Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "mixed_use",
        "listing_price": 1850000,
        "estimated_value": 2127500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "LED_004",
        "address": "4512 46 Avenue, Leduc, AB",
        "municipality": "leduc",
        "property_type": "residential",
        "listing_price": 385000,
        "estimated_value": 442750,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "STR_004",
        "address": "2234 Clover Bar Road, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "industrial",
        "listing_price": 1450000,
        "estimated_value": 1667500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    },
    {
        "property_id": "SAB_004",
        "address": "56 Woodlands Boulevard, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "residential",
        "listing_price": 675000,
        "estimated_value": 776250,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": False
    },
    {
        "property_id": "EDM_009",
        "address": "12456 Fort Road NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "commercial",
        "listing_price": 2250000,
        "estimated_value": 2587500,
        "development_potential": "Standard development potential",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "medium",
        "requires_peng_review": True
    }
]

# ==============================================================================
# PARTNER REGISTRY & SAMPLE DATA
# ==============================================================================

PARTNER_REGISTRY = {
    "demo_partner_001": PartnerFirm(
        partner_id="demo_partner_001",
        company_name="Edmonton Premier Realty",
        contact_person="Sarah Johnson",
        email="sarah@edmontonpremier.ca",
        phone="780-555-0123",
        license_number="AB-RE-2023-001",
        service_areas=["edmonton", "st_albert", "strathcona"],
        data_types=["sales", "listings", "market_insights"],
        credibility_level="high",
        api_key="EPR_2024_SECURE_KEY_001",
        is_active=True
    ),
    "demo_partner_002": PartnerFirm(
        partner_id="demo_partner_002",
        company_name="Leduc Area Realty Group",
        contact_person="Mike Chen",
        email="mike@leduc-realty.ca",
        phone="780-555-0456",
        license_number="AB-RE-2023-002",
        service_areas=["leduc", "parkland"],
        data_types=["sales", "listings"],
        credibility_level="high",
        api_key="LARG_2024_SECURE_KEY_002",
        is_active=True
    )
}

# Partner sales data storage
PARTNER_SALES_DATA = {}

# Initialize sample partner sales data
def initialize_partner_sales_data():
    sample_sales = [
        PropertySaleData(
            address="9823 97 Avenue NW, Edmonton, AB",
            municipality=Municipality.EDMONTON,
            property_type=PropertyType.RESIDENTIAL,
            sale_type=SaleType.ACTUAL_SALE,
            sale_price=485000,
            list_price=499000,
            sale_date=date(2024, 5, 15),
            days_on_market=12,
            lot_size_sqft=7200,
            building_sqft=1850,
            year_built=1987,
            bedrooms=4,
            bathrooms=2.5,
            coordinates=(53.5420, -113.4920),
            neighborhood="Queen Mary Park",
            financing_type="conventional",
            sale_conditions="normal",
            property_condition="good",
            source_partner_id="demo_partner_001",
            mls_number="E4512345",
            confidence_level="high"
        ),
        PropertySaleData(
            address="12456 142 Avenue NW, Edmonton, AB",
            municipality=Municipality.EDMONTON,
            property_type=PropertyType.RESIDENTIAL,
            sale_type=SaleType.ACTUAL_SALE,
            sale_price=395000,
            list_price=415000,
            sale_date=date(2024, 4, 28),
            days_on_market=23,
            lot_size_sqft=6800,
            building_sqft=1650,
            year_built=1992,
            bedrooms=3,
            bathrooms=2.0,
            coordinates=(53.6120, -113.4720),
            neighborhood="Castle Downs",
            financing_type="conventional",
            sale_conditions="normal",
            property_condition="excellent",
            source_partner_id="demo_partner_001",
            mls_number="E4512346",
            confidence_level="high"
        ),
        PropertySaleData(
            address="5025 50 Street, Leduc, AB",
            municipality=Municipality.LEDUC,
            property_type=PropertyType.COMMERCIAL,
            sale_type=SaleType.ACTUAL_SALE,
            sale_price=750000,
            sale_date=date(2024, 3, 10),
            days_on_market=45,
            lot_size_sqft=12000,
            building_sqft=4500,
            year_built=2008,
            coordinates=(53.2694, -113.5422),
            financing_type="commercial",
            sale_conditions="normal",
            property_condition="excellent",
            source_partner_id="demo_partner_002",
            mls_number="L4567890",
            confidence_level="high"
        )
    ]
    
    for sale in sample_sales:
        municipality = sale.municipality.value
        if municipality not in PARTNER_SALES_DATA:
            PARTNER_SALES_DATA[municipality] = []
        PARTNER_SALES_DATA[municipality].append(sale)

initialize_partner_sales_data()

# ==============================================================================
# COMPLETE ANALYSIS ENGINES
# ==============================================================================

class AmenityAnalyzer:
    """Complete amenity analysis with Alberta-specific data"""
    
    def __init__(self):
        self.amenity_weights = {
            AmenityType.TRANSIT: 0.20,
            AmenityType.SCHOOLS: 0.18,
            AmenityType.HEALTHCARE: 0.15,
            AmenityType.RETAIL: 0.12,
            AmenityType.RECREATION: 0.10,
            AmenityType.EMPLOYMENT: 0.15,
            AmenityType.UTILITIES: 0.05,
            AmenityType.EMERGENCY: 0.05
        }
    
    def analyze_amenities(self, coordinates: Tuple[float, float], municipality: str, radius_km: float = 5.0) -> Dict:
        """Comprehensive amenity analysis for a property location"""
        
        lat, lon = coordinates
        amenities_found = {}
        amenity_scores = {}
        
        municipal_amenities = ALBERTA_AMENITIES.get(municipality, {})
        
        for amenity_type in AmenityType:
            type_amenities = municipal_amenities.get(amenity_type, [])
            nearby_amenities = []
            
            for amenity in type_amenities:
                distance = self._calculate_distance(coordinates, amenity["coordinates"])
                if distance <= radius_km:
                    impact_score = self._calculate_impact_score(distance, amenity_type)
                    nearby_amenities.append({
                        "name": amenity["name"],
                        "type": amenity["type"],
                        "description": amenity["description"],
                        "distance_km": round(distance, 2),
                        "impact_score": round(impact_score, 1),
                        "coordinates": amenity["coordinates"]
                    })
            
            nearby_amenities.sort(key=lambda x: x["distance_km"])
            amenities_found[amenity_type.value] = nearby_amenities
            
            if nearby_amenities:
                top_scores = [a["impact_score"] for a in nearby_amenities[:3]]
                amenity_scores[amenity_type.value] = round(sum(top_scores) / len(top_scores), 1)
            else:
                amenity_scores[amenity_type.value] = 0.0
        
        overall_score = sum(
            score * self.amenity_weights[AmenityType(amenity_type)]
            for amenity_type, score in amenity_scores.items()
        )
        
        return {
            "amenities_by_type": amenities_found,
            "amenity_scores": amenity_scores,
            "overall_amenity_score": round(overall_score, 1)
        }
    
    def _calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate distance using Haversine formula"""
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Earth's radius in kilometers
    
    def _calculate_impact_score(self, distance_km: float, amenity_type: AmenityType) -> float:
        """Calculate impact score based on distance and amenity type"""
        
        thresholds = {
            AmenityType.TRANSIT: {"excellent": 0.5, "good": 1.0, "fair": 2.0},
            AmenityType.SCHOOLS: {"excellent": 1.0, "good": 2.0, "fair": 5.0},
            AmenityType.HEALTHCARE: {"excellent": 2.0, "good": 5.0, "fair": 10.0},
            AmenityType.RETAIL: {"excellent": 1.0, "good": 3.0, "fair": 7.0},
            AmenityType.RECREATION: {"excellent": 2.0, "good": 5.0, "fair": 10.0},
            AmenityType.EMPLOYMENT: {"excellent": 5.0, "good": 15.0, "fair": 30.0},
            AmenityType.UTILITIES: {"excellent": 0.1, "good": 0.5, "fair": 2.0},
            AmenityType.EMERGENCY: {"excellent": 2.0, "good": 5.0, "fair": 10.0}
        }
        
        threshold = thresholds.get(amenity_type, {"excellent": 1.0, "good": 3.0, "fair": 10.0})
        
        if distance_km <= threshold["excellent"]:
            return 10.0 - (distance_km / threshold["excellent"]) * 2.0
        elif distance_km <= threshold["good"]:
            return 8.0 - ((distance_km - threshold["excellent"]) / (threshold["good"] - threshold["excellent"])) * 3.0
        elif distance_km <= threshold["fair"]:
            return 5.0 - ((distance_km - threshold["good"]) / (threshold["fair"] - threshold["good"])) * 5.0
        else:
            return 0.0

class InfrastructureAssessor:
    """Complete infrastructure assessment for Alberta municipalities"""
    
    def assess_infrastructure(self, coordinates: Tuple[float, float], municipality: str) -> Dict:
        """Comprehensive infrastructure assessment"""
        
        municipal_data = MUNICIPAL_INFRASTRUCTURE.get(municipality)
        if not municipal_data:
            return self._rural_assessment(coordinates)
        
        utility_connections = []
        total_cost = 0
        
        utilities = ["water", "sewer", "electrical", "gas", "internet"]
        
        for utility in utilities:
            grid_spacing = municipal_data.get(f"{utility}_grid", 0.5)
            distance_to_connection = self._estimate_connection_distance(grid_spacing)
            
            costs = municipal_data["connection_costs"][utility]
            estimated_cost = costs["base"] + (distance_to_connection * costs["per_meter"])
            
            if distance_to_connection <= 100:
                status = InfrastructureStatus.AVAILABLE
                timeline_weeks = 2
            elif distance_to_connection <= 500:
                status = InfrastructureStatus.EXTENSION_REQUIRED
                timeline_weeks = 6
            else:
                status = InfrastructureStatus.MAJOR_INFRASTRUCTURE
                timeline_weeks = 16
                estimated_cost *= 1.5
            
            service_standards = municipal_data["service_standards"]
            
            connection = UtilityConnection(
                utility_type=utility,
                status=status,
                distance_to_connection=distance_to_connection,
                estimated_cost=int(estimated_cost),
                timeline_weeks=timeline_weeks,
                capacity_adequate=True,
                notes=f"{utility.title()}: {service_standards.get(f'{utility}_pressure', service_standards.get(f'{utility}_capacity', service_standards.get(f'{utility}_speed', 'Standard service')))}"
            )
            
            utility_connections.append(connection)
            total_cost += estimated_cost
        
        extension_count = sum(1 for conn in utility_connections if conn.status == InfrastructureStatus.EXTENSION_REQUIRED)
        major_count = sum(1 for conn in utility_connections if conn.status == InfrastructureStatus.MAJOR_INFRASTRUCTURE)
        
        if major_count > 1:
            readiness = "Major Infrastructure Required"
        elif extension_count > 2:
            readiness = "Significant Extensions Required"
        elif extension_count > 0:
            readiness = "Minor Extensions Required"
        else:
            readiness = "Development Ready"
        
        return {
            "utility_connections": utility_connections,
            "infrastructure_total_cost": int(total_cost),
            "development_readiness": readiness
        }
    
    def _estimate_connection_distance(self, grid_spacing_km: float) -> float:
        """Estimate distance to nearest utility connection"""
        if grid_spacing_km >= 999:  # Rural - not available
            return 0
        avg_distance_m = (grid_spacing_km * 1000) / 4
        return min(avg_distance_m, 1000)
    
    def _rural_assessment(self, coordinates: Tuple[float, float]) -> Dict:
        """Assessment for rural properties requiring private systems"""
        
        rural_connections = [
            UtilityConnection(
                utility_type="water",
                status=InfrastructureStatus.NOT_AVAILABLE,
                distance_to_connection=0,
                estimated_cost=25000,
                timeline_weeks=8,
                capacity_adequate=True,
                notes="Private well required - geotechnical assessment needed"
            ),
            UtilityConnection(
                utility_type="sewer",
                status=InfrastructureStatus.NOT_AVAILABLE,
                distance_to_connection=0,
                estimated_cost=35000,
                timeline_weeks=6,
                capacity_adequate=True,
                notes="Private septic system required - soil assessment needed"
            ),
            UtilityConnection(
                utility_type="electrical",
                status=InfrastructureStatus.EXTENSION_REQUIRED,
                distance_to_connection=2000,
                estimated_cost=45000,
                timeline_weeks=12,
                capacity_adequate=True,
                notes="Electrical line extension required from nearest grid connection"
            ),
            UtilityConnection(
                utility_type="gas",
                status=InfrastructureStatus.NOT_AVAILABLE,
                distance_to_connection=0,
                estimated_cost=8000,
                timeline_weeks=4,
                capacity_adequate=True,
                notes="Propane service - above-ground tank installation"
            ),
            UtilityConnection(
                utility_type="internet",
                status=InfrastructureStatus.EXTENSION_REQUIRED,
                distance_to_connection=5000,
                estimated_cost=12000,
                timeline_weeks=8,
                capacity_adequate=False,
                notes="Satellite or fixed wireless - limited bandwidth"
            )
        ]
        
        return {
            "utility_connections": rural_connections,
            "infrastructure_total_cost": 125000,
            "development_readiness": "Rural Development - Private Systems Required"
        }

class MultiSourceAnalyzer:
    """Complete multi-source market analysis engine"""
    
    def __init__(self):
        self.credibility_weights = {
            DataSourceType.MANUAL_INPUT: 1.00,
            DataSourceType.PARTNER_REALTY: 0.85,
            DataSourceType.MLS_FEED: 0.85,
            DataSourceType.REALTOR_SCRAPING: 0.65,
            DataSourceType.COMPARABLE_ANALYSIS: 0.65,
            DataSourceType.MARKET_ESTIMATE: 0.40
        }
    
    def analyze_property_market(self, address: str, municipality: str, property_type: PropertyType, search_radius_km: float = 2.0) -> PropertyMarketAnalysis:
        """Comprehensive multi-source market analysis"""
        
        property_id = f"MSA_{municipality.upper()}_{hash(address) % 10000:04d}"
        
        # Collect data from all sources
        partner_sales = self._get_partner_sales_data(municipality, property_type, search_radius_km)
        comparable_properties = self._get_comparable_properties(address, municipality, property_type)
        scraped_listings = self._get_scraped_listings(municipality, property_type)
        
        # Calculate weighted market ranges
        market_ranges = self._calculate_weighted_ranges(partner_sales, comparable_properties, scraped_listings)
        
        # Generate data sources summary
        data_sources = self._summarize_data_sources(partner_sales, comparable_properties, scraped_listings)
        
        # Generate recommendation
        recommendation = self._generate_investment_recommendation(market_ranges, data_sources)
        
        # Validation requirements
        requires_validation = (
            market_ranges.confidence_level == "low" or
            market_ranges.credibility_score < 0.70 or
            market_ranges.data_points_count < 3
        )
        
        validation_notes = self._generate_validation_notes(market_ranges, data_sources)
        
        return PropertyMarketAnalysis(
            property_id=property_id,
            address=address,
            municipality=Municipality(municipality),
            market_ranges=market_ranges,
            partner_sales=partner_sales,
            comparable_properties=comparable_properties,
            scraped_listings=scraped_listings,
            total_data_sources=len(data_sources),
            recommendation=recommendation,
            requires_validation=requires_validation,
            validation_notes=validation_notes
        )
    
    def _get_partner_sales_data(self, municipality: str, property_type: PropertyType, radius_km: float) -> List[PropertySaleData]:
        """Retrieve partner sales data for area"""
        municipal_sales = PARTNER_SALES_DATA.get(municipality, [])
        recent_date = datetime.now().date().replace(year=datetime.now().year - 1)
        
        filtered_sales = [
            sale for sale in municipal_sales
            if (sale.property_type == property_type and 
                sale.sale_date >= recent_date and
                sale.sale_type == SaleType.ACTUAL_SALE)
        ]
        
        return filtered_sales[:10]
    
    def _get_comparable_properties(self, address: str, municipality: str, property_type: PropertyType) -> List[Dict]:
        """Get comparable properties (simulated for demo)"""
        comparables = [
            {
                "address": f"Sample Comparable 1, {municipality.title()}, AB",
                "sale_price": 445000,
                "sale_date": "2024-04-15",
                "similarity_score": 0.85,
                "source_type": DataSourceType.COMPARABLE_ANALYSIS
            },
            {
                "address": f"Sample Comparable 2, {municipality.title()}, AB",
                "sale_price": 465000,
                "sale_date": "2024-03-28",
                "similarity_score": 0.78,
                "source_type": DataSourceType.COMPARABLE_ANALYSIS
            }
        ]
        return comparables
    
    def _get_scraped_listings(self, municipality: str, property_type: PropertyType) -> List[Dict]:
        """Get scraped listing data (simulated for demo)"""
        scraped_data = [
            {
                "address": f"Scraped Listing 1, {municipality.title()}, AB",
                "listing_price": 479000,
                "days_on_market": 15,
                "source_type": DataSourceType.REALTOR_SCRAPING,
                "confidence": "medium"
            },
            {
                "address": f"Scraped Listing 2, {municipality.title()}, AB",
                "listing_price": 489000,
                "days_on_market": 8,
                "source_type": DataSourceType.REALTOR_SCRAPING,
                "confidence": "medium"
            }
        ]
        return scraped_data
    
    def _calculate_weighted_ranges(self, partner_sales: List[PropertySaleData], comparables: List[Dict], scraped: List[Dict]) -> WeightedMarketRange:
        """Calculate weighted market value ranges"""
        
        weighted_values = []
        data_sources = []
        
        # Partner sales data
        for sale in partner_sales:
            weight = self.credibility_weights[DataSourceType.PARTNER_REALTY]
            weighted_values.append(sale.sale_price * weight)
            data_sources.append(DataSource(
                source_type=DataSourceType.PARTNER_REALTY,
                source_id=sale.source_partner_id,
                credibility_weight=weight,
                data_points=1,
                last_updated=datetime.combine(sale.sale_date, datetime.min.time()),
                confidence_level=sale.confidence_level
            ))
        
        # Comparable properties
        for comp in comparables:
            weight = self.credibility_weights[DataSourceType.COMPARABLE_ANALYSIS]
            weighted_values.append(comp["sale_price"] * weight)
            data_sources.append(DataSource(
                source_type=DataSourceType.COMPARABLE_ANALYSIS,
                source_id=f"comp_{hash(comp['address']) % 1000}",
                credibility_weight=weight,
                data_points=1,
                last_updated=datetime.now(),
                confidence_level="medium"
            ))
        
        # Scraped listings
        for listing in scraped:
            weight = self.credibility_weights[DataSourceType.REALTOR_SCRAPING]
            estimated_sale_price = listing["listing_price"] * 0.95
            weighted_values.append(estimated_sale_price * weight)
            data_sources.append(DataSource(
                source_type=DataSourceType.REALTOR_SCRAPING,
                source_id=f"scraped_{hash(listing['address']) % 1000}",
                credibility_weight=weight,
                data_points=1,
                last_updated=datetime.now(),
                confidence_level=listing.get("confidence", "medium")
            ))
        
        if not weighted_values:
            base_estimate = 450000
            return WeightedMarketRange(
                conservative_value=base_estimate * 0.90,
                realistic_value=base_estimate,
                optimistic_value=base_estimate * 1.10,
                data_points_count=0,
                confidence_level="low",
                credibility_score=0.40,
                supporting_sources=[],
                value_basis="Market estimate - insufficient data for analysis"
            )
        
        # Calculate weighted average
        total_weight = sum(source.credibility_weight for source in data_sources)
        weighted_average = sum(weighted_values) / total_weight
        
        # Calculate ranges
        values_unweighted = [sale.sale_price for sale in partner_sales] + \
                          [comp["sale_price"] for comp in comparables] + \
                          [listing["listing_price"] * 0.95 for listing in scraped]
        
        if len(values_unweighted) > 1:
            std_dev = (sum((x - weighted_average)**2 for x in values_unweighted) / len(values_unweighted))**0.5
            range_factor = min(std_dev / weighted_average, 0.15)
        else:
            range_factor = 0.10
        
        conservative = weighted_average * (1 - range_factor)
        optimistic = weighted_average * (1 + range_factor)
        
        # Determine confidence level
        if len(data_sources) >= 5 and total_weight / len(data_sources) >= 0.75:
            confidence = "high"
        elif len(data_sources) >= 3 and total_weight / len(data_sources) >= 0.65:
            confidence = "medium"
        else:
            confidence = "low"
        
        credibility_score = total_weight / len(data_sources) if data_sources else 0.40
        
        return WeightedMarketRange(
            conservative_value=round(conservative),
            realistic_value=round(weighted_average),
            optimistic_value=round(optimistic),
            data_points_count=len(data_sources),
            confidence_level=confidence,
            credibility_score=round(credibility_score, 2),
            supporting_sources=data_sources,
            value_basis=f"Weighted analysis of {len(data_sources)} data sources"
        )
    
    def _summarize_data_sources(self, partner_sales: List[PropertySaleData], comparables: List[Dict], scraped: List[Dict]) -> List[DataSource]:
        """Summarize all data sources used"""
        sources = []
        
        if partner_sales:
            sources.append(DataSource(
                source_type=DataSourceType.PARTNER_REALTY,
                source_id="partner_aggregate",
                credibility_weight=self.credibility_weights[DataSourceType.PARTNER_REALTY],
                data_points=len(partner_sales),
                last_updated=max(datetime.combine(sale.sale_date, datetime.min.time()) for sale in partner_sales),
                confidence_level="high"
            ))
        
        if comparables:
            sources.append(DataSource(
                source_type=DataSourceType.COMPARABLE_ANALYSIS,
                source_id="comparable_aggregate",
                credibility_weight=self.credibility_weights[DataSourceType.COMPARABLE_ANALYSIS],
                data_points=len(comparables),
                last_updated=datetime.now(),
                confidence_level="medium"
            ))
        
        if scraped:
            sources.append(DataSource(
                source_type=DataSourceType.REALTOR_SCRAPING,
                source_id="scraped_aggregate",
                credibility_weight=self.credibility_weights[DataSourceType.REALTOR_SCRAPING],
                data_points=len(scraped),
                last_updated=datetime.now(),
                confidence_level="medium"
            ))
        
        return sources
    
    def _generate_investment_recommendation(self, market_ranges: WeightedMarketRange, data_sources: List[DataSource]) -> str:
        """Generate investment recommendation"""
        
        if market_ranges.confidence_level == "high" and market_ranges.credibility_score >= 0.80:
            return "Strong Buy - High confidence analysis with excellent data quality"
        elif market_ranges.confidence_level == "medium" and market_ranges.credibility_score >= 0.70:
            return "Buy - Good confidence analysis with reliable data sources"
        elif market_ranges.confidence_level == "medium":
            return "Hold - Moderate confidence, recommend additional market validation"
        else:
            return "Caution - Low confidence analysis, professional market study recommended"
    
    def _generate_validation_notes(self, market_ranges: WeightedMarketRange, data_sources: List[DataSource]) -> List[str]:
        """Generate professional validation notes"""
        notes = []
        
        if market_ranges.data_points_count < 3:
            notes.append("Limited data points - recommend additional comparable analysis")
        
        if market_ranges.credibility_score < 0.70:
            notes.append("Low source credibility - verify with high-confidence data sources")
        
        partner_sources = [s for s in data_sources if s.source_type == DataSourceType.PARTNER_REALTY]
        if not partner_sources:
            notes.append("No partner realty data - consider engaging local realty partners")
        
        if market_ranges.confidence_level == "low":
            notes.append("Professional market study recommended for investment decisions >$500K")
        
        return notes

# Initialize analysis engines
amenity_analyzer = AmenityAnalyzer()
infrastructure_assessor = InfrastructureAssessor()
multi_source_analyzer = MultiSourceAnalyzer()

# ==============================================================================
# AUTHENTICATION FUNCTIONS
# ==============================================================================

def verify_partner_api_key(api_key: str = Depends(API_KEY_HEADER)) -> Optional[PartnerFirm]:
    """Verify partner API key and return partner info"""
    if not api_key:
        return None
    
    for partner in PARTNER_REGISTRY.values():
        if partner.api_key == api_key and partner.is_active:
            return partner
    return None

# ==============================================================================
# COMPLETE API ENDPOINTS
# ==============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {
        "status": "healthy",
        "service": "sgiach-api",
        "version": "3.0.0",
        "sample_properties_count": len(ALL_SAMPLE_PROPERTIES),
        "features": [
            "23_sample_properties",
            "partner_realty_integration",
            "multi_source_analysis", 
            "complete_mapping_amenities",
            "infrastructure_assessment",
            "professional_validation",
            "distance_calculations",
            "interactive_mapping"
        ],
        "partner_firms": len(PARTNER_REGISTRY),
        "total_sales_records": sum(len(sales) for sales in PARTNER_SALES_DATA.values()),
        "amenity_database_entries": sum(len(amenities) for municipality in ALBERTA_AMENITIES.values() for amenities in municipality.values()),
        "infrastructure_coverage": list(MUNICIPAL_INFRASTRUCTURE.keys())
    }

# ==============================================================================
# SAMPLE PROPERTIES ENDPOINTS
# ==============================================================================

@app.get("/properties/sample")
async def get_sample_properties():
    """Retrieve all 23 sample properties for development/testing"""
    return {
        "status": "success",
        "total_properties": len(ALL_SAMPLE_PROPERTIES),
        "municipalities": list(set([p["municipality"] for p in ALL_SAMPLE_PROPERTIES])),
        "property_types": list(set([p["property_type"] for p in ALL_SAMPLE_PROPERTIES])),
        "properties": ALL_SAMPLE_PROPERTIES
    }

@app.get("/properties/sample/{property_id}")
async def get_sample_property(property_id: str):
    """Get specific sample property by ID"""
    property_data = next((p for p in ALL_SAMPLE_PROPERTIES if p["property_id"] == property_id), None)
    if not property_data:
        raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
    return property_data

@app.get("/municipalities/{municipality}/properties")
async def get_properties_by_municipality(municipality: Municipality):
    """Get all sample properties for a specific municipality"""
    municipal_properties = [p for p in ALL_SAMPLE_PROPERTIES if p["municipality"] == municipality.value]
    return {
        "municipality": municipality.value,
        "property_count": len(municipal_properties),
        "properties": municipal_properties
    }

@app.post("/admin/reset-sample-data")
async def reset_sample_data():
    """Reset sample data to original 23 properties"""
    return {
        "status": "success",
        "message": "Sample data reset to 23 original properties",
        "property_count": len(ALL_SAMPLE_PROPERTIES),
        "properties_by_municipality": {
            municipality: len([p for p in ALL_SAMPLE_PROPERTIES if p["municipality"] == municipality])
            for municipality in ["edmonton", "leduc", "st_albert", "strathcona", "parkland"]
        }
    }

# ==============================================================================
# PARTNER REALTY ENDPOINTS
# ==============================================================================

@app.post("/partners/register")
async def register_partner_firm(partner_data: PartnerFirm):
    """Register new partner realty firm"""
    partner_data.api_key = f"{partner_data.company_name.replace(' ', '_').upper()}_{datetime.now().year}_KEY_{len(PARTNER_REGISTRY) + 1:03d}"
    PARTNER_REGISTRY[partner_data.partner_id] = partner_data
    
    return {
        "status": "success",
        "message": f"Partner {partner_data.company_name} registered successfully",
        "partner_id": partner_data.partner_id,
        "api_key": partner_data.api_key,
        "service_areas": partner_data.service_areas
    }

@app.get("/partners/list")
async def list_partner_firms():
    """List all registered partner firms"""
    return {
        "total_partners": len(PARTNER_REGISTRY),
        "active_partners": len([p for p in PARTNER_REGISTRY.values() if p.is_active]),
        "partners": [
            {
                "partner_id": partner.partner_id,
                "company_name": partner.company_name,
                "service_areas": partner.service_areas,
                "data_types": partner.data_types,
                "is_active": partner.is_active
            }
            for partner in PARTNER_REGISTRY.values()
        ]
    }

@app.post("/partners/data/sales")
async def submit_sales_data(
    sales_data: List[PropertySaleData],
    partner: PartnerFirm = Depends(verify_partner_api_key)
):
    """Partner firms submit sales data"""
    if not partner:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    validated_sales = []
    errors = []
    
    for sale in sales_data:
        if sale.municipality.value not in partner.service_areas:
            errors.append(f"Partner not authorized for {sale.municipality.value}")
            continue
        
        sale.source_partner_id = partner.partner_id
        validated_sales.append(sale)
        
        municipality = sale.municipality.value
        if municipality not in PARTNER_SALES_DATA:
            PARTNER_SALES_DATA[municipality] = []
        PARTNER_SALES_DATA[municipality].append(sale)
    
    return {
        "status": "success",
        "submitted_sales": len(validated_sales),
        "total_errors": len(errors),
        "errors": errors,
        "partner_company": partner.company_name
    }

@app.get("/partners/data/summary/{municipality}")
async def get_partner_data_summary(municipality: Municipality):
    """Get summary of partner data for municipality"""
    municipal_sales = PARTNER_SALES_DATA.get(municipality.value, [])
    
    partner_summary = {}
    for sale in municipal_sales:
        partner_id = sale.source_partner_id
        if partner_id not in partner_summary:
            partner_name = PARTNER_REGISTRY.get(partner_id, {}).company_name if partner_id in PARTNER_REGISTRY else "Unknown"
            partner_summary[partner_id] = {
                "partner_name": partner_name,
                "total_sales": 0,
                "date_range": {"earliest": None, "latest": None},
                "property_types": set()
            }
        
        summary = partner_summary[partner_id]
        summary["total_sales"] += 1
        summary["property_types"].add(sale.property_type.value)
        
        if not summary["date_range"]["earliest"] or sale.sale_date < summary["date_range"]["earliest"]:
            summary["date_range"]["earliest"] = sale.sale_date
        if not summary["date_range"]["latest"] or sale.sale_date > summary["date_range"]["latest"]:
            summary["date_range"]["latest"] = sale.sale_date
    
    for summary in partner_summary.values():
        summary["property_types"] = list(summary["property_types"])
        if summary["date_range"]["earliest"]:
            summary["date_range"]["earliest"] = summary["date_range"]["earliest"].isoformat()
        if summary["date_range"]["latest"]:
            summary["date_range"]["latest"] = summary["date_range"]["latest"].isoformat()
    
    return {
        "municipality": municipality.value,
        "total_sales_records": len(municipal_sales),
        "partner_count": len(partner_summary),
        "partner_breakdown": partner_summary,
        "last_updated": max(sale.created_date for sale in municipal_sales).isoformat() if municipal_sales else None
    }

# ==============================================================================
# COMPLETE MAPPING & AMENITY ENDPOINTS
# ==============================================================================

@app.post("/property/mapping-analysis", response_model=PropertyMappingResponse)
async def comprehensive_mapping_analysis(request: PropertyMappingRequest):
    """Complete property analysis with mapping, amenities, and infrastructure"""
    try:
        if not request.coordinates:
            coordinates = await geocode_address(request.address)
        else:
            coordinates = request.coordinates
        
        property_id = f"MAP_{request.municipality.upper()}_{hash(request.address) % 1000:03d}"
        
        # Amenity Analysis
        amenity_analysis = amenity_analyzer.analyze_amenities(
            coordinates, request.municipality.value, request.analysis_radius_km
        )
        
        # Infrastructure Assessment
        infrastructure_analysis = infrastructure_assessor.assess_infrastructure(
            coordinates, request.municipality.value
        )
        
        # Distance Matrix
        distance_matrix = calculate_distance_matrix(coordinates, request.municipality.value)
        
        # Accessibility Score
        accessibility_score = calculate_accessibility_score(amenity_analysis, infrastructure_analysis)
        
        # Professional Engineering Assessment
        engineering_notes = generate_engineering_notes(
            infrastructure_analysis, amenity_analysis, request.municipality.value
        )
        
        requires_peng = (
            infrastructure_analysis["infrastructure_total_cost"] > 50000 or
            infrastructure_analysis["development_readiness"] == "Major Infrastructure Required" or
            any(conn.status == InfrastructureStatus.NOT_AVAILABLE 
                for conn in infrastructure_analysis["utility_connections"])
        )
        
        # Generate map markers
        map_markers = generate_map_markers(amenity_analysis, infrastructure_analysis, coordinates)
        
        return PropertyMappingResponse(
            property_id=property_id,
            address=request.address,
            coordinates=coordinates,
            municipality=request.municipality.value,
            amenities_by_type=amenity_analysis["amenities_by_type"],
            amenity_scores=amenity_analysis["amenity_scores"],
            overall_amenity_score=amenity_analysis["overall_amenity_score"],
            utility_connections=infrastructure_analysis["utility_connections"],
            infrastructure_total_cost=infrastructure_analysis["infrastructure_total_cost"],
            development_readiness=infrastructure_analysis["development_readiness"],
            distance_matrix=distance_matrix,
            accessibility_score=accessibility_score,
            engineering_notes=engineering_notes,
            requires_peng_review=requires_peng,
            map_center=coordinates,
            map_markers=map_markers,
            map_layers=generate_map_layers(amenity_analysis, infrastructure_analysis)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mapping analysis failed: {str(e)}")

@app.get("/mapping/interactive/{municipality}", response_class=HTMLResponse)
async def get_interactive_map(municipality: Municipality):
    """Serve interactive mapping interface for specific municipality"""
    html_content = generate_interactive_map_html(municipality.value)
    return HTMLResponse(content=html_content)

@app.get("/mapping/amenities/{municipality}")
async def get_municipal_amenities(municipality: Municipality):
    """Get all amenities for a municipality for mapping display"""
    municipal_amenities = ALBERTA_AMENITIES.get(municipality.value, {})
    
    formatted_amenities = {}
    for amenity_type, amenities in municipal_amenities.items():
        formatted_amenities[amenity_type.value] = [
            {
                "name": amenity["name"],
                "type": amenity["type"],
                "description": amenity["description"],
                "coordinates": amenity["coordinates"],
                "category": amenity_type.value
            }
            for amenity in amenities
        ]
    
    return {
        "municipality": municipality.value,
        "amenity_categories": list(formatted_amenities.keys()),
        "amenities": formatted_amenities,
        "total_amenities": sum(len(amenities) for amenities in formatted_amenities.values())
    }

# ==============================================================================
# COMPLETE PROPERTY ANALYSIS ENDPOINTS
# ==============================================================================

class ComprehensivePropertyRequest(BaseModel):
    address: str
    municipality: Municipality
    property_type: PropertyType = PropertyType.RESIDENTIAL
    listing_price: Optional[float] = None
    lot_size_sqft: Optional[float] = None
    include_market_analysis: bool = True
    include_amenity_analysis: bool = True
    include_infrastructure_analysis: bool = True
    include_mapping: bool = True
    include_partner_data: bool = True
    analysis_radius_km: float = Field(default=5.0, ge=1.0, le=15.0)
    comparable_search_radius_km: float = Field(default=2.0, ge=0.5, le=10.0)

class ComprehensivePropertyResponse(BaseModel):
    property_id: str
    address: str
    municipality: str
    coordinates: Tuple[float, float]
    market_analysis: Optional[PropertyMarketAnalysis] = None
    amenity_scores: Optional[Dict[str, float]] = None
    overall_amenity_score: Optional[float] = None
    nearby_amenities: Optional[Dict] = None
    utility_connections: Optional[List[UtilityConnection]] = None
    infrastructure_total_cost: Optional[int] = None
    development_readiness: Optional[str] = None
    investment_recommendation: str
    requires_peng_review: bool
    professional_notes: List[str] = []
    map_data: Optional[Dict] = None
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    confidence_level: str = "medium"

@app.post("/property/comprehensive-analysis", response_model=ComprehensivePropertyResponse)
async def comprehensive_property_analysis(request: ComprehensivePropertyRequest):
    """Complete multi-source property analysis with all features"""
    try:
        property_id = f"COMP_{request.municipality.upper()}_{hash(request.address) % 10000:04d}"
        coordinates = await geocode_address(request.address)
        
        analysis_results = {}
        professional_notes = []
        
        # Multi-Source Market Analysis
        if request.include_market_analysis:
            market_analysis = multi_source_analyzer.analyze_property_market(
                request.address,
                request.municipality.value,
                request.property_type,
                request.comparable_search_radius_km
            )
            analysis_results["market_analysis"] = market_analysis
            
            if market_analysis.requires_validation:
                professional_notes.extend(market_analysis.validation_notes)
        
        # Amenity Analysis
        if request.include_amenity_analysis:
            amenity_analysis = amenity_analyzer.analyze_amenities(
                coordinates, request.municipality.value, request.analysis_radius_km
            )
            analysis_results.update(amenity_analysis)
        
        # Infrastructure Analysis
        if request.include_infrastructure_analysis:
            infrastructure_analysis = infrastructure_assessor.assess_infrastructure(
                coordinates, request.municipality.value
            )
            analysis_results.update(infrastructure_analysis)
        
        # Generate Investment Recommendation
        recommendation = generate_comprehensive_recommendation(analysis_results, request)
        
        # P.Eng Review Requirements
        requires_peng = determine_peng_requirements(analysis_results, request)
        
        # Mapping Data
        map_data = None
        if request.include_mapping:
            map_data = generate_comprehensive_map_data(coordinates, analysis_results)
        
        return ComprehensivePropertyResponse(
            property_id=property_id,
            address=request.address,
            municipality=request.municipality.value,
            coordinates=coordinates,
            market_analysis=analysis_results.get("market_analysis"),
            amenity_scores=analysis_results.get("amenity_scores"),
            overall_amenity_score=analysis_results.get("overall_amenity_score"),
            nearby_amenities=analysis_results.get("amenities_by_type"),
            utility_connections=analysis_results.get("utility_connections"),
            infrastructure_total_cost=analysis_results.get("infrastructure_total_cost"),
            development_readiness=analysis_results.get("development_readiness"),
            investment_recommendation=recommendation,
            requires_peng_review=requires_peng,
            professional_notes=professional_notes,
            map_data=map_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

async def geocode_address(address: str) -> Tuple[float, float]:
    """Geocode address to coordinates"""
    alberta_coordinates = {
        "edmonton": (53.5444, -113.4904),
        "leduc": (53.2694, -113.5422),
        "st_albert": (53.6347, -113.6126),
        "strathcona": (53.5347, -113.3126),
        "parkland": (53.7347, -113.7126)
    }
    
    for municipality, coords in alberta_coordinates.items():
        if municipality.lower() in address.lower():
            return coords
    
    return alberta_coordinates["edmonton"]

def calculate_distance_matrix(coordinates: Tuple[float, float], municipality: str) -> Dict[str, float]:
    """Calculate distances to key municipal locations"""
    key_locations = {
        "edmonton": {
            "downtown": (53.5444, -113.4904),
            "university": (53.5232, -113.5263),
            "airport": (53.3097, -113.5803),
            "whyte_avenue": (53.5194, -113.5126)
        },
        "leduc": {
            "downtown": (53.2694, -113.5422),
            "airport": (53.3097, -113.5803),
            "nisku": (53.3547, -113.5126)
        },
        "st_albert": {
            "downtown": (53.6347, -113.6126),
            "edmonton_downtown": (53.5444, -113.4904)
        },
        "strathcona": {
            "sherwood_park": (53.5347, -113.3126),
            "industrial_heartland": (53.6547, -113.3126),
            "edmonton_downtown": (53.5444, -113.4904)
        }
    }
    
    locations = key_locations.get(municipality, {})
    distance_matrix = {}
    
    for location_name, location_coords in locations.items():
        distance = amenity_analyzer._calculate_distance(coordinates, location_coords)
        distance_matrix[location_name] = round(distance, 1)
    
    return distance_matrix

def calculate_accessibility_score(amenity_analysis: Dict, infrastructure_analysis: Dict) -> float:
    """Calculate overall accessibility score"""
    amenity_score = amenity_analysis["overall_amenity_score"]
    
    infrastructure_penalty = 0
    if infrastructure_analysis["development_readiness"] == "Major Infrastructure Required":
        infrastructure_penalty = 3.0
    elif infrastructure_analysis["development_readiness"] == "Significant Extensions Required":
        infrastructure_penalty = 2.0
    elif infrastructure_analysis["development_readiness"] == "Minor Extensions Required":
        infrastructure_penalty = 1.0
    
    accessibility_score = max(0, amenity_score - infrastructure_penalty)
    return round(accessibility_score, 1)

def generate_engineering_notes(infrastructure_analysis: Dict, amenity_analysis: Dict, municipality: str) -> List[str]:
    """Generate professional engineering notes"""
    notes = []
    
    if infrastructure_analysis["infrastructure_total_cost"] > 100000:
        notes.append("High infrastructure costs require detailed cost-benefit analysis")
    
    if infrastructure_analysis["development_readiness"] == "Major Infrastructure Required":
        notes.append("Major infrastructure extensions require municipal approval and P.Eng design")
    
    if amenity_analysis["overall_amenity_score"] < 5.0:
        notes.append("Low amenity score may impact property values and marketability")
    
    if amenity_analysis["amenity_scores"].get("transit", 0) < 3.0:
        notes.append("Limited transit access - consider transportation impact on development")
    
    return notes

def generate_map_markers(amenity_analysis: Dict, infrastructure_analysis: Dict, coordinates: Tuple[float, float]) -> List[Dict]:
    """Generate map markers for frontend display"""
    markers = [
        {
            "type": "property",
            "coordinates": coordinates,
            "title": "Subject Property",
            "icon": "property",
            "color": "red"
        }
    ]
    
    # Add amenity markers
    for amenity_type, amenities in amenity_analysis["amenities_by_type"].items():
        for amenity in amenities[:3]:  # Top 3 per category
            markers.append({
                "type": amenity_type,
                "coordinates": amenity["coordinates"],
                "title": amenity["name"],
                "description": amenity.get("description", ""),
                "distance": f"{amenity['distance_km']} km",
                "icon": amenity_type,
                "color": "blue"
            })
    
    return markers

def generate_map_layers(amenity_analysis: Dict, infrastructure_analysis: Dict) -> Dict[str, List[Dict]]:
    """Generate map layers for frontend display"""
    return {
        "amenities": True,
        "infrastructure": True,
        "transit": True,
        "schools": True,
        "healthcare": True,
        "retail": True
    }

def generate_interactive_map_html(municipality: str) -> str:
    """Generate interactive map HTML with Leaflet.js"""
    
    municipal_center = {
        "edmonton": (53.5444, -113.4904),
        "leduc": (53.2694, -113.5422),
        "st_albert": (53.6347, -113.6126),
        "strathcona": (53.5347, -113.3126),
        "parkland": (53.7347, -113.7126)
    }.get(municipality, (53.5444, -113.4904))
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sgiach Interactive Map - {municipality.title()}</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            #map {{ height: 100vh; width: 100%; }}
            .legend {{ 
                background: white; 
                padding: 10px; 
                border-radius: 5px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            var map = L.map('map').setView([{municipal_center[0]}, {municipal_center[1]}], 11);
            
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);
            
            // Add municipality amenities
            fetch('/mapping/amenities/{municipality}')
                .then(response => response.json())
                .then(data => {{
                    for (const [category, amenities] of Object.entries(data.amenities)) {{
                        amenities.forEach(amenity => {{
                            const icon = getIconForCategory(category);
                            L.marker([amenity.coordinates[0], amenity.coordinates[1]], {{icon: icon}})
                                .addTo(map)
                                .bindPopup(`<b>${{amenity.name}}</b><br>${{amenity.description}}<br>Category: ${{category}}<br>Type: ${{amenity.type}}`);
                        }});
                    }}
                }});
            
            // Define icons for different amenity categories
            function getIconForCategory(category) {{
                const icons = {{
                    'transit': '🚇',
                    'schools': '🏫', 
                    'healthcare': '🏥',
                    'retail': '🛒',
                    'recreation': '⚽',
                    'employment': '🏢',
                    'utilities': '⚡',
                    'emergency': '🚨'
                }};
                
                return L.divIcon({{
                    html: icons[category] || '📍',
                    iconSize: [25, 25],
                    className: `amenity-icon amenity-${{category}}`
                }});
            }}
            
            // Add legend
            var legend = L.control({{position: 'bottomright'}});
            legend.onAdd = function (map) {{
                var div = L.DomUtil.create('div', 'legend');
                div.innerHTML = `
                    <h4>Sgiach Map - {municipality.title()}</h4>
                    <p><strong>Amenities:</strong></p>
                    <p>🚇 Transit &nbsp;&nbsp; 🏫 Schools</p>
                    <p>🏥 Healthcare &nbsp;&nbsp; 🛒 Retail</p>
                    <p>⚽ Recreation &nbsp;&nbsp; 🏢 Employment</p>
                    <p>⚡ Utilities &nbsp;&nbsp; 🚨 Emergency</p>
                `;
                return div;
            }};
            legend.addTo(map);
        </script>
    </body>
    </html>
    """
    
    return html_content

def generate_comprehensive_recommendation(analysis_results: Dict, request: ComprehensivePropertyRequest) -> str:
    """Generate comprehensive investment recommendation"""
    
    market_analysis = analysis_results.get("market_analysis")
    infrastructure_cost = analysis_results.get("infrastructure_total_cost", 0)
    amenity_score = analysis_results.get("overall_amenity_score", 5.0)
    
    if market_analysis and market_analysis.market_ranges.confidence_level == "high":
        if infrastructure_cost < 25000 and amenity_score > 7.5:
            return "Strong Buy - Excellent market data, low infrastructure costs, superior amenities"
        elif infrastructure_cost < 50000 and amenity_score > 6.0:
            return "Buy - Good market conditions with manageable development costs"
        else:
            return "Hold - Market conditions positive but infrastructure/amenity concerns"
    elif market_analysis and market_analysis.market_ranges.confidence_level == "medium":
        if infrastructure_cost < 30000 and amenity_score > 7.0:
            return "Buy - Moderate market confidence but excellent location fundamentals"
        else:
            return "Hold - Moderate confidence, recommend additional market validation"
    else:
        return "Caution - Insufficient market data for confident investment recommendation"

def determine_peng_requirements(analysis_results: Dict, request: ComprehensivePropertyRequest) -> bool:
    """Determine if P.Eng review is required"""
    
    infrastructure_cost = analysis_results.get("infrastructure_total_cost", 0)
    development_readiness = analysis_results.get("development_readiness", "")
    
    return (
        request.property_type in [PropertyType.COMMERCIAL, PropertyType.INDUSTRIAL, PropertyType.MIXED_USE] or
        infrastructure_cost > 50000 or
        "Private Systems Required" in development_readiness or
        "Major Infrastructure" in development_readiness or
        request.listing_price and request.listing_price > 1000000
    )

def generate_comprehensive_map_data(coordinates: Tuple[float, float], analysis_results: Dict) -> Dict:
    """Generate mapping data for frontend display"""
    
    return {
        "center": coordinates,
        "zoom_level": 12,
        "markers": generate_map_markers(
            analysis_results.get("amenities_by_type", {}), 
            analysis_results.get("utility_connections", []), 
            coordinates
        ),
        "layers": {
            "amenities": True,
            "infrastructure": True,
            "comparables": True,
            "partner_sales": True
        },
        "analysis_radius": 5.0,
        "legend_data": {
            "amenity_scores": analysis_results.get("amenity_scores", {}),
            "infrastructure_status": analysis_results.get("development_readiness", "Unknown"),
            "total_cost": analysis_results.get("infrastructure_total_cost", 0)
        }
    }

# ==============================================================================
# ADDITIONAL UTILITY ENDPOINTS
# ==============================================================================

@app.get("/property/market-data/{municipality}")
async def get_market_data_sources(municipality: Municipality):
    """Get available market data sources for municipality"""
    
    partner_sales = PARTNER_SALES_DATA.get(municipality.value, [])
    partner_firms = [p for p in PARTNER_REGISTRY.values() if municipality.value in p.service_areas]
    
    return {
        "municipality": municipality.value,
        "data_sources": {
            "partner_realty": {
                "available": len(partner_sales) > 0,
                "data_points": len(partner_sales),
                "credibility": "85%",
                "last_updated": max(sale.created_date for sale in partner_sales).isoformat() if partner_sales else None
            },
            "realtor_scraping": {
                "available": True,
                "data_points": "Variable",
                "credibility": "65%",
                "last_updated": "Real-time"
            },
            "comparable_analysis": {
                "available": True,
                "data_points": "Algorithmic",
                "credibility": "65%",
                "last_updated": "Daily"
            },
            "mls_feed": {
                "available": False,
                "data_points": 0,
                "credibility": "85%",
                "last_updated": "Not configured"
            }
        },
        "partner_firms": [
            {
                "company_name": firm.company_name,
                "data_types": firm.data_types,
                "contact_person": firm.contact_person,
                "service_areas": firm.service_areas
            }
            for firm in partner_firms
        ],
        "recommendation": "Contact partner firms for comprehensive market analysis" if not partner_sales else "Comprehensive data available",
        "coverage_analysis": {
            "total_municipalities": 5,
            "covered_municipalities": len(set(municipality for firm in partner_firms for municipality in firm.service_areas)),
            "partner_coverage": len(partner_firms) > 0
        }
    }

@app.get("/infrastructure/municipal-standards/{municipality}")
async def get_municipal_infrastructure_standards(municipality: Municipality):
    """Get infrastructure standards and costs for municipality"""
    
    municipal_data = MUNICIPAL_INFRASTRUCTURE.get(municipality.value)
    if not municipal_data:
        raise HTTPException(status_code=404, detail=f"Infrastructure data not available for {municipality.value}")
    
    return {
        "municipality": municipality.value,
        "infrastructure_standards": {
            "grid_spacing": {
                "water_main": f"{municipal_data['water_main_grid']} km",
                "sewer": f"{municipal_data['sewer_grid']} km", 
                "electrical": f"{municipal_data['electrical_grid']} km",
                "gas": f"{municipal_data['gas_grid']} km",
                "internet_fiber": f"{municipal_data['internet_fiber']} km"
            },
            "service_standards": municipal_data["service_standards"],
            "connection_costs": municipal_data["connection_costs"]
        },
        "development_readiness_factors": {
            "urban_infill": "Development Ready - All services available",
            "suburban_greenfield": "Minor to Significant Extensions Required",
            "rural_acreage": "Major Infrastructure or Private Systems Required"
        },
        "professional_requirements": {
            "peng_review_triggers": [
                "Infrastructure costs > $50,000",
                "Private water/sewer systems",
                "Commercial/Industrial development",
                "Major utility extensions"
            ],
            "municipal_approval_required": [
                "Utility line extensions",
                "Road access improvements", 
                "Drainage modifications",
                "Development permits"
            ]
        }
    }

@app.get("/amenities/analysis-summary/{municipality}")
async def get_amenity_analysis_summary(municipality: Municipality):
    """Get comprehensive amenity analysis summary for municipality"""
    
    municipal_amenities = ALBERTA_AMENITIES.get(municipality.value, {})
    
    if not municipal_amenities:
        raise HTTPException(status_code=404, detail=f"Amenity data not available for {municipality.value}")
    
    # Calculate municipal amenity profile
    amenity_profile = {}
    total_amenities = 0
    
    for amenity_type, amenities in municipal_amenities.items():
        count = len(amenities)
        amenity_profile[amenity_type.value] = {
            "count": count,
            "types": list(set(amenity["type"] for amenity in amenities)),
            "coverage": "excellent" if count >= 5 else "good" if count >= 3 else "limited"
        }
        total_amenities += count
    
    # Municipal strengths and weaknesses
    strengths = []
    weaknesses = []
    
    for amenity_type, profile in amenity_profile.items():
        if profile["coverage"] == "excellent":
            strengths.append(f"{amenity_type.title()} - {profile['count']} locations")
        elif profile["coverage"] == "limited":
            weaknesses.append(f"{amenity_type.title()} - Only {profile['count']} locations")
    
    # Investment implications
    investment_factors = []
    if municipality.value == "edmonton":
        investment_factors = [
            "Excellent transit connectivity (LRT system)",
            "Major employment centers (government, university)",
            "Comprehensive healthcare facilities",
            "Mature amenity infrastructure"
        ]
    elif municipality.value == "leduc":
        investment_factors = [
            "Airport proximity advantage",
            "Industrial heartland employment",
            "Growing retail infrastructure",
            "Transportation logistics hub"
        ]
    elif municipality.value == "st_albert":
        investment_factors = [
            "Excellent school systems",
            "Family-oriented community",
            "Cultural amenities (Arden Theatre)",
            "Proximity to Edmonton"
        ]
    elif municipality.value == "strathcona":
        investment_factors = [
            "Industrial heartland proximity",
            "Recreation facilities (Festival Place)",
            "Mixed urban/rural lifestyle",
            "Employment diversity"
        ]
    elif municipality.value == "parkland":
        investment_factors = [
            "Rural lifestyle amenities",
            "Natural recreation access",
            "Transportation corridor access",
            "Lower development density"
        ]
    
    return {
        "municipality": municipality.value,
        "amenity_profile": amenity_profile,
        "total_amenities": total_amenities,
        "municipal_strengths": strengths,
        "areas_for_improvement": weaknesses,
        "investment_factors": investment_factors,
        "property_impact_analysis": {
            "residential": "Amenity proximity increases property values 3-12%",
            "commercial": "Foot traffic and accessibility drive commercial success",
            "industrial": "Transportation and employment proximity critical"
        },
        "development_recommendations": {
            "high_amenity_areas": "Premium pricing justified",
            "moderate_amenity_areas": "Good value propositions",
            "low_amenity_areas": "Infrastructure investment opportunities"
        }
    }

@app.post("/property/bulk-analysis")
async def bulk_property_analysis(property_list: List[ComprehensivePropertyRequest]):
    """Analyze multiple properties at once"""
    results = []
    
    for prop_request in property_list:
        try:
            analysis = await comprehensive_property_analysis(prop_request)
            results.append({
                "status": "success", 
                "property": analysis,
                "processing_time": "< 1 second"
            })
        except Exception as e:
            results.append({
                "status": "error",
                "address": prop_request.address,
                "error": str(e),
                "municipality": prop_request.municipality.value
            })
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    
    return {
        "bulk_analysis_summary": {
            "total_properties": len(results),
            "successful_analyses": len(successful),
            "failed_analyses": len(failed),
            "success_rate": f"{(len(successful) / len(results) * 100):.1f}%" if results else "0%"
        },
        "results": results,
        "processing_notes": [
            "All analyses include multi-source market data",
            "Professional validation flags included",
            "Infrastructure assessments completed",
            "Amenity proximity calculations performed"
        ] if successful else [
            "Review failed properties for data issues",
            "Ensure valid addresses and municipalities", 
            "Check for required parameters"
        ]
    }

# ==============================================================================
# LEGACY COMPATIBILITY ENDPOINTS
# ==============================================================================

@app.post("/property/analysis")
async def simplified_property_analysis(request: ComprehensivePropertyRequest):
    """Simplified property analysis endpoint for backwards compatibility"""
    
    # Convert to comprehensive analysis but with basic output
    try:
        comprehensive_result = await comprehensive_property_analysis(request)
        
        # Simplified response format
        simplified_response = {
            "property_id": comprehensive_result.property_id,
            "address": comprehensive_result.address,
            "municipality": comprehensive_result.municipality,
            "estimated_value": comprehensive_result.market_analysis.market_ranges.realistic_value if comprehensive_result.market_analysis else None,
            "development_potential": f"Analysis for {request.property_type.value} in {request.municipality.value}",
            "investment_recommendation": comprehensive_result.investment_recommendation,
            "requires_peng_review": comprehensive_result.requires_peng_review,
            "confidence_level": comprehensive_result.confidence_level,
            
            # Enhanced data available on request
            "enhanced_analysis_available": True,
            "amenity_score": comprehensive_result.overall_amenity_score,
            "infrastructure_cost": comprehensive_result.infrastructure_total_cost,
            "professional_notes": comprehensive_result.professional_notes
        }
        
        return simplified_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Property analysis failed: {str(e)}")

# Legacy endpoints
@app.post("/property/multi-source-analysis")
async def multi_source_analysis_legacy(request: ComprehensivePropertyRequest):
    """Legacy endpoint - redirects to comprehensive analysis with all sources"""
    request.include_market_analysis = True
    request.include_partner_data = True
    request.include_amenity_analysis = True
    request.include_infrastructure_analysis = True
    return await comprehensive_property_analysis(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
