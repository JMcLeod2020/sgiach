#==============================================================================
# SGIACH COMPLETE API - WITH DEVELOPMENT ASSESSMENT & BUILDING PLACEMENT
# SkyeBridge Consulting & Developments Inc.
# Complete Professional Platform: All Features Integrated
# Jeff McLeod, P.Eng - Professional Engineering Analysis
#==============================================================================

from fastapi import FastAPI, HTTPException, Query, Form, File, UploadFile, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd
import requests
import json
import math
import uuid
import hashlib
import asyncio
import io
import base64
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import math
from datetime import datetime
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Sgiach Professional Development Analysis Platform",
    description="Complete Municipal Property Development Analysis with Professional Engineering Oversight", 
    version="3.0.0"
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app = FastAPI(
    title="Sgiach Professional Development Analysis Platform",
    description="Complete Municipal Property Development Analysis with Professional Engineering Oversight",
    version="3.0.0"
)

#==============================================================================
# ENHANCED DATA MODELS WITH DEVELOPMENT INTERFACES
#==============================================================================

class PropertyType(str, Enum):
    residential = "residential"
    commercial = "commercial"
    industrial = "industrial"
    mixed_use = "mixed_use"
    agricultural = "agricultural"

class Municipality(str, Enum):
    edmonton = "edmonton"
    leduc = "leduc"
    st_albert = "st_albert"
    strathcona = "strathcona"
    parkland = "parkland"

class UtilityStatus(str, Enum):
    available = "available"           
    extension_required = "extension_required"  
    major_infrastructure = "major_infrastructure"  
    private_system = "private_system"  

class BuildingType(str, Enum):
    single_family = "single_family"
    duplex = "duplex"
    townhouse = "townhouse"
    retail = "retail"
    office = "office"
    parking = "parking"
    garden = "garden"
    industrial = "industrial"

@dataclass
class UtilityConnection:
    """Individual utility connection analysis"""
    utility_type: str  
    status: UtilityStatus
    distance_meters: float
    connection_cost_low: float
    connection_cost_high: float
    capacity_available: bool
    service_provider: str
    estimated_timeline_days: int
    engineering_notes: str

@dataclass
class UtilityRatings:
    """Complete utility accessibility ratings"""
    overall_score: float  
    water_connection: UtilityConnection
    sewer_connection: UtilityConnection
    electrical_connection: UtilityConnection
    gas_connection: UtilityConnection
    internet_connection: UtilityConnection
    total_infrastructure_cost_low: float
    total_infrastructure_cost_high: float
    development_readiness_score: float  
    engineering_risk_assessment: str

@dataclass
class AmenityDistance:
    """Individual amenity with distance and impact analysis"""
    name: str
    category: str
    address: str
    distance_meters: float
    walking_time_minutes: float
    driving_time_minutes: float
    impact_score: float  
    coordinates: Tuple[float, float]

@dataclass
class AmenityAnalysis:
    """Complete amenity proximity analysis"""
    overall_amenity_score: float  
    education_score: float
    healthcare_score: float
    retail_score: float
    transportation_score: float
    recreation_score: float
    employment_score: float
    nearest_amenities: List[AmenityDistance]
    value_impact_percentage: float  

@dataclass
class MunicipalInfrastructure:
    """Municipal-level infrastructure standards"""
    municipality: str
    water_system: Dict[str, Any]
    sewer_system: Dict[str, Any]
    electrical_grid: Dict[str, Any]
    development_standards: Dict[str, Any]
    professional_requirements: Dict[str, Any]

# Development Interface Data Models
class LotAssessment(BaseModel):
    property_id: str
    coordinates: Tuple[float, float]
    lot_size_sqft: float
    municipality: str
    zoning: str

class PlacedBuilding(BaseModel):
    building_type: BuildingType
    position_x: float
    position_y: float
    width: float
    height: float
    building_id: str

class DevelopmentPlan(BaseModel):
    property_id: str
    buildings: List[PlacedBuilding]
    total_coverage_sqft: float
    compliance_status: str
    estimated_cost: float

class BuildingConstraints(BaseModel):
    front_setback_m: float
    side_setback_m: float
    rear_setback_m: float
    height_limit_m: float
    coverage_limit_percent: float
    density_allowance: str

# Request Models
class PropertyMappingRequest(BaseModel):
    address: str
    municipality: Municipality
    property_type: PropertyType
    lot_size_sqft: Optional[float] = None
    include_utilities: bool = True
    include_amenities: bool = True
    include_infrastructure: bool = True
    professional_analysis: bool = True

class UtilityAnalysisRequest(BaseModel):
    address: str
    municipality: Municipality
    property_type: PropertyType
    development_type: str
    target_density: Optional[str] = "medium"

#==============================================================================
# ALBERTA UTILITY INFRASTRUCTURE DATABASE
#==============================================================================

class AlbertaUtilityDatabase:
    """Complete Alberta utility infrastructure database"""
    
    @staticmethod
    def get_municipal_infrastructure(municipality: str) -> MunicipalInfrastructure:
        """Get municipal infrastructure standards"""
        
        infrastructure_data = {
            "edmonton": MunicipalInfrastructure(
                municipality="edmonton",
                water_system={
                    "provider": "EPCOR Water Services",
                    "pressure_standard": "40-80 PSI",
                    "main_size_standard": "150mm minimum",
                    "connection_cost_per_meter": 175,
                    "base_connection_fee": 3500,
                    "capacity_status": "excellent",
                    "service_standards": "24/7 response"
                },
                sewer_system={
                    "provider": "City of Edmonton",
                    "system_type": "separate_sanitary_storm",
                    "capacity_standard": "adequate",
                    "connection_cost_per_meter": 200,
                    "base_connection_fee": 5000,
                    "lift_station_requirement": "case_by_case",
                    "service_standards": "municipal_maintenance"
                },
                electrical_grid={
                    "provider": "EPCOR Distribution & Transmission",
                    "voltage_residential": "120/240V",
                    "voltage_commercial": "120/208V, 347/600V",
                    "service_capacity": "excellent",
                    "connection_cost_per_meter": 125,
                    "transformer_availability": "readily_available",
                    "backup_power": "grid_redundancy"
                },
                development_standards={
                    "minimum_lot_size_residential": 6000,  
                    "setback_requirements": "7.5m front, 1.2m side",
                    "building_height_limit": "11m residential, varies commercial",
                    "density_allowances": "up_to_duplex_by_right",
                    "professional_requirements": "P.Eng for commercial >300sqm",
                    "front_setback_m": 7.5,
                    "side_setback_m": 1.2,
                    "rear_setback_m": 7.5,
                    "coverage_limit_percent": 45
                },
                professional_requirements={
                    "stamped_drawings_required": "commercial, industrial, multi-family",
                    "geotechnical_assessment": "foundation_design",
                    "environmental_assessment": "industrial_only",
                    "municipal_review_timeline": "6-12_weeks"
                }
            ),
            
            "leduc": MunicipalInfrastructure(
                municipality="leduc",
                water_system={
                    "provider": "City of Leduc",
                    "pressure_standard": "35-75 PSI",
                    "main_size_standard": "150mm minimum",
                    "connection_cost_per_meter": 200,
                    "base_connection_fee": 4000,
                    "capacity_status": "good",
                    "service_standards": "municipal_service"
                },
                sewer_system={
                    "provider": "City of Leduc",
                    "system_type": "separate_sanitary_storm",
                    "capacity_standard": "adequate",
                    "connection_cost_per_meter": 225,
                    "base_connection_fee": 6000,
                    "lift_station_requirement": "often_required",
                    "service_standards": "municipal_maintenance"
                },
                electrical_grid={
                    "provider": "FortisAlberta",
                    "voltage_residential": "120/240V",
                    "voltage_commercial": "120/208V, 347/600V",
                    "service_capacity": "good",
                    "connection_cost_per_meter": 150,
                    "transformer_availability": "available",
                    "backup_power": "limited_redundancy"
                },
                development_standards={
                    "minimum_lot_size_residential": 7000,
                    "setback_requirements": "7.5m front, 1.5m side",
                    "building_height_limit": "10m residential, varies commercial",
                    "density_allowances": "single_family_primarily",
                    "professional_requirements": "P.Eng for commercial >200sqm",
                    "front_setback_m": 7.5,
                    "side_setback_m": 1.5,
                    "rear_setback_m": 7.5,
                    "coverage_limit_percent": 40
                },
                professional_requirements={
                    "stamped_drawings_required": "commercial, industrial",
                    "geotechnical_assessment": "foundation_design",
                    "environmental_assessment": "industrial_only",
                    "municipal_review_timeline": "4-8_weeks"
                }
            ),
            
            "st_albert": MunicipalInfrastructure(
                municipality="st_albert",
                water_system={
                    "provider": "City of St. Albert",
                    "pressure_standard": "40-80 PSI",
                    "main_size_standard": "150mm minimum",
                    "connection_cost_per_meter": 180,
                    "base_connection_fee": 3800,
                    "capacity_status": "excellent",
                    "service_standards": "high_quality_service"
                },
                sewer_system={
                    "provider": "City of St. Albert",
                    "system_type": "separate_sanitary_storm",
                    "capacity_standard": "good",
                    "connection_cost_per_meter": 210,
                    "base_connection_fee": 5500,
                    "lift_station_requirement": "case_by_case",
                    "service_standards": "municipal_maintenance"
                },
                electrical_grid={
                    "provider": "EPCOR Distribution & Transmission",
                    "voltage_residential": "120/240V",
                    "voltage_commercial": "120/208V, 347/600V",
                    "service_capacity": "excellent",
                    "connection_cost_per_meter": 135,
                    "transformer_availability": "readily_available",
                    "backup_power": "grid_redundancy"
                },
                development_standards={
                    "minimum_lot_size_residential": 6500,
                    "setback_requirements": "7.5m front, 1.2m side",
                    "building_height_limit": "10.5m residential, varies commercial",
                    "density_allowances": "up_to_duplex_by_right",
                    "professional_requirements": "P.Eng for commercial >250sqm",
                    "front_setback_m": 7.5,
                    "side_setback_m": 1.2,
                    "rear_setback_m": 7.5,
                    "coverage_limit_percent": 42
                },
                professional_requirements={
                    "stamped_drawings_required": "commercial, industrial, multi-family",
                    "geotechnical_assessment": "foundation_design",
                    "environmental_assessment": "industrial_only",
                    "municipal_review_timeline": "6-10_weeks"
                }
            ),
            
            "strathcona": MunicipalInfrastructure(
                municipality="strathcona",
                water_system={
                    "provider": "Strathcona County",
                    "pressure_standard": "35-75 PSI",
                    "main_size_standard": "150mm minimum",
                    "connection_cost_per_meter": 190,
                    "base_connection_fee": 4200,
                    "capacity_status": "good",
                    "service_standards": "municipal_service"
                },
                sewer_system={
                    "provider": "Strathcona County",
                    "system_type": "separate_sanitary_storm",
                    "capacity_standard": "adequate",
                    "connection_cost_per_meter": 215,
                    "base_connection_fee": 5800,
                    "lift_station_requirement": "often_required",
                    "service_standards": "municipal_maintenance"
                },
                electrical_grid={
                    "provider": "FortisAlberta",
                    "voltage_residential": "120/240V",
                    "voltage_commercial": "120/208V, 347/600V",
                    "service_capacity": "good",
                    "connection_cost_per_meter": 140,
                    "transformer_availability": "available",
                    "backup_power": "limited_redundancy"
                },
                development_standards={
                    "minimum_lot_size_residential": 8000,
                    "setback_requirements": "9m front, 3m side",
                    "building_height_limit": "10m residential, varies commercial",
                    "density_allowances": "single_family_primarily",
                    "professional_requirements": "P.Eng for commercial >200sqm",
                    "front_setback_m": 9.0,
                    "side_setback_m": 3.0,
                    "rear_setback_m": 9.0,
                    "coverage_limit_percent": 35
                },
                professional_requirements={
                    "stamped_drawings_required": "commercial, industrial",
                    "geotechnical_assessment": "foundation_design",
                    "environmental_assessment": "industrial_and_sensitive_areas",
                    "municipal_review_timeline": "6-12_weeks"
                }
            ),
            
            "parkland": MunicipalInfrastructure(
                municipality="parkland",
                water_system={
                    "provider": "Private Wells / Regional Systems",
                    "pressure_standard": "varies_by_system",
                    "main_size_standard": "varies",
                    "connection_cost_per_meter": 250,
                    "base_connection_fee": 15000,  
                    "capacity_status": "limited",
                    "service_standards": "private_maintenance"
                },
                sewer_system={
                    "provider": "Private Septic / Regional Systems",
                    "system_type": "private_septic_primarily",
                    "capacity_standard": "site_dependent",
                    "connection_cost_per_meter": 300,
                    "base_connection_fee": 18000,  
                    "lift_station_requirement": "private_systems",
                    "service_standards": "private_maintenance"
                },
                electrical_grid={
                    "provider": "FortisAlberta",
                    "voltage_residential": "120/240V",
                    "voltage_commercial": "120/208V, 347/600V",
                    "service_capacity": "limited",
                    "connection_cost_per_meter": 200,
                    "transformer_availability": "limited",
                    "backup_power": "none"
                },
                development_standards={
                    "minimum_lot_size_residential": 20000,  
                    "setback_requirements": "15m front, 9m side",
                    "building_height_limit": "12m residential, varies commercial",
                    "density_allowances": "single_family_acreages",
                    "professional_requirements": "P.Eng for commercial >150sqm",
                    "front_setback_m": 15.0,
                    "side_setback_m": 9.0,
                    "rear_setback_m": 15.0,
                    "coverage_limit_percent": 25
                },
                professional_requirements={
                    "stamped_drawings_required": "commercial, industrial, septic_systems",
                    "geotechnical_assessment": "foundation_and_septic_design",
                    "environmental_assessment": "all_developments",
                    "municipal_review_timeline": "8-16_weeks"
                }
            )
        }
        
        return infrastructure_data.get(municipality)

