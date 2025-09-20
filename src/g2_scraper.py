import requests
from bs4 import BeautifulSoup

def scrape_g2(company_name):
    """
    Scrape reviews from G2 for the given company.
    Returns a list of review dicts.
    """
    
    reviews = []
    base_url =f"https://www.g2.com/products/{company_name.lower().replace(' ', '-')}/reviews"
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "lxml")
        review_divs = soup.find_all("div", class_="paper")
        if not review_divs:
            break
        
        for div in review_divs:
            try:
                title = div.find("h3").text.strip()
                description = div.find("p").text.strip()
                date = div.find("time")["datetime"]
                rating = div.find("div", class_="rating")["aria-label"]
                reviewer = div.find("span", class_="user-name").text.strip()
                reviews.append({
                    "title": title,
                    "description":description,
                    "date":date,
                    "rating":rating,
                    "reviewer":reviewer
                })
            except:
                continue
            
        page += 1
        
    return reviews