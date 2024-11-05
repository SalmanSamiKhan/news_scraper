# Web Scraper for New Age BD Articles

This Python script asynchronously scrapes article data from the New Age BD website's archive for a specified date. It extracts the title, description, and link of each article on the archive page, then retrieves the full title and content from each article's individual page. The data is saved to an Excel file.

## Features

- Asynchronous requests for faster data retrieval
- Logging of each step to monitor progress and errors
- Saves output as an Excel file with all article details

## Requirements

- Python 3.8+
- `aiohttp` - For asynchronous HTTP requests
- `BeautifulSoup4` - For parsing HTML content
- `pandas` - For data manipulation and saving to Excel
- `openpyxl` - For saving Excel files

## Installation

1. Clone the repository or download the script.
2. Install the required packages:
   ```bash
   pip install aiohttp beautifulsoup4 pandas openpyxl





# Web Scraper for New Age BD Articles

This Python script asynchronously scrapes article data from the New Age BD website's archive for a specified date. It extracts the title, description, and link of each article on the archive page, then retrieves the full title and content from each article's individual page. The data is saved to an Excel file.

## Features

- Asynchronous requests for faster data retrieval
- Logging of each step to monitor progress and errors
- Saves output as an Excel file with all article details

## Requirements

- Python 3.8+
- `aiohttp` - For asynchronous HTTP requests
- `BeautifulSoup4` - For parsing HTML content
- `pandas` - For data manipulation and saving to Excel
- `openpyxl` - For saving Excel files

## Installation

1. Clone the repository or download the script.
2. Install the required packages:
   ```bash
   pip install aiohttp beautifulsoup4 pandas openpyxl
   ```

## Usage

1. Set the target date by changing the `date` variable in the script (format: `YYYY-MM-DD`).
2. Run the script:
   ```bash
   python your_script_name.py
   ```
3. The output Excel file will be saved with a filename based on the target date (e.g., `2024-08-06_articles_full_content.xlsx`).

## Logging

The script logs each step to track which articles were successfully fetched and logs any errors encountered during scraping.

## Timing

The script displays the total time taken for scraping at the end.

## Example Output

The output file contains the following columns:
- **Title**: Full title of the article
- **Content**: Full content of the article
- **Link**: Direct link to the article

## Notes

- Ensure a stable internet connection for smooth execution.
- The target date should be in the format `YYYY-MM-DD`.
- This script scrapes public data; check the website's `robots.txt` and terms of service before large-scale scraping.
```

---

This `README.md` provides clear instructions on installation, usage, features, logging, and timing. The script and documentation together form a complete solution for asynchronously scraping articles.