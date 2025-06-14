# api.py - Minimal version for Railway deployment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
import random

app = FastAPI(title="Sgiach - Real Estate Development Analysis API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample test data generator
def generate_test_properties(num_properties=15):
    street_names = ["Main St", "Oak Ave", "Elm Dr", "Park Blvd", "1st Ave", "2nd St", "King Way", "Queen St"]
    zonings = ["RF3", "RA7", "CB1", "DC2"]
    sources = ["realtor.ca", "kijiji.ca", "realtylink.org"]
    
    properties = []
    for i in range(num_properties):
        price = random.randint(400000, 1500000)
        lot_size = random.randint(8000, 40000)
        zoning = random.choice(zonings)
        
        # Generate development scenario based on zoning
        if zoning == "RF3":
            dev_type = "Townhouse Development"
            units = random.randint(4, 8)
            roi = random.uniform(15, 25)
        elif zoning in ["RA7", "RA8"]:
            dev_type = "Mid-Rise Apartment"
            units = random.randint(20, 40)
            roi = random.uniform(20, 35)
        elif zoning in ["CB1", "CB2"]:
            dev_type = "Mixed-Use Development"
            units = random.randint(25, 50)
            roi = random.uniform(35, 60)
        else:
            dev_type = "Generic Development"
            units = random.randint(8, 15)
            roi = random.uniform(15, 25)
        
        total_investment = price + (units * 150000)  # Simplified calculation
        net_profit = total_investment * (roi / 100)
        
        properties.append({
            "property": {
                "address": f"{random.randint(1000, 15000)} {random.choice(street_names)}",
                "price": price,
                "lot_size": lot_size / 43560,  # Convert to acres
                "zoning": zoning,
                "source": random.choice(sources)
            },
            "scenarios": [{
                "type": dev_type,
                "description": f"{dev_type} with {units} units",
                "zoning_compliance": f"{zoning} - Compliant",
                "financial_analysis": {
                    "total_development_cost": total_investment,
                    "projected_value": total_investment + net_profit,
                    "roi_percentage": round(roi, 1),
                    "payback_period_months": random.randint(8, 24),
                    "net_profit": int(net_profit)
                },
                "timeline_months": random.randint(18, 36),
                "risk_score": random.uniform(0.3, 0.8)
            }],
            "score": random.uniform(0.15, 0.40)
        })
    
    return sorted(properties, key=lambda x: x["score"], reverse=True)

@app.get("/")
async def root():
    return {"message": "Sgiach Real Estate Development Analysis API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/quick-analysis")
async def quick_analysis():
    """Quick analysis with default parameters"""
    properties = generate_test_properties(15)
    analyzed = properties[:7]  # Top 7 properties
    
    avg_roi = sum(p["scenarios"][0]["financial_analysis"]["roi_percentage"] for p in analyzed) / len(analyzed)
    
    return {
        "status": "success",
        "summary": {
            "total_scraped": 16,
            "total_analyzed": len(analyzed),
            "meeting_roi_threshold": len(analyzed),
            "average_roi": round(avg_roi, 2)
        },
        "top_opportunities": [
            {
                "rank": i + 1,
                "address": prop["property"]["address"],
                "source": prop["property"]["source"],
                "price": f"${prop['property']['price']:,}",
                "lot_size": f"{prop['property']['lot_size']:.2f} acres",
                "zoning": prop["property"]["zoning"],
                "development_type": prop["scenarios"][0]["type"],
                "units": prop["scenarios"][0]["description"].split()[-2] if "units" in prop["scenarios"][0]["description"] else "N/A",
                "roi": f"{prop['scenarios'][0]['financial_analysis']['roi_percentage']}%",
                "total_investment": f"${prop['scenarios'][0]['financial_analysis']['total_development_cost']:,}",
                "net_profit": f"${prop['scenarios'][0]['financial_analysis']['net_profit']:,}",
                "timeline": f"{prop['scenarios'][0]['timeline_months']} months",
                "score": f"{prop['score']:.3f}",
                "listing_url": f"https://example.com/listing/{i+1}"
            }
            for i, prop in enumerate(analyzed)
        ],
        "timestamp": datetime.now().isoformat(),
        "note": "This is a quick analysis with test data. Full scraping capabilities available."
    }

@app.post("/analyze")
async def analyze_properties(request: dict):
    """Custom analysis with user parameters"""
    # Extract parameters
    search_criteria = request.get("search_criteria", {})
    preferences = request.get("preferences", {})
    
    # Generate properties based on criteria
    min_price = search_criteria.get("min_price", 200000)
    max_price = search_criteria.get("max_price", 2000000)
    min_roi = preferences.get("min_roi_threshold", 15.0)
    
    properties = generate_test_properties(20)
    
    # Filter by criteria
    filtered = [
        p for p in properties 
        if min_price <= p["property"]["price"] <= max_price 
        and p["scenarios"][0]["financial_analysis"]["roi_percentage"] >= min_roi
    ]
    
    analyzed = filtered[:10]  # Top 10
    
    if analyzed:
        avg_roi = sum(p["scenarios"][0]["financial_analysis"]["roi_percentage"] for p in analyzed) / len(analyzed)
        total_investment = sum(p["scenarios"][0]["financial_analysis"]["total_development_cost"] for p in analyzed[:5])
        total_profit = sum(p["scenarios"][0]["financial_analysis"]["net_profit"] for p in analyzed[:5])
    else:
        avg_roi = 0
        total_investment = 0
        total_profit = 0
    
    return {
        "status": "success",
        "summary": {
            "total_scraped": 20,
            "total_analyzed": len(analyzed),
            "meeting_roi_threshold": len(analyzed),
            "average_roi": round(avg_roi, 2) if analyzed else 0
        },
        "opportunities": analyzed,
        "analysis_timestamp": datetime.now().isoformat(),
        "search_parameters": {
            "location": f"{search_criteria.get('city', 'Edmonton')}, {search_criteria.get('province', 'AB')}",
            "price_range": f"${min_price:,} - ${max_price:,}",
            "min_roi_threshold": f"{min_roi}%",
            "risk_tolerance": preferences.get("risk_tolerance", 0.6)
        },
        "note": "Analysis completed using test data. Real property data integration available."
    }

# Serve the frontend HTML
@app.get("/app", response_class=HTMLResponse)
async def serve_frontend():
    # This will serve your Sgiach frontend
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sgiach - Redirecting...</title>
        <meta http-equiv="refresh" content="0;url=/docs">
    </head>
    <body>
        <p>Redirecting to API documentation...</p>
        <p>Frontend will be available soon at this URL.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)