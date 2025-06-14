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

app = FastAPI(title="Sgiach Real Estate Analysis API", version="1.0.0")

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
        "message": "Sgiach API is running!",
        "status": "online",
        "version": "1.0.0",
        "description": "Your Winged View of Development - Real Estate Analysis Platform",
        "endpoints": {
            "health": "/health",
            "quick_analysis": "/quick-analysis", 
            "upload_properties": "/upload-properties",
            "analyze_property": "/analyze-property/{property_id}",
            "list_properties": "/properties",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "properties_loaded": len(property_database),
        "api_version": "1.0.0"
    }

@app.post("/upload-properties")
async def upload_properties(file: UploadFile = File(...)):
    """Upload CSV file with real property data"""
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read CSV content
        content = await file.read()
        csv_string = content.decode('utf-8')
        
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(csv_string))
        new_properties = []
        
        for row in csv_reader:
            property_data = {
                "id": row.get('MLS_Number', f"PROP_{len(property_database) + len(new_properties)}"),
                "address": row.get('Address', 'Unknown Address'),
                "city": row.get('City', 'Unknown City'),
                "province": row.get('Province', 'AB'),
                "price": float(row.get('Price', 0)),
                "property_type": row.get('Property_Type', 'Unknown'),
                "land_size_sqft": row.get('Land_Size_SqFt', ''),
                "zoning": row.get('Zoning', 'Unknown'),
                "features": row.get('Features', ''),
                "time_on_market": int(row.get('Time_on_Market', 0)),
                "listing_agent": row.get('Listing_Agent', 'Unknown'),
                "brokerage": row.get('Brokerage', 'Unknown'),
                "uploaded_at": datetime.now().isoformat()
            }
            new_properties.append(property_data)
        
        # Add to database
        property_database.extend(new_properties)
        
        return {
            "message": f"Successfully uploaded {len(new_properties)} properties",
            "properties_added": len(new_properties),
            "total_properties": len(property_database),
            "uploaded_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/properties")
async def list_properties():
    """List all uploaded properties"""
    return {
        "total_properties": len(property_database),
        "properties": property_database,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/analyze-property/{property_id}")
async def analyze_property(property_id: str):
    """Analyze a specific uploaded property"""
    # Find property in database
    property_data = None
    for prop in property_database:
        if prop["id"] == property_id:
            property_data = prop
            break
    
    if not property_data:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Run development analysis
    analysis = run_development_analysis(property_data)
    
    return {
        "property_id": property_id,
        "property_data": property_data,
        "analysis": analysis,
        "analyzed_at": datetime.now().isoformat()
    }

def run_development_analysis(property_data):
    """Run development analysis on a real property"""
    price = property_data["price"]
    zoning = property_data["zoning"]
    property_type = property_data["property_type"]
    
    # Determine development potential based on zoning
    scenarios = []
    
    if "Agricultural" in zoning or "Agricultural" in property_type:
        # Agricultural to residential subdivision
        scenarios.append({
            "scenario": "Residential Subdivision",
            "description": "Convert agricultural land to residential lots",
            "development_cost": price * 0.4,  # 40% of land cost for development
            "potential_value": price * 2.2,   # 2.2x multiple for subdivision
            "timeline_months": 36,
            "roi_percent": 75.0,
            "risk_level": "Medium"
        })
    
    if "Commercial" in zoning or "Commercial" in property_type:
        # Commercial development
        scenarios.append({
            "scenario": "Commercial Development", 
            "description": "Develop commercial/retail space",
            "development_cost": price * 0.6,
            "potential_value": price * 1.8,
            "timeline_months": 24,
            "roi_percent": 45.0,
            "risk_level": "Low"
        })
    
    if "Industrial" in zoning or "Industrial" in property_type:
        # Industrial development
        scenarios.append({
            "scenario": "Industrial Complex",
            "description": "Develop industrial/warehouse facilities", 
            "development_cost": price * 0.5,
            "potential_value": price * 2.0,
            "timeline_months": 30,
            "roi_percent": 60.0,
            "risk_level": "Medium"
        })
    
    # If no specific scenarios, create general development
    if not scenarios:
        scenarios.append({
            "scenario": "General Development",
            "description": "Development potential based on location",
            "development_cost": price * 0.3,
            "potential_value": price * 1.5,
            "timeline_months": 24,
            "roi_percent": 25.0,
            "risk_level": "Medium"
        })
    
    # Calculate financial metrics for best scenario
    best_scenario = max(scenarios, key=lambda x: x["roi_percent"])
    
    return {
        "scenarios": scenarios,
        "recommended_scenario": best_scenario,
        "financial_summary": {
            "current_value": price,
            "total_investment": price + best_scenario["development_cost"],
            "projected_value": best_scenario["potential_value"],
            "net_profit": best_scenario["potential_value"] - (price + best_scenario["development_cost"]),
            "roi_percentage": best_scenario["roi_percent"],
            "payback_period_months": best_scenario["timeline_months"]
        },
        "location_factors": {
            "city": property_data["city"],
            "province": property_data["province"], 
            "zoning": property_data["zoning"],
            "time_on_market": property_data["time_on_market"]
        }
    }

@app.get("/quick-analysis")
async def quick_analysis():
    """Quick analysis endpoint - now uses real data if available"""
    if property_database:
        # Use real uploaded properties
        sample_properties = random.sample(property_database, min(5, len(property_database)))
        analyzed_properties = []
        
        for prop in sample_properties:
            analysis = run_development_analysis(prop)
            analyzed_properties.append({
                "property": prop,
                "analysis": analysis["financial_summary"],
                "recommended_scenario": analysis["recommended_scenario"]["scenario"]
            })
        
        return {
            "message": "Real Estate Development Analysis - Real Alberta Properties",
            "data_source": "Uploaded Real Properties", 
            "total_properties_analyzed": len(analyzed_properties),
            "opportunities": analyzed_properties,
            "generated_at": datetime.now().isoformat()
        }
    else:
        # Fallback to sample data if no properties uploaded
        return await quick_analysis_sample_data()

async def quick_analysis_sample_data():
    """Fallback sample data for testing"""
    sample_properties = [
        {
            "address": "4201 Main St",
            "city": "Edmonton", 
            "price": 631000,
            "roi_percentage": 15.7,
            "investment_required": 947000,
            "projected_profit": 149000,
            "development_type": "Residential",
            "zoning": "RA7"
        },
        {
            "address": "2477 Main St", 
            "city": "Edmonton",
            "price": 845000,
            "roi_percentage": 34.4,
            "investment_required": 1470000,
            "projected_profit": 413000,
            "development_type": "Commercial",
            "zoning": "CB1"
        }
    ]
    
    return {
        "message": "Real Estate Development Analysis - Sample Data",
        "data_source": "Sample/Test Data",
        "note": "Upload real property CSV for actual analysis",
        "opportunities": sample_properties,
        "generated_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
