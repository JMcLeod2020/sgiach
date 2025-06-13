"""
analyzer_complete.py - Complete Real Estate Analyzer with Web Scraping
This is a standalone version that includes all necessary components
"""

import asyncio
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass
from datetime import datetime

# Import our scraper
from web_scraper import get_real_properties, PropertyScraperManager

# Data Classes
@dataclass
class DeveloperPreferences:
    """Developer preferences for evaluating properties"""
    risk_tolerance: float  # 0-1 scale (0=conservative, 1=aggressive)
    preferred_property_types: List[str]
    min_roi_threshold: float
    max_development_timeline_months: int
    financing_preference: str
    location_preferences: Dict[str, float]

@dataclass
class PropertyListing:
    """Basic property information"""
    listing_id: str
    address: str
    city: str
    province: str
    price: float
    lot_size_sqft: float
    zoning: str
    listing_url: str

@dataclass
class DevelopmentScenario:
    """What could be built on the property"""
    scenario_name: str
    total_units: int
    construction_cost: float
    timeline_months: int
    projected_revenue: float

@dataclass
class FinancialAnalysis:
    """Financial metrics for a development"""
    total_investment: float
    projected_revenue: float
    net_profit: float
    roi_percentage: float
    payback_months: int

class RealEstateAnalyzer:
    """Complete analyzer that uses real scraped data"""
    
    def __init__(self):
        self.scraper_manager = PropertyScraperManager()
        self.properties_analyzed = 0
        
    async def analyze_market(self, search_criteria: Dict, preferences: DeveloperPreferences) -> Dict:
        """Main analysis function using real scraped data"""
        
        print("🔍 Starting property search...")
        print(f"Location: {search_criteria.get('city', 'Edmonton')}, {search_criteria.get('province', 'AB')}")
        print(f"Price Range: ${search_criteria.get('min_price', 0):,} - ${search_criteria.get('max_price', 10000000):,}")
        
        # Get real properties from web scraping
        properties = await get_real_properties(search_criteria)
        
        if not properties:
            return {
                'status': 'error',
                'message': 'No properties found matching criteria',
                'results': []
            }
            
        print(f"\n✅ Found {len(properties)} properties to analyze")
        
        # Analyze each property
        analyzed_properties = []
        
        for i, prop_data in enumerate(properties):
            print(f"\n📊 Analyzing property {i+1}/{len(properties)}: {prop_data['address']}")
            
            try:
                # Create property object
                property = PropertyListing(
                    listing_id=prop_data['id'],
                    address=prop_data['address'],
                    city=prop_data['city'],
                    province=prop_data['province'],
                    price=prop_data['price'],
                    lot_size_sqft=prop_data['lot_size_sqft'],
                    zoning=prop_data.get('zoning', 'Unknown'),
                    listing_url=prop_data.get('url', '#')
                )
                
                # Skip if price is too low (likely error)
                if property.price < 10000:
                    continue
                    
                # Generate development scenarios
                scenarios = self._generate_scenarios(property)
                
                # Find best scenario
                best_scenario = None
                best_financial = None
                best_score = -1
                
                for scenario in scenarios:
                    financial = self._analyze_financials(property, scenario)
                    
                    # Only consider if meets ROI threshold
                    if financial.roi_percentage >= preferences.min_roi_threshold:
                        score = self._calculate_weighted_score(financial, scenario, preferences)
                        
                        if score > best_score:
                            best_score = score
                            best_scenario = scenario
                            best_financial = financial
                
                if best_scenario:
                    analyzed_properties.append({
                        'property': property,
                        'scenario': best_scenario,
                        'financial': best_financial,
                        'score': best_score,
                        'source': prop_data.get('source', 'Unknown')
                    })
                    
            except Exception as e:
                print(f"❌ Error analyzing property: {e}")
                continue
        
        # Sort by score
        analyzed_properties.sort(key=lambda x: x['score'], reverse=True)
        
        # Create detailed report
        report = self._create_report(analyzed_properties, preferences)
        
        return {
            'status': 'success',
            'summary': {
                'total_scraped': len(properties),
                'total_analyzed': len(analyzed_properties),
                'meeting_roi_threshold': len([p for p in analyzed_properties if p['financial'].roi_percentage >= preferences.min_roi_threshold]),
                'average_roi': sum(p['financial'].roi_percentage for p in analyzed_properties) / len(analyzed_properties) if analyzed_properties else 0
            },
            'top_opportunities': self._format_opportunities(analyzed_properties[:10]),
            'detailed_report': report,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_scenarios(self, property: PropertyListing) -> List[DevelopmentScenario]:
        """Generate possible development scenarios based on zoning"""
        
        scenarios = []
        
        # Edmonton/Alberta zoning categories
        if property.zoning in ['R1', 'RF1', 'RSL']:
            # Single family residential
            scenarios.append(DevelopmentScenario(
                scenario_name="Single Family Homes",
                total_units=int(property.lot_size_sqft / 6000),  # 6000 sqft per lot
                construction_cost=property.lot_size_sqft * 0.6 * 150,  # 60% coverage, $150/sqft
                timeline_months=18,
                projected_revenue=int(property.lot_size_sqft / 6000) * 650000  # $650k per home
            ))
            
        elif property.zoning in ['R2', 'RF3', 'RF4']:
            # Duplex/Row housing
            units = int(property.lot_size_sqft / 2500)
            scenarios.append(DevelopmentScenario(
                scenario_name="Townhouse Development",
                total_units=units,
                construction_cost=property.lot_size_sqft * 0.7 * 125,
                timeline_months=24,
                projected_revenue=units * 450000
            ))
            
        elif property.zoning in ['R3', 'RA7', 'RA8', 'RA9']:
            # Low/Medium rise apartment
            units = int(property.lot_size_sqft / 1000)
            scenarios.append(DevelopmentScenario(
                scenario_name="Low-Rise Apartment",
                total_units=units,
                construction_cost=property.lot_size_sqft * 1.5 * 175,
                timeline_months=30,
                projected_revenue=units * 350000
            ))
            
        elif property.zoning in ['C1', 'C2', 'CB1', 'CB2']:
            # Commercial/Mixed use
            scenarios.append(DevelopmentScenario(
                scenario_name="Mixed-Use Development",
                total_units=int(property.lot_size_sqft / 800),
                construction_cost=property.lot_size_sqft * 2.0 * 200,
                timeline_months=36,
                projected_revenue=property.lot_size_sqft * 2.0 * 400
            ))
            
        else:
            # Generic development for unknown zoning
            scenarios.append(DevelopmentScenario(
                scenario_name="Generic Development",
                total_units=int(property.lot_size_sqft / 3000),
                construction_cost=property.lot_size_sqft * 0.5 * 150,
                timeline_months=24,
                projected_revenue=property.lot_size_sqft * 0.5 * 300
            ))
            
        return scenarios
    
    def _analyze_financials(self, property: PropertyListing, scenario: DevelopmentScenario) -> FinancialAnalysis:
        """Calculate financial metrics"""
        
        # Acquisition cost (property price + closing costs)
        acquisition_cost = property.price * 1.02
        
        # Soft costs (permits, design, etc) - 15% of construction
        soft_costs = scenario.construction_cost * 0.15
        
        # Total investment
        total_investment = acquisition_cost + scenario.construction_cost + soft_costs
        
        # Calculate profit and ROI
        net_profit = scenario.projected_revenue - total_investment
        roi = (net_profit / total_investment) * 100 if total_investment > 0 else 0
        
        # Simple payback calculation
        monthly_revenue = scenario.projected_revenue / 12  # Assume sold over 1 year
        payback_months = int(total_investment / monthly_revenue) if monthly_revenue > 0 else 999
        
        return FinancialAnalysis(
            total_investment=total_investment,
            projected_revenue=scenario.projected_revenue,
            net_profit=net_profit,
            roi_percentage=roi,
            payback_months=payback_months
        )
    
    def _calculate_weighted_score(self, financial: FinancialAnalysis, scenario: DevelopmentScenario, 
                                preferences: DeveloperPreferences) -> float:
        """Calculate score based on developer preferences"""
        
        # ROI Score (0-1)
        roi_score = min(financial.roi_percentage / 100, 1.0)
        
        # Timeline Score (faster is better)
        timeline_score = max(0, 1 - (scenario.timeline_months / preferences.max_development_timeline_months))
        
        # Investment Size Score (based on available capital)
        # Assume preference for projects under $5M
        investment_score = max(0, 1 - (financial.total_investment / 5000000))
        
        # Risk-adjusted weighting
        if preferences.risk_tolerance > 0.7:
            # High risk tolerance - prioritize ROI
            weights = {'roi': 0.6, 'timeline': 0.2, 'investment': 0.2}
        elif preferences.risk_tolerance > 0.4:
            # Medium risk tolerance - balanced
            weights = {'roi': 0.4, 'timeline': 0.3, 'investment': 0.3}
        else:
            # Low risk tolerance - prioritize smaller, faster projects
            weights = {'roi': 0.3, 'timeline': 0.4, 'investment': 0.3}
            
        return (
            roi_score * weights['roi'] +
            timeline_score * weights['timeline'] +
            investment_score * weights['investment']
        )
    
    def _format_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Format opportunities for output"""
        
        formatted = []
        for i, opp in enumerate(opportunities):
            formatted.append({
                'rank': i + 1,
                'address': opp['property'].address,
                'source': opp['source'],
                'price': f"${opp['property'].price:,.0f}",
                'lot_size': f"{opp['property'].lot_size_sqft:,.0f} sqft ({opp['property'].lot_size_sqft/43560:.2f} acres)",
                'zoning': opp['property'].zoning,
                'development_type': opp['scenario'].scenario_name,
                'units': opp['scenario'].total_units,
                'roi': f"{opp['financial'].roi_percentage:.1f}%",
                'total_investment': f"${opp['financial'].total_investment:,.0f}",
                'net_profit': f"${opp['financial'].net_profit:,.0f}",
                'timeline': f"{opp['scenario'].timeline_months} months",
                'score': f"{opp['score']:.3f}",
                'listing_url': opp['property'].listing_url
            })
            
        return formatted
    
    def _create_report(self, opportunities: List[Dict], preferences: DeveloperPreferences) -> str:
        """Create detailed analysis report"""
        
        if not opportunities:
            return "No viable opportunities found matching criteria."
            
        report = f"""
# Real Estate Development Opportunity Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Search Parameters
- Risk Tolerance: {preferences.risk_tolerance} ({"High" if preferences.risk_tolerance > 0.7 else "Medium" if preferences.risk_tolerance > 0.4 else "Low"})
- Minimum ROI Threshold: {preferences.min_roi_threshold}%
- Maximum Timeline: {preferences.max_development_timeline_months} months
- Preferred Types: {', '.join(preferences.preferred_property_types)}

## Executive Summary
- Properties Analyzed: {len(opportunities)}
- Average ROI: {sum(o['financial'].roi_percentage for o in opportunities) / len(opportunities):.1f}%
- Total Investment Required (Top 5): ${sum(o['financial'].total_investment for o in opportunities[:5]):,.0f}
- Projected Profit (Top 5): ${sum(o['financial'].net_profit for o in opportunities[:5]):,.0f}

## Top 5 Development Opportunities

"""
        
        for i, opp in enumerate(opportunities[:5]):
            report += f"""
### {i+1}. {opp['property'].address}
**Source:** {opp['source']} | **Zoning:** {opp['property'].zoning}

**Property Details:**
- Purchase Price: ${opp['property'].price:,.0f}
- Lot Size: {opp['property'].lot_size_sqft:,.0f} sqft ({opp['property'].lot_size_sqft/43560:.2f} acres)

**Development Plan:** {opp['scenario'].scenario_name}
- Total Units: {opp['scenario'].total_units}
- Construction Timeline: {opp['scenario'].timeline_months} months
- Construction Cost: ${opp['scenario'].construction_cost:,.0f}

**Financial Analysis:**
- Total Investment: ${opp['financial'].total_investment:,.0f}
- Projected Revenue: ${opp['financial'].projected_revenue:,.0f}
- Net Profit: ${opp['financial'].net_profit:,.0f}
- ROI: {opp['financial'].roi_percentage:.1f}%
- Payback Period: {opp['financial'].payback_months} months

**Investment Score:** {opp['score']:.3f}/1.000

---
"""
        
        return report

# Main analysis function
async def analyze_real_properties(search_criteria: Dict, developer_preferences: Dict) -> Dict:
    """Main entry point for real property analysis"""
    
    # Create preferences object
    prefs = DeveloperPreferences(**developer_preferences)
    
    # Create analyzer
    analyzer = RealEstateAnalyzer()
    
    # Run analysis
    results = await analyzer.analyze_market(search_criteria, prefs)
    
    return results

# Test function
if __name__ == "__main__":
    async def test():
        search = {
            'city': 'Edmonton',
            'province': 'AB',
            'min_price': 200000,
            'max_price': 2000000
        }
        
        prefs = {
            'risk_tolerance': 0.6,
            'preferred_property_types': ['commercial', 'residential'],
            'min_roi_threshold': 15.0,
            'max_development_timeline_months': 36,
            'financing_preference': 'mixed',
            'location_preferences': {'Edmonton': 1.0}
        }
        
        results = await analyze_real_properties(search, prefs)
        print("\nAnalysis complete!")
        
    asyncio.run(test())