"""
PropertyDataModel - Foundation Class for Sgiach Platform
SkyeBridge Consulting & Developments Inc.

This model serves as the standardized data structure that flows between
Module 1 (Land Valuation Engine) and Module 2 (Development Scenario Generator).

Designed for Alberta/Edmonton development projects with P.Eng validation
and professional service integration.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from enum import Enum
import json
from decimal import Decimal


class ZoningClassification(Enum):
    """Edmonton/Alberta zoning classifications"""
    # Residential
    RF1 = "Single Detached Residential"
    RF3 = "Small Scale Infill"
    RF4 = "Semi-Detached Residential" 
    RF5 = "Row Housing"
    RF6 = "Medium Density Multiple Family"
    RA7 = "Low Rise Apartment"
    RA8 = "Medium Rise Apartment"
    RA9 = "High Rise Apartment"
    
    # Commercial
    CB1 = "Low Intensity Business"
    CB2 = "General Business"
    CB3 = "Community Business"
    
    # Industrial
    IM = "Medium Industrial"
    IH = "Heavy Industrial"
    IL = "Light Industrial"
    
    # Mixed Use
    DC1 = "Direct Control"
    DC2 = "Site Specific Development Control"
    
    # Special Areas
    US = "Urban Services"
    PU = "Public Utility"
    A = "Metropolitan Recreation"


class DevelopmentConstraintType(Enum):
    """Types of development constraints"""
    ENVIRONMENTAL = "Environmental"
    REGULATORY = "Regulatory" 
    INFRASTRUCTURE = "Infrastructure"
    GEOTECHNICAL = "Geotechnical"
    CULTURAL = "Cultural/Heritage"
    TREATY = "Indigenous Treaty Rights"


class PropertyType(Enum):
    """Property classification for development analysis"""
    VACANT_LAND = "Vacant Land"
    RESIDENTIAL_EXISTING = "Existing Residential"
    COMMERCIAL_EXISTING = "Existing Commercial"
    INDUSTRIAL_EXISTING = "Existing Industrial"
    MIXED_USE_EXISTING = "Existing Mixed Use"
    AGRICULTURAL = "Agricultural"
    INSTITUTIONAL = "Institutional"


@dataclass
class GeographicData:
    """Geographic and spatial information"""
    coordinates: Tuple[float, float]  # (latitude, longitude)
    property_boundaries: Dict[str, Any]  # GeoJSON polygon
    legal_description: str
    municipal_address: str
    lot_size_sqm: float
    lot_size_acres: float
    frontage_meters: float
    depth_meters: float
    topography: str  # "flat", "sloped", "irregular"
    orientation: str  # "north", "south", "east", "west"


@dataclass
class ZoningInformation:
    """Zoning regulations and development rules"""
    primary_zoning: ZoningClassification
    overlay_zones: List[str] = field(default_factory=list)
    
    # Development parameters
    max_height_meters: Optional[float] = None
    max_stories: Optional[int] = None
    max_density_units_per_hectare: Optional[float] = None
    max_floor_area_ratio: Optional[float] = None
    
    # Setback requirements (meters)
    front_setback: Optional[float] = None
    rear_setback: Optional[float] = None
    side_setback: Optional[float] = None
    
    # Use permissions
    permitted_uses: List[str] = field(default_factory=list)
    discretionary_uses: List[str] = field(default_factory=list)
    
    # Special requirements
    parking_ratio: Optional[float] = None  # spaces per unit
    landscaping_requirement: Optional[float] = None  # percentage
    affordable_housing_requirement: Optional[float] = None  # percentage


@dataclass
class MarketAnalysis:
    """Current market valuation and comparable sales data"""
    current_assessed_value: Decimal
    current_market_value_estimate: Decimal
    value_per_sqm: Decimal
    value_per_acre: Decimal
    
    # Comparable sales
    comparable_sales: List[Dict[str, Any]] = field(default_factory=list)
    market_trend_6_month: float = 0.0  # percentage change
    market_trend_12_month: float = 0.0  # percentage change
    
    # Market conditions
    average_days_on_market: Optional[int] = None
    market_absorption_rate: Optional[float] = None
    competition_analysis: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DevelopmentConstraint:
    """Individual development constraint"""
    constraint_type: DevelopmentConstraintType
    description: str
    severity: str  # "low", "medium", "high", "blocking"
    mitigation_cost_estimate: Optional[Decimal] = None
    mitigation_timeline_months: Optional[int] = None
    regulatory_reference: Optional[str] = None


@dataclass
class InfrastructureScoring:
    """Proximity and accessibility scoring for development viability"""
    # Transportation (0-10 scale)
    highway_access_score: float
    public_transit_score: float
    airport_proximity_score: float
    
    # Essential Services (0-10 scale)
    schools_score: float
    healthcare_score: float
    shopping_score: float
    employment_centers_score: float
    
    # Utilities (0-10 scale)
    water_sewer_score: float
    electrical_capacity_score: float
    natural_gas_score: float
    telecommunications_score: float
    
    # Infrastructure costs
    utility_connection_cost_estimate: Optional[Decimal] = None
    road_access_improvement_cost: Optional[Decimal] = None
    
    # Detailed proximity data
    proximity_details: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class RegulatoryCompliance:
    """Regulatory requirements and compliance status"""
    municipal_approval_probability: float  # 0-1 scale
    environmental_assessment_required: bool = False
    indigenous_consultation_required: bool = False
    heritage_assessment_required: bool = False
    
    # Treaty territory information
    treaty_territory: Optional[str] = None  # "Treaty 6", "Treaty 7", "Treaty 8"
    indigenous_communities_affected: List[str] = field(default_factory=list)
    
    # Permit timeline estimates
    development_permit_timeline_months: Optional[int] = None
    building_permit_timeline_months: Optional[int] = None
    subdivision_timeline_months: Optional[int] = None
    
    # Associated costs
    regulatory_compliance_cost_estimate: Optional[Decimal] = None


@dataclass
class PropertyDataModel:
    """
    Comprehensive property data model for Sgiach platform.
    
    This model serves as the standardized data structure that flows between
    Module 1 (Land Valuation Engine) and Module 2 (Development Scenario Generator).
    
    All spatial data uses WGS84 coordinate system.
    All monetary values use CAD currency.
    All measurements use metric system.
    """
    
    # Basic identification
    property_id: str
    analysis_timestamp: datetime
    analyzed_by: str  # "Module1", "Professional_Validation", etc.
    
    # Core property data
    geographic_data: GeographicData
    property_type: PropertyType
    zoning_info: ZoningInformation
    market_analysis: MarketAnalysis
    
    # Development analysis
    infrastructure_scoring: InfrastructureScoring
    development_constraints: List[DevelopmentConstraint] = field(default_factory=list)
    regulatory_compliance: RegulatoryCompliance = field(default_factory=lambda: RegulatoryCompliance(0.5))
    
    # Development potential indicators
    development_potential_score: Optional[float] = None  # 0-10 overall score
    estimated_development_timeline_months: Optional[int] = None
    development_complexity_rating: str = "medium"  # "low", "medium", "high", "complex"
    
    # Professional validation status
    engineering_validation_required: bool = False
    architectural_validation_required: bool = False
    market_validation_required: bool = False
    validation_triggers: List[str] = field(default_factory=list)
    
    # Module 2 readiness
    module2_ready: bool = False
    module2_trigger_reasons: List[str] = field(default_factory=list)
    
    # Metadata
    data_sources: List[str] = field(default_factory=list)
    data_quality_score: float = 1.0  # 0-1 confidence level
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate data and set computed fields after initialization"""
        self._validate_data()
        self._calculate_development_potential()
        self._determine_validation_requirements()
        self._assess_module2_readiness()
    
    def _validate_data(self) -> None:
        """Validate critical data fields"""
        if not self.geographic_data.coordinates:
            raise ValueError("Property coordinates are required")
        
        if self.geographic_data.lot_size_sqm <= 0:
            raise ValueError("Lot size must be positive")
        
        if self.market_analysis.current_market_value_estimate <= 0:
            raise ValueError("Market value must be positive")
    
    def _calculate_development_potential(self) -> None:
        """Calculate overall development potential score (0-10)"""
        scores = [
            self.infrastructure_scoring.highway_access_score * 0.15,
            self.infrastructure_scoring.public_transit_score * 0.10,
            self.infrastructure_scoring.water_sewer_score * 0.20,
            self.infrastructure_scoring.schools_score * 0.10,
            self.infrastructure_scoring.employment_centers_score * 0.15,
            (10 - len(self.development_constraints)) * 0.20,  # fewer constraints = higher score
            self.regulatory_compliance.municipal_approval_probability * 10 * 0.10
        ]
        
        self.development_potential_score = max(0, min(10, sum(scores)))
        
        # Set complexity rating based on constraints and approvals
        constraint_count = len([c for c in self.development_constraints if c.severity in ["high", "blocking"]])
        if constraint_count >= 3 or self.regulatory_compliance.municipal_approval_probability < 0.3:
            self.development_complexity_rating = "complex"
        elif constraint_count >= 2 or self.regulatory_compliance.municipal_approval_probability < 0.6:
            self.development_complexity_rating = "high"
        elif constraint_count >= 1:
            self.development_complexity_rating = "medium"
        else:
            self.development_complexity_rating = "low"
    
    def _determine_validation_requirements(self) -> None:
        """Determine what professional validation is required"""
        # Engineering validation triggers
        engineering_triggers = []
        if self.zoning_info.max_height_meters and self.zoning_info.max_height_meters > 15:
            engineering_triggers.append("Building height >15m requires structural engineering")
        
        if any(c.constraint_type == DevelopmentConstraintType.GEOTECHNICAL for c in self.development_constraints):
            engineering_triggers.append("Geotechnical constraints require engineering assessment")
        
        if self.geographic_data.lot_size_acres > 5:
            engineering_triggers.append("Large development requires infrastructure engineering")
        
        # Architectural validation triggers  
        architectural_triggers = []
        if self.zoning_info.max_stories and self.zoning_info.max_stories > 3:
            architectural_triggers.append("Multi-story development requires architectural design")
        
        if any("mixed" in use.lower() for use in self.zoning_info.permitted_uses):
            architectural_triggers.append("Mixed-use development requires architectural coordination")
        
        # Market validation triggers
        market_triggers = []
        if self.market_analysis.current_market_value_estimate > Decimal('2000000'):
            market_triggers.append("High-value development requires market validation")
        
        if self.development_potential_score < 6:
            market_triggers.append("Lower potential score requires market analysis validation")
        
        # Set validation requirements
        self.engineering_validation_required = len(engineering_triggers) > 0
        self.architectural_validation_required = len(architectural_triggers) > 0
        self.market_validation_required = len(market_triggers) > 0
        
        self.validation_triggers = engineering_triggers + architectural_triggers + market_triggers
    
    def _assess_module2_readiness(self) -> None:
        """Determine if property data is sufficient for Module 2 scenario generation"""
        readiness_criteria = []
        
        # Required data checks
        if not self.zoning_info.primary_zoning:
            readiness_criteria.append("Zoning classification required")
        
        if not self.zoning_info.permitted_uses:
            readiness_criteria.append("Permitted uses information required")
        
        if self.infrastructure_scoring.water_sewer_score == 0:
            readiness_criteria.append("Utility infrastructure information required")
        
        if self.development_potential_score is None or self.development_potential_score < 3:
            readiness_criteria.append("Insufficient development potential")
        
        # Check for blocking constraints
        blocking_constraints = [c for c in self.development_constraints if c.severity == "blocking"]
        if blocking_constraints:
            readiness_criteria.append(f"Blocking constraints must be resolved: {', '.join(c.description for c in blocking_constraints)}")
        
        # Set Module 2 readiness
        self.module2_ready = len(readiness_criteria) == 0
        self.module2_trigger_reasons = readiness_criteria if not self.module2_ready else ["All criteria met - ready for scenario generation"]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        def convert_value(value):
            if isinstance(value, (Decimal, datetime)):
                return str(value)
            elif isinstance(value, Enum):
                return value.value
            elif hasattr(value, '__dict__'):
                return {k: convert_value(v) for k, v in value.__dict__.items()}
            elif isinstance(value, list):
                return [convert_value(item) for item in value]
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items()}
            return value
        
        return convert_value(self.__dict__)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PropertyDataModel':
        """Create PropertyDataModel from dictionary"""
        # This would include deserialization logic
        # Implementation depends on your specific data structure needs
        pass
    
    def get_scenario_generation_inputs(self) -> Dict[str, Any]:
        """
        Extract the key data needed for Module 2 scenario generation.
        
        Returns:
            Dictionary with essential data for development scenario creation
        """
        return {
            'property_id': self.property_id,
            'lot_size_sqm': self.geographic_data.lot_size_sqm,
            'lot_size_acres': self.geographic_data.lot_size_acres,
            'zoning_classification': self.zoning_info.primary_zoning.value,
            'max_density': self.zoning_info.max_density_units_per_hectare,
            'max_height': self.zoning_info.max_height_meters,
            'max_stories': self.zoning_info.max_stories,
            'permitted_uses': self.zoning_info.permitted_uses,
            'setbacks': {
                'front': self.zoning_info.front_setback,
                'rear': self.zoning_info.rear_setback,
                'side': self.zoning_info.side_setback
            },
            'current_land_value': float(self.market_analysis.current_market_value_estimate),
            'infrastructure_scores': {
                'transit': self.infrastructure_scoring.public_transit_score,
                'utilities': self.infrastructure_scoring.water_sewer_score,
                'schools': self.infrastructure_scoring.schools_score,
                'employment': self.infrastructure_scoring.employment_centers_score
            },
            'development_constraints': [
                {
                    'type': c.constraint_type.value,
                    'severity': c.severity,
                    'description': c.description,
                    'mitigation_cost': float(c.mitigation_cost_estimate) if c.mitigation_cost_estimate else None
                }
                for c in self.development_constraints
            ],
            'development_potential_score': self.development_potential_score,
            'complexity_rating': self.development_complexity_rating,
            'professional_validation_required': {
                'engineering': self.engineering_validation_required,
                'architectural': self.architectural_validation_required,
                'market': self.market_validation_required
            }
        }
    
    def calculate_buildable_area(self) -> Dict[str, float]:
        """
        Calculate maximum buildable area based on zoning and setbacks.
        
        Returns:
            Dictionary with buildable area calculations
        """
        # Account for setbacks
        effective_width = self.geographic_data.frontage_meters
        effective_depth = self.geographic_data.depth_meters
        
        if self.zoning_info.front_setback:
            effective_depth -= self.zoning_info.front_setback
        if self.zoning_info.rear_setback:
            effective_depth -= self.zoning_info.rear_setback
        if self.zoning_info.side_setback:
            effective_width -= (self.zoning_info.side_setback * 2)
        
        buildable_footprint = max(0, effective_width * effective_depth)
        
        # Calculate maximum floor area based on FAR
        max_floor_area = buildable_footprint
        if self.zoning_info.max_floor_area_ratio:
            max_floor_area = min(
                buildable_footprint * self.zoning_info.max_floor_area_ratio,
                self.geographic_data.lot_size_sqm * self.zoning_info.max_floor_area_ratio
            )
        
        return {
            'buildable_footprint_sqm': buildable_footprint,
            'max_floor_area_sqm': max_floor_area,
            'effective_width_m': effective_width,
            'effective_depth_m': effective_depth,
            'setback_area_lost_sqm': self.geographic_data.lot_size_sqm - buildable_footprint
        }