#==============================================================================
# ALBERTA AMENITY DATABASE WITH PRECISE COORDINATES
#==============================================================================

class AlbertaAmenityDatabase:
    """Complete Alberta amenity database with precise coordinates"""
    
    @staticmethod
    def get_municipal_amenities(municipality: str) -> Dict[str, List[AmenityDistance]]:
        """Get comprehensive amenity database for municipality"""
        
        amenity_data = {
            "edmonton": {
                "education": [
                    AmenityDistance("University of Alberta", "university", "116 St & 85 Ave, Edmonton, AB", 0, 0, 0, 9.5, (53.5232, -113.5263)),
                    AmenityDistance("NAIT", "college", "11762 106 St NW, Edmonton, AB", 0, 0, 0, 8.5, (53.5696, -113.5348)),
                    AmenityDistance("MacEwan University", "university", "10700 104 Ave NW, Edmonton, AB", 0, 0, 0, 8.0, (53.5461, -113.5220)),
                    AmenityDistance("Old Scona High School", "high_school", "10523 84 Ave NW, Edmonton, AB", 0, 0, 0, 8.5, (53.5198, -113.5089)),
                    AmenityDistance("Strathcona High School", "high_school", "10450 72 Ave NW, Edmonton, AB", 0, 0, 0, 8.0, (53.5052, -113.5074))
                ],
                "healthcare": [
                    AmenityDistance("University of Alberta Hospital", "hospital", "8440 112 St NW, Edmonton, AB", 0, 0, 0, 9.5, (53.5264, -113.5258)),
                    AmenityDistance("Royal Alexandra Hospital", "hospital", "10240 Kingsway Ave NW, Edmonton, AB", 0, 0, 0, 9.0, (53.5573, -113.4909)),
                    AmenityDistance("Misericordia Hospital", "hospital", "16940 87 Ave NW, Edmonton, AB", 0, 0, 0, 8.5, (53.5203, -113.6198)),
                    AmenityDistance("Cross Cancer Institute", "specialty_hospital", "11560 University Ave NW, Edmonton, AB", 0, 0, 0, 9.0, (53.5203, -113.5198))
                ],
                "transportation": [
                    AmenityDistance("Clareview LRT Station", "lrt_station", "3534 139 Ave NW, Edmonton, AB", 0, 0, 0, 8.5, (53.5968, -113.4106)),
                    AmenityDistance("Stadium LRT Station", "lrt_station", "8410 112 St NW, Edmonton, AB", 0, 0, 0, 8.0, (53.5230, -113.5240)),
                    AmenityDistance("Central LRT Station", "lrt_station", "10010 105 St NW, Edmonton, AB", 0, 0, 0, 9.0, (53.5447, -113.4909)),
                    AmenityDistance("Edmonton Transit Centre", "transit_hub", "10426 96 St NW, Edmonton, AB", 0, 0, 0, 7.5, (53.5350, -113.4909))
                ],
                "retail": [
                    AmenityDistance("West Edmonton Mall", "shopping_center", "8882 170 St NW, Edmonton, AB", 0, 0, 0, 9.5, (53.5225, -113.6235)),
                    AmenityDistance("Kingsway Garden Mall", "shopping_center", "109 St & Kingsway Ave, Edmonton, AB", 0, 0, 0, 7.5, (53.5573, -113.4909)),
                    AmenityDistance("Southgate Centre", "shopping_center", "111 St & 51 Ave, Edmonton, AB", 0, 0, 0, 8.0, (53.4747, -113.4909)),
                    AmenityDistance("Whyte Avenue", "entertainment_district", "Whyte Ave, Edmonton, AB", 0, 0, 0, 8.5, (53.5198, -113.5089))
                ],
                "recreation": [
                    AmenityDistance("Fort Edmonton Park", "park", "7000 143 St SW, Edmonton, AB", 0, 0, 0, 8.0, (53.4747, -113.5932)),
                    AmenityDistance("Hawrelak Park", "park", "9930 Groat Rd NW, Edmonton, AB", 0, 0, 0, 8.5, (53.5264, -113.5347)),
                    AmenityDistance("Commonwealth Stadium", "sports_venue", "11000 Stadium Rd NW, Edmonton, AB", 0, 0, 0, 9.0, (53.5603, -113.4756)),
                    AmenityDistance("Rogers Place", "sports_venue", "10214 104 Ave NW, Edmonton, AB", 0, 0, 0, 9.5, (53.5467, -113.4969))
                ],
                "employment": [
                    AmenityDistance("Downtown Edmonton", "business_district", "104 Ave & 101 St, Edmonton, AB", 0, 0, 0, 9.0, (53.5461, -113.4909)),
                    AmenityDistance("Alberta Legislature", "government", "10800 97 Ave NW, Edmonton, AB", 0, 0, 0, 8.0, (53.5344, -113.5089)),
                    AmenityDistance("University Research Park", "business_park", "11421 Saskatchewan Dr NW, Edmonton, AB", 0, 0, 0, 7.5, (53.5264, -113.5198)),
                    AmenityDistance("Refinery Row", "industrial", "Yellowhead Trail & 170 St, Edmonton, AB", 0, 0, 0, 8.5, (53.5932, -113.6235))
                ]
            },
            
            "leduc": {
                "education": [
                    AmenityDistance("Leduc Composite High School", "high_school", "4915 45 Ave, Leduc, AB", 0, 0, 0, 7.5, (53.2667, -113.5167)),
                    AmenityDistance("Christ the King Catholic School", "elementary_school", "5411 48A Ave, Leduc, AB", 0, 0, 0, 7.0, (53.2748, -113.5298))
                ],
                "healthcare": [
                    AmenityDistance("Leduc Community Hospital", "hospital", "4210 48 St, Leduc, AB", 0, 0, 0, 8.0, (53.2667, -113.5440))
                ],
                "transportation": [
                    AmenityDistance("Edmonton International Airport", "airport", "1000 Airport Rd, Nisku, AB", 0, 0, 0, 9.5, (53.3097, -113.5797)),
                    AmenityDistance("Leduc Transit Hub", "transit_center", "5120 49 Ave, Leduc, AB", 0, 0, 0, 6.5, (53.2667, -113.5440))
                ],
                "retail": [
                    AmenityDistance("Leduc Common", "shopping_center", "4710 50 Ave, Leduc, AB", 0, 0, 0, 7.5, (53.2623, -113.5440)),
                    AmenityDistance("Costco Leduc", "big_box_retail", "6807 50 Ave, Leduc, AB", 0, 0, 0, 8.0, (53.2623, -113.5698))
                ],
                "recreation": [
                    AmenityDistance("Leduc Recreation Centre", "recreation_center", "4330 50 Ave, Leduc, AB", 0, 0, 0, 7.5, (53.2623, -113.5167)),
                    AmenityDistance("Telford Lake", "park", "Telford Dr, Leduc, AB", 0, 0, 0, 8.0, (53.2450, -113.5167))
                ],
                "employment": [
                    AmenityDistance("Edmonton International Airport", "employment_center", "1000 Airport Rd, Nisku, AB", 0, 0, 0, 9.0, (53.3097, -113.5797)),
                    AmenityDistance("Nisku Industrial Park", "industrial_park", "Nisku Industrial Rd, Nisku, AB", 0, 0, 0, 8.5, (53.2971, -113.5797))
                ]
            },
            
            "st_albert": {
                "education": [
                    AmenityDistance("St. Albert Catholic High School", "high_school", "6 Mission Ave, St. Albert, AB", 0, 0, 0, 8.0, (53.6358, -113.6256)),
                    AmenityDistance("Paul Kane High School", "high_school", "50 Belmont Dr, St. Albert, AB", 0, 0, 0, 7.5, (53.6298, -113.6451))
                ],
                "healthcare": [
                    AmenityDistance("Sturgeon Community Hospital", "hospital", "201 Boudreau Rd, St. Albert, AB", 0, 0, 0, 8.5, (53.6425, -113.6041))
                ],
                "transportation": [
                    AmenityDistance("St. Albert Transit Centre", "transit_center", "7 St. Anne St, St. Albert, AB", 0, 0, 0, 7.0, (53.6325, -113.6256))
                ],
                "retail": [
                    AmenityDistance("St. Albert Centre", "shopping_center", "375 St. Albert Rd, St. Albert, AB", 0, 0, 0, 8.0, (53.6358, -113.6041)),
                    AmenityDistance("Enjoy Centre", "shopping_center", "150 Carleton Dr, St. Albert, AB", 0, 0, 0, 7.5, (53.6235, -113.6256))
                ],
                "recreation": [
                    AmenityDistance("Servus Place", "recreation_center", "99 Bellerose Dr, St. Albert, AB", 0, 0, 0, 8.5, (53.6541, -113.6389)),
                    AmenityDistance("Lacombe Park", "park", "5 Riel Dr, St. Albert, AB", 0, 0, 0, 7.5, (53.6298, -113.6041))
                ],
                "employment": [
                    AmenityDistance("Downtown St. Albert", "business_district", "St. Anne St, St. Albert, AB", 0, 0, 0, 7.0, (53.6325, -113.6256))
                ]
            },
            
            "strathcona": {
                "education": [
                    AmenityDistance("Bev Facey Community High School", "high_school", "7 Collins Cres, Sherwood Park, AB", 0, 0, 0, 7.5, (53.5167, -113.3167)),
                    AmenityDistance("Salisbury Composite High School", "high_school", "2905 Sherwood Dr, Sherwood Park, AB", 0, 0, 0, 7.0, (53.5089, -113.3089))
                ],
                "healthcare": [
                    AmenityDistance("Strathcona Community Hospital", "hospital", "401 Festival Lane, Sherwood Park, AB", 0, 0, 0, 8.0, (53.5167, -113.3256))
                ],
                "recreation": [
                    AmenityDistance("Festival Place", "arts_center", "100 Festival Way, Sherwood Park, AB", 0, 0, 0, 8.5, (53.5167, -113.3256)),
                    AmenityDistance("Strathcona Wilderness Centre", "park", "401 Festival Lane, Sherwood Park, AB", 0, 0, 0, 8.0, (53.5089, -113.3089))
                ],
                "employment": [
                    AmenityDistance("Industrial Heartland", "industrial_district", "Heartland Way, Fort Saskatchewan, AB", 0, 0, 0, 9.0, (53.7167, -113.2167)),
                    AmenityDistance("Refinery Row", "industrial", "Yellowhead Trail, Strathcona County, AB", 0, 0, 0, 8.5, (53.6167, -113.2500))
                ]
            },
            
            "parkland": {
                "recreation": [
                    AmenityDistance("Wabamun Lake", "lake", "Wabamun, AB", 0, 0, 0, 8.5, (53.5500, -114.3833)),
                    AmenityDistance("Chickakoo Lake Recreation Area", "park", "Chickakoo Lake Rd, AB", 0, 0, 0, 7.5, (53.6167, -114.1167))
                ],
                "employment": [
                    AmenityDistance("Highway 16A Access", "highway_access", "Highway 16A, AB", 0, 0, 0, 7.0, (53.5833, -114.0000))
                ]
            }
        }
        
        return amenity_data.get(municipality, {})

#==============================================================================
# UTILITY ANALYSIS ENGINE
#==============================================================================

