# AI INSTRUCTIONS

You are guiding a novice user through a step by step webscraping process. Assume limited understanding of technical concepts related to Python, web development, or environment setup.

The user has provided details of the scrape they wish to undertake in START_HERE.md. You'll find relevant URLs there, along with fieldnames for the data to be scraped. The final output of this project will be a CSV file.

Environment: The user is either on a Windows or a Mac running a Chromium browser. For shell commands, always use python3 and pip3 as python and pip may not have been aliased. Do not ask for the virtual environment of the user but instead run all commands with full filepath references.

Sample scripts: Sample scripts of a nursery website scrape have been provided in sample_scripts. Do not edit or alter these files in any way, and do not add more files to this directory. Just use it for reference.

Read the steps below and construct a to-do list.

# STEPS

1. Restate the purpose of the scraping project as given by the user in question 1 of START_HERE.md and ask them to confirm whether they wish to proceed. Wait for a response.

2. Ask the user whether they have completed the Environment Setup steps as outlined in START_HERE.md. Wait for a response.

3. Read their answers to START_HERE.md and verify that they have provided necessary input files under html_input and (optionally) file_input. If they have provided a PDF file input, run `pip3 install PyPDF2`. If any inputs seem to be missing, alert the user. Otherwise proceed to the next step.

4. For each field that the user wants to capture in the scrape (as provided in question 5 of START_HERE.md), check that you can locate it in the inputs.

   - Locate each field value in the HTML by grepping likely words or patterns to be found in each fieldname, and note the appropriate CSS selector for the values of each field
   - When choosing selectors, avoid brittle nth-child references, and instead use XPATH where appropriate.
   - If any required field is missing from the provided HTML, alert the user

5. Save the fieldname selectors to an appropriately named text file, e.g. 'selectors.txt'.

6. Explain to the user that you want to check what Python packages are already installed, then run `pip3 list`.

7. If BeautifulSoup or lxml are missing, install them using `pip3 install beautifulsoup4 lxml`. Otherwise proceed to the next step.

8. Create a test script to check whether you can extract the values from your selectors text file using BeautifulSoup. Run the script and report the extracted values to the user. Ask them to confirm whether everything looks correct and await a response.

9. Test whether we can conduct the actual scrape using BeautifulSoup or whether a headful browser approach is needed (do not bother testing a headless browser).

   - Start by updating the placeholder URL in template_simple_scraper.py with the EXAMPLE_DETAILS_PAGE_URL provided by the user, then run `python3 template_simple_scraper.py`.
   - If BeautifulSoup managed to retrieve a value that matches the first <p> from our html input, then we know the scrape worked. E
   - Explain to the user that our test scrape succeeded and proceed to building the real scripts (step 12).

10. If BeautifulSoup results in an error or if the retrieved <p> element contains text such as "We believe you may be a bot", then we know that HTTP requests will not work and we will need to try a headful browser.

11. Explain to the user that you need to install more packages, and that this might take a few minutes. Run `pip3 install -r requirements.txt`.

12. If Playwright is among the recently installed packages, alert the user that you need to install a Playwright browser and that this might take a few minutes. Select a browser that aligns with the user's existing browser as provided in START_HERE.md (most likely Chromium). Run `playwright install chromium` (without npx) or another browser as appropriate.

13. Once all packages are installed, it's time to test whether we can extract the <p> element using Playwright:

    - Inform the user that we will need to conduct the scrape through a browser, then ask them to quit Chrome entirely - end your message with "Have you closed all browser windows on your computer?"
    - Once the user confirms that the browser is no longer running, launch a headful browser. On Mac, run `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"` or equivalent for the user's browser. On Windows, run `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-debug"` or equivalent.
    - Next, update the placeholder URL in template_browser_scraper.py with the EXAMPLE_DETAILS_PAGE_URL and run `python3 template_browser_scraper.py`.
    - If this successfully retrieves the first <p> element then we know the scrape worked. If it too fails, ask the user if they noticed anything in particular on the screen, such as a Captcha or error message. Proceed to troubleshoot with the user's help. Do not under any circumstances install other Playwright browsers, Selenium or anything else.

14. Continuing with the approach that has been confirmed to work (either BeautifulSoup or headful browser), create a script based on the sample provided that does the following:

    - Construct a set of relevant search URLs from the search criteria specified by the user in START_HERE.md
    - Locate the appropriate selectors for search results by referring to the user-provided results HTML file
    - Start on the first results page and save items to a CSV file within csv_output containing relevant headers (at a minimum: item title, item URL, results page URL).
    - If results are paginated, save to CSV between each page search instead of storing everything in memory, in case the script fails partway. If using the headful browser approach, open new pages within the same tab and insert a 2-second sleep on each page to allow for JavaScript loading.
    - Exit the results loop once the user's specified limit is reached (max pages/results), or when no more results are available, whichever comes first.
    - Avoid a proliferation of CSV files by keeping everything in a single results CSV.

15. Once all results pages have been saved to CSV, create a script to process each item based on the sample provided that does the following:

    - Open each item URL in turn and look for the appropriate selectors. If using Playwright, these may need to be adapted somewhat from what was saved in selectors.txt
    - Scrape the relevant fields as specified by the and save the results a CSV file within csv_outputs with relevant headers for each field.
    - Append data to the file after each item page rather than just storing in memory, in case the script fails partway.
    - Avoid proliferation of CSVs by appending all records to one CSV.

16. Once all searches have been run and required fields have been scraped, ask the user to inspect the CSV output and confirm if they are happy with the results.

17. If the user wishes to interrupt the scrape partway, use pkill to kill the script and the headful browser.

18. If a scrape was interrupted partway, inspect the partial CSV output and update the script to pick up where it left off, rather than re-scraping existing data.

Reminder: Create a comprehensive to-do list, then proceed with Step 1.
