"""
web_scraper.py - Real Estate Web Scraping Module
Includes multiple scraping strategies and sites
"""
from test_data_scraper import get_test_properties

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import pandas as pd
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
    zoning: Optional[str]
    listing_url: str
    image_url: Optional[str]
    description: str
    listing_date: Optional[str]
    mls_number: Optional[str]
    raw_data: Dict

class BasePropertyScraper:
    """Base class for all property scrapers"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
    def parse_price(self, price_str: str) -> float:
        """Convert price string to float"""
        if not price_str:
            return 0.0
        # Remove currency symbols and commas
        price_cleaned = re.sub(r'[^0-9.]', '', price_str)
        try:
            return float(price_cleaned)
        except:
            return 0.0
            
    def parse_lot_size(self, lot_str: str) -> str:
        """Standardize lot size format"""
        if not lot_str:
            return "N/A"
        # Keep original format but clean it up
        return lot_str.strip()

class RealtorCAScraper(BasePropertyScraper):
    """
    Scraper for Realtor.ca using Selenium
    Note: Realtor.ca has strong anti-scraping measures
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.realtor.ca"

    def setup_driver(self):
        """Setup Selenium Chrome driver with anti-detection measures"""
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        
        # Optional: Run headless (without browser window)
        # options.add_argument('--headless')

        # User agent rotation
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Additional anti-detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
        
    async def search_properties(self, city: str, province: str, min_price: float = 0, 
                              max_price: float = 10000000, property_type: str = "vacant land") -> List[ScrapedProperty]:
        """Search for properties on realtor.ca"""
        
        driver = self.setup_driver()
        properties = []
        
        try:
            # Construct search URL
            search_url = f"{self.base_url}/map#ZoomLevel=10&Center={city}%2C{province}&LatitudeMax=53.7&LongitudeMax=-113.3&LatitudeMin=53.3&LongitudeMin=-113.7&PriceMin={int(min_price)}&PriceMax={int(max_price)}&PropertyTypeGroupID=1&TransactionTypeId=2&Currency=CAD"
            
            driver.get(search_url)
            
            # Wait for page to load
            wait = WebDriverWait(driver, 20)
            
            # Wait for property cards to load
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cardCon")))
            
            # Scroll to load more properties
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Extract property data
            property_cards = driver.find_elements(By.CLASS_NAME, "cardCon")
            
            for card in property_cards[:20]:  # Limit to 20 for testing
                try:
                    # Extract data from card
                    price_elem = card.find_element(By.CLASS_NAME, "priceValue")
                    address_elem = card.find_element(By.CLASS_NAME, "address")
                    
                    # Get property details link
                    link_elem = card.find_element(By.TAG_NAME, "a")
                    property_url = link_elem.get_attribute("href")
                    
                    # Extract MLS number from URL
                    mls_match = re.search(r'/([\w\d]+)$', property_url)
                    mls_number = mls_match.group(1) if mls_match else None
                    
                    property_data = ScrapedProperty(
                        source="realtor.ca",
                        listing_id=mls_number or f"realtor-{len(properties)}",
                        address=address_elem.text.split(',')[0],
                        city=city,
                        province=province,
                        postal_code="",  # Would need detail page
                        price=self.parse_price(price_elem.text),
                        lot_size="N/A",  # Would need detail page
                        property_type=property_type,
                        zoning=None,  # Would need detail page
                        listing_url=property_url,
                        image_url=None,
                        description="",
                        listing_date=None,
                        mls_number=mls_number,
                        raw_data={"card_html": card.get_attribute('outerHTML')}
                    )
                    
                    properties.append(property_data)
                    
                except Exception as e:
                    print(f"Error parsing property card: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping realtor.ca: {e}")
            
        finally:
            driver.quit()
            
        return properties