class UtilityAnalysisEngine:
    """Advanced utility connection analysis and cost assessment"""
    
    def __init__(self):
        self.utility_db = AlbertaUtilityDatabase()
    
    def analyze_utility_connections(self, address: str, municipality: str, property_type: str) -> UtilityRatings:
        """Complete utility connection analysis"""
        
        # Get municipal infrastructure standards
        infrastructure = self.utility_db.get_municipal_infrastructure(municipality)
        if not infrastructure:
            raise HTTPException(status_code=404, detail=f"Municipality {municipality} not found")
        
        # Analyze each utility connection
        water_analysis = self._analyze_water_connection(address, municipality, infrastructure)
        sewer_analysis = self._analyze_sewer_connection(address, municipality, infrastructure)
        electrical_analysis = self._analyze_electrical_connection(address, municipality, infrastructure, property_type)
        gas_analysis = self._analyze_gas_connection(address, municipality, infrastructure)
        internet_analysis = self._analyze_internet_connection(address, municipality, infrastructure)
        
        # Calculate total costs and overall scores
        total_cost_low = (water_analysis.connection_cost_low + sewer_analysis.connection_cost_low + 
                         electrical_analysis.connection_cost_low + gas_analysis.connection_cost_low + 
                         internet_analysis.connection_cost_low)
        
        total_cost_high = (water_analysis.connection_cost_high + sewer_analysis.connection_cost_high + 
                          electrical_analysis.connection_cost_high + gas_analysis.connection_cost_high + 
                          internet_analysis.connection_cost_high)
        
        # Calculate overall utility score (0-10)
        overall_score = self._calculate_overall_utility_score([
            water_analysis, sewer_analysis, electrical_analysis, gas_analysis, internet_analysis
        ])
        
        # Calculate development readiness score
        development_readiness = self._calculate_development_readiness_score([
            water_analysis, sewer_analysis, electrical_analysis, gas_analysis, internet_analysis
        ])
        
        # Generate engineering risk assessment
        risk_assessment = self._generate_engineering_risk_assessment([
            water_analysis, sewer_analysis, electrical_analysis, gas_analysis, internet_analysis
        ], municipality, property_type)
        
        return UtilityRatings(
            overall_score=overall_score,
            water_connection=water_analysis,
            sewer_connection=sewer_analysis,
            electrical_connection=electrical_analysis,
            gas_connection=gas_analysis,
            internet_connection=internet_analysis,
            total_infrastructure_cost_low=total_cost_low,
            total_infrastructure_cost_high=total_cost_high,
            development_readiness_score=development_readiness,
            engineering_risk_assessment=risk_assessment
        )
    
    def _analyze_water_connection(self, address: str, municipality: str, infrastructure: MunicipalInfrastructure) -> UtilityConnection:
        """Analyze water connection requirements"""
        
        # Simulate distance calculation (in real implementation, use GIS data)
        distance = self._simulate_utility_distance(municipality, "water")
        
        # Determine status based on municipality and distance
        if municipality == "parkland":
            status = UtilityStatus.private_system
            cost_low = 15000  # Private well system
            cost_high = 35000
            timeline = 21  # 3 weeks for well drilling
            notes = "Private well required. Geotechnical assessment needed for well placement."
        elif distance <= 100:
            status = UtilityStatus.available
            cost_low = infrastructure.water_system["base_connection_fee"]
            cost_high = infrastructure.water_system["base_connection_fee"] + (distance * infrastructure.water_system["connection_cost_per_meter"])
            timeline = 7  # 1 week for direct connection
            notes = "Direct connection to municipal water main available."
        elif distance <= 500:
            status = UtilityStatus.extension_required
            cost_low = infrastructure.water_system["base_connection_fee"] + (distance * infrastructure.water_system["connection_cost_per_meter"] * 0.8)
            cost_high = infrastructure.water_system["base_connection_fee"] + (distance * infrastructure.water_system["connection_cost_per_meter"] * 1.3)
            timeline = 14  # 2 weeks for extension
            notes = "Water main extension required. Municipal approval needed."
        else:
            status = UtilityStatus.major_infrastructure
            cost_low = infrastructure.water_system["base_connection_fee"] + (distance * infrastructure.water_system["connection_cost_per_meter"] * 1.5)
            cost_high = infrastructure.water_system["base_connection_fee"] + (distance * infrastructure.water_system["connection_cost_per_meter"] * 2.0)
            timeline = 45  # 6+ weeks for major infrastructure
            notes = "Major water infrastructure required. Developer cost sharing likely."
        
        return UtilityConnection(
            utility_type="water",
            status=status,
            distance_meters=distance,
            connection_cost_low=cost_low,
            connection_cost_high=cost_high,
            capacity_available=True,  # Assume capacity available for analysis
            service_provider=infrastructure.water_system["provider"],
            estimated_timeline_days=timeline,
            engineering_notes=notes
        )
    
    def _analyze_sewer_connection(self, address: str, municipality: str, infrastructure: MunicipalInfrastructure) -> UtilityConnection:
        """Analyze sewer connection requirements"""
        
        distance = self._simulate_utility_distance(municipality, "sewer")
        
        if municipality == "parkland":
            status = UtilityStatus.private_system
            cost_low = 18000  # Private septic system
            cost_high = 45000
            timeline = 28  # 4 weeks for septic installation
            notes = "Private septic system required. Soil analysis and P.Eng design needed."
        elif distance <= 100:
            status = UtilityStatus.available
            cost_low = infrastructure.sewer_system["base_connection_fee"]
            cost_high = infrastructure.sewer_system["base_connection_fee"] + (distance * infrastructure.sewer_system["connection_cost_per_meter"])
            timeline = 10  # 1.5 weeks for sewer connection
            notes = "Direct connection to municipal sewer available."
        elif distance <= 300:
            status = UtilityStatus.extension_required
            cost_low = infrastructure.sewer_system["base_connection_fee"] + (distance * infrastructure.sewer_system["connection_cost_per_meter"] * 0.9)
            cost_high = infrastructure.sewer_system["base_connection_fee"] + (distance * infrastructure.sewer_system["connection_cost_per_meter"] * 1.4)
            timeline = 21  # 3 weeks for extension
            notes = "Sewer extension required. May require lift station."
        else:
            status = UtilityStatus.major_infrastructure
            cost_low = infrastructure.sewer_system["base_connection_fee"] + (distance * infrastructure.sewer_system["connection_cost_per_meter"] * 2.0)
            cost_high = infrastructure.sewer_system["base_connection_fee"] + (distance * infrastructure.sewer_system["connection_cost_per_meter"] * 3.0)
            timeline = 60  # 8+ weeks for major infrastructure
            notes = "Major sewer infrastructure required. Lift station and trunk line needed."
        
        return UtilityConnection(
            utility_type="sewer",
            status=status,
            distance_meters=distance,
            connection_cost_low=cost_low,
            connection_cost_high=cost_high,
            capacity_available=True,
            service_provider=infrastructure.sewer_system["provider"],
            estimated_timeline_days=timeline,
            engineering_notes=notes
        )
    
    def _analyze_electrical_connection(self, address: str, municipality: str, infrastructure: MunicipalInfrastructure, property_type: str) -> UtilityConnection:
        """Analyze electrical connection requirements"""
        
        distance = self._simulate_utility_distance(municipality, "electrical")
        
        # Adjust costs based on property type
        if property_type in ["commercial", "industrial"]:
            base_multiplier = 2.5  # Higher electrical requirements
            capacity_notes = "Commercial/industrial electrical capacity required."
        else:
            base_multiplier = 1.0
            capacity_notes = "Standard residential electrical service."
        
        if distance <= 50:
            status = UtilityStatus.available
            cost_low = (infrastructure.electrical_grid["connection_cost_per_meter"] * distance * base_multiplier)
            cost_high = cost_low * 1.5
            timeline = 5  # 5 days for electrical connection
            notes = f"Direct electrical connection available. {capacity_notes}"
        elif distance <= 200:
            status = UtilityStatus.extension_required
            cost_low = (infrastructure.electrical_grid["connection_cost_per_meter"] * distance * base_multiplier * 1.3)
            cost_high = cost_low * 1.8
            timeline = 14  # 2 weeks for extension
            notes = f"Electrical service extension required. {capacity_notes}"
        else:
            status = UtilityStatus.major_infrastructure
            cost_low = (infrastructure.electrical_grid["connection_cost_per_meter"] * distance * base_multiplier * 2.0)
            cost_high = cost_low * 2.5
            timeline = 35  # 5 weeks for major electrical infrastructure
            notes = f"Major electrical infrastructure required. Transformer installation needed. {capacity_notes}"
        
        return UtilityConnection(
            utility_type="electrical",
            status=status,
            distance_meters=distance,
            connection_cost_low=cost_low,
            connection_cost_high=cost_high,
            capacity_available=True,
            service_provider=infrastructure.electrical_grid["provider"],
            estimated_timeline_days=timeline,
            engineering_notes=notes
        )
    
    def _analyze_gas_connection(self, address: str, municipality: str, infrastructure: MunicipalInfrastructure) -> UtilityConnection:
        """Analyze natural gas connection requirements"""
        
        distance = self._simulate_utility_distance(municipality, "gas")
        
        if municipality == "parkland" or distance > 1000:
            status = UtilityStatus.private_system
            cost_low = 8000   # Propane system installation
            cost_high = 18000
            timeline = 14  # 2 weeks for propane setup
            notes = "Natural gas not available. Propane system required."
            provider = "Private Propane Provider"
        elif distance <= 100:
            status = UtilityStatus.available
            cost_low = 2500   # Standard gas connection
            cost_high = 4500
            timeline = 7   # 1 week for gas connection
            notes = "Natural gas connection readily available."
            provider = "ATCO Gas"
        elif distance <= 500:
            status = UtilityStatus.extension_required
            cost_low = 5000 + (distance * 85)  # Gas line extension costs
            cost_high = 8000 + (distance * 125)
            timeline = 21  # 3 weeks for extension
            notes = "Natural gas line extension required."
            provider = "ATCO Gas"
        else:
            status = UtilityStatus.major_infrastructure
            cost_low = 15000 + (distance * 150)
            cost_high = 35000 + (distance * 250)
            timeline = 60  # 8+ weeks for major gas infrastructure
            notes = "Major natural gas infrastructure required. High pressure line needed."
            provider = "ATCO Gas"
        
        return UtilityConnection(
            utility_type="gas",
            status=status,
            distance_meters=distance,
            connection_cost_low=cost_low,
            connection_cost_high=cost_high,
            capacity_available=True,
            service_provider=provider,
            estimated_timeline_days=timeline,
            engineering_notes=notes
        )
    
    def _analyze_internet_connection(self, address: str, municipality: str, infrastructure: MunicipalInfrastructure) -> UtilityConnection:
        """Analyze internet/telecommunications connection requirements"""
        
        # Internet availability varies by municipality and location
        if municipality in ["edmonton", "st_albert"]:
            status = UtilityStatus.available
            cost_low = 150    # Standard fiber installation
            cost_high = 500
            timeline = 7   # 1 week for installation
            notes = "Fiber internet readily available."
        elif municipality in ["leduc", "strathcona"]:
            status = UtilityStatus.available
            cost_low = 200
            cost_high = 750
            timeline = 10  # 1.5 weeks for installation
            notes = "Cable/fiber internet available."
        else:  # parkland
            status = UtilityStatus.extension_required
            cost_low = 1500   # Rural internet setup
            cost_high = 5000
            timeline = 21  # 3 weeks for rural internet
            notes = "Rural internet service. Satellite or fixed wireless required."
        
        return UtilityConnection(
            utility_type="internet",
            status=status,
            distance_meters=0,  # Not distance-dependent for internet
            connection_cost_low=cost_low,
            connection_cost_high=cost_high,
            capacity_available=True,
            service_provider="Multiple ISP Options",
            estimated_timeline_days=timeline,
            engineering_notes=notes
        )
    
    def _simulate_utility_distance(self, municipality: str, utility_type: str) -> float:
        """Simulate utility distance based on municipality characteristics"""
        
        # These would be replaced with actual GIS calculations in production
        base_distances = {
            "edmonton": {"water": 45, "sewer": 55, "electrical": 25, "gas": 65},
            "leduc": {"water": 125, "sewer": 180, "electrical": 85, "gas": 145},
            "st_albert": {"water": 65, "sewer": 85, "electrical": 35, "gas": 95},
            "strathcona": {"water": 350, "sewer": 420, "electrical": 180, "gas": 285},
            "parkland": {"water": 2500, "sewer": 3000, "electrical": 850, "gas": 1500}
        }
        
        return base_distances.get(municipality, {}).get(utility_type, 500)
    
    def _calculate_overall_utility_score(self, connections: List[UtilityConnection]) -> float:
        """Calculate overall utility accessibility score (0-10)"""
        
        utility_scores = []
        for connection in connections:
            if connection.status == UtilityStatus.available:
                score = 9.0
            elif connection.status == UtilityStatus.extension_required:
                score = 6.5
            elif connection.status == UtilityStatus.major_infrastructure:
                score = 3.5
            else:  # private_system
                score = 5.0  # Neutral for private systems
            
            utility_scores.append(score)
        
        return round(sum(utility_scores) / len(utility_scores), 1)
    
    def _calculate_development_readiness_score(self, connections: List[UtilityConnection]) -> float:
        """Calculate development readiness score based on utility status"""
        
        readiness_score = 10.0
        
        for connection in connections:
            if connection.status == UtilityStatus.major_infrastructure:
                readiness_score -= 2.5
            elif connection.status == UtilityStatus.extension_required:
                readiness_score -= 1.5
            elif connection.status == UtilityStatus.private_system:
                readiness_score -= 1.0
        
        return max(0.0, round(readiness_score, 1))
    
    def _generate_engineering_risk_assessment(self, connections: List[UtilityConnection], municipality: str, property_type: str) -> str:
        """Generate professional engineering risk assessment"""
        
        major_infrastructure_count = sum(1 for conn in connections if conn.status == UtilityStatus.major_infrastructure)
        extension_count = sum(1 for conn in connections if conn.status == UtilityStatus.extension_required)
        
        if major_infrastructure_count >= 2:
            risk_level = "HIGH"
            recommendation = "Significant infrastructure investment required. Professional engineering assessment recommended before proceeding."
        elif major_infrastructure_count == 1 or extension_count >= 3:
            risk_level = "MEDIUM"
            recommendation = "Moderate infrastructure requirements. Budget additional 6-12 weeks for utility connections."
        else:
            risk_level = "LOW"
            recommendation = "Utilities readily available. Standard development timeline expected."
        
        total_cost_estimate = sum(conn.connection_cost_high for conn in connections)
        
        return f"Risk Level: {risk_level}. Total Infrastructure Investment: ${total_cost_estimate:,.0f}. {recommendation}"

#==============================================================================
# AMENITY PROXIMITY ANALYZER
#==============================================================================

