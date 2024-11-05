# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Set up the Selenium WebDriver (ensure ChromeDriver is in PATH)
# driver = webdriver.Chrome()

# # Open the page
# driver.get("https://www.newagebd.net/archive?date=2024-08-05")  # Replace with the actual URL of the page you're scraping

# # Wait until the article links are present
# wait = WebDriverWait(driver, 10)
# article_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.row div.col-md-4 a")))

# # Loop through the article links

# # Create a DataFrame to store the scraped data
# df = pd.DataFrame(columns=['title', 'content'])

# for link in article_links:
#     try:
#         # Ensure we have the latest link by getting the href attribute each time
#         article_url = link.get_attribute('href')
#         print(f"Processing article: {article_url}")
        
#         # Navigate to the article page
#         driver.get(article_url)
        
#         # Wait for the title and content to be available
#         title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.entry-title")))
#         content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.post-content")))

#         # Extract the title and content
#         article_title = title.text
#         article_content = content.text
        
#         # Add the data to the DataFrame
#         df = df.append({'title': article_title, 'content': article_content}, ignore_index=True)
    
#     except Exception as e:
#         print(f"Error processing article: {e}")
#         continue  # Move to the next link if an error occurs

# # Save the DataFrame to an Excel file
# df.to_excel('news_articles.xlsx', index=False)

# # Close the driver once done
# driver.quit()



from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get('https://www.newagebd.net/archive?date=2024-08-05')
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.block-area'))
)

# Initialize lists for data
titles = []
descriptions = []
links = []
full_titles = []
full_contents = []

# Locate all the article elements
articles = driver.find_elements(By.CSS_SELECTOR, 'div.block-area article.card.card-full.hover-a.mb-module')

# Loop through each article to extract initial information
for article in articles:
    try:
        # Get the title and link
        title_element = article.find_element(By.CSS_SELECTOR, 'h2.card-title a')
        title = title_element.text
        link = title_element.get_attribute('href')
        
        # Get the description
        description_element = article.find_element(By.CSS_SELECTOR, 'p.card-text.mb-2.d-none.d-lg-block')
        description = description_element.text
        
        # Append to lists
        titles.append(title)
        descriptions.append(description)
        links.append(link)
        
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Link: {link}")
        print('-' * 80)  # Separator for clarity

    except Exception as e:
        print(f"Error extracting data from an article: {e}")
        continue

# Go to each link to extract the full title and content
for link in links:
    driver.get(link)
    time.sleep(2)  # Add delay to ensure the page loads fully

    try:
        # Extract the full title
        full_title_element = driver.find_element(By.CSS_SELECTOR, 'h1.entry-title')
        full_title = full_title_element.text

        # Extract the content paragraphs
        content_elements = driver.find_elements(By.CSS_SELECTOR, 'div.post-content p')
        full_content = ' '.join([element.text for element in content_elements])

        # Append to lists
        full_titles.append(full_title)
        full_contents.append(full_content)

        print(f"Full Title: {full_title}")
        print(f"Content: {full_content[:150]}...")  # Print first 150 characters for preview
        print('-' * 80)

    except Exception as e:
        print(f"Error extracting data from article page: {e}")
        full_titles.append(None)
        full_contents.append(None)

# Create a DataFrame and save to Excel
df = pd.DataFrame({
    'Title': titles,
    'Description': descriptions,
    'Link': links,
    'Full Title': full_titles,
    'Content': full_contents,
})

df.to_excel('24_08_05_articles_selenium.xlsx', index=False, engine='openpyxl')
print("Data saved to 24_08_05_articles_selenium.xlsx")
