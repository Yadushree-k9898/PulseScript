from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_g2_reviews(company_slug):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.g2.com/products/{company_slug}/reviews"
    driver.get(url)

    # Wait for reviews container
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='review']"))
        )
    except:
        print("Reviews not loaded")
        driver.quit()
        return []

    # Scroll to load more reviews (repeat if needed)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    reviews = []
    for el in soup.select("div[data-testid='review']"):
        text = el.select_one("p[data-testid='review-body']").get_text(strip=True) if el.select_one("p[data-testid='review-body']") else ""
        rating = el.select_one("div[data-testid='star-rating']").get("aria-label") if el.select_one("div[data-testid='star-rating']") else ""
        date = el.select_one("time").get("datetime") if el.select_one("time") else ""
        reviews.append({"text": text, "rating": rating, "date": date})

    return reviews
