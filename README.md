# Newbscraping: AI-Assisted Web Scraping for Newbs

This repository provides a **guided, step-by-step process for web scraping using Cursor AI**, designed specifically for beginners with no prior web scraping or programming experience.

## Purpose

Whether you need to extract data from websites for research, business analysis, or personal projects, this repository will walk you through the entire process using Cursor's AI assistant. No coding knowledge required - the AI will handle all the technical aspects while you provide the requirements.

The webscraper is designed to work with websites that lists search results. It will go over each result and extract your desired data. It is not designed for open-ended desk research across multiple websites (try using a tool like ChatGPT Deep Research for that).

## Repository Structure

```
webscraping/
├── START_HERE.md         # Your main starting point - complete the questions here
├── AI_Instructions.md    # Technical instructions for the AI assistant
├── sample_code/          # Example code that the AI can reference
├── html_input/           # Place sample HTML files here
├── file_input/           # Place sample PDF/CSV files here
└── csv_output/           # Your scraped data will be saved here as CSV files
```

## How It Works

1. **Complete the guided questionnaire** in `START_HERE.md` to describe what you want to scrape
2. **Download sample pages** from your target website and place them in the `html_input` folder
3. **Let Cursor AI analyze** your requirements and create custom scraping scripts
4. **Run the scripts** to extract your data into organized CSV files

## Getting Started

### Download or Clone the Project

- **If you use git**: Clone the repository and open it in Cursor.

```bash
git clone https://github.com/eriklonnroth/newbscraping.git
cd newbscraping
```

Then in Cursor, use File > Open Folder to select the `newbscraping` folder you just cloned.

- **If you don't know about git**: Click the green "Code" button on GitHub, choose "Download ZIP", unzip it on your computer, then in Cursor use File > Open Folder and select the unzipped `newbscraping` folder.

## What You'll Need

- Google Chrome or Edge, Firefox, Brave - Safari not supported
- Python 3, available from pythong.org or the Microsoft Store
- Cursor IDE with the Python extension, available at cursor.com (new users get free trial of Pro)

Everything else is handled automatically by the AI assistant!

**👉 Check out `START_HERE.md` to begin your web scraping journey!**

That file contains a simple questionnaire that will guide you through defining your scraping requirements. Once you've completed it, Cursor AI will take over and create the necessary scripts to extract your data.
