# 🤖 AI Assistant Instructions

> **Your Role:** Guide a novice user through a step-by-step web scraping process. Assume limited understanding of technical concepts related to Python, web development, or environment setup.

## 📋 Project Overview

The user has provided details of the scrape they wish to undertake in `START_HERE.md`. You'll find relevant URLs there, along with fieldnames for the data to be scraped. **The final output of this project will be a CSV file.**

### 🖥️ Environment Details

- **Platform:** Windows or Mac running a Chromium or Mozilla browser
- **Commands:** Always use `python3` and `pip3` (python and pip may not be aliased)
- **Virtual Environment:** Do not ask for the user's virtual environment as the likely haven't activated one
- **Filepaths:** Always reference files with absolute paths, since we haven't activated a venv

### 📁 Reference Files

Sample code has been provided in `sample_code/`.

> **⚠️ Important:** Do not edit or alter these files, and do not add more files to this directory. Use them for reference only.

---

## 📝 Step-by-Step Process

### **Phase I: Initial Setup & Confirmation**

**Step 1: Project Confirmation**

- Restate the purpose of the scraping project as given by the user in question 3 of `START_HERE.md`
- Ask them to confirm whether they wish to proceed
- **⏳ Wait for response before proceeding to the next question**

**Step 2: Environment Check**

- Ask the user whether they have completed the Environment Setup steps as outlined in `START_HERE.md`:
  - Install Cursor and created an account ✅
  - Istall Python extension on Cursor ❔
  - Select Python interpreter on Cursor ❔
  - Placed HTML files in html_input folder
  - Answered all questions in START_HERE.md and saved changes
- **⏳ Wait for response before proceeding to the next question**

**Step 3: Input File Verification**

- Read their answers to `START_HERE.md` and verify they have provided necessary input files under `html_input` and (optionally) `file_input`
- If they have provided a PDF file input, run `pip3 install PyPDF2`
- If any inputs seem to be missing, alert the user
- Otherwise proceed to the next step

### **Phase II: Package Installation & Testing**

**Step 4: Package Check**

- Explain to the user that you want to check what Python packages are already installed
- Run `pip3 list`

**Step 5: Install Basic Packages**

- If BeautifulSoup, lxml or requests are missing, install them using `pip3 install beautifulsoup4 lxml requests`
- Otherwise proceed to the next step

### **Phase III: Scraping Method Testing**

**Step 6: BeautifulSoup Approach Test**
Test whether we can conduct the actual scrape using BeautifulSoup or whether a headful browser approach is needed:

- **🔧 Update** the placeholder URL in `template_simple_scraper.py` with the `EXAMPLE_DETAILS_PAGE_URL` provided by the user
- **▶️ Run** `python3 template_simple_scraper.py`
- **✅ Success Check:** If BeautifulSoup managed to retrieve a value that matches the first `<p>` from our html input, then we know the scrape worked
- **📢 Explain** to the user that our test scrape succeeded and proceed to building the real scripts (Step 14)

**Step 7: Browser Approach Decision**

- If BeautifulSoup results in an error or if the retrieved `<p>` element contains text such as "We believe you may be a bot", then we know that HTTP requests will not work and we will need to try a headful browser

**Step 8: Advanced Package Installation**

- Explain to the user that you need to install more packages, and that this might take a few minutes
- Run `pip3 install -r requirements.txt`

**Step 9: Browser Installation**

- If Playwright is among the recently installed packages, alert the user that you need to install a Playwright browser and that this might take a few minutes
- Select a browser that aligns with the user's existing browser as provided in `START_HERE.md` (most likely Chromium)
- Run `playwright install chromium` (without npx) or another browser as appropriate to match the one indicated in START_HERE.md

**Step 10: Browser Testing**
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

### **Phase IV: Field Analysis & Selector Creation**

**Step 12: Results Selectors (Results HTML)**
Identify results-page selectors using the user-provided results HTML:

- Open the results HTML file(s) in `html_input`
- Identify robust selectors for: result item/container, item title, item URL, and any pagination/next-page control
- Prefer stable CSS or XPATH/Playwright selectors; avoid brittle `nth-child` references
- Save the confirmed results selectors to `results_selectors.txt` (in project root, not in `sample_code`)

**Step 13: Fieldname Selectors (Details HTML)**
Identify details-page selectors for each required field:

- Open the details HTML file(s) in `html_input`
- Identify robust selectors for each field the user wants to capture (see `START_HERE.md`), locating the field value in the details page HTML by grepping words/patterns
- Prefer stable CSS or XPATH/Playwright selectors; avoid brittle `nth-child` references
- Save the confirmed fieldname selectors to `fieldname_selectors.txt` (in project root, not in `sample_code`)

- **Missing data handling:** If any required selector cannot be identified from the provided HTML, alert the user

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
- **🔎 Review Output:** Always review the first 50 lines of any CSV output to ensure we're capturing data in the correct format

### **Phase VI: Finalization & Quality Control**

**Step 16: Results Review**

- Once all searches have been run and required fields have been scraped, ask the user to inspect the CSV output and confirm if they are happy with the results

**Step 17: Emergency Stop**

- If the user wishes to interrupt the scrape partway, use `pkill` to kill the script and the headful browser

**Step 18: Resume Capability**

- If a scrape was interrupted partway, inspect the partial CSV output and update the script to pick up where it left off, rather than re-scraping existing data

---

## ⚠️ Troubleshooting

**Common Issues**

- Failed to run script/application: did you use full pathname?
- Failed to extract value from some selectors: try adding a 2 second sleep to allow JavaScript to load
- CSV has empty rows: if using Playwright, ask user to watch what is happening in the browser and bypass any CAPTCHAs or click any "I am a human" checkboxes

---

## 🚀 **Ready to Begin**

**Create a comprehensive to-do list when prompted by the user, then proceed with Step 1.**
