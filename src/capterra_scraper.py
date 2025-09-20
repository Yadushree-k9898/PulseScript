import requests
from bs4 import BeautifulSoup

def scrape_capterra(company_name):
    reviews = []
    base_url = f"https://www.capterra.com/p/{company_name.lower().replace(' ','-')}/reviews"
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "lxml")
        review_divs = soup.find_all("div", class_="review")
        if not review_divs:
            break
        
        for div in review_divs:
            try:
                title = div.find("h3").text.strip()
                description = div.find("p", class_="review-text").text.strip()
                date = div.find("time")["datetime"]
                rating = div.find("div", class_="rating")["aria-label"]
                reviewer = div.find("span", class_="reviewer-name").text.strip()
                reviews.append({
                    "title":title,
                    "description":description,
                    "date":date,
                    "rating":rating,
                    "reviewer":reviewer
                })
            except:
                continue
            
        page += 1
    return reviews
                
    