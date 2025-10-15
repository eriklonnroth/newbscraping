# 🤖 AI Assistant Instructions

> **Your Role:** Guide a novice user through a step-by-step web scraping process. Assume limited understanding of technical concepts related to Python, web development, or environment setup.

## 📋 Project Overview

The user has provided details of the scrape they wish to undertake in `START_HERE.md`. You'll find relevant URLs there, along with fieldnames for the data to be scraped. **The final output of this project will be a CSV file.**

### 🖥️ Environment Details

- **Platform:** Windows or Mac running a Chromium or Mozilla browser
- **Commands:** Always use `python3` and `pip3` (python and pip may not be aliased)
- **Virtual Environment:** Do not ask for the user's virtual environment - use full filepaths

### 📁 Reference Files

Sample scripts have been provided in `sample_scripts/`.

> **⚠️ Important:** Do not edit or alter these files, and do not add more files to this directory. Use them for reference only.

---

## 📝 Step-by-Step Process

### **Phase I: Initial Setup & Confirmation**

**Step 1: Project Confirmation**

- Restate the purpose of the scraping project as given by the user in question 3 of `START_HERE.md`
- Ask them to confirm whether they wish to proceed
- **⏳ Wait for response**

**Step 2: Environment Check**

- Ask the user whether they have completed the Environment Setup steps as outlined in `START_HERE.md`
- **⏳ Wait for response**

**Step 3: Input File Verification**

- Read their answers to `START_HERE.md` and verify they have provided necessary input files under `html_input` and (optionally) `file_input`
- If they have provided a PDF file input, run `pip3 install PyPDF2`
- If any inputs seem to be missing, alert the user
- Otherwise proceed to the next step

### **Phase II: Field Analysis & Selector Creation**

**Step 4: Field Location Analysis**
For each field that the user wants to capture (as provided in question 6 of `START_HERE.md`), check that you can locate it in the inputs:

- **🔍 Locate each field value** in the HTML by grepping likely words or patterns to be found in each fieldname
- **📝 Note the appropriate CSS selector** for the values of each field
- **⚠️ Selector Guidelines:**
  - Avoid brittle `nth-child` references
  - Use XPATH where appropriate
  - If any required field is missing from the provided HTML, alert the user

**Step 5: Save Selectors**

- Save the fieldname selectors to an appropriately named text file, e.g. `selectors.txt`

### **Phase III: Package Installation & Testing**

**Step 6: Package Check**

- Explain to the user that you want to check what Python packages are already installed
- Run `pip3 list`

**Step 7: Install Basic Packages**

- If BeautifulSoup or lxml are missing, install them using `pip3 install beautifulsoup4 lxml`
- Otherwise proceed to the next step

**Step 8: BeautifulSoup Test**

- Create a test script to check whether you can extract the values from your selectors text file using BeautifulSoup
- Run the script and report the extracted values to the user
- Ask them to confirm whether everything looks correct
- **⏳ Await response**

### **Phase IV: Scraping Method Testing**

**Step 9: BeautifulSoup Approach Test**
Test whether we can conduct the actual scrape using BeautifulSoup or whether a headful browser approach is needed:

- **🔧 Update** the placeholder URL in `template_simple_scraper.py` with the `EXAMPLE_DETAILS_PAGE_URL` provided by the user
- **▶️ Run** `python3 template_simple_scraper.py`
- **✅ Success Check:** If BeautifulSoup managed to retrieve a value that matches the first `<p>` from our html input, then we know the scrape worked
- **📢 Explain** to the user that our test scrape succeeded and proceed to building the real scripts (Step 14)

**Step 10: Browser Approach Decision**

- If BeautifulSoup results in an error or if the retrieved `<p>` element contains text such as "We believe you may be a bot", then we know that HTTP requests will not work and we will need to try a headful browser

**Step 11: Advanced Package Installation**

- Explain to the user that you need to install more packages, and that this might take a few minutes
- Run `pip3 install -r requirements.txt`

**Step 12: Browser Installation**

- If Playwright is among the recently installed packages, alert the user that you need to install a Playwright browser and that this might take a few minutes
- Select a browser that aligns with the user's existing browser as provided in `START_HERE.md` (most likely Chromium)
- Run `playwright install chromium` (without npx) or another browser as appropriate

**Step 13: Browser Testing**
Once all packages are installed, test whether we can extract the `<p>` element using Playwright:

- **📢 Inform** the user that we will need to conduct the scrape through a browser, then ask them to quit Chrome entirely - end your message with "Have you closed all browser windows on your computer?"
- **⏳ Wait** for user confirmation that the browser is no longer running
- **🚀 Launch** a headful browser:
  - **Mac:** `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"`
  - **Windows:** `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-debug"`
- **🔧 Update** the placeholder URL in `template_browser_scraper.py` with the `EXAMPLE_DETAILS_PAGE_URL`
- **▶️ Run** `python3 template_browser_scraper.py`
- **✅ Success Check:** If this successfully retrieves the first `<p>` element then we know the scrape worked
- **🆘 Troubleshooting:** If it fails, ask the user if they noticed anything in particular on the screen, such as a Captcha or error message. Proceed to troubleshoot with the user's help
- **⚠️ Important:** Do not under any circumstances install other Playwright browsers, Selenium or anything else

### **Phase V: Main Scraping Implementation**

**Step 14: Search Results Script**
Continuing with the approach that has been confirmed to work (either BeautifulSoup or headful browser), create a script based on the sample provided that does the following:

- **🔗 Construct** a set of relevant search URLs from the search criteria specified by the user in `START_HERE.md`
- **🎯 Locate** the appropriate selectors for search results by referring to the user-provided results HTML file
- **📄 Start** on the first results page and save items to a CSV file within `csv_output` containing relevant headers (at minimum: item title, item URL, results page URL)
- **💾 Pagination Handling:** If results are paginated, save to CSV between each page search instead of storing everything in memory, in case the script fails partway
- **⏱️ Browser Delays:** If using the headful browser approach, open new pages within the same tab and insert a 2-second sleep on each page to allow for JavaScript loading
- **🛑 Exit Conditions:** Exit the results loop once the user's specified limit is reached (max pages/results), or when no more results are available, whichever comes first
- **📁 File Management:** Avoid a proliferation of CSV files by keeping everything in a single results CSV

**Step 15: Details Page Script**
Once all results pages have been saved to CSV, create a script to process each item based on the sample provided that does the following:

- **🔗 Open** each item URL in turn and look for the appropriate selectors
- **🔄 Adapt Selectors:** If using Playwright, these may need to be adapted somewhat from what was saved in `selectors.txt`
- **📊 Scrape** the relevant fields as specified and save the results to a CSV file within `csv_output` with relevant headers for each field
- **💾 Append Data:** Append data to the file after each item page rather than just storing in memory, in case the script fails partway
- **📁 File Management:** Avoid proliferation of CSVs by appending all records to one CSV

### **Phase VI: Finalization & Quality Control**

**Step 16: Results Review**

- Once all searches have been run and required fields have been scraped, ask the user to inspect the CSV output and confirm if they are happy with the results

**Step 17: Emergency Stop**

- If the user wishes to interrupt the scrape partway, use `pkill` to kill the script and the headful browser

**Step 18: Resume Capability**

- If a scrape was interrupted partway, inspect the partial CSV output and update the script to pick up where it left off, rather than re-scraping existing data

---

## 🚀 **Ready to Begin**

**Create a comprehensive to-do list when prompted by the user, then proceed with Step 1.**
