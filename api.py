from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import random
import os
from io import StringIO
import csv

app = FastAPI(
    title="Sgiach Real Estate Analysis API", 
    version="1.0.0",
    description="Your Winged View of Development"
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
        "api_endpoints": {
            "health": "/health",
            "analysis": "/quick-analysis", 
            "upload": "/upload-properties",
            "properties": "/properties"
        },
        "contact": "jeff@skyebridgedevelopments.ca"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "✅ HEALTHY",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "properties_loaded": len(property_database)
    }

@app.post("/upload-properties")
async def upload_properties(file: UploadFile):
    """Upload CSV file with Alberta property data"""
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=422, detail="No file provided")
            
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")
        
        content = await file.read()
        csv_string = content.decode('utf-8')
        
        # Clear existing data
        property_database.clear()
        
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(csv_string))
        new_properties = []
        
        for row in csv_reader:
            # Extract price safely
            price_text = row.get('Price', '0')
            try:
                # Remove dollar signs, commas, spaces
                clean_price = str(price_text).replace('$', '').replace(',', '').replace(' ', '').strip()
                price = float(clean_price) if clean_price else 0
            except:
                price = 0
            
            # Extract time on market safely  
            time_text = row.get('Time_on_Market', '0')
            try:
                time_on_market = int(float(str(time_text).strip())) if time_text else 0
            except:
                time_on_market = 0
                
            property_data = {
                "id": row.get('MLS_Number', f"PROP_{len(new_properties)}"),
                "address": row.get('Address', 'Unknown Address'),
                "city": row.get('City', 'Unknown City'), 
                "province": row.get('Province', 'AB'),
                "price": price,
                "property_type": row.get('Property_Type', 'Unknown'),
                "land_size_sqft": row.get('Land_Size_SqFt', ''),
                "zoning": row.get('Zoning', 'Unknown'),
                "features": row.get('Features', ''),
                "time_on_market": time_on_market,
                "listing_agent": row.get('Listing_Agent', 'Unknown'),
                "brokerage": row.get('Brokerage', 'Unknown'),
                "uploaded_at": datetime.now().isoformat()
            }
            new_properties.append(property_data)
        
        property_database.extend(new_properties)
        
        return {
            "🎉 SUCCESS": f"Uploaded {len(new_properties)} Alberta properties",
            "total_properties": len(property_database),
            "sample_data": [
                {
                    "id": prop["id"],
                    "address": prop["address"], 
                    "city": prop["city"],
                    "price": f"${prop['price']:,.0f}"
                } for prop in new_properties[:3]
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/quick-analysis")
async def quick_analysis():
    """Real estate development analysis"""
    if not property_database:
        return {
            "🦅 SGIACH ANALYSIS": "No properties loaded",
            "message": "Upload Alberta property data first"
        }
    
    # Use real properties
    sample_size = min(5, len(property_database))
    sample_properties = random.sample(property_database, sample_size)
    analyzed_opportunities = []
    
    for prop in sample_properties:
        analysis = analyze_property_simple(prop)
        analyzed_opportunities.append({
            "🏠 PROPERTY": {
                "id": prop["id"],
                "address": prop["address"],
                "city": prop["city"],
                "price": f"${prop['price']:,.0f}",
                "type": prop["property_type"],
                "zoning": prop["zoning"]
            },
            "💰 ANALYSIS": {
                "roi": f"{analysis['roi']:.1f}%",
                "profit": f"${analysis['profit']:,.0f}",
                "investment": f"${analysis['investment']:,.0f}",
                "grade": analysis['grade']
            },
            "⭐ SCENARIO": analysis['scenario']
        })
    
    # Sort by ROI
    analyzed_opportunities.sort(key=lambda x: float(x["💰 ANALYSIS"]["roi"].rstrip('%')), reverse=True)
    
    return {
        "🦅 SGIACH DEVELOPMENT ANALYSIS": {
            "platform": "Your Winged View of Development",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "✅ Real Alberta Properties",
            "analyzed": len(analyzed_opportunities)
        },
        "📊 MARKET": {
            "total_properties": len(property_database),
            "focus": "Edmonton Metropolitan Area"
        },
        "🏆 OPPORTUNITIES": analyzed_opportunities,
        "🤝 CONTACT": {
            "company": "SkyeBridge Consulting & Developments",
            "email": "jeff@skyebridgedevelopments.ca",
            "phone": "780.218.1178"
        }
    }

def analyze_property_simple(prop):
    """Simple property analysis"""
    price = prop["price"]
    prop_type = prop["property_type"]
    zoning = prop["zoning"]
    
    # Determine scenario based on type/zoning
    if "Agricultural" in prop_type or "Agricultural" in zoning:
        scenario = "🏘️ Residential Subdivision"
        roi = 75.0
        multiplier = 2.2
        dev_cost_ratio = 0.4
    elif "Commercial" in prop_type or "Commercial" in zoning:
        scenario = "🏢 Commercial Development"
        roi = 45.0
        multiplier = 1.8
        dev_cost_ratio = 0.6
    elif "Industrial" in prop_type or "Industrial" in zoning:
        scenario = "🏭 Industrial Complex"
        roi = 60.0
        multiplier = 2.0
        dev_cost_ratio = 0.5
    else:
        scenario = "🔄 General Development"
        roi = 25.0
        multiplier = 1.5
        dev_cost_ratio = 0.3
    
    # Calculate financials
    dev_cost = price * dev_cost_ratio
    total_investment = price + dev_cost
    projected_value = price * multiplier
    profit = projected_value - total_investment
    
    # Investment grade
    if roi >= 50:
        grade = "🌟 EXCELLENT (A+)"
    elif roi >= 30:
        grade = "⭐ VERY GOOD (A)"
    elif roi >= 20:
        grade = "✅ GOOD (B+)"
    else:
        grade = "🔶 FAIR (B)"
    
    return {
        "scenario": scenario,
        "roi": roi,
        "investment": total_investment,
        "profit": profit,
        "grade": grade
    }

@app.get("/properties")
async def list_properties():
    """List all properties"""
    return {
        "total_properties": len(property_database),
        "properties": property_database[:10] if len(property_database) > 10 else property_database
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
