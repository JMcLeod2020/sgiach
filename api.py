from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime
import os

app = FastAPI(title="Sgiach Real Estate Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Sgiach API is running!", "status": "online", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/quick-analysis")
def quick_analysis():
    properties = []
    for i in range(5):
        roi = random.uniform(15, 45)
        price = random.randint(400000, 1500000)
        investment = price * 1.5
        profit = investment * (roi / 100)
        
        properties.append({
            "rank": i + 1,
            "address": f"{random.randint(1000, 9999)} Main St",
            "price": f"${price:,}",
            "roi": f"{roi:.1f}%",
            "investment": f"${int(investment):,}",
            "profit": f"${int(profit):,}",
            "zoning": random.choice(["RF3", "RA7", "CB1"])
        })
    
    return {
        "status": "success",
        "summary": {
            "total_analyzed": 5,
            "average_roi": sum(float(p["roi"][:-1]) for p in properties) / 5
        },
        "opportunities": properties,
        "timestamp": datetime.now().isoformat()
    }