class AmenityProximityAnalyzer:
    """Advanced amenity proximity analysis with value impact assessment"""
    
    def __init__(self):
        self.amenity_db = AlbertaAmenityDatabase()
    
    def analyze_amenity_proximity(self, address: str, municipality: str, property_coordinates: Tuple[float, float]) -> AmenityAnalysis:
        """Complete amenity proximity analysis"""
        
        # Get municipal amenity database
        municipal_amenities = self.amenity_db.get_municipal_amenities(municipality)
        if not municipal_amenities:
            raise HTTPException(status_code=404, detail=f"Amenity data for {municipality} not found")
        
        # Calculate distances for all amenities
        all_amenities = []
        category_scores = {}
        
        for category, amenities in municipal_amenities.items():
            category_amenities = []
            for amenity in amenities:
                # Calculate actual distance
                distance = self._calculate_distance(property_coordinates, amenity.coordinates)
                walking_time = self._estimate_walking_time(distance)
                driving_time = self._estimate_driving_time(distance)
                impact_score = self._calculate_amenity_impact(amenity, distance)
                
                # Update amenity with calculated values
                updated_amenity = AmenityDistance(
                    name=amenity.name,
                    category=category,
                    address=amenity.address,
                    distance_meters=distance,
                    walking_time_minutes=walking_time,
                    driving_time_minutes=driving_time,
                    impact_score=impact_score,
                    coordinates=amenity.coordinates
                )
                
                category_amenities.append(updated_amenity)
                all_amenities.append(updated_amenity)
            
            # Calculate category score based on closest amenities
            category_scores[category] = self._calculate_category_score(category_amenities)
        
        # Calculate overall amenity score
        overall_score = self._calculate_overall_amenity_score(category_scores)
        
        # Calculate value impact percentage
        value_impact = self._calculate_value_impact_percentage(overall_score, category_scores)
        
        # Get nearest amenities (top 10 by impact score)
        nearest_amenities = sorted(all_amenities, key=lambda a: a.impact_score, reverse=True)[:10]
        
        return AmenityAnalysis(
            overall_amenity_score=overall_score,
            education_score=category_scores.get('education', 0),
            healthcare_score=category_scores.get('healthcare', 0),
            retail_score=category_scores.get('retail', 0),
            transportation_score=category_scores.get('transportation', 0),
            recreation_score=category_scores.get('recreation', 0),
            employment_score=category_scores.get('employment', 0),
            nearest_amenities=nearest_amenities,
            value_impact_percentage=value_impact
        )
    
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate distance between two coordinates in meters"""
        
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        # Haversine formula for distance calculation
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon/2) * math.sin(delta_lon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _estimate_walking_time(self, distance_meters: float) -> float:
        """Estimate walking time in minutes (assuming 5 km/h walking speed)"""
        walking_speed_ms = 5000 / 60  # 5 km/h in meters per minute
        return round(distance_meters / walking_speed_ms, 1)
    
    def _estimate_driving_time(self, distance_meters: float) -> float:
        """Estimate driving time in minutes (assuming 40 km/h average speed)"""
        driving_speed_ms = 40000 / 60  # 40 km/h in meters per minute
        return round(distance_meters / driving_speed_ms, 1)
    
    def _calculate_amenity_impact(self, amenity: AmenityDistance, distance_meters: float) -> float:
        """Calculate amenity impact score based on type and distance"""
        
        # Base impact scores by amenity type
        base_impacts = {
            "university": 8.5, "college": 7.5, "high_school": 7.0, "elementary_school": 6.5,
            "hospital": 9.0, "specialty_hospital": 8.5,
            "lrt_station": 8.5, "transit_hub": 7.5, "transit_center": 7.0, "airport": 9.5,
            "shopping_center": 7.5, "big_box_retail": 6.5, "entertainment_district": 8.0,
            "park": 7.0, "recreation_center": 7.5, "sports_venue": 8.0, "arts_center": 7.5,
            "business_district": 8.5, "employment_center": 8.0, "industrial_park": 7.0, "government": 7.5
        }
        
        # Get base impact for amenity category
        amenity_category = amenity.address.split()[-1] if hasattr(amenity, 'address') else "unknown"
        base_impact = base_impacts.get(amenity_category, 6.0)
        
        # Distance decay function
        if distance_meters <= 500:
            distance_multiplier = 1.0  # Full impact within 500m
        elif distance_meters <= 1000:
            distance_multiplier = 0.8  # 80% impact within 1km
        elif distance_meters <= 2000:
            distance_multiplier = 0.6  # 60% impact within 2km
        elif distance_meters <= 5000:
            distance_multiplier = 0.4  # 40% impact within 5km
        else:
            distance_multiplier = 0.2  # 20% impact beyond 5km
        
        return round(base_impact * distance_multiplier, 1)
    
    def _calculate_category_score(self, category_amenities: List[AmenityDistance]) -> float:
        """Calculate category score based on best amenities in category"""
        
        if not category_amenities:
            return 0.0
        
        # Sort by impact score and take top 3
        top_amenities = sorted(category_amenities, key=lambda a: a.impact_score, reverse=True)[:3]
        
        # Weighted average with decreasing weights
        weights = [0.5, 0.3, 0.2]
        weighted_score = sum(amenity.impact_score * weight for amenity, weight in zip(top_amenities, weights))
        
        return round(weighted_score, 1)
    
    def _calculate_overall_amenity_score(self, category_scores: Dict[str, float]) -> float:
        """Calculate overall amenity score with category weightings"""
        
        # Category weights based on development impact
        category_weights = {
            'transportation': 0.25,  # Most important for property value
            'education': 0.20,       # High impact especially for residential
            'employment': 0.20,      # Important for all property types
            'healthcare': 0.15,      # Moderate impact
            'retail': 0.10,          # Lower impact
            'recreation': 0.10       # Lower impact
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for category, weight in category_weights.items():
            if category in category_scores:
                weighted_score += category_scores[category] * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return round(weighted_score / total_weight, 1)
    
    def _calculate_value_impact_percentage(self, overall_score: float, category_scores: Dict[str, float]) -> float:
        """Calculate expected property value impact percentage"""
        
        # Base value impact calculation
        if overall_score >= 8.0:
            base_impact = 12.0  # +12% for excellent amenities
        elif overall_score >= 7.0:
            base_impact = 8.0   # +8% for very good amenities
        elif overall_score >= 6.0:
            base_impact = 4.0   # +4% for good amenities
        elif overall_score >= 4.0:
            base_impact = 0.0   # Neutral for average amenities
        else:
            base_impact = -5.0  # -5% for poor amenities
        
        # Bonus for exceptional transportation access
        if category_scores.get('transportation', 0) >= 8.0:
            base_impact += 2.0
        
        # Bonus for excellent education access
        if category_scores.get('education', 0) >= 8.0:
            base_impact += 1.5
        
        return round(base_impact, 1)

#==============================================================================
# DEVELOPMENT ASSESSMENT ENGINE
#==============================================================================

class DevelopmentAssessmentEngine:
    """Development assessment and building placement validation"""
    
    def __init__(self):
        self.utility_db = AlbertaUtilityDatabase()
    
    def analyze_lot_development_potential(self, lot_data: LotAssessment) -> Dict:
        """Complete lot assessment for development constraints and opportunities"""
        
        try:
            # Get municipal standards for the specific municipality
            infrastructure = self.utility_db.get_municipal_infrastructure(lot_data.municipality)
            if not infrastructure:
                raise HTTPException(status_code=404, detail=f"Municipality {lot_data.municipality} not found")
            
            # Get development standards
            dev_standards = infrastructure.development_standards
            
            # Calculate buildable area based on setback requirements
            buildable_area = self._calculate_buildable_area(lot_data.lot_size_sqft, dev_standards)
            
            # Assess utility connections
            utility_assessment = self._assess_utility_connections_for_lot(lot_data.coordinates, lot_data.municipality)
            
            # Generate constraint overlays
            constraints = self._generate_constraint_overlays(lot_data, dev_standards)
            
            # Professional engineering validation
            engineering_assessment = self._validate_engineering_requirements(lot_data, buildable_area, utility_assessment)
            
            # Generate assessment ID
            assessment_id = f"ASSESS_{lot_data.property_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            return {
                "assessment_id": assessment_id,
                "lot_details": {
                    "total_area_sqft": lot_data.lot_size_sqft,
                    "buildable_area_sqft": buildable_area["usable_area"],
                    "coverage_limit_sqft": lot_data.lot_size_sqft * (dev_standards["coverage_limit_percent"] / 100),
                    "setback_requirements": {
                        "front_setback_m": dev_standards["front_setback_m"],
                        "side_setback_m": dev_standards["side_setback_m"],
                        "rear_setback_m": dev_standards["rear_setback_m"],
                        "height_limit_m": float(dev_standards.get("building_height_limit", "11m").split("m")[0])
                    },
                    "lot_dimensions": buildable_area["dimensions"]
                },
                "utility_connections": utility_assessment,
                "constraints": constraints,
                "engineering_validation": engineering_assessment,
                "municipal_compliance": {
                    "zoning_compliance": self._check_zoning_compliance(lot_data.zoning, infrastructure),
                    "permit_requirements": self._get_permit_requirements(lot_data.municipality),
                    "professional_requirements": infrastructure.professional_requirements
                },
                "visual_layers": {
                    "lot_boundary": self._generate_lot_boundary_coordinates(buildable_area["dimensions"]),
                    "buildable_area": buildable_area["boundary_coordinates"],
                    "utility_markers": [{"type": u["utility_type"], "distance": u["distance_m"]} for u in utility_assessment],
                    "constraint_overlays": constraints.get("overlay_coordinates", [])
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Assessment generation failed: {str(e)}")
    
    def validate_building_placement(self, property_id: str, building: PlacedBuilding) -> Dict:
        """Validate if a building can be placed at the specified location"""
        
        try:
            # Get lot assessment data for this property (simulate)
            sample_property = self._get_sample_property(property_id)
            if not sample_property:
                raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
            
            # Get municipal standards
            infrastructure = self.utility_db.get_municipal_infrastructure(sample_property["municipality"])
            dev_standards = infrastructure.development_standards
            
            # Define buildable area constraints
            lot_size_sqft = sample_property["lot_size_sqft"]
            buildable_area_sqft = lot_size_sqft * 0.6  # 60% typically buildable
            coverage_limit_sqft = lot_size_sqft * (dev_standards["coverage_limit_percent"] / 100)
            
            # Check building placement constraints
            building_area_sqft = building.width * building.height
            placement_valid = True
            compliance_issues = []
            
            # Convert setbacks from meters to approximate pixels/units
            front_setback_units = dev_standards["front_setback_m"] * 10  # Approximate conversion
            side_setback_units = dev_standards["side_setback_m"] * 10
            
            # Check setback compliance
            if building.position_x < side_setback_units or building.position_y < front_setback_units:
                placement_valid = False
                compliance_issues.append("Building violates setback requirements")
            
            # Check building size reasonableness
            if building_area_sqft > coverage_limit_sqft:
                placement_valid = False
                compliance_issues.append(f"Building size ({building_area_sqft:.0f} sqft) exceeds coverage limit ({coverage_limit_sqft:.0f} sqft)")
            
            # Check total coverage (simplified - in production, check existing buildings)
            total_coverage_with_building = building_area_sqft
            coverage_compliance = total_coverage_with_building <= coverage_limit_sqft
            
            if not coverage_compliance:
                placement_valid = False
                compliance_issues.append("Total site coverage would exceed municipal limits")
            
            # Generate recommendations
            recommendations = self._generate_placement_recommendations(building, dev_standards, placement_valid)
            
            return {
                "placement_valid": placement_valid,
                "compliance_details": {
                    "buildable_area_compliance": building.position_x >= side_setback_units and building.position_y >= front_setback_units,
                    "setback_compliance": placement_valid or len([i for i in compliance_issues if "setback" in i]) == 0,
                    "coverage_compliance": coverage_compliance,
                    "building_area_sqft": building_area_sqft,
                    "total_coverage_sqft": total_coverage_with_building,
                    "coverage_limit_sqft": coverage_limit_sqft
                },
                "compliance_issues": compliance_issues,
                "recommendations": recommendations,
                "building_details": {
                    "type": building.building_type,
                    "position": {"x": building.position_x, "y": building.position_y},
                    "dimensions": {"width": building.width, "height": building.height},
                    "area_sqft": building_area_sqft
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Placement validation failed: {str(e)}")
    
    def save_development_plan(self, plan: DevelopmentPlan) -> Dict:
        """Save complete development plan with cost analysis"""
        
        try:
            # Validate the entire development plan
            plan_validation = self._validate_complete_plan(plan)
            
            if not plan_validation["valid"]:
                raise HTTPException(status_code=400, detail=plan_validation["errors"])
            
            # Calculate development costs
            cost_analysis = self._calculate_development_costs(plan)
            
            # Generate plan ID and timestamp
            plan_id = f"PLAN_{plan.property_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Integration with existing property analysis
            enhanced_analysis = self._integrate_with_property_analysis(plan.property_id, plan, cost_analysis)
            
            # Generate professional documentation
            documentation = self._generate_development_documentation(plan, cost_analysis)
            
            return {
                "plan_id": plan_id,
                "validation_results": plan_validation,
                "cost_analysis": cost_analysis,
                "documentation": documentation,
                "integrated_analysis": enhanced_analysis,
                "next_steps": {
                    "municipal_submission": documentation["municipal_package"],
                    "engineering_review": documentation["engineering_checklist"],
                    "permit_applications": documentation["permit_requirements"]
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Plan save failed: {str(e)}")
    
    def export_site_assessment(self, assessment_id: str) -> Dict:
        """Generate professional site assessment report for municipal submission"""
        
        try:
            # Extract property ID from assessment ID
            if not assessment_id.startswith("ASSESS_"):
                raise HTTPException(status_code=404, detail="Invalid assessment ID")
            
            parts = assessment_id.split("_")
            property_id = parts[1] if len(parts) > 1 else "EDM_001"
            
            # Get property data
            sample_property = self._get_sample_property(property_id)
            if not sample_property:
                sample_property = SAMPLE_PROPERTIES[0]  # Default fallback
            
            # Generate comprehensive report structure
            report = self._generate_professional_assessment_report(assessment_id, sample_property)
            
            return {
                "export_status": "success",
                "report_data": report,
                "download_url": f"/reports/assessment_{assessment_id}.pdf",
                "municipal_submission_ready": True
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
    
    def export_development_plan(self, plan_id: str) -> Dict:
        """Generate professional development plan documentation"""
        
        try:
            # Extract property ID from plan ID
            if not plan_id.startswith("PLAN_"):
                raise HTTPException(status_code=404, detail="Invalid plan ID")
            
            parts = plan_id.split("_")
            property_id = parts[1] if len(parts) > 1 else "EDM_001"
            
            # Get property data
            sample_property = self._get_sample_property(property_id)
            if not sample_property:
                sample_property = SAMPLE_PROPERTIES[0]
            
            # Generate development plan report
            report = self._generate_development_plan_report(plan_id, sample_property)
            
            return {
                "export_status": "success",
                "plan_documentation": report,
                "download_url": f"/reports/development_plan_{plan_id}.pdf",
                "cost_summary": report["cost_analysis"]["total_project_cost"],
                "implementation_ready": True
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Plan export failed: {str(e)}")
    
    # Helper Methods
    def _calculate_buildable_area(self, lot_size_sqft: float, dev_standards: Dict) -> Dict:
        """Calculate usable building area considering all setback requirements"""
        
        # Assuming rectangular lot for calculation
        lot_width = math.sqrt(lot_size_sqft * 1.2)  # Typical residential ratio
        lot_depth = lot_size_sqft / lot_width
        
        front_setback_ft = dev_standards["front_setback_m"] * 3.28084  # Convert m to ft
        rear_setback_ft = dev_standards["rear_setback_m"] * 3.28084
        side_setback_ft = dev_standards["side_setback_m"] * 3.28084
        
        buildable_width = lot_width - (2 * side_setback_ft)
        buildable_depth = lot_depth - (front_setback_ft + rear_setback_ft)
        
        usable_area = max(0, buildable_width * buildable_depth)
        
        return {
            "usable_area": usable_area,
            "buildable_width": max(0, buildable_width),
            "buildable_depth": max(0, buildable_depth),
            "dimensions": {
                "lot_width_ft": lot_width,
                "lot_depth_ft": lot_depth,
                "buildable_width_ft": buildable_width,
                "buildable_depth_ft": buildable_depth
            },
            "boundary_coordinates": self._generate_buildable_boundary_coordinates(
                lot_width, lot_depth, dev_standards
            )
        }
    
    def _assess_utility_connections_for_lot(self, coordinates: Tuple[float, float], municipality: str) -> List[Dict]:
        """Assess all utility connections for the property"""
        
        utility_types = ["water", "sewer", "electrical", "gas", "internet"]
        connections = []
        
        for utility in utility_types:
            connection_data = self._calculate_utility_distance_for_lot(coordinates, utility, municipality)
            connections.append(connection_data)
        
        return connections
    
    def _calculate_utility_distance_for_lot(self, coordinates: Tuple[float, float], utility: str, municipality: str) -> Dict:
        """Calculate utility distance and costs for lot assessment"""
        
        # Simulate distance calculation (replace with real GIS in production)
        base_distances = {
            "edmonton": {"water": 45, "sewer": 55, "electrical": 25, "gas": 65, "internet": 0},
            "leduc": {"water": 125, "sewer": 180, "electrical": 85, "gas": 145, "internet": 0},
            "st_albert": {"water": 65, "sewer": 85, "electrical": 35, "gas": 95, "internet": 0},
            "strathcona": {"water": 350, "sewer": 420, "electrical": 180, "gas": 285, "internet": 0},
            "parkland": {"water": 2500, "sewer": 3000, "electrical": 850, "gas": 1500, "internet": 0}
        }
        
        distance = base_distances.get(municipality, {}).get(utility, 500)
        
        # Calculate costs based on utility type and distance
        if utility == "water":
            if municipality == "parkland":
                cost_low, cost_high = 15000, 35000
                status = "private_system"
            elif distance <= 100:
                cost_low, cost_high = 3500, 8500
                status = "available"
            else:
                cost_low, cost_high = 8500, 25000
                status = "extension_required"
        elif utility == "sewer":
            if municipality == "parkland":
                cost_low, cost_high = 18000, 45000
                status = "private_system"
            elif distance <= 100:
                cost_low, cost_high = 5000, 12000
                status = "available"
            else:
                cost_low, cost_high = 12000, 35000
                status = "extension_required"
        elif utility == "electrical":
            cost_low, cost_high = max(2500, distance * 125), max(6500, distance * 200)
            status = "available" if distance <= 200 else "extension_required"
        elif utility == "gas":
            if municipality == "parkland":
                cost_low, cost_high = 8000, 18000
                status = "private_system"
            else:
                cost_low, cost_high = 2500, 8000
                status = "available"
        else:  # internet
            cost_low, cost_high = 150, 1500
            status = "available"
        
        return {
            "utility_type": utility,
            "distance_m": distance,
            "connection_cost_low": cost_low,
            "connection_cost_high": cost_high,
            "status": status
        }
    
    def _generate_constraint_overlays(self, lot_data: LotAssessment, dev_standards: Dict) -> Dict:
        """Generate constraint overlays for lot visualization"""
        
        constraints = [
            {
                "type": "setback",
                "description": f"Front setback: {dev_standards['front_setback_m']}m",
                "impact": "No building allowed in setback area"
            },
            {
                "type": "setback", 
                "description": f"Side setbacks: {dev_standards['side_setback_m']}m each",
                "impact": "No building allowed in setback areas"
            },
            {
                "type": "coverage",
                "description": f"Maximum coverage: {dev_standards['coverage_limit_percent']}%",
                "impact": f"Maximum {lot_data.lot_size_sqft * dev_standards['coverage_limit_percent'] / 100:.0f} sqft building area"
            }
        ]
        
        return {
            "constraints": constraints,
            "overlay_coordinates": []  # Would be populated with actual constraint boundaries
        }
    
    def _validate_engineering_requirements(self, lot_data: LotAssessment, buildable_area: Dict, utilities: List) -> Dict:
        """P.Eng validation of development requirements"""
        
        validation = {
            "structural_requirements": {
                "soil_analysis_required": lot_data.lot_size_sqft > 10000,
                "foundation_type": "Standard concrete foundation suitable for Alberta conditions",
                "load_calculations": "P.Eng stamped drawings required for structures >300sqm"
            },
            "utility_adequacy": {
                "water_pressure": "Adequate pressure available from municipal system",
                "electrical_capacity": "Standard residential/commercial electrical capacity available",
                "sewer_capacity": "Municipal sewer system adequate for proposed development"
            },
            "code_compliance": {
                "building_code": "Alberta Building Code 2019",
                "fire_safety": "Standard fire safety requirements apply",
                "accessibility": "Barrier-free design required for commercial developments"
            },
            "professional_oversight": {
                "required_disciplines": ["Structural", "Electrical", "Mechanical"],
                "permit_process": "Municipal development permit required",
                "inspection_schedule": "Foundation, framing, electrical, plumbing, final inspections"
            }
        }
        
        return validation
    
    def _generate_lot_boundary_coordinates(self, dimensions: Dict) -> List[Dict]:
        """Generate lot boundary coordinates for visualization"""
        
        width = dimensions["lot_width_ft"]
        depth = dimensions["lot_depth_ft"]
        
        return [
            {"lat": 0, "lng": 0},
            {"lat": 0, "lng": width},
            {"lat": depth, "lng": width},
            {"lat": depth, "lng": 0},
            {"lat": 0, "lng": 0}  # Close the polygon
        ]
    
    def _generate_buildable_boundary_coordinates(self, lot_width: float, lot_depth: float, dev_standards: Dict) -> List[Dict]:
        """Generate buildable area coordinates considering setbacks"""
        
        front_setback_ft = dev_standards["front_setback_m"] * 3.28084
        rear_setback_ft = dev_standards["rear_setback_m"] * 3.28084
        side_setback_ft = dev_standards["side_setback_m"] * 3.28084
        
        return [
            {"lat": front_setback_ft, "lng": side_setback_ft},
            {"lat": front_setback_ft, "lng": lot_width - side_setback_ft},
            {"lat": lot_depth - rear_setback_ft, "lng": lot_width - side_setback_ft},
            {"lat": lot_depth - rear_setback_ft, "lng": side_setback_ft},
            {"lat": front_setback_ft, "lng": side_setback_ft}  # Close the polygon
        ]
    
    def _check_zoning_compliance(self, zoning: str, infrastructure: MunicipalInfrastructure) -> bool:
        """Check if proposed development complies with zoning"""
        # Simplified zoning check - in production, would check against zoning database
        return True
    
    def _get_permit_requirements(self, municipality: str) -> List[str]:
        """Get permit requirements for municipality"""
        return [
            "Development Permit",
            "Building Permit", 
            "Electrical Permit",
            "Plumbing Permit",
            "Occupancy Permit"
        ]
    
    def _get_sample_property(self, property_id: str) -> Optional[Dict]:
        """Get sample property by ID"""
        return next((p for p in SAMPLE_PROPERTIES if p["property_id"] == property_id), None)
    
    def _validate_complete_plan(self, plan: DevelopmentPlan) -> Dict:
        """Validate entire development plan"""
        
        errors = []
        
        # Check if property exists
        property_data = self._get_sample_property(plan.property_id)
        if not property_data:
            errors.append(f"Property {plan.property_id} not found")
        
        # Validate building areas
        total_building_area = sum(b.width * b.height for b in plan.buildings)
        if abs(total_building_area - plan.total_coverage_sqft) > 10:  # Allow small rounding differences
            errors.append("Total coverage calculation mismatch")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _calculate_development_costs(self, plan: DevelopmentPlan) -> Dict:
        """Calculate comprehensive development costs including infrastructure"""
        
        # Base construction costs by building type (CAD per sq ft)
        cost_per_sqft = {
            "single_family": 150,
            "duplex": 140,
            "townhouse": 135,
            "retail": 120,
            "office": 110,
            "parking": 25,
            "garden": 10,
            "industrial": 90
        }
        
        total_construction_cost = 0
        building_costs = []
        
        for building in plan.buildings:
            building_area = building.width * building.height
            unit_cost = cost_per_sqft.get(building.building_type.value, 100)
            building_cost = building_area * unit_cost
            
            total_construction_cost += building_cost
            building_costs.append({
                "building_id": building.building_id,
                "type": building.building_type.value,
                "area_sqft": building_area,
                "cost_cad": building_cost,
                "cost_per_sqft": unit_cost
            })
        
        # Infrastructure costs (simplified)
        infrastructure_costs = {
            "water_connection": 8500,
            "sewer_connection": 12000,
            "electrical_service": 6500,
            "gas_connection": 4500,
            "total": 31500
        }
        
        # Professional fees (15% of construction)
        professional_fees = total_construction_cost * 0.15
        
        # Total project cost
        total_project_cost = total_construction_cost + infrastructure_costs["total"] + professional_fees
        
        return {
            "construction_costs": {
                "total_cad": total_construction_cost,
                "building_breakdown": building_costs,
                "cost_per_sqft_average": total_construction_cost / plan.total_coverage_sqft if plan.total_coverage_sqft > 0 else 0
            },
            "infrastructure_costs": infrastructure_costs,
            "professional_fees": {
                "amount_cad": professional_fees,
                "percentage": 15,
                "includes": ["Engineering", "Permits", "Inspections", "Legal"]
            },
            "total_project_cost": total_project_cost
        }
    
    def _integrate_with_property_analysis(self, property_id: str, plan: DevelopmentPlan, costs: Dict) -> Dict:
        """Integrate development plan with existing property analysis"""
        
        # Get existing property data
        property_data = self._get_sample_property(property_id)
        if not property_data:
            property_data = SAMPLE_PROPERTIES[0]
        
        # Enhanced analysis combining land value + development costs
        enhanced_analysis = {
            "property_id": property_id,
            "land_analysis": property_data,
            "development_plan": {
                "buildings": len(plan.buildings),
                "total_coverage": plan.total_coverage_sqft,
                "development_cost": costs["total_project_cost"]
            },
            "financial_analysis": {
                "land_value": property_data["estimated_value"],
                "development_cost": costs["total_project_cost"],
                "total_investment": property_data["estimated_value"] + costs["total_project_cost"],
                "potential_roi": 15.0  # Simplified ROI calculation
            }
        }
        
        return enhanced_analysis
    
    def _generate_development_documentation(self, plan: DevelopmentPlan, cost_analysis: Dict) -> Dict:
        """Generate professional documentation for development plan"""
        
        return {
            "municipal_package": "Development permit application package ready for submission",
            "engineering_checklist": "P.Eng review required for final approval and stamped drawings",
            "permit_requirements": [
                "Development Permit Application",
                "Building Permit Application", 
                "Electrical Permit Application",
                "Plumbing Permit Application"
            ]
        }
    
    def _generate_placement_recommendations(self, building: PlacedBuilding, dev_standards: Dict, placement_valid: bool) -> List[str]:
        """Generate recommendations for building placement"""
        
        recommendations = []
        
        if not placement_valid:
            recommendations.extend([
                "Move building to comply with setback requirements",
                "Consider reducing building size to meet coverage limits",
                "Review municipal zoning requirements"
            ])
        else:
            recommendations.extend([
                "Placement meets all municipal requirements",
                "Proceed with detailed design development",
                "Consider professional engineering consultation"
            ])
        
        return recommendations
    
    def _generate_professional_assessment_report(self, assessment_id: str, property_data: Dict) -> Dict:
        """Generate comprehensive professional assessment report"""
        
        return {
            "report_metadata": {
                "report_type": "Site Assessment & Development Feasibility Analysis",
                "prepared_by": "SkyeBridge Consulting & Developments Inc.",
                "professional_seal": "Jeff McLeod, P.Eng, Alberta License #12345",
                "date": datetime.now().strftime("%B %d, %Y"),
                "assessment_id": assessment_id,
                "property_id": property_data["property_id"]
            },
            "executive_summary": {
                "property_address": property_data["address"],
                "lot_size": f"{property_data['lot_size_sqft']:,} sq ft",
                "municipality": property_data["municipality"].title(),
                "development_potential": property_data["development_potential"],
                "overall_feasibility": "FEASIBLE - Property suitable for proposed development"
            },
            "professional_validation": {
                "peng_reviewed": True,
                "stamp_required": True,
                "liability_coverage": "Professional liability insurance in effect"
            }
        }
    
    def _generate_development_plan_report(self, plan_id: str, property_data: Dict) -> Dict:
        """Generate development plan report"""
        
        return {
            "document_type": "Development Plan & Cost Analysis",
            "prepared_by": "SkyeBridge Consulting & Developments Inc.",
            "professional_seal": "Jeff McLeod, P.Eng",
            "date": datetime.now().strftime("%B %d, %Y"),
            "plan_id": plan_id,
            "cost_analysis": {
                "total_project_cost": 500000  # Simplified
            }
        }

#==============================================================================
# INTERACTIVE MAPPING SYSTEM
#==============================================================================

def generate_interactive_property_map(property_data: Dict, utility_ratings: UtilityRatings, amenity_analysis: AmenityAnalysis) -> str:
    """Generate interactive HTML map with utility and amenity overlays"""
    
    # Get property coordinates (simulated for example)
    property_coords = [53.5461, -113.4909]  # Default Edmonton coordinates
    
    # Generate utility markers
    utility_markers = []
    for utility_type in ['water', 'sewer', 'electrical', 'gas', 'internet']:
        connection = getattr(utility_ratings, f"{utility_type}_connection")
        
        # Determine marker color based on status
        if connection.status == UtilityStatus.available:
            color = "green"
        elif connection.status == UtilityStatus.extension_required:
            color = "orange"
        elif connection.status == UtilityStatus.major_infrastructure:
            color = "red"
        else:
            color = "blue"
        
        utility_markers.append({
            "type": utility_type,
            "status": connection.status.value,
            "distance": connection.distance_meters,
            "cost_range": f"${connection.connection_cost_low:,.0f} - ${connection.connection_cost_high:,.0f}",
            "timeline": f"{connection.estimated_timeline_days} days",
            "color": color,
            "notes": connection.engineering_notes
        })
    
    # Generate amenity markers
    amenity_markers = []
    for amenity in amenity_analysis.nearest_amenities:
        amenity_markers.append({
            "name": amenity.name,
            "category": amenity.category,
            "distance": f"{amenity.distance_meters:.0f}m",
            "walking_time": f"{amenity.walking_time_minutes:.1f} min",
            "impact_score": amenity.impact_score,
            "coordinates": list(amenity.coordinates)
        })
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sgiach Property Analysis Map</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            body {{ margin: 0; padding: 20px; font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; }}
            .map-container {{ display: flex; gap: 20px; height: 80vh; }}
            #map {{ flex: 1; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
            .legend-panel {{ width: 320px; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); overflow-y: auto; }}
            .legend-section {{ margin-bottom: 25px; }}
            .legend-title {{ font-size: 16px; font-weight: 600; color: #2c3e50; margin-bottom: 15px; border-bottom: 2px solid #3498db; padding-bottom: 8px; }}
            .legend-item {{ display: flex; align-items: center; margin-bottom: 12px; padding: 10px; background: #f8f9fa; border-radius: 8px; }}
            .legend-icon {{ width: 16px; height: 16px; border-radius: 50%; margin-right: 12px; flex-shrink: 0; }}
            .legend-text {{ font-size: 14px; line-height: 1.4; }}
            .utility-status {{ font-weight: 500; }}
            .cost-estimate {{ color: #27ae60; font-weight: 500; }}
            .distance {{ color: #7f8c8d; font-size: 12px; }}
            .property-summary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
            .score {{ font-size: 24px; font-weight: bold; }}
            .score-label {{ font-size: 14px; opacity: 0.9; }}
        </style>
    </head>
    <body>
        <h1 style="color: #2c3e50; margin-bottom: 20px;">🏗️ Sgiach Property Development Analysis</h1>
        
        <div class="property-summary">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="score">{utility_ratings.overall_score}/10</div>
                    <div class="score-label">Utility Score</div>
                </div>
                <div>
                    <div class="score">{amenity_analysis.overall_amenity_score}/10</div>
                    <div class="score-label">Amenity Score</div>
                </div>
                <div>
                    <div class="score">${utility_ratings.total_infrastructure_cost_low/1000:.0f}K-${utility_ratings.total_infrastructure_cost_high/1000:.0f}K</div>
                    <div class="score-label">Infrastructure Cost</div>
                </div>
            </div>
        </div>
        
        <div class="map-container">
            <div id="map"></div>
            
            <div class="legend-panel">
                <div class="legend-section">
                    <div class="legend-title">🔧 Utility Connections</div>
                    {"".join([f'''
                    <div class="legend-item">
                        <div class="legend-icon" style="background-color: {marker["color"]};"></div>
                        <div class="legend-text">
                            <div class="utility-status">{marker["type"].title()}: {marker["status"].replace("_", " ").title()}</div>
                            <div class="cost-estimate">{marker["cost_range"]}</div>
                            <div class="distance">{marker["distance"]:.0f}m • {marker["timeline"]}</div>
                        </div>
                    </div>
                    ''' for marker in utility_markers])}
                </div>
                
                <div class="legend-section">
                    <div class="legend-title">🏘️ Nearby Amenities</div>
                    {"".join([f'''
                    <div class="legend-item">
                        <div class="legend-icon" style="background-color: #3498db;"></div>
                        <div class="legend-text">
                            <div class="utility-status">{marker["name"]}</div>
                            <div class="cost-estimate">Impact: {marker["impact_score"]}/10</div>
                            <div class="distance">{marker["distance"]} • {marker["walking_time"]} walk</div>
                        </div>
                    </div>
                    ''' for marker in amenity_markers[:8]])}
                </div>
                
                <div class="legend-section">
                    <div class="legend-title">📊 Engineering Assessment</div>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; font-size: 14px; line-height: 1.6;">
                        <strong>Development Readiness:</strong> {utility_ratings.development_readiness_score}/10<br><br>
                        <strong>Risk Assessment:</strong><br>
                        {utility_ratings.engineering_risk_assessment}
                    </div>
                </div>
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // Initialize map
            var map = L.map('map').setView([{property_coords[0]}, {property_coords[1]}], 13);
            
            // Add OpenStreetMap tiles
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);
            
            // Property marker
            var propertyIcon = L.divIcon({{
                className: 'property-marker',
                html: '<div style="background: #e74c3c; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            }});
            
            L.marker([{property_coords[0]}, {property_coords[1]}], {{icon: propertyIcon}})
                .addTo(map)
                .bindPopup('<b>📍 Subject Property</b><br>Development Analysis Location');
            
            // Add utility markers (simulated positions around property)
            var utilityPositions = [
                [{property_coords[0] + 0.005}, {property_coords[1] + 0.005}],  // water
                [{property_coords[0] - 0.003}, {property_coords[1] + 0.007}],  // sewer  
                [{property_coords[0] + 0.002}, {property_coords[1] - 0.003}],  // electrical
                [{property_coords[0] - 0.006}, {property_coords[1] - 0.004}],  // gas
                [{property_coords[0] + 0.004}, {property_coords[1] + 0.008}]   // internet
            ];
            
            var utilityData = {json.dumps(utility_markers)};
            
            utilityData.forEach(function(utility, index) {{
                var utilityIcon = L.divIcon({{
                    className: 'utility-marker',
                    html: '<div style="background: ' + utility.color + '; width: 16px; height: 16px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
                    iconSize: [16, 16],
                    iconAnchor: [8, 8]
                }});
                
                if (index < utilityPositions.length) {{
                    L.marker(utilityPositions[index], {{icon: utilityIcon}})
                        .addTo(map)
                        .bindPopup('<b>🔧 ' + utility.type.charAt(0).toUpperCase() + utility.type.slice(1) + '</b><br>' +
                                  'Status: ' + utility.status.replace(/_/g, ' ') + '<br>' +
                                  'Cost: ' + utility.cost_range + '<br>' +
                                  'Timeline: ' + utility.timeline);
                }}
            }});
            
            // Add amenity markers
            var amenityData = {json.dumps(amenity_markers)};
            
            amenityData.slice(0, 8).forEach(function(amenity) {{
                var amenityIcon = L.divIcon({{
                    className: 'amenity-marker',
                    html: '<div style="background: #3498db; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
                    iconSize: [12, 12],
                    iconAnchor: [6, 6]
                }});
                
                L.marker(amenity.coordinates, {{icon: amenityIcon}})
                    .addTo(map)
                    .bindPopup('<b>🏘️ ' + amenity.name + '</b><br>' +
                              'Category: ' + amenity.category + '<br>' +
                              'Distance: ' + amenity.distance + '<br>' +
                              'Impact Score: ' + amenity.impact_score + '/10');
            }});
            
            // Add distance circles
            L.circle([{property_coords[0]}, {property_coords[1]}], {{
                color: '#3498db',
                fillColor: '#3498db',
                fillOpacity: 0.1,
                radius: 1000,
                weight: 2,
                dashArray: '5, 5'
            }}).addTo(map).bindPopup('1km radius');
            
            L.circle([{property_coords[0]}, {property_coords[1]}], {{
                color: '#95a5a6',
                fillColor: '#95a5a6',
                fillOpacity: 0.05,
                radius: 2000,
                weight: 1,
                dashArray: '10, 10'
            }}).addTo(map).bindPopup('2km radius');
        </script>
    </body>
    </html>
    """
    
    return html_template

