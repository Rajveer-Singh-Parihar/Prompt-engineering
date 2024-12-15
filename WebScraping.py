import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape housing listings
def scrape_housing(url, num_pages=1):
    properties = []

    # Loop over the desired number of pages
    for page in range(1, num_pages + 1):
        print(f"Scraping Page {page}...")
        
        # Add page number query if required (example URL format: ?page=2)
        page_url = f"{url}?page={page}"
        
        try:
            response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise error if request fails

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find property listing blocks (adjust selector based on inspection)
            listings = soup.find_all('div', class_='css-w7ny6m')  # Example class

            for listing in listings:
                # Extract details (inspect to find correct tags and classes)
                title = listing.find('h2', class_='css-1x8m3a5').get_text(strip=True) if listing.find('h2') else 'N/A'
                price = listing.find('div', class_='css-1qzox3b').get_text(strip=True) if listing.find('div', class_='css-1qzox3b') else 'N/A'
                location = listing.find('div', class_='css-148b6cp').get_text(strip=True) if listing.find('div', class_='css-148b6cp') else 'N/A'
                
                # Add extracted data to the list
                properties.append({
                    'Title': title,
                    'Price': price,
                    'Location': location
                })

        except Exception as e:
            print(f"Error on page {page}: {e}")

    # Save results to a CSV file
    if properties:
        df = pd.DataFrame(properties)
        df.to_csv('housing_listings.csv', index=False)
        print("Scraping complete! Data saved to 'housing_listings.csv'.")
    else:
        print("No data scraped. Check the page structure or URL.")

# URL to scrape (adjust based on search results)
base_url = 'https://housing.com/in/buy'
scrape_housing(base_url, num_pages=3)  # Scrape first 3 pages
