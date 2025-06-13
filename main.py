"""
Main entry point for the Real Estate Development Analysis API
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the analyzer code (from the previous artifact)
# You'll paste the previous code here or import it

def main():
    print("Real Estate Development Analyzer Setup Complete!")
    print(f"Python is running from: {os.sys.executable}")
    print("\nNext steps:")
    print("1. Add your API keys to the .env file")
    print("2. Copy the analyzer code to this directory")
    print("3. Run the API with: uvicorn api:app --reload")

if __name__ == "__main__":
    main()