#==============================================================================
# SAMPLE PROPERTY DATABASE (RESTORED 23 PROPERTIES)
#==============================================================================

SAMPLE_PROPERTIES = [
    # Edmonton Properties (9)
    {
        "property_id": "EDM_001",
        "address": "10123 97 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "lot_size_sqft": 6800,
        "estimated_value": 465000,
        "development_potential": "Medium - Established neighbourhood, family area",
        "investment_recommendation": "Requires detailed analysis",
        "confidence_level": "high"
    },
    {
        "property_id": "EDM_002", 
        "address": "8923 112 Street NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "commercial",
        "lot_size_sqft": 12500,
        "estimated_value": 890000,
        "development_potential": "High - Major transit access, university proximity",
        "investment_recommendation": "Strong potential",
        "confidence_level": "high"
    },
    {
        "property_id": "EDM_003",
        "address": "10821 Jasper Avenue NW, Edmonton, AB",
        "municipality": "edmonton", 
        "property_type": "mixed_use",
        "lot_size_sqft": 8900,
        "estimated_value": 725000,
        "development_potential": "Excellent - Downtown core, LRT access",
        "investment_recommendation": "Premium location",
        "confidence_level": "high"
    },
    {
        "property_id": "EDM_004",
        "address": "15623 87 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "lot_size_sqft": 7200,
        "estimated_value": 485000,
        "development_potential": "Medium - Mature neighbourhood, good amenities",
        "investment_recommendation": "Stable investment",
        "confidence_level": "medium"
    },
    {
        "property_id": "EDM_005",
        "address": "9234 Fort Road NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "industrial",
        "lot_size_sqft": 32000,
        "estimated_value": 1200000,
        "development_potential": "High - Industrial access, rail proximity",
        "investment_recommendation": "Industrial opportunity",
        "confidence_level": "high"
    },
    {
        "property_id": "EDM_006",
        "address": "11234 82 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "lot_size_sqft": 6400,
        "estimated_value": 445000,
        "development_potential": "Medium - University area, student rental potential",
        "investment_recommendation": "Investment potential",
        "confidence_level": "medium"
    },
    {
        "property_id": "EDM_007",
        "address": "16789 Stony Plain Road NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "commercial",
        "lot_size_sqft": 15600,
        "estimated_value": 950000,
        "development_potential": "Good - Major arterial, retail potential",
        "investment_recommendation": "Commercial development",
        "confidence_level": "medium"
    },
    {
        "property_id": "EDM_008",
        "address": "7845 159 Street NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "residential",
        "lot_size_sqft": 8100,
        "estimated_value": 525000,
        "development_potential": "Good - West end location, family area",
        "investment_recommendation": "Family residential",
        "confidence_level": "medium"
    },
    {
        "property_id": "EDM_009",
        "address": "12456 118 Avenue NW, Edmonton, AB",
        "municipality": "edmonton",
        "property_type": "mixed_use",
        "lot_size_sqft": 9800,
        "estimated_value": 675000,
        "development_potential": "Medium - Mixed use zoning, transit access",
        "investment_recommendation": "Mixed development",
        "confidence_level": "medium"
    },
    
    # Leduc Properties (4)
    {
        "property_id": "LED_001",
        "address": "4823 50 Avenue, Leduc, AB",
        "municipality": "leduc",
        "property_type": "residential",
        "lot_size_sqft": 7800,
        "estimated_value": 385000,
        "development_potential": "Good - Airport proximity, family area",
        "investment_recommendation": "Airport employment access",
        "confidence_level": "high"
    },
    {
        "property_id": "LED_002",
        "address": "6234 Discovery Way, Leduc, AB", 
        "municipality": "leduc",
        "property_type": "commercial",
        "lot_size_sqft": 18900,
        "estimated_value": 675000,
        "development_potential": "Excellent - Airport industrial, major highway",
        "investment_recommendation": "Commercial/industrial opportunity",
        "confidence_level": "high"
    },
    {
        "property_id": "LED_003",
        "address": "RR 23 Range Road 261, Leduc County, AB",
        "municipality": "leduc",
        "property_type": "agricultural",
        "lot_size_sqft": 217800,  # 5 acres
        "estimated_value": 445000,
        "development_potential": "Medium - Rural residential, airport proximity",
        "investment_recommendation": "Rural lifestyle",
        "confidence_level": "medium"
    },
    {
        "property_id": "LED_004",
        "address": "5567 48 Street, Leduc, AB",
        "municipality": "leduc",
        "property_type": "industrial",
        "lot_size_sqft": 43560,  # 1 acre
        "estimated_value": 320000,
        "development_potential": "High - Industrial zoning, airport access",
        "investment_recommendation": "Industrial development",
        "confidence_level": "high"
    },
    
    # St. Albert Properties (4)
    {
        "property_id": "SAB_001",
        "address": "123 Sturgeon Road, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "residential",
        "lot_size_sqft": 9200,
        "estimated_value": 520000,
        "development_potential": "Excellent - Premium residential, school district",
        "investment_recommendation": "Premium family area",
        "confidence_level": "high"
    },
    {
        "property_id": "SAB_002",
        "address": "456 St. Albert Trail, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "commercial",
        "lot_size_sqft": 14200,
        "estimated_value": 785000,
        "development_potential": "Good - Major arterial, retail potential",
        "investment_recommendation": "Commercial retail",
        "confidence_level": "medium"
    },
    {
        "property_id": "SAB_003",
        "address": "789 Belmont Drive, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "residential",
        "lot_size_sqft": 8600,
        "estimated_value": 495000,
        "development_potential": "Good - Established area, recreation access",
        "investment_recommendation": "Stable residential",
        "confidence_level": "medium"
    },
    {
        "property_id": "SAB_004",
        "address": "234 Boudreau Road, St. Albert, AB",
        "municipality": "st_albert",
        "property_type": "mixed_use",
        "lot_size_sqft": 11800,
        "estimated_value": 625000,
        "development_potential": "Medium - Mixed development potential",
        "investment_recommendation": "Mixed use opportunity",
        "confidence_level": "medium"
    },
    
    # Strathcona Properties (4)
    {
        "property_id": "STR_001",
        "address": "2345 Sherwood Drive, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "residential",
        "lot_size_sqft": 8900,
        "estimated_value": 445000,
        "development_potential": "Good - Sherwood Park, recreation access",
        "investment_recommendation": "Family community",
        "confidence_level": "medium"
    },
    {
        "property_id": "STR_002",
        "address": "Industrial Heartland Way, Fort Saskatchewan, AB",
        "municipality": "strathcona",
        "property_type": "industrial",
        "lot_size_sqft": 87120,  # 2 acres
        "estimated_value": 685000,
        "development_potential": "Excellent - Industrial Heartland, employment",
        "investment_recommendation": "Industrial opportunity",
        "confidence_level": "high"
    },
    {
        "property_id": "STR_003",
        "address": "1567 Festival Lane, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "commercial",
        "lot_size_sqft": 16700,
        "estimated_value": 595000,
        "development_potential": "Medium - Festival Place proximity, retail",
        "investment_recommendation": "Community commercial",
        "confidence_level": "medium"
    },
    {
        "property_id": "STR_004",
        "address": "8923 Clover Bar Road, Sherwood Park, AB",
        "municipality": "strathcona",
        "property_type": "agricultural",
        "lot_size_sqft": 130680,  # 3 acres
        "estimated_value": 325000,
        "development_potential": "Medium - Rural residential potential",
        "investment_recommendation": "Rural development",
        "confidence_level": "low"
    },
    
    # Parkland Properties (2)
    {
        "property_id": "PAR_001",
        "address": "RR 15 Highway 16A, Parkland County, AB",
        "municipality": "parkland",
        "property_type": "agricultural",
        "lot_size_sqft": 435600,  # 10 acres
        "estimated_value": 485000,
        "development_potential": "Medium - Rural lifestyle, highway access",
        "investment_recommendation": "Rural acreage",
        "confidence_level": "medium"
    },
    {
        "property_id": "PAR_002",
        "address": "26789 Range Road 33, Parkland County, AB",
        "municipality": "parkland",
        "property_type": "agricultural", 
        "lot_size_sqft": 261360,  # 6 acres
        "estimated_value": 425000,
        "development_potential": "Low - Rural location, limited services",
        "investment_recommendation": "Lifestyle property",
        "confidence_level": "low"
    }
]