class RealtyLinkScraper(BasePropertyScraper):
    """
    Scraper for RealtyLink.org (Alberta-specific)
    Generally more scraping-friendly than realtor.ca
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.realtylink.org"
        
    async def search_properties(self, city: str, min_price: float = 0, 
                              max_price: float = 10000000) -> List[ScrapedProperty]:
        """Search for properties on RealtyLink"""
        
        properties = []
        
        # Construct search parameters
        search_params = {
            'searchType': 'AdvancedSearch',
            'city': city,
            'minPrice': str(int(min_price)),
            'maxPrice': str(int(max_price)),
            'propertyType': 'Land'
        }
        
        try:
            # Make search request
            response = requests.get(
                f"{self.base_url}/en/properties~for-sale",
                params=search_params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find property listings
                listings = soup.find_all('div', class_='property-item')
                
                for listing in listings:
                    try:
                        # Extract data
                        price_elem = listing.find('span', class_='price')
                        address_elem = listing.find('span', class_='address')
                        link_elem = listing.find('a')
                        
                        if price_elem and address_elem:
                            property_url = f"{self.base_url}{link_elem.get('href')}" if link_elem else ""
                            
                            property_data = ScrapedProperty(
                                source="realtylink.org",
                                listing_id=f"realtylink-{len(properties)}",
                                address=address_elem.text.strip(),
                                city=city,
                                province="AB",
                                postal_code="",
                                price=self.parse_price(price_elem.text),
                                lot_size="N/A",
                                property_type="Land",
                                zoning=None,
                                listing_url=property_url,
                                image_url=None,
                                description="",
                                listing_date=None,
                                mls_number=None,
                                raw_data={"html": str(listing)}
                            )
                            
                            properties.append(property_data)
                            
                    except Exception as e:
                        print(f"Error parsing RealtyLink listing: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error scraping RealtyLink: {e}")
            
        return properties

class KijijiRealEstateScraper(BasePropertyScraper):
    """
    Scraper for Kijiji Real Estate listings
    Often has unique listings not on MLS
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.kijiji.ca"
        
    async def search_properties(self, city: str, province: str) -> List[ScrapedProperty]:
        """Search for land/property on Kijiji"""
        
        properties = []
        
        # Map city to Kijiji location ID (simplified)
        location_map = {
            'Edmonton': 'b-land-for-sale/edmonton-area/c641l1700203',
            'Calgary': 'b-land-for-sale/calgary/c641l1700199',
            'Red Deer': 'b-land-for-sale/red-deer/c641l1700136'
        }
        
        location_path = location_map.get(city, 'b-land-for-sale/alberta/c641l9003')
        
        try:
            url = f"{self.base_url}/{location_path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find listings
                listings = soup.find_all('div', {'data-testid': 'listing-card'})
                
                for listing in listings[:20]:  # Limit for testing
                    try:
                        # Extract data
                        title_elem = listing.find('h3')
                        price_elem = listing.find('p', {'data-testid': 'listing-price'})
                        location_elem = listing.find('p', {'data-testid': 'listing-location'})
                        link_elem = listing.find('a')
                        
                        if title_elem and price_elem:
                            listing_url = f"{self.base_url}{link_elem.get('href')}" if link_elem else ""
                            
                            # Extract lot size from title if present
                            lot_size_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:acres?|ac)', title_elem.text, re.I)
                            lot_size = f"{lot_size_match.group(1)} acres" if lot_size_match else "N/A"
                            
                            property_data = ScrapedProperty(
                                source="kijiji.ca",
                                listing_id=f"kijiji-{len(properties)}",
                                address=location_elem.text if location_elem else city,
                                city=city,
                                province=province,
                                postal_code="",
                                price=self.parse_price(price_elem.text),
                                lot_size=lot_size,
                                property_type="Land",
                                zoning=None,
                                listing_url=listing_url,
                                image_url=None,
                                description=title_elem.text,
                                listing_date=None,
                                mls_number=None,
                                raw_data={"title": title_elem.text}
                            )
                            
                            properties.append(property_data)
                            
                    except Exception as e:
                        print(f"Error parsing Kijiji listing: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error scraping Kijiji: {e}")
            
        return properties

