"""
api.py - Real Estate Development Analysis API
Updated to use the complete analyzer
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio

# Import the complete analyzer
from analyzer_complete import analyze_real_properties

app = FastAPI(
    title="Real Estate Development Analysis API",
    description="Analyzes real estate opportunities using web scraping and financial modeling",
    version="2.0.0"
)

# Enable CORS for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class SearchCriteria(BaseModel):
    city: str = "Edmonton"
    province: str = "AB" 
    min_price: float = 100000
    max_price: float = 5000000

class DeveloperPreferences(BaseModel):
    risk_tolerance: float = 0.6
    preferred_property_types: List[str] = ["commercial", "residential", "mixed_use"]
    min_roi_threshold: float = 15.0
    max_development_timeline_months: int = 36
    financing_preference: str = "mixed"
    location_preferences: Dict[str, float] = {"Edmonton": 1.0, "Calgary": 0.8}

# API Endpoints
@app.get("/")
def read_root():
    return {
        "message": "Real Estate Development Analysis API",
        "version": "2.0.0",
        "endpoints": {
            "/docs": "Interactive API documentation",
            "/analyze": "POST - Analyze properties with custom criteria",
            "/quick-analysis": "GET - Quick analysis with default parameters",
            "/health": "GET - API health check"
        }
    }

@app.post("/analyze")
async def analyze_properties_endpoint(
    search_criteria: SearchCriteria,
    preferences: DeveloperPreferences
):
    """
    Analyze real estate opportunities based on search criteria and developer preferences.
    
    This endpoint:
    1. Scrapes real properties from multiple sources (realtor.ca, Kijiji, etc.)
    2. Analyzes development potential based on zoning
    3. Calculates financial metrics (ROI, payback period, etc.)
    4. Ranks opportunities based on your preferences
    5. Returns detailed analysis and recommendations
    """
    try:
        result = await analyze_real_properties(
            search_criteria.dict(),
            preferences.dict()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quick-analysis")
async def quick_analysis():
    """
    Run a quick analysis with default parameters.
    Good for testing the system.
    """
    try:
        # Default search criteria
        search_criteria = {
            "city": "Edmonton",
            "province": "AB",
            "min_price": 200000,
            "max_price": 2000000
        }
        
        # Default preferences
        preferences = {
            "risk_tolerance": 0.6,
            "preferred_property_types": ["commercial", "residential", "mixed_use"],
            "min_roi_threshold": 15.0,
            "max_development_timeline_months": 36,
            "financing_preference": "mixed",
            "location_preferences": {"Edmonton": 1.0}
        }
        
        result = await analyze_real_properties(search_criteria, preferences)
        
        # Add note that this is a quick analysis
        result["note"] = "This is a quick analysis with default parameters. Use /analyze for custom criteria."
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Check if the API is running properly"""
    return {
        "status": "healthy",
        "message": "API is running",
        "services": {
            "web_scraping": "ready",
            "analyzer": "ready",
            "database": "not implemented yet"
        }
    }

@app.post("/test-scraping")
async def test_scraping(city: str = "Edmonton"):
    """Test the web scraping functionality only"""
    try:
        from web_scraper import PropertyScraperManager
        
        manager = PropertyScraperManager()
        results = await manager.search_all_sources(
            city=city,
            province="AB",
            min_price=100000,
            max_price=2000000
        )
        
        summary = {}
        for source, properties in results.items():
            summary[source] = {
                "count": len(properties),
                "sample": properties[0].__dict__ if properties else None
            }
            
        return {
            "status": "success",
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)