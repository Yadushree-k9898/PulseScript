from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import re
import json
import random
from datetime import datetime
from urllib.parse import urljoin, urlparse

class AdvancedReviewScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with advanced anti-detection settings"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")  # Try without JS first
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Random user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        self.driver = webdriver.Chrome(options=options)
        
        # Execute stealth scripts
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
    
    def find_company_urls(self, company_name, source):
        """Find potential URLs for the company on different platforms"""
        company_clean = company_name.lower().strip()
        company_slug = re.sub(r'[^a-z0-9\s-]', '', company_clean)
        company_slug = re.sub(r'\s+', '-', company_slug)
        company_slug_no_spaces = company_slug.replace('-', '')
        
        url_patterns = {
            'g2': [
                f"https://www.g2.com/products/{company_slug}",
                f"https://www.g2.com/products/{company_slug}/reviews",
                f"https://www.g2.com/products/{company_slug_no_spaces}",
                f"https://www.g2.com/products/{company_clean.replace(' ', '-')}",
                f"https://www.g2.com/products/{company_clean.replace(' ', '')}",
                f"https://www.g2.com/products/{company_clean.replace(' ', '_')}"
            ],
            'capterra': [
                f"https://www.capterra.com/p/{company_slug}",
                f"https://www.capterra.com/p/{company_slug}/reviews",
                f"https://www.capterra.com/software/{company_slug}",
                f"https://www.capterra.com/reviews/{company_slug}",
                f"https://www.capterra.com/p/{company_slug_no_spaces}"
            ],
            'trustpilot': [
                f"https://www.trustpilot.com/review/{company_slug}",
                f"https://www.trustpilot.com/review/{company_slug_no_spaces}",
                f"https://www.trustpilot.com/review/{company_clean.replace(' ', '')}",
                f"https://www.trustpilot.com/review/{company_clean.replace(' ', '-')}"
            ]
        }
        
        return url_patterns.get(source, [])
    
    def test_url_with_requests(self, url):
        """Test URL using requests first (faster)"""
        try:
            import requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Check for review content
                content = response.text.lower()
                review_indicators = ['review', 'rating', 'star', 'feedback', 'testimonial']
                if any(indicator in content for indicator in review_indicators):
                    return True, response.text
            return False, None
        except:
            return False, None
    
    def test_url_accessibility(self, url):
        """Test if URL is accessible and contains relevant content"""
        try:
            print(f"Testing URL: {url}")
            
            # First try with requests (faster)
            is_accessible, html_content = self.test_url_with_requests(url)
            if is_accessible:
                print(f"URL accessible via requests: {url}")
                return True
            
            # Fallback to selenium
            self.driver.get(url)
            time.sleep(5)  # Wait longer for page load
            
            # Check for common error indicators
            error_indicators = ['404', 'not found', 'error', 'page not found', 'access denied', 'blocked']
            page_title = self.driver.title.lower()
            page_source = self.driver.page_source.lower()
            
            for indicator in error_indicators:
                if indicator in page_title or indicator in page_source:
                    print(f"URL rejected due to error indicator: {indicator}")
                    return False
            
            # Check if page has review-related content
            review_indicators = ['review', 'rating', 'star', 'feedback', 'testimonial', 'opinion']
            has_review_content = any(indicator in page_source for indicator in review_indicators)
            
            if has_review_content:
                print(f"URL accepted - found review content")
                return True
            else:
                print(f"URL rejected - no review content found")
                return False
            
        except Exception as e:
            print(f"Error testing URL {url}: {e}")
            return False
    
    def extract_reviews_from_html(self, html_content, source):
        """Extract reviews from HTML content using BeautifulSoup"""
        soup = BeautifulSoup(html_content, 'html.parser')
        reviews = []
        
        # Multiple strategies to find review containers
        review_containers = []
        
        # Strategy 1: Look for specific review patterns
        patterns = [
            r'.*review.*',
            r'.*rating.*',
            r'.*feedback.*',
            r'.*testimonial.*',
            r'.*comment.*'
        ]
        
        for pattern in patterns:
            containers = soup.find_all('div', class_=re.compile(pattern, re.I))
            review_containers.extend(containers)
        
        # Strategy 2: Look for data attributes
        data_attrs = ['data-testid', 'data-review', 'data-rating', 'data-feedback']
        for attr in data_attrs:
            containers = soup.find_all(attrs={attr: re.compile(r'.*review.*', re.I)})
            review_containers.extend(containers)
        
        # Strategy 3: Look for semantic elements
        semantic_containers = soup.find_all(['article', 'section'], class_=re.compile(r'.*review.*', re.I))
        review_containers.extend(semantic_containers)
        
        # Strategy 4: Look for any element with review-like text
        all_elements = soup.find_all(['div', 'article', 'section'])
        for element in all_elements:
            text = element.get_text().lower()
            if any(word in text for word in ['review', 'rating', 'stars', 'feedback']) and len(text) > 50:
                review_containers.append(element)
        
        # Remove duplicates
        unique_containers = []
        seen = set()
        for container in review_containers:
            container_id = id(container)
            if container_id not in seen and len(container.get_text().strip()) > 30:
                unique_containers.append(container)
                seen.add(container_id)
        
        print(f"Found {len(unique_containers)} potential review containers")
        
        # Extract data from each container
        for i, container in enumerate(unique_containers):
            try:
                review_data = self.extract_review_data_from_container(container, source)
                if review_data:
                    reviews.append(review_data)
                    print(f"Extracted review {i+1}: {review_data.get('title', 'No title')[:50]}...")
            except Exception as e:
                print(f"Error extracting review {i+1}: {e}")
                continue
        
        return reviews
    
    def extract_review_data_from_container(self, container, source):
        """Extract review data from a container"""
        review_data = {
            'title': '',
            'description': '',
            'date': '',
            'rating': '',
            'reviewer': '',
            'source': source.title()
        }
        
        text_content = container.get_text()
        if len(text_content.strip()) < 30:
            return None
        
        # Extract title
        title_selectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', '.title', '.review-title', '.headline']
        for selector in title_selectors:
            title_elem = container.select_one(selector)
            if title_elem and title_elem.get_text().strip():
                title_text = title_elem.get_text().strip()
                if 5 < len(title_text) < 200:
                    review_data['title'] = title_text
                    break
        
        # Extract description
        desc_selectors = ['p', '.text', '.content', '.description', '.review-text', '.review-body']
        description_text = ""
        for selector in desc_selectors:
            desc_elem = container.select_one(selector)
            if desc_elem:
                desc_text = desc_elem.get_text().strip()
                if len(desc_text) > len(description_text) and len(desc_text) > 20:
                    description_text = desc_text
        
        if not description_text:
            # Fallback: use longest text block
            text_blocks = [p.get_text().strip() for p in container.find_all('p')]
            if text_blocks:
                description_text = max(text_blocks, key=len)
        
        review_data['description'] = re.sub(r'\s+', ' ', description_text).strip()
        
        # Extract rating
        rating_patterns = [
            r'(\d+)\s*out\s*of\s*(\d+)',
            r'(\d+)\s*/\s*(\d+)',
            r'(\d+)\s*stars?',
            r'rating[:\s]*(\d+)',
            r'(\d+)\s*★',
            r'(\d+)\s*⭐'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, text_content, re.I)
            if match:
                review_data['rating'] = match.group(1)
                break
        
        # Extract date
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{4})',
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},?\s+\d{4}',
            r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text_content, re.I)
            if match:
                review_data['date'] = match.group(1)
                break
        
        # Extract reviewer
        name_selectors = ['.name', '.author', '.reviewer', '.user', 'h3', 'h4', '.reviewer-name']
        for selector in name_selectors:
            name_elem = container.select_one(selector)
            if name_elem and name_elem.get_text().strip():
                name_text = name_elem.get_text().strip()
                if 2 < len(name_text) < 100:
                    review_data['reviewer'] = name_text
                    break
        
        # Only return if we have substantial content
        if len(review_data['description']) > 30:
            return review_data
        
        return None
    
    def scrape_reviews(self, company_name, source, max_pages=10):
        """Main method to scrape reviews"""
        print(f"Starting advanced scraping for {company_name} from {source}")
        
        # Find potential URLs
        urls = self.find_company_urls(company_name, source)
        working_url = None
        
        for url in urls:
            if self.test_url_accessibility(url):
                working_url = url
                break
        
        if not working_url:
            print(f"No accessible URLs found for {company_name} on {source}")
            return []
        
        # Try to get content with requests first
        is_accessible, html_content = self.test_url_with_requests(working_url)
        if is_accessible:
            print("Using requests for faster scraping...")
            reviews = self.extract_reviews_from_html(html_content, source)
            if reviews:
                return reviews
        
        # Fallback to selenium
        print("Using Selenium for dynamic content...")
        self.driver.get(working_url)
        time.sleep(5)
        
        # Scroll to load content - more aggressive scrolling
        for i in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            # Try to click "Load More" or "Show More" buttons
            try:
                load_more_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Load') or contains(text(), 'Show') or contains(text(), 'More')]")
                for button in load_more_buttons:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        time.sleep(2)
            except:
                pass
        
        # Extract reviews
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        reviews = self.extract_reviews_from_html(str(soup), source)
        
        return reviews
    
    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()

def scrape_g2_reviews_advanced(company_name):
    """Advanced G2 scraping"""
    scraper = AdvancedReviewScraper()
    try:
        return scraper.scrape_reviews(company_name, 'g2')
    finally:
        scraper.close()

def scrape_capterra_reviews_advanced(company_name):
    """Advanced Capterra scraping"""
    scraper = AdvancedReviewScraper()
    try:
        return scraper.scrape_reviews(company_name, 'capterra')
    finally:
        scraper.close()

def scrape_trustpilot_reviews_advanced(company_name):
    """Advanced Trustpilot scraping"""
    scraper = AdvancedReviewScraper()
    try:
        return scraper.scrape_reviews(company_name, 'trustpilot')
    finally:
        scraper.close()