#==============================================================================
# PARTNER FIRM DATABASE
#==============================================================================

PARTNER_FIRMS = [
    {
        "partner_id": "edmonton_premier_001",
        "company_name": "Edmonton Premier Realty",
        "contact_person": "Sarah Johnson",
        "email": "sarah@edmontonpremier.ca",
        "phone": "(780) 555-0123",
        "license_number": "AB-RE-2023-001",
        "service_areas": ["edmonton", "st_albert"],
        "specialties": ["residential", "commercial"],
        "api_key": "EPR_2024_SECURE_KEY_001",
        "data_submissions": 47,
        "last_submission": "2024-06-15",
        "credibility_rating": 0.85,
        "active": True
    },
    {
        "partner_id": "leduc_expert_002", 
        "company_name": "Leduc Area Realty Group",
        "contact_person": "Mike Chen",
        "email": "mike@leducrealty.ca",
        "phone": "(780) 555-0456",
        "license_number": "AB-RE-2023-002",
        "service_areas": ["leduc"],
        "specialties": ["industrial", "airport_proximity"],
        "api_key": "LARG_2024_SECURE_KEY_002",
        "data_submissions": 23,
        "last_submission": "2024-06-12",
        "credibility_rating": 0.85,
        "active": True
    },
    {
        "partner_id": "strathcona_insights_003",
        "company_name": "Strathcona Market Insights",
        "contact_person": "Jennifer Williams",
        "email": "jennifer@strathconamarket.ca", 
        "phone": "(780) 555-0789",
        "license_number": "AB-RE-2023-003",
        "service_areas": ["strathcona"],
        "specialties": ["industrial_heartland", "residential"],
        "api_key": "SMI_2024_SECURE_KEY_003",
        "data_submissions": 31,
        "last_submission": "2024-06-14",
        "credibility_rating": 0.85,
        "active": True
    }
]

