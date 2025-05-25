import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("🚀 Starting Amazon Scraper...")

# Setup options and driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: show browser if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

wait = WebDriverWait(driver, 10)

product_data = []

# Scrape 2 pages
for page in range(1, 3):
    url = f"https://www.amazon.in/s?k=toys+and+gifts&page={page}"
    print(f"\n🔄 Fetching page {page}: {url}")
    driver.get(url)

    # Wait for products to load
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot > div")))

    products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    print(f"🔍 Found {len(products)} products on page {page}")

    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, "h2 span").text
        except Exception:
            name = None

        try:
            price = product.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text.replace("₹", "").replace(",", "")
        except Exception:
            price = None

        try:
            rating = product.find_element(By.CSS_SELECTOR, ".a-icon-alt").get_attribute("innerHTML").split(" ")[0]
        except Exception:
            rating = None

        try:
            reviews = product.find_element(By.CSS_SELECTOR, ".a-size-base.s-underline-text").text
        except Exception:
            reviews = None

        try:
            link = product.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
        except Exception:
            link = None

        product_data.append({
            "Product Name": name,
            "Price": price,
            "Rating": rating,
            "Number of Reviews": reviews,
            "Product URL": link
        })

driver.quit()

# Save to CSV
df = pd.DataFrame(product_data)
df.to_csv("amazon_toys_gifts.csv", index=False)
print("\n✅ Scraping complete! Saved to 'amazon_toys_gifts.csv'")
