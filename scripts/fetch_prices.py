import urllib.request
import csv
import json
from datetime import datetime

# TODO: Replace this URL with the exact raw CSV link from the GOV.UK Fuel Finder developer page
#### CSV_URL = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/YOUR_FILE_ID_HERE/Weekly_Fuel_Prices.csv" #### original ai gave
CSV_URL ="https://www.developer.fuel-finder.service.gov.uk/access-latest-fuelprices"

# TODO: Check the CSV and update these strings to match the exact column names
UNLEADED_HEADER = "forecourt.fuel_price.E10"
DIESEL_HEADER = "forecourt.fuel_price.B7S"
DATE_HEADER = "Date"

def main():
    try:
        # Download CSV
        response = urllib.request.urlopen(CSV_URL)
        lines = [l.decode('utf-8-sig') for l in response.readlines()]
        
        # Parse CSV
        reader = csv.DictReader(lines)
        rows = list(reader)
        
        if not rows:
            print("No data found in CSV")
            return
            
        # Get the most recent row (usually the last row in the GOV UK dataset)
        latest_row = rows[-1]
        
        # Extract values (Prices in UK Gov CSV are usually in Pence per Litre)
        unleaded_ppl = float(latest_row[UNLEADED_HEADER])
        diesel_ppl = float(latest_row[DIESEL_HEADER])
        date_str = latest_row[DATE_HEADER]
        
        # Convert pence to pounds (£)
        data = {
            "unleaded": round(unleaded_ppl / 100, 3),
            "diesel": round(diesel_ppl / 100, 3),
            "last_updated": date_str
        }
        
        # Write to JSON
        with open('prices.json', 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Successfully updated prices.json: {data}")
        
    except Exception as e:
        print(f"Error fetching/parsing CSV: {e}")
        # Exit with error code so GitHub Action flags it as a failure
        exit(1)

if __name__ == "__main__":
    main()
