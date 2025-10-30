from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

URL = "https://www.ebay.com/globaldeals/tech"

def scrape_ebay_data():
    driver.get(URL)
    time.sleep(10) 
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  
    last_height = new_height

    products = driver.find_elements(By.XPATH, '//div[@itemscope="itemscope"]')
        
    ebay_data = []
    for product in products:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            title = product.find_element(By.XPATH, './/span[@itemprop="name"]').text
        except: 
            title = "N/A"
        try:
            discounted_price = product.find_element(By.XPATH, './/span[@itemprop="price"]').text
        except:
            discounted_price = "N/A"
        try:
            original_price = product.find_element(By.XPATH, './/span[@class="itemtile-price-strikethrough"]').text
        except: 
            original_price = "N/A"
        try:
            link = product.find_element(By.XPATH, './/a[@itemprop="url"]').get_attribute("href")
        except:
            link = "N/A"

        shipping = "N/A"  

        try:
            from bs4 import BeautifulSoup
            import requests

            resp = requests.get(
                link,
                headers={"User-Agent": ua.random}, 
                timeout=10
            )
            if resp.ok:
                soup = BeautifulSoup(resp.text, "html.parser")
                shipping_div = soup.find("div", class_="ux-labels-values__values-content")

                if shipping_div:
                    bold_span = shipping_div.find("span", class_="ux-textspans--BOLD")
                    spans = shipping_div.find_all("span", class_="ux-textspans")

                    bold_text = bold_span.get_text(strip=True) if bold_span else ""
                    rest_text = spans[2].get_text(strip=True) if len(spans) >= 3 else ""

                    candidate = f"{bold_text} {rest_text}".strip()
                    if candidate:
                        shipping = candidate
        except Exception:
            pass

        ebay_data.append({
                "timestamp": timestamp,
                "Title": title,
                "Original Price": original_price,
                "Discounted Price": discounted_price,
                "Shipping Details": shipping,
                "url": link,
        })

    return ebay_data

def save_to_csv(data):
    file_name = "ebay_tech_deals.csv" 
    df = pd.DataFrame(data) 
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    print("Scraping Ebay Data...")
    scraped_data = scrape_ebay_data()

    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to ebay_tech_deals.csv")
    else:
        print("Failed to scrape data.")

    driver.quit()