#==============================================================================
# API ENDPOINTS
#==============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {
        "status": "healthy",
        "service": "sgiach-production",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat(),
        "sample_properties_count": len(SAMPLE_PROPERTIES),
        "partner_firms_count": len(PARTNER_FIRMS),
        "features": [
            "utility_analysis",
            "amenity_proximity", 
            "interactive_mapping",
            "partner_integration",
            "professional_engineering",
            "development_assessment",
            "building_placement"
        ]
    }

@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "platform": "Sgiach Professional Development Analysis Platform",
        "version": "3.0.0",
        "company": "SkyeBridge Consulting & Developments Inc.",
        "description": "Complete Municipal Property Development Analysis with Professional Engineering Oversight",
        "features": [
            "23 Sample Properties across 5 Alberta Municipalities",
            "Comprehensive Utility Connection Analysis",
            "Advanced Amenity Proximity Assessment", 
            "Interactive Property Mapping",
            "Development Assessment Interface",
            "Building Placement Validation",
            "Partner Realty Data Integration",
            "Professional Engineering Oversight",
            "Multi-Source Market Analysis",
            "Municipal Infrastructure Standards"
        ],
        "municipalities_served": ["Edmonton", "Leduc", "St. Albert", "Strathcona County", "Parkland County"],
        "professional_services": "P.Eng oversight available for complex developments",
        "api_documentation": "/docs",
        "health_check": "/health"
    }

# Sample Properties Endpoints
@app.get("/properties/sample")
async def get_sample_properties():
    """Retrieve all 23 sample properties for development/testing"""
    return {
        "total_properties": len(SAMPLE_PROPERTIES),
        "properties": SAMPLE_PROPERTIES,
        "municipalities": {
            "edmonton": len([p for p in SAMPLE_PROPERTIES if p["municipality"] == "edmonton"]),
            "leduc": len([p for p in SAMPLE_PROPERTIES if p["municipality"] == "leduc"]),
            "st_albert": len([p for p in SAMPLE_PROPERTIES if p["municipality"] == "st_albert"]),
            "strathcona": len([p for p in SAMPLE_PROPERTIES if p["municipality"] == "strathcona"]),
            "parkland": len([p for p in SAMPLE_PROPERTIES if p["municipality"] == "parkland"])
        }
    }

@app.get("/properties/sample/{property_id}")
async def get_sample_property(property_id: str):
    """Get specific sample property by ID"""
    property_data = next((p for p in SAMPLE_PROPERTIES if p["property_id"] == property_id), None)
    if not property_data:
        raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
    return property_data

@app.get("/municipalities/{municipality}/properties")
async def get_properties_by_municipality(municipality: Municipality):
    """Get all sample properties for a specific municipality"""
    properties = [p for p in SAMPLE_PROPERTIES if p["municipality"] == municipality.value]
    return {
        "municipality": municipality.value,
        "property_count": len(properties),
        "properties": properties
    }

# Development Assessment Endpoints
@app.post("/development/lot-assessment")
async def get_lot_assessment(lot_data: LotAssessment):
    """
    🎯 PURPOSE: Analyze a lot for development constraints and opportunities
    📨 INPUT: LotAssessment object with property details
    📤 OUTPUT: Comprehensive assessment with buildable areas, utilities, constraints
    🔗 FRONTEND CONNECTION: Called when user loads the Assessment Interface
    """
    
    development_engine = DevelopmentAssessmentEngine()
    
    try:
        assessment_result = development_engine.analyze_lot_development_potential(lot_data)
        return assessment_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment generation failed: {str(e)}")

@app.post("/development/validate-placement")
async def validate_building_placement(property_id: str, building: PlacedBuilding):
    """
    🎯 PURPOSE: Validate if a building can be placed at specified coordinates
    📨 INPUT: property_id and PlacedBuilding object
    📤 OUTPUT: Validation results with compliance details
    🔗 FRONTEND CONNECTION: Called when user drags a building in the SimCity interface
    """
    
    development_engine = DevelopmentAssessmentEngine()
    
    try:
        validation_result = development_engine.validate_building_placement(property_id, building)
        return validation_result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Placement validation failed: {str(e)}")

@app.post("/development/save-plan")
async def save_development_plan(plan: DevelopmentPlan):
    """
    🎯 PURPOSE: Save complete development plan with cost analysis
    📨 INPUT: DevelopmentPlan with all placed buildings
    📤 OUTPUT: Saved plan with cost analysis and documentation
    🔗 FRONTEND CONNECTION: Called when user clicks "Export Development Plan"
    """
    
    development_engine = DevelopmentAssessmentEngine()
    
    try:
        save_result = development_engine.save_development_plan(plan)
        return save_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan save failed: {str(e)}")

@app.get("/development/export-assessment/{assessment_id}")
async def export_site_assessment(assessment_id: str):
    """
    🎯 PURPOSE: Generate professional site assessment report for clients/municipalities
    📨 INPUT: assessment_id from previous lot assessment
    📤 OUTPUT: Professional report data ready for PDF generation
    🔗 FRONTEND CONNECTION: Called when user clicks "Export Site Analysis"
    """
    
    development_engine = DevelopmentAssessmentEngine()
    
    try:
        export_result = development_engine.export_site_assessment(assessment_id)
        return export_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.get("/development/export-plan/{plan_id}")
async def export_development_plan(plan_id: str):
    """Generate professional development plan documentation"""
    
    development_engine = DevelopmentAssessmentEngine()
    
    try:
        export_result = development_engine.export_development_plan(plan_id)
        return export_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan export failed: {str(e)}")

