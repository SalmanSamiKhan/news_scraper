# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup
# import pandas as pd
# import logging
# import os
# import time

# # Ensure directories for logs and scraped data exist
# os.makedirs("log", exist_ok=True)
# os.makedirs("scraped_data", exist_ok=True)

# # Set date and file paths
# date = "2024-09-05"
# log_filename = f"log/{date}_scraping.log"
# output_filename = f'scraped_data/{date}_articles.xlsx'

# # Setup logging to file and console
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(log_filename),
#         logging.StreamHandler()  # Also keep console output
#     ]
# )
# logger = logging.getLogger(__name__)

# # Target URL and base URL
# base_url = "https://www.newagebd.net"
# archive_url = f"{base_url}/archive?date={date}"

# # Initialize lists for data
# titles = []
# descriptions = []
# links = []
# full_titles = []
# full_contents = []

# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()

# async def fetch_article_data(url, session):
#     try:
#         # Fetch the main archive page content
#         page_content = await fetch(session, url)
#         soup = BeautifulSoup(page_content, 'html.parser')
        
#         # Locate all articles on the page
#         articles = soup.select('div.block-area article.card.card-full.hover-a.mb-module')
        
#         for article in articles:
#             # Get the title and link
#             title_element = article.select_one('h2.card-title a')
#             title = title_element.text
#             link = title_element['href'] if 'http' in title_element['href'] else base_url + title_element['href']
            
#             # Get the description
#             description_element = article.select_one('p.card-text.mb-2.d-none.d-lg-block')
#             description = description_element.text if description_element else ""
            
#             # Append to lists
#             titles.append(title)
#             descriptions.append(description)
#             links.append(link)
#             logger.info(f"Fetched article: {title}")

#     except Exception as e:
#         logger.error(f"Error fetching archive data: {e}")

# async def fetch_full_content(session, url):
#     try:
#         # Fetch the article page content
#         page_content = await fetch(session, url)
#         soup = BeautifulSoup(page_content, 'html.parser')
        
#         # Extract full title
#         full_title_element = soup.select_one('h1.entry-title')
#         full_title = full_title_element.text if full_title_element else "No title found"
        
#         # Extract full content
#         content_elements = soup.select('div.post-content p')
#         full_content = ' '.join([element.text for element in content_elements]) if content_elements else "No content found"
        
#         # Append to lists
#         full_titles.append(full_title)
#         full_contents.append(full_content)
#         logger.info(f"Fetched full content for: {full_title[:50]}...")

#     except Exception as e:
#         logger.error(f"Error fetching full article content from {url}: {e}")
#         full_titles.append(None)
#         full_contents.append(None)

# async def main():
#     start_time = time.time()
#     async with aiohttp.ClientSession() as session:
#         # Fetch main page articles data
#         await fetch_article_data(archive_url, session)
        
#         # Fetch full content for each article concurrently
#         tasks = [fetch_full_content(session, link) for link in links]
#         await asyncio.gather(*tasks)
    
#     # Log the total time taken
#     total_time = time.time() - start_time
#     logger.info(f"Data scraping completed in {total_time:.2f} seconds.")

# # Run the main async function
# asyncio.run(main())

# Save full data to an Excel file
# df = pd.DataFrame({
#     'Title': titles,
#     'Description': descriptions,
#     'Link': links,
#     'Full Title': full_titles,
#     'Content': full_contents,
# })

# # Save full data to an Excel file
# # df = pd.DataFrame({
# #     'Title': full_titles,
# #     'Content': full_contents,
# #     'Link': links,
# # })

# df.to_excel(output_filename, index=False, engine='openpyxl')
# logger.info(f"Data saved to {output_filename}")





import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
import time

# Ensure directories for logs and scraped data exist
os.makedirs("log", exist_ok=True)
os.makedirs("scraped_data", exist_ok=True)

# Set date and file paths
date = "2024-08-05"
log_filename = f"log/{date}_scraping.log"
output_filename = f'scraped_data/{date}_articles.xlsx'

# Setup logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Also keep console output
    ]
)
logger = logging.getLogger(__name__)

# Target URL and base URL
base_url = "https://www.newagebd.net"
archive_url = f"{base_url}/archive?date={date}"

# Initialize lists for data
titles = []
descriptions = []
links = []
full_titles = []
full_contents = []

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                logger.error(f"Failed to fetch {url}: Status {response.status}")
                return None
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

async def fetch_article_data(url, session):
    try:
        # Fetch the main archive page content
        page_content = await fetch(session, url)
        if page_content is None:
            return  # Exit if the page content couldn't be fetched

        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Locate all articles on the page
        articles = soup.select('div.block-area article.card.card-full.hover-a.mb-module')
        
        for article in articles:
            # Get the title and link
            title_element = article.select_one('h2.card-title a')
            if title_element:
                title = title_element.text
                link = title_element['href'] if 'http' in title_element['href'] else base_url + title_element['href']
            else:
                logger.warning("No title element found.")
                continue  # Skip to the next article if title is not found
            
            # Get the description
            description_element = article.select_one('p.card-text.mb-2.d-none.d-lg-block')
            description = description_element.text if description_element else ""
            
            # Append to lists
            titles.append(title)
            descriptions.append(description)
            links.append(link)
            logger.info(f"Fetched article: {title}")

    except Exception as e:
        logger.error(f"Error fetching archive data: {e}")

async def fetch_full_content(session, url):
    retries = 3  # Number of retries for fetching full content
    for attempt in range(retries):
        try:
            # Fetch the article page content
            page_content = await fetch(session, url)
            if page_content is None:
                logger.warning(f"Failed to fetch content from {url}, attempt {attempt + 1}")
                continue  # Try again

            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Extract full title
            full_title_element = soup.select_one('h1.entry-title')
            full_title = full_title_element.text if full_title_element else "No title found"
            
            # Extract full content
            content_elements = soup.select('div.post-content p')
            full_content = ' '.join([element.text for element in content_elements]) if content_elements else "No content found"
            
            # Append to lists
            full_titles.append(full_title)
            full_contents.append(full_content)
            logger.info(f"Fetched full content for: {full_title[:50]}...")
            return  # Exit after successful fetch

        except Exception as e:
            logger.error(f"Error fetching full article content from {url}, attempt {attempt + 1}: {e}")

    # If all retries fail
    full_titles.append(f"Failed to fetch content from {url} after {retries} attempts")
    full_contents.append("Content could not be retrieved.")

async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        # Fetch main page articles data
        await fetch_article_data(archive_url, session)
        
        # Fetch full content for each article concurrently
        tasks = [fetch_full_content(session, link) for link in links]
        await asyncio.gather(*tasks)
    
    # Log the total time taken
    total_time = time.time() - start_time
    logger.info(f"Data scraping completed in {total_time:.2f} seconds.")

# Run the main async function
asyncio.run(main())

# Save full data to an Excel file
df = pd.DataFrame({
    'Title': full_titles,
    'Content': full_contents,
    'Link': links,
})

df.to_excel(output_filename, index=False, engine='openpyxl')
logger.info(f"Data saved to {output_filename}")
