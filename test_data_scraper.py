"""
test_data_scraper.py - Provides test data to verify the analysis system works
This simulates scraped properties for testing
"""

from typing import List, Dict
from dataclasses import dataclass
import random
from datetime import datetime

@dataclass
class ScrapedProperty:
    """Standardized property data from any source"""
    source: str
    listing_id: str
    address: str
    city: str
    province: str
    postal_code: str
    price: float
    lot_size: str
    property_type: str
    zoning: str
    listing_url: str
    image_url: str
    description: str
    listing_date: str
    mls_number: str
    raw_data: Dict

class TestDataProvider:
    """Provides realistic test properties for Edmonton"""
    
    def __init__(self):
        self.edmonton_neighborhoods = [
            "Glenora", "Oliver", "Windermere", "Terwillegar", "Summerside",
            "Ellerslie", "The Hamptons", "Keswick", "Webber Greens", "Laurel",
            "Downtown", "Strathcona", "Bonnie Doon", "Mill Woods", "Castle Downs"
        ]
        
        self.street_types = ["Avenue", "Street", "Drive", "Way", "Boulevard", "Place", "Lane"]
        
        self.zoning_types = [
            ("RF1", "Single Detached Residential"),
            ("RF3", "Small Scale Infill Development"),
            ("RA7", "Low Rise Apartment"),
            ("RA8", "Medium Rise Apartment"),
            ("CB1", "Low Intensity Business"),
            ("CB2", "General Business"),
            ("DC2", "Site Specific Development Control")
        ]
        
    def generate_test_properties(self, count: int = 20) -> List[ScrapedProperty]:
        """Generate realistic test properties"""
        properties = []
        
        for i in range(count):
            # Random neighborhood and address
            neighborhood = random.choice(self.edmonton_neighborhoods)
            street_num = random.randint(1000, 15000)
            street_name = random.randint(50, 150)
            street_type = random.choice(self.street_types)
            address = f"{street_num} {street_name} {street_type}"
            
            # Random zoning
            zoning_code, zoning_desc = random.choice(self.zoning_types)
            
            # Lot size based on zoning
            if zoning_code in ["RF1", "RF3"]:
                lot_size_sqft = random.randint(5000, 15000)
            elif zoning_code in ["RA7", "RA8"]:
                lot_size_sqft = random.randint(10000, 30000)
            else:  # Commercial
                lot_size_sqft = random.randint(15000, 50000)
                
            lot_size_acres = lot_size_sqft / 43560
            
            # Price based on lot size and zoning
            base_price_per_sqft = random.uniform(15, 50)
            if zoning_code in ["CB1", "CB2"]:
                base_price_per_sqft *= 1.5  # Commercial premium
            price = int(lot_size_sqft * base_price_per_sqft)
            
            # Source rotation
            sources = ["realtor.ca", "kijiji.ca", "realtylink.org"]
            source = sources[i % len(sources)]
            
            property = ScrapedProperty(
                source=source,
                listing_id=f"test-{i+1:03d}",
                address=address,
                city="Edmonton",
                province="AB",
                postal_code=f"T{random.randint(5,6)}{random.choice('ABCDEFGHIJKLMNPRSTUVWXYZ')} {random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPRSTUVWXYZ')}{random.randint(0,9)}",
                price=price,
                lot_size=f"{lot_size_acres:.2f} acres" if lot_size_acres > 0.5 else f"{lot_size_sqft} sqft",
                property_type="Vacant Land",
                zoning=zoning_code,
                listing_url=f"https://example.com/listing/{i+1}",
                image_url="https://via.placeholder.com/300x200",
                description=f"Prime development opportunity in {neighborhood}. {zoning_desc} zoning allows for various development options. Services at property line.",
                listing_date=datetime.now().strftime("%Y-%m-%d"),
                mls_number=f"E{random.randint(4100000, 4200000)}",
                raw_data={"neighborhood": neighborhood, "zoning_desc": zoning_desc}
            )
            
            properties.append(property)
            
        return properties

# Integration with existing scraper
async def get_test_properties(search_criteria: Dict) -> List[Dict]:
    """Get test properties instead of real scraping"""
    
    provider = TestDataProvider()
    test_properties = provider.generate_test_properties(20)
    
    # Filter by search criteria
    min_price = search_criteria.get('min_price', 0)
    max_price = search_criteria.get('max_price', 10000000)
    
    filtered_properties = []
    for prop in test_properties:
        if min_price <= prop.price <= max_price:
            # Convert lot size to square feet
            lot_sqft = 43560  # Default 1 acre
            if 'acre' in prop.lot_size.lower():
                try:
                    acres = float(prop.lot_size.split()[0])
                    lot_sqft = int(acres * 43560)
                except:
                    pass
            elif 'sqft' in prop.lot_size.lower():
                try:
                    lot_sqft = int(prop.lot_size.split()[0])
                except:
                    pass
                    
            filtered_properties.append({
                'id': prop.listing_id,
                'address': prop.address,
                'city': prop.city,
                'province': prop.province,
                'price': prop.price,
                'lot_size_sqft': lot_sqft,
                'zoning': prop.zoning,
                'url': prop.listing_url,
                'source': prop.source
            })
    
    print(f"\n✅ Generated {len(filtered_properties)} test properties")
    return filtered_properties

# Test function
if __name__ == "__main__":
    import asyncio
    
    async def test():
        properties = await get_test_properties({
            'min_price': 200000,
            'max_price': 2000000
        })
        
        print("\nSample Test Properties:")
        for i, prop in enumerate(properties[:5]):
            print(f"\n{i+1}. {prop['address']}")
            print(f"   Price: ${prop['price']:,}")
            print(f"   Lot: {prop['lot_size_sqft']:,} sqft")
            print(f"   Zoning: {prop['zoning']}")
            print(f"   Source: {prop['source']}")
    
    asyncio.run(test())