class PropertyScraperManager:
    """Manages multiple scrapers and combines results"""
    
    def __init__(self):
        self.scrapers = {
            'realtor.ca': RealtorCAScraper(),
            'realtylink': RealtyLinkScraper(),
            'kijiji': KijijiRealEstateScraper()
        }
        
    async def search_all_sources(self, city: str, province: str, min_price: float = 0,
                                max_price: float = 10000000) -> Dict[str, List[ScrapedProperty]]:
        """Search all available sources"""
        
        all_results = {}
        
        # Try each scraper
        for source_name, scraper in self.scrapers.items():
            print(f"Searching {source_name}...")
            try:
                if source_name == 'realtor.ca':
                    results = await scraper.search_properties(city, province, min_price, max_price)
                elif source_name == 'realtylink':
                    results = await scraper.search_properties(city, min_price, max_price)
                elif source_name == 'kijiji':
                    results = await scraper.search_properties(city, province)
                    
                all_results[source_name] = results
                print(f"Found {len(results)} properties on {source_name}")
                
            except Exception as e:
                print(f"Error with {source_name}: {e}")
                all_results[source_name] = []
                
        return all_results
    
    def combine_results(self, all_results: Dict[str, List[ScrapedProperty]]) -> pd.DataFrame:
        """Combine results from all sources into a DataFrame"""
        
        all_properties = []
        
        for source, properties in all_results.items():
            for prop in properties:
                all_properties.append({
                    'source': prop.source,
                    'address': prop.address,
                    'city': prop.city,
                    'province': prop.province,
                    'price': prop.price,
                    'lot_size': prop.lot_size,
                    'property_type': prop.property_type,
                    'zoning': prop.zoning or 'Unknown',
                    'url': prop.listing_url,
                    'description': prop.description[:100] + '...' if len(prop.description) > 100 else prop.description
                })
                
        df = pd.DataFrame(all_properties)
        
        # Remove duplicates based on address and price
        df = df.drop_duplicates(subset=['address', 'price'])
        
        # Sort by price
        df = df.sort_values('price', ascending=True)
        
        return df

# Test function
async def test_scraping():
    """Test the scraping functionality"""
    
    manager = PropertyScraperManager()
    
    # Search for properties in Edmonton
    print("Starting property search in Edmonton, AB...")
    print("This may take a few minutes...\n")
    
    results = await manager.search_all_sources(
        city="Edmonton",
        province="AB",
        min_price=100000,
        max_price=2000000
    )
    
    # Combine results
    df = manager.combine_results(results)
    
    print("\n=== SEARCH RESULTS ===")
    print(f"Total properties found: {len(df)}")
    print(f"Sources: {df['source'].value_counts().to_dict()}")
    print(f"Price range: ${df['price'].min():,.0f} - ${df['price'].max():,.0f}")
    
    print("\n=== TOP 10 PROPERTIES BY PRICE ===")
    print(df[['address', 'price', 'lot_size', 'source']].head(10).to_string(index=False))
    
    # Save to CSV
    df.to_csv('scraped_properties.csv', index=False)
    print("\nResults saved to 'scraped_properties.csv'")
    
    return df

# Integration function for the analyzer
async def get_real_properties(search_criteria: Dict) -> List[Dict]:
    """Get real properties from web scraping"""
    
    manager = PropertyScraperManager()
    
    results = await manager.search_all_sources(
        city=search_criteria.get('city', 'Edmonton'),
        province=search_criteria.get('province', 'AB'),
        min_price=search_criteria.get('min_price', 0),
        max_price=search_criteria.get('max_price', 10000000)
    )
    
    # Convert to format expected by analyzer
    properties = []
    for source, props in results.items():
        for prop in props:
            # Convert lot size to square feet if in acres
            lot_sqft = 43560  # Default 1 acre
            if 'acre' in prop.lot_size.lower():
                try:
                    acres = float(re.search(r'(\d+(?:\.\d+)?)', prop.lot_size).group(1))
                    lot_sqft = acres * 43560
                except:
                    pass
                    
            properties.append({
                'id': prop.listing_id,
                'address': prop.address,
                'city': prop.city,
                'province': prop.province,
                'price': prop.price,
                'lot_size_sqft': lot_sqft,
                'zoning': prop.zoning or 'Unknown',
                'url': prop.listing_url,
                'source': prop.source
            })
            
    return properties

if __name__ == "__main__":
    # Run test
    asyncio.run(test_scraping())
"""
Add this code to the END of your existing web_scraper.py file
This provides a fallback to test data when scraping fails
"""

# Add this import at the top of web_scraper.py:
# from test_data_scraper import get_test_properties

# Replace the existing get_real_properties function with this enhanced version:

