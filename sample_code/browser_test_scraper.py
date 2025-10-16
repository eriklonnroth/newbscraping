"""
Template for headful scraping using Chrome DevTools Protocol (CDP)

IMPORTANT: Before running this script:
1. Close your browser completely
2. Tell Cursor: "Read this file and launch a headful browser for debugging"
3. Wait for the browser to open with remote debugging enabled that Playwright can connect to for scraping.
4. Then run this script

"""

from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import os


# NOTE TO AI: Before running this script, ask the user for the target URL from example.com to an actual URL if not already changed:
URL = # URL from START_HERE.md here


def scrape_page(url, cdp_url="http://localhost:9222"):
    """
    Scrape a page using an existing browser via CDP
    
    Args:
        url: The URL to scrape
        cdp_url: Chrome DevTools Protocol endpoint (default: http://localhost:9222)
    
    Returns:
        tuple: (success: bool, data: str or None, error_message: str or None)
    """
    try:
        with sync_playwright() as p:
            # Connect to existing browser via CDP
            print(f"Connecting to browser at {cdp_url}...")
            try:
                browser = p.chromium.connect_over_cdp(cdp_url)
            except Exception as e:
                return False, None, f"Unable to connect to browser. Is it running with --remote-debugging-port=9222? Error: {str(e)}"
            
            # Get the default context (existing browser session)
            if not browser.contexts:
                browser.close()
                return False, None, "No browser contexts available. Please ensure browser is running."
            
            context = browser.contexts[0]
            
            # Create a new page
            page = context.new_page()
            
            # Navigate to URL and wait for page to load
            print(f"Loading page: {url}")
            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
            except Exception as e:
                page.close()
                return False, None, f"Unable to load page: {str(e)}"
            
            # Wait extra time for any dynamic content
            print("Waiting for content to load...")
            page.wait_for_timeout(2000)
            
            # NOTE TO AI: As a test we will scrape the first <p> element to verify that it's working. 
            # Once this has been done, ask user for actual fieldnames they wish to scrape
            # To find matching selectors, ask user to save the full HTML of the webpage using Shift + Ctrl + S, and place the file in this project folder so it can be parsed.
            print("Searching for first <p> element...")
            try:
                p_element = page.query_selector('p')
                if not p_element:
                    page.close()
                    return False, None, "Unable to locate <p> element on the page"
                
                # Get text content
                p_text = p_element.text_content()
                if not p_text:
                    page.close()
                    return False, None, "Found <p> element but it contains no text"
                
                print(f"Found <p> element with text: {p_text[:100]}...")
                
            except Exception as e:
                page.close()
                return False, None, f"Error while extracting <p> element: {str(e)}"
            
            # Close the page but not the browser
            page.close()
            
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
    # NOTE TO AI: Ask the user what filename format they want for the output
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/{timestamp}_output.csv'
    
    # Write to CSV
    # NOTE TO AI: As a test, we start by finding the first <p> element. Once this has been done, ask user for actual fieldnames and selectors they wish to scrape (see above)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['p'])
        writer.writeheader()
        writer.writerow({'p': data})
    
    return filename


def main():
    print("=" * 60)
    print("Headful Scraper Template")
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