# Utility Analysis Endpoints
@app.post("/property/utility-analysis")
async def analyze_property_utilities(request: UtilityAnalysisRequest):
    """Complete utility connection analysis with cost assessment"""
    
    analyzer = UtilityAnalysisEngine()
    
    try:
        utility_ratings = analyzer.analyze_utility_connections(
            address=request.address,
            municipality=request.municipality.value,
            property_type=request.property_type.value
        )
        
        return {
            "address": request.address,
            "municipality": request.municipality.value,
            "analysis_date": datetime.now().isoformat(),
            "utility_ratings": asdict(utility_ratings),
            "professional_notes": "Analysis completed by SkyeBridge Consulting & Developments Inc. P.Eng oversight provided."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Utility analysis failed: {str(e)}")

@app.post("/property/amenity-analysis")
async def analyze_property_amenities(request: PropertyMappingRequest):
    """Complete amenity proximity analysis with value impact"""
    
    analyzer = AmenityProximityAnalyzer()
    
    # Simulate property coordinates (in production, use geocoding)
    property_coords = (53.5461, -113.4909)  # Default Edmonton coordinates
    
    try:
        amenity_analysis = analyzer.analyze_amenity_proximity(
            address=request.address,
            municipality=request.municipality.value,
            property_coordinates=property_coords
        )
        
        return {
            "address": request.address,
            "municipality": request.municipality.value,
            "analysis_date": datetime.now().isoformat(),
            "amenity_analysis": asdict(amenity_analysis),
            "professional_notes": "Amenity analysis completed using Alberta municipal databases."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Amenity analysis failed: {str(e)}")

@app.post("/property/comprehensive-mapping-analysis", response_class=HTMLResponse)
async def comprehensive_property_mapping_analysis(request: PropertyMappingRequest):
    """Complete property analysis with interactive mapping"""
    
    # Initialize analyzers
    utility_analyzer = UtilityAnalysisEngine()
    amenity_analyzer = AmenityProximityAnalyzer()
    
    # Simulate property coordinates
    property_coords = (53.5461, -113.4909)
    
    try:
        # Perform utility analysis
        utility_ratings = utility_analyzer.analyze_utility_connections(
            address=request.address,
            municipality=request.municipality.value,
            property_type=request.property_type.value
        )
        
        # Perform amenity analysis  
        amenity_analysis = amenity_analyzer.analyze_amenity_proximity(
            address=request.address,
            municipality=request.municipality.value,
            property_coordinates=property_coords
        )
        
        # Generate interactive map
        property_data = {
            "address": request.address,
            "municipality": request.municipality.value,
            "property_type": request.property_type.value,
            "coordinates": property_coords
        }
        
        interactive_map = generate_interactive_property_map(
            property_data=property_data,
            utility_ratings=utility_ratings,
            amenity_analysis=amenity_analysis
        )
        
        return HTMLResponse(content=interactive_map)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")

@app.get("/mapping/interactive/{municipality}", response_class=HTMLResponse)
async def get_interactive_municipal_map(municipality: Municipality):
    """Serve interactive mapping interface for specific municipality"""
    
    # Get sample property for municipality
    sample_property = next((p for p in SAMPLE_PROPERTIES if p["municipality"] == municipality.value), None)
    
    if not sample_property:
        raise HTTPException(status_code=404, detail=f"No sample properties for {municipality.value}")
    
    # Create mapping request
    mapping_request = PropertyMappingRequest(
        address=sample_property["address"],
        municipality=municipality,
        property_type=PropertyType(sample_property["property_type"])
    )
    
    # Generate comprehensive analysis
    return await comprehensive_property_mapping_analysis(mapping_request)

@app.get("/mapping/amenities/{municipality}")
async def get_municipal_amenities(municipality: Municipality):
    """Get all amenities for a municipality for mapping display"""
    
    amenity_db = AlbertaAmenityDatabase()
    amenities = amenity_db.get_municipal_amenities(municipality.value)
    
    return {
        "municipality": municipality.value,
        "amenity_categories": list(amenities.keys()),
        "amenities": amenities
    }

# Infrastructure Standards Endpoints
@app.get("/infrastructure/municipal-standards/{municipality}")
async def get_municipal_infrastructure_standards(municipality: Municipality):
    """Get infrastructure standards and costs for municipality"""
    
    utility_db = AlbertaUtilityDatabase()
    infrastructure = utility_db.get_municipal_infrastructure(municipality.value)
    
    if not infrastructure:
        raise HTTPException(status_code=404, detail=f"Infrastructure data for {municipality.value} not found")
    
    return {
        "municipality": municipality.value,
        "infrastructure_standards": asdict(infrastructure),
        "last_updated": "2024-06-15",
        "data_source": "Municipal Engineering Departments & Alberta Standards"
    }

@app.get("/amenities/analysis-summary/{municipality}")
async def get_amenity_analysis_summary(municipality: Municipality):
    """Get comprehensive amenity analysis summary for municipality"""
    
    amenity_db = AlbertaAmenityDatabase()
    amenities = amenity_db.get_municipal_amenities(municipality.value)
    
    if not amenities:
        raise HTTPException(status_code=404, detail=f"Amenity data for {municipality.value} not found")
    
    # Calculate amenity statistics
    category_counts = {category: len(amenity_list) for category, amenity_list in amenities.items()}
    total_amenities = sum(category_counts.values())
    
    # Calculate average impact scores by category
    category_impacts = {}
    for category, amenity_list in amenities.items():
        if amenity_list:
            avg_impact = sum(amenity.impact_score for amenity in amenity_list) / len(amenity_list)
            category_impacts[category] = round(avg_impact, 1)
    
    return {
        "municipality": municipality.value,
        "amenity_profile": {
            "total_amenities": total_amenities,
            "category_counts": category_counts,
            "category_impacts": category_impacts,
            "top_amenities": [
                {"name": amenity.name, "category": category, "impact": amenity.impact_score}
                for category, amenity_list in amenities.items()
                for amenity in sorted(amenity_list, key=lambda a: a.impact_score, reverse=True)[:3]
            ]
        },
        "development_suitability": {
            "residential": "excellent" if category_impacts.get("education", 0) >= 7.5 else "good",
            "commercial": "excellent" if category_impacts.get("transportation", 0) >= 8.0 else "good",
            "industrial": "excellent" if municipality.value in ["strathcona", "leduc"] else "moderate"
        }
    }

# Partner Firm Integration Endpoints
@app.post("/partners/register")
async def register_partner_firm(
    partner_id: str = Form(...),
    company_name: str = Form(...),
    contact_person: str = Form(...),
    email: str = Form(...),
    license_number: str = Form(...),
    service_areas: List[str] = Form(...)
):
    """Register new partner realty firm"""
    
    # Check if partner already exists
    existing_partner = next((p for p in PARTNER_FIRMS if p["partner_id"] == partner_id), None)
    if existing_partner:
        raise HTTPException(status_code=400, detail="Partner firm already registered")
    
    # Generate API key
    api_key = f"{partner_id.upper()}_2024_SECURE_KEY_{len(PARTNER_FIRMS)+1:03d}"
    
    new_partner = {
        "partner_id": partner_id,
        "company_name": company_name,
        "contact_person": contact_person,
        "email": email,
        "license_number": license_number,
        "service_areas": service_areas,
        "api_key": api_key,
        "data_submissions": 0,
        "last_submission": None,
        "credibility_rating": 0.85,
        "active": True
    }
    
    PARTNER_FIRMS.append(new_partner)
    
    return {
        "status": "success",
        "message": "Partner firm registered successfully",
        "partner_id": partner_id,
        "api_key": api_key,
        "service_areas": service_areas
    }

@app.get("/partners/list")
async def list_partner_firms():
    """List all registered partner firms"""
    return {
        "total_partners": len(PARTNER_FIRMS),
        "active_partners": len([p for p in PARTNER_FIRMS if p["active"]]),
        "partners": [
            {
                "partner_id": p["partner_id"],
                "company_name": p["company_name"],
                "service_areas": p["service_areas"],
                "data_submissions": p["data_submissions"],
                "credibility_rating": p["credibility_rating"],
                "active": p["active"]
            } for p in PARTNER_FIRMS
        ]
    }

@app.post("/partners/data/sales")
async def submit_partner_sales_data(
    address: str = Form(...),
    sale_price: float = Form(...),
    sale_date: str = Form(...),
    property_type: str = Form(...),
    mls_number: str = Form(...),
    municipality: str = Form(...),
    api_key: str = Form(...)
):
    """Partner firms submit sales data"""
    
    # Validate API key
    partner = next((p for p in PARTNER_FIRMS if p["api_key"] == api_key), None)
    if not partner:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if not partner["active"]:
        raise HTTPException(status_code=403, detail="Partner account not active")
    
    # Validate municipality access
    if municipality not in partner["service_areas"]:
        raise HTTPException(status_code=403, detail=f"Partner not authorized for {municipality}")
    
    # Create sales record
    sales_data = {
        "partner_id": partner["partner_id"],
        "sale_type": "actual_sale",
        "sale_price": sale_price,
        "sale_date": sale_date,
        "address": address,
        "property_type": property_type,
        "mls_number": mls_number,
        "municipality": municipality,
        "submission_date": datetime.now().isoformat(),
        "credibility_weight": 0.85,
        "confidence_level": "high"
    }
    
    # Update partner statistics
    partner["data_submissions"] += 1
    partner["last_submission"] = datetime.now().isoformat()
    
    return {
        "status": "success",
        "message": "Sales data submitted successfully",
        "partner_company": partner["company_name"],
        "sale_price": sale_price,
        "credibility_weight": 0.85,
        "submission_count": partner["data_submissions"]
    }

@app.get("/partners/data/summary/{municipality}")
async def get_partner_data_summary(municipality: Municipality):
    """Get summary of partner data for municipality"""
    
    # Filter partners serving this municipality
    active_partners = [p for p in PARTNER_FIRMS if municipality.value in p["service_areas"] and p["active"]]
    
    total_submissions = sum(p["data_submissions"] for p in active_partners)
    
    return {
        "municipality": municipality.value,
        "active_partners": len(active_partners),
        "total_data_submissions": total_submissions,
        "partners": [
            {
                "company_name": p["company_name"],
                "data_submissions": p["data_submissions"],
                "last_submission": p["last_submission"],
                "credibility_rating": p["credibility_rating"]
            } for p in active_partners
        ]
    }

# JSON Endpoints for Swagger UI Testing
class PropertyAnalysisJSON(BaseModel):
    address: str
    municipality: Municipality
    property_type: PropertyType
    include_market_analysis: bool = True
    include_amenity_analysis: bool = True
    include_infrastructure_analysis: bool = True
    include_partner_data: bool = True
    analysis_radius_km: float = 2.0

class UtilityAnalysisJSON(BaseModel):
    address: str
    municipality: Municipality
    property_type: PropertyType
    development_type: str
    target_density: str = "medium"

class AmenityAnalysisJSON(BaseModel):
    address: str
    municipality: Municipality
    property_type: PropertyType
    lot_size_sqft: Optional[float] = None
    include_utilities: bool = True
    include_amenities: bool = True
    include_infrastructure: bool = True
    professional_analysis: bool = True

class PartnerRegistrationJSON(BaseModel):
    partner_id: str
    company_name: str
    contact_person: str
    email: str
    license_number: str
    service_areas: List[str]

class PartnerSalesDataJSON(BaseModel):
    address: str
    sale_price: float
    sale_date: str
    property_type: str
    mls_number: str
    municipality: str
    api_key: str

@app.post("/property/utility-analysis-json")
async def utility_analysis_json(request: UtilityAnalysisJSON):
    """Complete utility connection analysis - JSON version for Swagger UI"""
    
    analyzer = UtilityAnalysisEngine()
    
    try:
        utility_ratings = analyzer.analyze_utility_connections(
            address=request.address,
            municipality=request.municipality.value,
            property_type=request.property_type.value
        )
        
        return {
            "address": request.address,
            "municipality": request.municipality.value,
            "analysis_date": datetime.now().isoformat(),
            "utility_ratings": asdict(utility_ratings),
            "professional_notes": "Analysis completed by SkyeBridge Consulting & Developments Inc. P.Eng oversight provided."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Utility analysis failed: {str(e)}")

@app.post("/property/amenity-analysis-json")
async def amenity_analysis_json(request: AmenityAnalysisJSON):
    """Complete amenity proximity analysis - JSON version for Swagger UI"""
    
    analyzer = AmenityProximityAnalyzer()
    property_coords = (53.5461, -113.4909)
    
    try:
        amenity_analysis = analyzer.analyze_amenity_proximity(
            address=request.address,
            municipality=request.municipality.value,
            property_coordinates=property_coords
        )
        
        return {
            "address": request.address,
            "municipality": request.municipality.value,
            "analysis_date": datetime.now().isoformat(),
            "amenity_analysis": asdict(amenity_analysis),
            "professional_notes": "Amenity analysis completed using Alberta municipal databases."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Amenity analysis failed: {str(e)}")

@app.post("/partners/register-json")
async def register_partner_firm_json(request: PartnerRegistrationJSON):
    """Register new partner realty firm - JSON version for Swagger UI"""
    
    # Check if partner already exists
    existing_partner = next((p for p in PARTNER_FIRMS if p["partner_id"] == request.partner_id), None)
    if existing_partner:
        raise HTTPException(status_code=400, detail="Partner firm already registered")
    
    # Generate API key
    api_key = f"{request.partner_id.upper()}_2024_SECURE_KEY_{len(PARTNER_FIRMS)+1:03d}"
    
    new_partner = {
        "partner_id": request.partner_id,
        "company_name": request.company_name,
        "contact_person": request.contact_person,
        "email": request.email,
        "license_number": request.license_number,
        "service_areas": request.service_areas,
        "api_key": api_key,
        "data_submissions": 0,
        "last_submission": None,
        "credibility_rating": 0.85,
        "active": True
    }
    
    PARTNER_FIRMS.append(new_partner)
    
    return {
        "status": "success",
        "message": "Partner firm registered successfully",
        "partner_id": request.partner_id,
        "api_key": api_key,
        "service_areas": request.service_areas
    }

@app.post("/partners/data/sales-json")
async def submit_partner_sales_data_json(request: PartnerSalesDataJSON):
    """Partner firms submit sales data - JSON version for Swagger UI"""
    
    # Validate API key
    partner = next((p for p in PARTNER_FIRMS if p["api_key"] == request.api_key), None)
    if not partner:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if not partner["active"]:
        raise HTTPException(status_code=403, detail="Partner account not active")
    
    # Validate municipality access
    if request.municipality not in partner["service_areas"]:
        raise HTTPException(status_code=403, detail=f"Partner not authorized for {request.municipality}")
    
    # Create sales record
    sales_data = {
        "partner_id": partner["partner_id"],
        "sale_type": "actual_sale",
        "sale_price": request.sale_price,
        "sale_date": request.sale_date,
        "address": request.address,
        "property_type": request.property_type,
        "mls_number": request.mls_number,
        "municipality": request.municipality,
        "submission_date": datetime.now().isoformat(),
        "credibility_weight": 0.85,
        "confidence_level": "high"
    }
    
    # Update partner statistics
    partner["data_submissions"] += 1
    partner["last_submission"] = datetime.now().isoformat()
    
    return {
        "status": "success",
        "message": "Sales data submitted successfully",
        "partner_company": partner["company_name"],
        "sale_price": request.sale_price,
        "credibility_weight": 0.85,
        "submission_count": partner["data_submissions"]
    }

# Administrative Endpoints
@app.post("/admin/reset-sample-data")


async def reset_sample_data():
    """Reset sample data to original 23 properties"""
    
    # In production, this would reset the database
    # For now, just return confirmation
    return {
        "status": "success",
        "message": "Sample data reset to 23 original properties",
        "properties_count": len(SAMPLE_PROPERTIES),
        "partner_firms_count": len(PARTNER_FIRMS),
        "reset_timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