async def get_real_properties(search_criteria: Dict) -> List[Dict]:
    """Get real properties from web scraping with test data fallback"""
    
    manager = PropertyScraperManager()
    
    # Try real scraping first
    results = await manager.search_all_sources(
        city=search_criteria.get('city', 'Edmonton'),
        province=search_criteria.get('province', 'AB'),
        min_price=search_criteria.get('min_price', 0),
        max_price=search_criteria.get('max_price', 10000000)
    )
    
    # Check if we got any results
    total_properties = sum(len(props) for props in results.values())
    
    if total_properties == 0:
        print("\n⚠️  No real properties found. Using test data for demonstration...")
        print("This allows you to see how the system works with sample properties.")
        
        # Import test data provider
        from test_data_scraper import get_test_properties
        
        # Get test properties
        return await get_test_properties(search_criteria)
    
    # Convert to format expected by analyzer
    properties = []
    for source, props in results.items():
        for prop in props:
            # Convert lot size to square feet if in acres
            lot_sqft = 43560  # Default 1 acre
            if 'acre' in prop.lot_size.lower():
                try:
                    acres = float(re.search(r'(\d+(?:\.\d+)?)', prop.lot_size).group(1))
                    lot_sqft = acres * 43560
                except:
                    pass
                    
            properties.append({
                'id': prop.listing_id,
                'address': prop.address,
                'city': prop.city,
                'province': prop.province,
                'price': prop.price,
                'lot_size_sqft': lot_sqft,
                'zoning': prop.zoning or 'Unknown',
                'url': prop.listing_url,
                'source': prop.source
            })
            
    return properties

# Also add this improved Kijiji scraper to replace the existing one:

class KijijiRealEstateScraper(BasePropertyScraper):
    """
    Improved Kijiji scraper
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.kijiji.ca"
        
    async def search_properties(self, city: str, province: str) -> List[ScrapedProperty]:
        """Search for land/property on Kijiji with better error handling"""
        
        properties = []
        
        # Updated URL structure for Kijiji
        if city.lower() == 'edmonton':
            url = "https://www.kijiji.ca/b-land-for-sale/edmonton-area/c641l1700203"
        elif city.lower() == 'calgary':
            url = "https://www.kijiji.ca/b-land-for-sale/calgary/c641l1700199"
        else:
            url = f"https://www.kijiji.ca/b-land-for-sale/alberta/c641l9003"
        
        try:
            # Add delay to be respectful
            await asyncio.sleep(1)
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Updated selectors for current Kijiji structure
                listings = soup.find_all(['div', 'li'], class_=lambda x: x and ('search-item' in x or 'regular-ad' in x))
                
                if not listings:
                    # Try alternative selector
                    listings = soup.find_all('div', attrs={'data-listing-id': True})
                
                for listing in listings[:10]:  # Limit for testing
                    try:
                        # Multiple selector attempts for robustness
                        title_elem = (
                            listing.find('a', class_='title') or 
                            listing.find('div', class_='title') or
                            listing.find(['h3', 'h4'])
                        )
                        
                        price_elem = (
                            listing.find('div', class_='price') or
                            listing.find('span', class_='price')
                        )
                        
                        location_elem = (
                            listing.find('div', class_='location') or
                            listing.find('span', class_='location')
                        )
                        
                        if title_elem and price_elem:
                            # Extract href
                            link_elem = listing.find('a', href=True)
                            listing_url = f"{self.base_url}{link_elem['href']}" if link_elem else ""
                            
                            # Clean price
                            price_text = price_elem.text.strip()
                            
                            property_data = ScrapedProperty(
                                source="kijiji.ca",
                                listing_id=f"kijiji-{len(properties)}",
                                address=location_elem.text.strip() if location_elem else city,
                                city=city,
                                province=province,
                                postal_code="",
                                price=self.parse_price(price_text),
                                lot_size="N/A",
                                property_type="Land",
                                zoning=None,
                                listing_url=listing_url,
                                image_url=None,
                                description=title_elem.text.strip(),
                                listing_date=None,
                                mls_number=None,
                                raw_data={"title": title_elem.text.strip()}
                            )
                            
                            properties.append(property_data)
                            
                    except Exception as e:
                        continue
                        
        except requests.RequestException as e:
            print(f"Network error scraping Kijiji: {e}")
        except Exception as e:
            print(f"Error scraping Kijiji: {e}")
            
        return properties