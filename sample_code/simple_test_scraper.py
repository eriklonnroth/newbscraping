"""
Template for simple scraping using Requests and BeautifulSoup4

This template uses basic HTTP requests without browser automation.
Use this for server-side rendered pages that don't require JavaScript execution.

For pages with JavaScript rendering or bot protection, use template_browser_scraper.py instead.
"""

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os


# NOTE TO AI: Before running this script, update the URL below to match that of EXAMPLE_DETAILS_PAGE_URL from Human_Instructions.md:
URL = # URL from START_HERE.md here

def scrape_page(url):
    """
    Scrape a page using requests and BeautifulSoup
    
    Args:
        url: The URL to scrape
    
    Returns:
        tuple: (success: bool, data: str or None, error_message: str or None)
    """
    try:
        # Send HTTP request with realistic headers
        print(f"Fetching page: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return False, None, f"Unable to load page: {str(e)}"
        
        # Parse HTML
        print("Parsing HTML...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # NOTE TO AI: As a test we will scrape the first <p> element to verify that it's working. 
        print("Searching for first <p> element...")
        try:
            p_element = soup.select_one('p')
            if not p_element:
                return False, None, "Unable to locate <p> element on the page"
            
            # Get text content
            p_text = p_element.get_text(strip=True)
            if not p_text:
                return False, None, "Found <p> element but it contains no text"
            
            print(f"Found <p> element with text: {p_text[:100]}...")
            
        except Exception as e:
            return False, None, f"Error while extracting <p> element: {str(e)}"
        
        return True, p_text, None
        
    except Exception as e:
        return False, None, f"Unexpected error during scraping: {str(e)}"


def save_to_csv(data, output_dir='csv_output'):
    """
    Save data to CSV file with timestamp
    
    Args:
        data: The text content to save
        output_dir: Directory to save the output file
    
    Returns:
        str: Path to saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/{timestamp}_test_output.csv'
    
    # Write to CSV
    # NOTE TO AI: As a test, we start by finding the first <p> element.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['p'])
        writer.writeheader()
        writer.writerow({'p': data})
    
    return filename


def main():
    print("=" * 60)
    print("Simple Scraper Template")
    print("=" * 60)
    
    # Scrape the page
    success, data, error_message = scrape_page(URL)
    
    if not success:
        print(f"\n ERROR: {error_message}")
        return
    
    # Save to CSV
    try:
        output_file = save_to_csv(data)
        print(f"\n SUCCESS: Data saved to {output_file}")
        print(f"\nExtracted content preview:")
        print(f"{data[:200]}..." if len(data) > 200 else data)
    except Exception as e:
        print(f"\n ERROR: Unable to save data to CSV: {str(e)}")


if __name__ == "__main__":
    main()

