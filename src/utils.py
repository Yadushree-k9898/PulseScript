from datetime import datetime
import dateparser

def filter_reviews_by_date(reviews, start_date, end_date):
    """
    Filters review list by date.
    reviews: list of dicts with 'date' key
    start_date, end_date: string in YYYY-MM-DD format
    """
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    filtered = []
    for review in reviews:
        review_date = dateparser.parse(review.get("date", ""))
        if review_date and start <= review_date <= end:
            filtered.append(review)
            
    return filtered 