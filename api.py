from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

property_database = []

@app.get("/")
async def root():
    return {
        "platform": "Sgiach Real Estate Analysis",
        "tagline": "Your Winged View of Development",
        "status": "ONLINE",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "properties_loaded": len(property_database)
    }

@app.post("/upload-properties")
async def upload_properties(file: UploadFile):
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=422, detail="No file provided")
            
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV")
        
        content = await file.read()
        csv_string = content.decode('utf-8')
        
        property_database.clear()
        csv_reader = csv.DictReader(StringIO(csv_string))
        new_properties = []
        
        for row in csv_reader:
            price_text = row.get('Price') or '0'
            try:
                clean_price = str(price_text).replace('$', '').replace(',', '').strip()
                price = float(clean_price) if clean_price else 0
            except:
                price = 0
            
            time_text = row.get('Time_on_Market') or '0'
            try:
                time_on_market = int(float(str(time_text).strip())) if time_text else 0
            except:
                time_on_market = 0
                
            property_data = {
                "id": row.get('MLS_Number') or f"PROP_{len(new_properties)}",
                "address": row.get('Address') or 'Unknown Address',
                "city": row.get('City') or 'Unknown City',
                "province": row.get('Province') or 'AB',
                "price": price,
                "property_type": row.get('Property_Type') or 'Unknown',
                "zoning": row.get('Zoning') or 'Unknown',
                "features": row.get('Features') or '',
                "time_on_market": time_on_market,
                "listing_agent": row.get('Listing_Agent') or 'Unknown',
                "brokerage": row.get('Brokerage') or 'Unknown',
                "uploaded_at": datetime.now().isoformat()
            }
            new_properties.append(property_data)
        
        property_database.extend(new_properties)
        
        return {
            "SUCCESS": f"Uploaded {len(new_properties)} properties",
            "total_properties": len(property_database),
            "first_property": {
                "id": new_properties[0]["id"] if new_properties else "None",
                "address": new_properties[0]["address"] if new_properties else "None",
                "price": new_properties[0]["price"] if new_properties else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/quick-analysis")
async def quick_analysis():
    if not property_database:
        return {"message": "No properties loaded"}
    
    sample_size = min(5, len(property_database))
    sample_properties = random.sample(property_database, sample_size)
    results = []
    
    for prop in sample_properties:
        price = prop["price"]
        
        if "Agricultural" in prop["property_type"]:
            roi = 75.0
            scenario = "Residential Subdivision"
        elif "Commercial" in prop["property_type"]:
            roi = 45.0
            scenario = "Commercial Development"
        elif "Industrial" in prop["property_type"]:
            roi = 60.0
            scenario = "Industrial Complex"
        else:
            roi = 25.0
            scenario = "General Development"
        
        profit = price * (roi / 100)
        investment = price + (price * 0.4)
        
        results.append({
            "PROPERTY": {
                "id": prop["id"],
                "address": prop["address"],
                "city": prop["city"],
                "price": f"${price:,.0f}",
                "type": prop["property_type"]
            },
            "ANALYSIS": {
                "roi": f"{roi}%",
                "profit": f"${profit:,.0f}",
                "investment": f"${investment:,.0f}",
                "scenario": scenario
            }
        })
    
    return {
        "SGIACH_ANALYSIS": {
            "platform": "Your Winged View of Development",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analyzed": len(results)
        },
        "OPPORTUNITIES": results
    }

@app.get("/properties")
async def list_properties():
    return {
        "total": len(property_database),
        "properties": property_database[:5]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
