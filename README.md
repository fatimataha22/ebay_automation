# Ebay_Automation
## Methodology 
This project builds a complete data pipeline for analyzing live eBay Global Tech Deals.
The workflow consisted of three main stages:
### 1. Web Scraping (scraper.py):
- Used Selenium to scrape product data from eBay Tech Deals
- Extracted details such as timestamp, title, price, original price, shipping info, and item URL.
- Saved results into ebay_tech_deals.csv and automated updates every 3 hours using GitHub Actions.
### 2. Data Cleaning (clean_data.py):
- Removed duplicate and invalid rows (especially entries with Title = NA).
- Cleaned Discounted Price and Priginal Price columns by removing symbols and formatting inconsistencies.
- Replaced missing Original Price values with price.
- Normalized missing Shipping Details information as “Shipping info unavailable.”
- Calculated the Discount Percentage
- Saved the cleaned dataset as cleaned_ebay_deals.csv.
### 3. Exploratory Data Analysis (EDA.ipynb):
Performed detailed analysis and visualization on the cleaned dataset using Pandas, Matplotlib, and Seaborn.

## Key Findings from EDA
### Time Series Analysis
All recorded deals fall at hour 5, because the dataset comes from a single scraping run saved at that time. With multiple runs across different hours, we’d expect bars at additional hours.
### Price and Discount Analysis
Product prices on eBay Tech Deals are heavily concentrated under $500, with a few high-end items creating a long right increase to $4000.
The majority of discounts fall under 10%, though a smaller portion of listings enjoy significant reductions (30–60%).
A clear correlation between original and discounted prices confirms consistent pricing behavior across listings.
### Shipping Information Analysis
Most eBay Tech Deals did not include specific shipping information — over 95% of the listings were labeled as “Shipping info unavailable.”
Only a handful of products displayed free or timed delivery options.
### Text Analysis on Product Titles
Text analysis of product titles reveals a clear dominance of Apple-related products, with “Apple” and “iPhone” being the most frequent keywords.
Other brands such as “Samsung” and categories like “Laptop” and “Tablet” appear much less often, indicating that the scraped deals were heavily focused on Apple devices.
### Price Difference Analysis
The majority of products show modest savings under $100, suggesting that most eBay Tech Deals feature relatively small discounts.
Only a few listings show larger reductions exceeding $500, representing premium items or special promotional offers.
### Top 5 Deals by Discount
The highest discount (≈67%) was found on the Soundcore Liberty 4 SE Earbuds, followed by large reductions on the Sigma Lens Converter and Apple iPhone 14 Pro.

## Challenges Faced
- One of the challenges i faced was that when i ran the code on VS code, I got a lot of filled "Shipping Details" rows, but when i uploaded it on github and let it scrape data on itself for 2 days, most of the "Shipping Details" were "NA".
- Some products were scraped twice, but the second time was missing all the values but the Discounted Price, so I had to remove the products with "NA" as title.
- Sometimes the scraper was taking more than 15 mins to run. 

## Potential Improvements
- Use API-based scraping if available to improve data accuracy and speed.
- Enhance text analysis with NLP techniques (tokenization, word clouds, or sentiment scoring).
- Increase duration of scraping (beyond 2 days) to analyze trends over a longer period