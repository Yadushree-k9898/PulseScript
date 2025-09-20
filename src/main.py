import argparse
import json
from src import g2_scraper, capterra_scraper, trustpilot_scraper
from src.utils import filter_reviews_by_date

def main():
    parser = argparse.ArgumentParser(description="Scrape product reviews from SaaS review sites.")
    parser.add_argument("--campany", type=str, required=True, help="Company name")
    parser.add_argument("--start_date", type=str, required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end_date", type=str, required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--source", type=str, required=True, choices=["g2", "capterra", "trustpilot"], help="Source to scrape: g2, capterra, or trustpilot")
    
    args = parser.parse_args()
    
    company = args.company
    start_date = args.start_date
    end_date = args.end_date
    source = args.source
    
    if source == "g2":
        reviews = g2_scraper.scrape_g2(company)
    elif source == "capterra":
        reviews = capterra_scraper.scrape_capterra(company)
    elif source == "trustpilot":
        reviews = trustpilot_scraper.scrape_trustpilot(company)
    else:
        print("Invalid source")
        return
    
    reviews_filtered = filter_reviews_by_date(reviews, start_date, end_date)
    
    output_file = f"outputs/reviews_{company.replace(' ', ' ')}_{source}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews_filtered, f, indent=4, ensure_ascii=False)
        
    print(f"Scraped {len(reviews_filtered)} reviews. Saved to {output_file}")
    
if __name__ == "__main__":
    main()
    