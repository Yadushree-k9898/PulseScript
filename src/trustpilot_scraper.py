import requests
from bs4 import BeautifulSoup

def scrape_trustpilot(company_name):
    reviews =[]
    base_url=f"https://www.trustpilot.com/review/{company_name.lower().replace(' ', '-')}"
    page=1
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "lxml")
        review_divs = soup.find_all("div", class_="review-card")
        if not review_divs:
            break
        
        for div in review_divs:
            try:
                title = div.find("h2").text.strip()
                description = div.find("p").text.strip()
                date = div.find("time")["datetime"]
                rating = div.find("div", class_="star-rating")[title]
                reviewer = div.find("div", class_="consumer-name").text.strip()
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
        