"""
Template for headful scraping using Chrome DevTools Protocol (CDP)

IMPORTANT: Before running this script, inform the user that they should closer their existing browser completely

"""

from playwright.sync_api import sync_playwright
import sys


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
                    return False, None, "Unable to locate <p> element on the page"
                
                # Get text content
                p_text = p_element.text_content()
                if not p_text:
                    return False, None, "Found <p> element but it contains no text"
                
                print(f"Found <p> element with text: {p_text[:100]}...")
                
            except Exception as e:
                return False, None, f"Error while extracting <p> element: {str(e)}"
            
            return True, p_text, None
            
    except Exception as e:
        return False, None, f"Unexpected error during scraping: {str(e)}"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python browser_test_scraper.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    print("=" * 60)
    print("Headful Scraper Template")
    print("=" * 60)
    
    # Scrape the page
    success, data, error_message = scrape_page(url)
    
    if not success:
        print(f"\n ERROR: {error_message}")
        return
    
    print("\n SUCCESS: Scrape completed")
    print("\nExtracted content preview:")
    print(f"{data[:200]}..." if len(data) > 200 else data)


if __name__ == "__main__":
    main()