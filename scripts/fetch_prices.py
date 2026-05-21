import urllib.request
import re

PAGE_URL = "https://www.developer.fuel-finder.service.gov.uk/access-latest-fuelprices"

# Column names from the official government CSV layout
UNLEADED_HEADER = "forecourts.fuel_price.E10"
DIESEL_HEADER = "forecourts.fuel_price.B7S"

def main():
    try:
        # Step 1: Request the landing web page disguised as a browser
        req_page = urllib.request.Request(
            PAGE_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        html_content = urllib.request.urlopen(req_page).read().decode('utf-8')
        
        # Step 2: Use an expression to find the temporary messy Amazon CSV link hidden on the page
        match = re.search(r'href="(https://ff-raw-data-bronze-ics-prod.s3.[^"]+\.csv[^"]*)"', html_content)
        
        if not match:
            print("Could not find the dynamic CSV link on the government page.")
            return
            
        csv_url = match.group(1).replace('&amp;', '&')
        print(f"Success! Found today's live data link: {csv_url[:60]}...")

        # Step 3: Now fetch the actual spreadsheet content using that fresh link
        req_csv = urllib.request.Request(
            csv_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        response = urllib.request.urlopen(req_csv)
        lines = [l.decode('utf-8-sig') for l in response.readlines()]
        print(f"Successfully downloaded {len(lines)} lines of fuel data.")
        
        # (Your AI's remaining calculations and file saving logic should stay right below here)
        
    except Exception as e:
        print(f"Error fetching or parsing data: {e}")
        raise e

if __name__ == "__main__":
    main()
