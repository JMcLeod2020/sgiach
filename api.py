@app.post("/upload-properties")
async def upload_properties(file: UploadFile):
    """Upload CSV file with real property data - Fixed CSV mapping"""
    try:
        # Check if file was provided
        if not file:
            raise HTTPException(status_code=422, detail="❌ No file provided. Please select a CSV file to upload.")
        
        # Check filename exists
        if not file.filename:
            raise HTTPException(status_code=422, detail="❌ File must have a filename")
            
        # Validate file type
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="❌ File must be a CSV format (.csv extension required)")
        
        # Read CSV content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="❌ Uploaded file is empty")
            
        csv_string = content.decode('utf-8')
        
        # Debug: Print first few lines to see actual CSV structure
        lines = csv_string.split('\n')[:3]
        print("CSV Debug - First 3 lines:")
        for i, line in enumerate(lines):
            print(f"Line {i}: {line}")
        
        # Parse CSV with proper field mapping
        csv_reader = csv.DictReader(StringIO(csv_string))
        new_properties = []
        
        # Print headers to debug
        print("CSV Headers found:", csv_reader.fieldnames)
        
        for row_num, row in enumerate(csv_reader, 1):
            try:
                # Debug: Print first row to see data structure
                if row_num == 1:
                    print("First row data:", dict(row))
                
                # Map CSV fields correctly - handle various possible field names
                mls_number = row.get('MLS_Number') or row.get('MLS Number') or row.get('mls_number') or f"PROP_{len(property_database) + len(new_properties)}"
                address = row.get('Address') or row.get('address') or 'Unknown Address'
                city = row.get('City') or row.get('city') or 'Unknown City'
                province = row.get('Province') or row.get('province') or 'AB'
                
                # Handle price conversion more carefully
                price_str = row.get('Price') or row.get('price') or '0'
                try:
                    # Remove any commas, dollar signs, or spaces
                    price_clean = str(price_str).replace('$', '').replace(',', '').replace(' ', '').strip()
                    price = float(price_clean) if price_clean and price_clean != '' else 0
                except (ValueError, TypeError):
                    price = 0
                    print(f"Warning: Could not parse price '{price_str}' for row {row_num}")
                
                property_type = row.get('Property_Type') or row.get('Property Type') or row.get('property_type') or 'Unknown'
                land_size_sqft = row.get('Land_Size_SqFt') or row.get('Land Size SqFt') or row.get('land_size_sqft') or ''
                zoning = row.get('Zoning') or row.get('zoning') or 'Unknown'
                features = row.get('Features') or row.get('features') or ''
                
                # Handle time on market
                time_str = row.get('Time_on_Market') or row.get('Time on Market') or row.get('time_on_market') or '0'
                try:
                    time_on_market = int(float(str(time_str).strip())) if time_str and str(time_str).strip() != '' else 0
                except (ValueError, TypeError):
                    time_on_market = 0
                
                listing_agent = row.get('Listing_Agent') or row.get('Listing Agent') or row.get('listing_agent') or 'Unknown'
                brokerage = row.get('Brokerage') or row.get('brokerage') or 'Unknown'
                
                property_data = {
                    "id": mls_number,
                    "address": address,
                    "city": city,
                    "province": province,
                    "price": price,
                    "property_type": property_type,
                    "land_size_sqft": land_size_sqft,
                    "zoning": zoning,
                    "features": features,
                    "time_on_market": time_on_market,
                    "listing_agent": listing_agent,
                    "brokerage": brokerage,
                    "uploaded_at": datetime.now().isoformat()
                }
                
                # Debug: Print first processed property
                if row_num == 1:
                    print("First processed property:", property_data)
                
                new_properties.append(property_data)
                
            except Exception as row_error:
                print(f"Error processing row {row_num}: {row_error}")
                print(f"Row data: {dict(row)}")
                continue
        
        if len(new_properties) == 0:
            raise HTTPException(status_code=400, detail="❌ No valid properties found in CSV file")
        
        # Clear existing properties and add new ones
        property_database.clear()
        property_database.extend(new_properties)
        
        # Debug: Print summary of loaded properties
        print(f"Loaded {len(new_properties)} properties")
        print("Sample property addresses:", [prop['address'] for prop in new_properties[:3]])
        print("Sample property prices:", [prop['price'] for prop in new_properties[:3]])
        
        return {
            "🎉 UPLOAD SUCCESS": {
                "message": f"Successfully processed {len(new_properties)} Alberta properties",
                "properties_added": len(new_properties),
                "total_properties_in_database": len(property_database),
                "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "📊 DATA SUMMARY": {
                "file_name": file.filename,
                "file_size": f"{len(content)} bytes",
                "properties_processed": len(new_properties),
                "data_source": "Real Alberta Properties - Realtor.ca Export",
                "csv_headers_found": list(csv_reader.fieldnames) if csv_reader.fieldnames else []
            },
            "🔍 DEBUG INFO": {
                "sample_addresses": [prop['address'] for prop in new_properties[:3]],
                "sample_prices": [f"${prop['price']:,.0f}" for prop in new_properties[:3]],
                "sample_cities": [prop['city'] for prop in new_properties[:3]]
            },
            "✅ NEXT STEPS": [
                "Visit /quick-analysis for development opportunities",
                "Use /analyze-property/{property_id} for detailed analysis",
                "Check /properties to view all loaded data"
            ]
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error processing file: {str(e)}")

# Also add this debugging endpoint to check what data is actually loaded
@app.get("/debug-properties")
async def debug_properties():
    """Debug endpoint to see what properties are actually loaded"""
    if not property_database:
        return {"message": "No properties loaded"}
    
    return {
        "total_properties": len(property_database),
        "first_3_properties": property_database[:3],
        "sample_addresses": [prop.get('address', 'NO ADDRESS') for prop in property_database[:5]],
        "sample_prices": [prop.get('price', 'NO PRICE') for prop in property_database[:5]],
        "sample_cities": [prop.get('city', 'NO CITY') for prop in property_database[:5]],
        "all_property_ids": [prop.get('id', 'NO ID') for prop in property_database[:10]]
    }
