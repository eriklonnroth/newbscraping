# HUMAN INSTRUCTIONS

NB: This document assumes you are using Google Chrome but most browsers other than Safari will work, including Edge, Firefox, Brave, etc. If using a Mac, use the Command key (⌘) instead of Ctrl for any keyboard shortcuts mentioned below.

# QUESTIONS

Type your answers to each question below (placeholders have been provided). These will be read by Cursor's AI, which will then guide you through the scraping process to produce a CSV output with all your scraped data.

# 1. Are you using a Mac or Windows computer?

    Windows

# 2. What browser are you running (Chrome, Edge, Brave, etc). NB: Safari is not supported.

    Chrome

# 3. At a high level, what information do you wish to scrape?

    I want to scrape data about nurseries in London and Birmingham from daynurseries.co.uk

# 4a. If this scrape requires a search step, describe the search criteria in plain English below. e.g. "Search for day nurseries in a 10 mile radius of postcodes W1B 2AE, B1 1AY, and LS1 1DN." The specified criteria must be available in the website's search interface. If the list of records is obtained browsing a structured directory instead of a search form, then describe the browsing criteria instead ("e.g. all nurseries in London"). If you only wish to limit the number of results to be scraped, include the page range below as well (e.g. "fist 10 pages" or "first 100 results").

    SEARCH_CRITERIA: The first 50 nurseries listed for each of London and Birmingham

# 4b. For at least one of your searches, paste the full URL of page 2 of the results below. If the search results aren't paginated, the first page is fine. Verify that your criteria are captured in the URL (e.g. look for 'radius=10mi' or 'county/Birmingham/', etc). If your criteria vary significantly across searches, then paste more than one URL below so that the AI can understand the differing URL structures for each one.

    RESULTS_PAGE_2_URL: https://www.daynurseries.co.uk/day_nursery_search_results.cfm/searchcounty/London/startpage/2

# 4c. If you provided a URL above, save a copy of the HTML file of that page by navigating to it in Chrome and hitting Ctrl + S. Give the file a recognisable name, e.g. "Nursery results page 2.html". Place the downloaded HTML file into the 'html_input' folder in the left sidebar on Cursor (you can drag and drop it there from Windows File Explorer).

# 5a. Does this scrape require you to click on individual results to bring up more details? If so, copy the full URL of an example search result (e.g. a listing for an individual nursery).

    EXAMPLE_DETAILS_PAGE_URL: https://www.daynurseries.co.uk/daynursery.cfm/searchazref/65432253422

# 5b. If you provided a URL above, save a copy of the HTML file of that page by navigating to it in Chrome and hitting Ctrl + S. Give it a recognisable name, e.g. "details.html". Place the downloaded HTML file into the 'html_input' folder in the left sidebar on Cursor (you can drag and drop it there from Windows File Explorer). If not, skip this question.

# 6. Does this scrape require you to download data in the form of PDF or CSV files? If so, place an example of such a file into the 'file_input' folder in the left sidebar on Cursor. If not, skip this question.

# 7. List every data field you wish to capture, separated by commas.

    REQUIRED_FIELDS: nursery name, address, review score, number of reviews, staff number, places, age range, group

# 8. Please provide any additional information below that you believe may be relevant for the AI when conducting this scrape.

    ADDITIONAL_INFO: Not all data fields are available for every nursery

# 9. Now hit Ctrl + S to save your answers to this file, then follow the instructions below to set up Cursor for the scrape (you can skip the steps below if you've previously completed them on this computer).

# ENVIRONMENT SETUP

# 1. Ensure you have the following applications installed on your computer: Google Chrome, Python, Cursor

# 2. Hit Ctrl + Shift + X in Cursor to open the Extensions View. Search for Python and install the extension called 'Python' by ms-python. This gives Cursor the necessary tools to analyse Python code and detect errors, etc.

# 3. Hit Ctrl + Shift + P in Cursor to open the Command Palette and type 'Python: Select Interpreter'. Click on the Python Interpreter from Microsoft App Store. This tells Cursor which Python version to run for this project.

# LAUNCH AI

# Hit Ctrl + L in Cursor to open the AI chat and paste this line: "Read AI_Instructions.md, Human_Instrcuctions.md along with input files, then proceed with the scrape step by step".
