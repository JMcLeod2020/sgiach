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
        
        # Expected headers: MLS_Number,Address,City,Province,Price,Property_Type,Land_Size_SqFt,Zoning,Features,Time_on_Market,Listing_Agent,Brokerage
        
        for row in csv_reader:
            # Use EXACTLY the headers you specified
            mls_number = row['MLS_Number'] if 'MLS_Number' in row else f"PROP_{len(new_properties)}"
            address = row['Address'] if 'Address' in row else 'No Address'
            city = row['City'] if 'City' in row else 'No City'
            province = row['Province'] if 'Province' in row else 'AB'
            
            # Handle Price
            price_text = row['Price'] if 'Price' in row else '0'
            try:
                price = float(str(price_text).replace(',', '').strip())
            except:
                price = 0
            
            property_type = row['Property_Type'] if 'Property_Type' in row else 'Unknown Type'
            land_size = row['Land_Size_SqFt'] if 'Land_Size_SqFt' in row else ''
            zoning = row['Zoning'] if 'Zoning' in row else 'Unknown Zoning'
            features = row['Features'] if 'Features' in row else ''
            
            # Handle Time_on_Market
            time_text = row['Time_on_Market'] if 'Time_on_Market' in row else '0'
            try:
                time_on_market = int(float(str(time_text).strip()))
            except:
                time_on_market = 0
            
            listing_agent = row['Listing_Agent'] if 'Listing_Agent' in row else 'Unknown Agent'
            brokerage = row['Brokerage'] if 'Brokerage' in row else 'Unknown Brokerage'
                
            property_data = {
                "id": mls_number,
                "address": address,
                "city": city,
                "province": province,
                "price": price,
                "property_type": property_type,
                "land_size_sqft": land_size,
                "zoning": zoning,
                "features": features,
                "time_on_market": time_on_market,
                "listing_agent": listing_agent,
                "brokerage": brokerage,
                "uploaded_at": datetime.now().isoformat()
            }
            new_properties.append(property_data)
        
        property_database.extend(new_properties)
        
        return {
            "SUCCESS": f"Uploaded {len(new_properties)} properties",
            "total_properties": len(property_database),
            "headers_found": list(csv_reader.fieldnames) if csv_reader.fieldnames else [],
            "first_property_check": {
                "id": new_properties[0]["id"] if new_properties else "None",
                "address": new_properties[0]["address"] if new_properties else "None",
                "city": new_properties[0]["city"] if new_properties else "None",
                "price": new_properties[0]["price"] if new_properties else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/debug-csv")
async def debug_csv():
    """Debug endpoint to see what's actually in the database"""
    if not property_database:
        return {"message": "No properties in database"}
    
    return {
        "total_properties": len(property_database),
        "first_3_properties": property_database[:3],
        "all_addresses": [prop["address"] for prop in property_database[:10]],
        "all_cities": [prop["city"] for prop in property_database[:10]],
        "all_prices": [prop["price"] for prop in property_database[:10]]
    }

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