# Example usage and factory functions
def create_edmonton_property_template() -> PropertyDataModel:
    """Create a template PropertyDataModel for Edmonton properties"""
    return PropertyDataModel(
        property_id="EDM_TEMPLATE",
        analysis_timestamp=datetime.now(),
        analyzed_by="Template_Generator",
        geographic_data=GeographicData(
            coordinates=(53.5461, -113.4938),  # Edmonton coordinates
            property_boundaries={},
            legal_description="TBD",
            municipal_address="TBD",
            lot_size_sqm=1000.0,
            lot_size_acres=0.25,
            frontage_meters=30.0,
            depth_meters=33.3,
            topography="flat",
            orientation="south"
        ),
        property_type=PropertyType.VACANT_LAND,
        zoning_info=ZoningInformation(
            primary_zoning=ZoningClassification.RF1,
            max_height_meters=10.0,
            max_stories=2,
            front_setback=6.0,
            rear_setback=6.0,
            side_setback=1.5,
            permitted_uses=["Single detached dwelling"]
        ),
        market_analysis=MarketAnalysis(
            current_assessed_value=Decimal('400000'),
            current_market_value_estimate=Decimal('450000'),
            value_per_sqm=Decimal('450'),
            value_per_acre=Decimal('1800000')
        ),
        infrastructure_scoring=InfrastructureScoring(
            highway_access_score=7.0,
            public_transit_score=6.0,
            airport_proximity_score=8.0,
            schools_score=8.0,
            healthcare_score=7.0,
            shopping_score=7.0,
            employment_centers_score=8.0,
            water_sewer_score=9.0,
            electrical_capacity_score=9.0,
            natural_gas_score=9.0,
            telecommunications_score=8.0
        )
    )


if __name__ == "__main__":
    # Example usage
    property_data = create_edmonton_property_template()
    
    print("PropertyDataModel Example:")
    print(f"Development Potential Score: {property_data.development_potential_score:.2f}/10")
    print(f"Complexity Rating: {property_data.development_complexity_rating}")
    print(f"Module 2 Ready: {property_data.module2_ready}")
    print(f"Professional Validation Required: Engineering={property_data.engineering_validation_required}, Architectural={property_data.architectural_validation_required}")
    
    # Calculate buildable area
    buildable = property_data.calculate_buildable_area()
    print(f"Buildable Footprint: {buildable['buildable_footprint_sqm']:.1f} sqm")
    
    # Get scenario generation inputs
    scenario_inputs = property_data.get_scenario_generation_inputs()
    print(f"Ready for scenario generation with {len(scenario_inputs)} data points")
