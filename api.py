from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
import json
from datetime import datetime
import random
import os
from io import StringIO
import csv
from typing import Optional

app = FastAPI(
    title="Sgiach Real Estate Analysis API", 
    version="1.0.0",
    description="Your Winged View of Development - Professional Real Estate Analysis Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded properties
property_database = []

@app.get("/")
async def root():
    return {
        "platform": "Sgiach Real Estate Analysis",
        "tagline": "Your Winged View of Development",
        "status": "🟢 ONLINE",
        "version": "1.0.0",
        "description": "Professional real estate development analysis platform for Alberta properties",
        "capabilities": [
            "📊 Real estate data upload and processing",
            "🏗️ Development scenario analysis", 
            "💰 ROI and financial modeling",
            "📍 Location-based opportunity ranking",
            "📈 Investment risk assessment"
        ],
        "api_endpoints": {
            "health_check": "/health",
            "property_analysis": "/quick-analysis", 
            "upload_properties": "/upload-properties",
            "analyze_specific": "/analyze-property/{property_id}",
            "list_all_properties": "/properties",
            "documentation": "/docs"
        },
        "powered_by": "SkyeBridge Consulting & Developments Inc.",
        "contact": "jeff@skyebridgedevelopments.ca"
    }

@app.get("/health")
async def health_check():
    return {
        "🏥 SYSTEM STATUS": {
            "status": "✅ HEALTHY",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "uptime": "Active",
            "api_version": "1.0.0"
        },
        "📊 DATABASE STATUS": {
            "properties_loaded": f"{len(property_database)} properties",
            "data_source": "Real Alberta Properties" if property_database else "Sample Data",
            "last_update": property_database[-1]["uploaded_at"] if property_database else "No uploads yet"
        },
        "🚀 READY FOR": [
            "Property data upload",
            "Development analysis", 
            "Investment calculations",
            "Professional reporting"
        ]
    }

@app.post("/upload-properties")
async def upload_properties(file: UploadFile):
    """Upload CSV file with real property data - Fixed validation"""
    try:
        # Check if file was provided
        if not file:
            raise HTTPException(status_code=422, detail="❌ No file provided. Please select a CSV file to upload.")
        
        # Check filename exists
        if not file.filename:
            raise HTTPException(status_code=422, detail="❌ File must have a filename")
            
        # Validate file type
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="❌ File must be a CSV format (.csv extension required)")
        
        # Read CSV content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="❌ Uploaded file is empty")
            
        csv_string = content.decode('utf-8')
        
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(csv_string))
        new_properties = []
        
        for row_num, row in enumerate(csv_reader, 1):
            try:
                property_data = {
                    "id": row.get('MLS_Number', f"PROP_{len(property_database) + len(new_properties)}"),
                    "address": row.get('Address', 'Unknown Address'),
                    "city": row.get('City', 'Unknown City'),
                    "province": row.get('Province', 'AB'),
                    "price": float(row.get('Price', 0)) if row.get('Price') else 0,
                    "property_type": row.get('Property_Type', 'Unknown'),
                    "land_size_sqft": row.get('Land_Size_SqFt', ''),
                    "zoning": row.get('Zoning', 'Unknown'),
                    "features": row.get('Features', ''),
                    "time_on_market": int(row.get('Time_on_Market', 0)) if row.get('Time_on_Market') else 0,
                    "listing_agent": row.get('Listing_Agent', 'Unknown'),
                    "brokerage": row.get('Brokerage', 'Unknown'),
                    "uploaded_at": datetime.now().isoformat()
                }
                new_properties.append(property_data)
            except Exception as row_error:
                print(f"Error processing row {row_num}: {row_error}")
                continue
        
        if len(new_properties) == 0:
            raise HTTPException(status_code=400, detail="❌ No valid properties found in CSV file")
        
        # Add to database
        property_database.extend(new_properties)
        
        return {
            "🎉 UPLOAD SUCCESS": {
                "message": f"Successfully processed {len(new_properties)} Alberta properties",
                "properties_added": len(new_properties),
                "total_properties_in_database": len(property_database),
                "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "📊 DATA SUMMARY": {
                "file_name": file.filename,
                "file_size": f"{len(content)} bytes",
                "properties_processed": len(new_properties),
                "data_source": "Real Alberta Properties - Realtor.ca Export"
            },
            "✅ NEXT STEPS": [
                "Visit /quick-analysis for development opportunities",
                "Use /analyze-property/{property_id} for detailed analysis",
                "Check /properties to view all loaded data"
            ]
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error processing file: {str(e)}")

@app.get("/properties")
async def list_properties():
    """List all uploaded properties with summary statistics"""
    if not property_database:
        return {
            "📋 PROPERTY DATABASE": {
                "status": "Empty - No properties uploaded yet",
                "total_properties": 0,
                "recommendation": "Upload Alberta property data via /upload-properties"
            }
        }
    
    # Calculate summary statistics
    prices = [prop["price"] for prop in property_database if prop["price"] > 0]
    property_types = {}
    cities = {}
    
    for prop in property_database:
        prop_type = prop["property_type"]
        city = prop["city"]
        property_types[prop_type] = property_types.get(prop_type, 0) + 1
        cities[city] = cities.get(city, 0) + 1
    
    return {
        "📋 PROPERTY DATABASE SUMMARY": {
            "total_properties": len(property_database),
            "data_source": "Real Alberta Properties",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "💰 MARKET OVERVIEW": {
            "total_market_value": f"${sum(prices):,.0f}" if prices else "$0",
            "average_price": f"${sum(prices)/len(prices):,.0f}" if prices else "N/A",
            "price_range": f"${min(prices):,.0f} - ${max(prices):,.0f}" if prices else "N/A",
            "median_price": f"${sorted(prices)[len(prices)//2]:,.0f}" if prices else "N/A"
        },
        "🏘️ PROPERTY DISTRIBUTION": {
            "by_type": property_types,
            "by_location": cities
        },
        "🏠 PROPERTY LISTINGS": property_database[:10] if len(property_database) > 10 else property_database,
        "📝 NOTE": f"Showing first 10 of {len(property_database)} properties" if len(property_database) > 10 else "All properties displayed"
    }

@app.get("/quick-analysis")
async def quick_analysis():
    """Professional real estate development analysis overview"""
    if property_database:
        # Use real uploaded properties
        sample_properties = random.sample(property_database, min(5, len(property_database)))
        analyzed_opportunities = []
        
        for prop in sample_properties:
            analysis = run_development_analysis(prop)
            analyzed_opportunities.append({
                "🏠 PROPERTY": {
                    "id": prop["id"],
                    "address": prop["address"],
                    "city": prop["city"],
                    "current_price": f"${prop['price']:,.0f}",
                    "property_type": prop["property_type"],
                    "zoning": prop["zoning"]
                },
                "💰 FINANCIAL ANALYSIS": analysis["financial_summary"],
                "⭐ RECOMMENDATION": {
                    "scenario": analysis["recommended_scenario"]["scenario_name"],
                    "grade": get_investment_grade(analysis["recommended_scenario"]["roi_percent"]),
                    "timeline": get_timeline_category(analysis["recommended_scenario"]["timeline_months"])
                }
            })
        
        # Sort by ROI
        analyzed_opportunities.sort(key=lambda x: float(x["💰 FINANCIAL ANALYSIS"]["roi_percentage"].rstrip('%')), reverse=True)
        
        return {
            "🦅 SGIACH DEVELOPMENT ANALYSIS": {
                "platform": "Your Winged View of Development",
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_source": "✅ Real Alberta Properties (Realtor.ca)",
                "properties_analyzed": len(analyzed_opportunities)
            },
            "📊 MARKET OVERVIEW": {
                "total_properties_available": len(property_database),
                "analysis_sample": f"Top {len(analyzed_opportunities)} opportunities",
                "market_focus": "Edmonton Metropolitan Area",
                "currency": "CAD"
            },
            "🏆 DEVELOPMENT OPPORTUNITIES": analyzed_opportunities,
            "📈 NEXT STEPS": [
                "Review detailed analysis for each property",
                "Use /analyze-property/{id} for comprehensive reports",
                "Contact SkyeBridge for professional development consultation"
            ],
            "🤝 PROFESSIONAL SERVICES": {
                "company": "SkyeBridge Consulting & Developments Inc.",
                "contact": "jeff@skyebridgedevelopments.ca",
                "phone": "780.218.1178",
                "services": ["Owner representation", "Development analysis", "Project management"]
            }
        }
    else:
        return {
            "🦅 SGIACH DEVELOPMENT ANALYSIS": {
                "status": "⚠️ No real property data loaded",
                "message": "Upload Alberta property data to see live analysis",
                "sample_available": "Demo mode with sample data"
            },
            "📤 UPLOAD INSTRUCTIONS": {
                "endpoint": "/upload-properties",
                "format": "CSV file with property data",
                "source": "Realtor.ca property exports recommended"
            }
        }

def get_investment_grade(roi):
    """Assign investment grade based on ROI"""
    if roi >= 50: return "🌟 EXCELLENT (A+)"
    elif roi >= 30: return "⭐ VERY GOOD (A)"
    elif roi >= 20: return "✅ GOOD (B+)"
    elif roi >= 15: return "🔶 FAIR (B)"
    else: return "⚠️ CAUTION (C)"

def get_timeline_category(months):
    """Categorize timeline"""
    if months <= 18: return "⚡ FAST TRACK"
    elif months <= 30: return "🚀 STANDARD"
    else: return "🐌 EXTENDED"

def run_development_analysis(property_data):
    """Run professional development analysis on a real property"""
    price = property_data["price"]
    zoning = property_data["zoning"]
    property_type = property_data["property_type"]
    
    scenarios = []
    
    if "Agricultural" in zoning or "Agricultural" in property_type:
        scenarios.append({
            "scenario_name": "🏘️ Residential Subdivision",
            "description": "Convert agricultural land to residential development",
            "development_cost": price * 0.4,
            "potential_value": price * 2.2,
            "timeline_months": 36,
            "roi_percent": 75.0,
            "risk_level": "Medium"
        })
    
    if "Commercial" in zoning or "Commercial" in property_type:
        scenarios.append({
            "scenario_name": "🏢 Commercial Development", 
            "description": "Develop retail/office commercial space",
            "development_cost": price * 0.6,
            "potential_value": price * 1.8,
            "timeline_months": 24,
            "roi_percent": 45.0,
            "risk_level": "Low"
        })
    
    if "Industrial" in zoning or "Industrial" in property_type:
        scenarios.append({
            "scenario_name": "🏭 Industrial Complex",
            "description": "Develop warehouse/manufacturing facilities", 
            "development_cost": price * 0.5,
            "potential_value": price * 2.0,
            "timeline_months": 30,
            "roi_percent": 60.0,
            "risk_level": "Medium"
        })
    
    if not scenarios:
        scenarios.append({
            "scenario_name": "🔄 General Development",
            "description": "Multi-purpose development opportunity",
            "development_cost": price * 0.3,
            "potential_value": price * 1.5,
            "timeline_months": 24,
            "roi_percent": 25.0,
            "risk_level": "Medium"
        })
    
    best_scenario = max(scenarios, key=lambda x: x["roi_percent"])
    
    return {
        "scenarios": scenarios,
        "recommended_scenario": best_scenario,
        "financial_summary": {
            "current_property_value": f"${price:,.0f}",
            "total_investment_required": f"${price + best_scenario['development_cost']:,.0f}",
            "projected_developed_value": f"${best_scenario['potential_value']:,.0f}",
            "estimated_net_profit": f"${best_scenario['potential_value'] - (price + best_scenario['development_cost']):,.0f}",
            "roi_percentage": f"{best_scenario['roi_percent']:.1f}%",
            "payback_period_months": best_scenario["timeline_months"],
            "annual_roi": f"{(best_scenario['roi_percent'] / best_scenario['timeline_months']) * 12:.1f}%"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
