from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
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

# Dynamic property database - user controlled
property_database = []

class PropertyInput(BaseModel):
    mls_number: str
    address: str
    city: str
    province: str = "AB"
    price: float
    property_type: str
    zoning: Optional[str] = ""
    features: Optional[str] = ""
    time_on_market: Optional[int] = 0
    listing_agent: Optional[str] = ""
    brokerage: Optional[str] = ""

@app.get("/")
async def root():
    return {
        "platform": "Sgiach Real Estate Analysis",
        "tagline": "Your Winged View of Development",
        "status": "ONLINE",
        "version": "1.0.0",
        "properties_loaded": len(property_database),
        "data_management": {
            "csv_upload": "/upload-csv",
            "manual_entry": "/add-property",
            "bulk_manual": "/add-properties",
            "clear_all": "/clear-properties"
        }
    }

@app.post("/upload-csv")
async def upload_csv(file: UploadFile):
    """Upload CSV with flexible column detection"""
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=422, detail="No file provided")
        
        content = await file.read()
        csv_string = content.decode('utf-8')
        
        # Handle different CSV formats and separators
        # Try different delimiters
        for delimiter in [',', ';', '\t', '|']:
            try:
                test_reader = csv.DictReader(StringIO(csv_string), delimiter=delimiter)
                headers = test_reader.fieldnames
                if headers and len(headers) > 1:
                    break
            except:
                continue
        else:
            raise HTTPException(status_code=400, detail="Could not parse CSV - check file format")
        
        csv_reader = csv.DictReader(StringIO(csv_string), delimiter=delimiter)
        new_properties = []
        
        # Flexible field mapping - handles various column name formats
        def find_field(row, possible_names):
            for name in possible_names:
                if name in row and row[name] and str(row[name]).strip():
                    return str(row[name]).strip()
            return None
        
        for row_num, row in enumerate(csv_reader):
            try:
                # Try to find MLS/ID field
                mls_id = find_field(row, [
                    'MLS_Number', 'MLS Number', 'MLS_number', 'mls_number',
                    'ID', 'id', 'Property_ID', 'Property ID'
                ]) or f"PROP_{len(new_properties) + 1}"
                
                # Try to find address
                address = find_field(row, [
                    'Address', 'address', 'ADDRESS', 'Property_Address', 
                    'Property Address', 'Street_Address', 'Street Address'
                ])
                
                # Try to find city
                city = find_field(row, [
                    'City', 'city', 'CITY', 'Municipality', 'Location'
                ])
                
                # Try to find province
                province = find_field(row, [
                    'Province', 'province', 'PROVINCE', 'State', 'Region'
                ]) or 'AB'
                
                # Try to find price
                price_text = find_field(row, [
                    'Price', 'price', 'PRICE', 'List_Price', 'List Price',
                    'Asking_Price', 'Asking Price', 'Value'
                ])
                
                price = 0
                if price_text:
                    try:
                        clean_price = str(price_text).replace('$', '').replace(',', '').replace(' ', '').strip()
                        price = float(clean_price)
                    except:
                        price = 0
                
                # Try to find property type
                property_type = find_field(row, [
                    'Property_Type', 'Property Type', 'property_type', 'Type',
                    'Category', 'Use', 'Classification'
                ]) or 'Unknown'
                
                # Try to find zoning
                zoning = find_field(row, [
                    'Zoning', 'zoning', 'ZONING', 'Zone', 'Land_Use'
                ]) or ''
                
                # Try to find features
                features = find_field(row, [
                    'Features', 'features', 'Description', 'Details', 'Notes'
                ]) or ''
                
                # Try to find time on market
                time_text = find_field(row, [
                    'Time_on_Market', 'Time on Market', 'Days_on_Market', 
                    'Days on Market', 'DOM', 'Time_Listed'
                ])
                
                time_on_market = 0
                if time_text:
                    try:
                        time_on_market = int(float(str(time_text).strip()))
                    except:
                        time_on_market = 0
                
                # Try to find agent
                listing_agent = find_field(row, [
                    'Listing_Agent', 'Listing Agent', 'Agent', 'Realtor',
                    'Sales_Agent', 'Sales Agent'
                ]) or ''
                
                # Try to find brokerage
                brokerage = find_field(row, [
                    'Brokerage', 'brokerage', 'Company', 'Firm', 'Office'
                ]) or ''
                
                # Only add if we have minimum required data
                if address and city and price > 0:
                    property_data = {
                        "id": mls_id,
                        "address": address,
                        "city": city,
                        "province": province,
                        "price": price,
                        "property_type": property_type,
                        "zoning": zoning,
                        "features": features,
                        "time_on_market": time_on_market,
                        "listing_agent": listing_agent,
                        "brokerage": brokerage,
                        "uploaded_at": datetime.now().isoformat()
                    }
                    new_properties.append(property_data)
                    
            except Exception as e:
                print(f"Error processing row {row_num}: {e}")
                continue
        
        if not new_properties:
            raise HTTPException(status_code=400, detail="No valid properties found in CSV")
        
        # Clear existing and add new
        property_database.clear()
        property_database.extend(new_properties)
        
        return {
            "SUCCESS": f"Uploaded {len(new_properties)} properties",
            "total_properties": len(property_database),
            "detected_delimiter": delimiter,
            "headers_found": list(csv_reader.fieldnames),
            "sample_properties": [
                {
                    "id": prop["id"],
                    "address": prop["address"],
                    "city": prop["city"],
                    "price": f"${prop['price']:,.0f}"
                } for prop in new_properties[:3]
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.post("/add-property")
async def add_property(property_data: PropertyInput):
    """Add a single property manually"""
    new_property = {
        "id": property_data.mls_number,
        "address": property_data.address,
        "city": property_data.city,
        "province": property_data.province,
        "price": property_data.price,
        "property_type": property_data.property_type,
        "zoning": property_data.zoning,
        "features": property_data.features,
        "time_on_market": property_data.time_on_market,
        "listing_agent": property_data.listing_agent,
        "brokerage": property_data.brokerage,
        "uploaded_at": datetime.now().isoformat()
    }
    
    property_database.append(new_property)
    
    return {
        "SUCCESS": f"Added property {property_data.mls_number}",
        "total_properties": len(property_database),
        "property": new_property
    }

@app.post("/add-properties")
async def add_multiple_properties(properties: List[PropertyInput]):
    """Add multiple properties at once"""
    added_properties = []
    
    for prop_data in properties:
        new_property = {
            "id": prop_data.mls_number,
            "address": prop_data.address,
            "city": prop_data.city,
            "province": prop_data.province,
            "price": prop_data.price,
            "property_type": prop_data.property_type,
            "zoning": prop_data.zoning,
            "features": prop_data.features,
            "time_on_market": prop_data.time_on_market,
            "listing_agent": prop_data.listing_agent,
            "brokerage": prop_data.brokerage,
            "uploaded_at": datetime.now().isoformat()
        }
        property_database.append(new_property)
        added_properties.append(new_property)
    
    return {
        "SUCCESS": f"Added {len(added_properties)} properties",
        "total_properties": len(property_database),
        "added_properties": added_properties
    }

@app.delete("/clear-properties")
async def clear_properties():
    """Clear all properties from database"""
    count = len(property_database)
    property_database.clear()
    return {"SUCCESS": f"Cleared {count} properties", "total_properties": 0}

@app.delete("/remove-property/{property_id}")
async def remove_property(property_id: str):
    """Remove a specific property"""
    original_count = len(property_database)
    property_database[:] = [p for p in property_database if p["id"] != property_id]
    
    if len(property_database) == original_count:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return {
        "SUCCESS": f"Removed property {property_id}",
        "total_properties": len(property_database)
    }

@app.get("/quick-analysis")
async def quick_analysis():
    if not property_database:
        return {
            "message": "No properties loaded",
            "instructions": "Upload CSV via /upload-csv or add properties via /add-property"
        }
    
    sample_size = min(5, len(property_database))
    sample_properties = random.sample(property_database, sample_size)
    results = []
    
    for prop in sample_properties:
        price = prop["price"]
        
        if "Agricultural" in prop["property_type"]:
            roi = 75.0
            scenario = "🏘️ Residential Subdivision"
        elif "Commercial" in prop["property_type"]:
            roi = 45.0
            scenario = "🏢 Commercial Development"
        elif "Industrial" in prop["property_type"]:
            roi = 60.0
            scenario = "🏭 Industrial Complex"
        elif "Development" in prop["property_type"]:
            roi = 50.0
            scenario = "🏗️ Mixed Use Development"
        else:
            roi = 25.0
            scenario = "🏠 General Development"
        
        profit = price * (roi / 100)
        investment = price + (price * 0.4)
        
        if roi >= 50:
            grade = "🌟 EXCELLENT (A+)"
        elif roi >= 30:
            grade = "⭐ VERY GOOD (A)"
        elif roi >= 20:
            grade = "✅ GOOD (B+)"
        else:
            grade = "🔶 FAIR (B)"
        
        results.append({
            "🏠 PROPERTY": {
                "id": prop["id"],
                "address": prop["address"],
                "city": prop["city"],
                "price": f"${price:,.0f}",
                "type": prop["property_type"]
            },
            "💰 ANALYSIS": {
                "roi": f"{roi}%",
                "profit": f"${profit:,.0f}",
                "investment": f"${investment:,.0f}",
                "grade": grade
            },
            "⭐ SCENARIO": scenario
        })
    
    results.sort(key=lambda x: float(x["💰 ANALYSIS"]["roi"].rstrip('%')), reverse=True)
    
    return {
        "🦅 SGIACH ANALYSIS": {
            "platform": "Your Winged View of Development",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analyzed": len(results)
        },
        "📊 PORTFOLIO": {
            "total_properties": len(property_database),
            "total_value": f"${sum(p['price'] for p in property_database):,.0f}"
        },
        "🏆 OPPORTUNITIES": results
    }

@app.get("/properties")
async def list_properties():
    return {
        "total_properties": len(property_database),
        "total_value": f"${sum(p['price'] for p in property_database):,.0f}",
        "properties": property_database
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
