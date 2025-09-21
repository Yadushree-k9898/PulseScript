from datetime import datetime
import dateparser
import re

def validate_date_format(date_string):
    """
    Validate if date string is in YYYY-MM-DD format
    """
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_string):
        return False
    
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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

def clean_text(text):
    """
    Clean and normalize text content
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', str(text)).strip()
    
    # Remove common HTML artifacts
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    return text 