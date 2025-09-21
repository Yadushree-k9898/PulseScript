#!/usr/bin/env python3
"""
Universal Review Scraper - Main Entry Point
Scrapes product reviews from G2, Capterra, and Trustpilot for any company
"""

import argparse
import json
import os
import sys
from datetime import datetime
import traceback

# Add src directory to path
sys.path.append('src')

from src.advanced_scraper import scrape_g2_reviews_advanced, scrape_capterra_reviews_advanced, scrape_trustpilot_reviews_advanced
from src.utils import filter_reviews_by_date, validate_date_format

def print_banner():
    """Print the application banner"""
    print("=" * 80)
    print("🚀 UNIVERSAL REVIEW SCRAPER")
    print("=" * 80)
    print("Scrape product reviews from G2, Capterra, and Trustpilot")
    print("Supports any company name with intelligent URL detection")
    print("=" * 80)

def print_usage_examples():
    """Print usage examples"""
    print("\n📖 USAGE EXAMPLES:")
    print("-" * 40)
    print("python main.py --company \"Zoom\" --start_date \"2023-01-01\" --end_date \"2023-12-31\" --source g2")
    print("python main.py --company \"Slack\" --start_date \"2023-06-01\" --end_date \"2023-12-31\" --source capterra")
    print("python main.py --company \"Microsoft Teams\" --start_date \"2023-01-01\" --end_date \"2023-12-31\" --source trustpilot")
    print("\n💡 TIP: Try different company name variations if no results are found")
    print("   Examples: 'Microsoft', 'Microsoft Teams', 'MS Teams', 'Teams'")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Universal Review Scraper - Scrape product reviews from any SaaS review site",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --company "Zoom" --start_date "2023-01-01" --end_date "2023-12-31" --source g2
  python main.py --company "Slack" --start_date "2023-06-01" --end_date "2023-12-31" --source capterra
  python main.py --company "Microsoft Teams" --start_date "2023-01-01" --end_date "2023-12-31" --source trustpilot
        """
    )
    
    parser.add_argument("--company", type=str, required=False, 
                       help="Company name (e.g., 'Zoom', 'Slack', 'Microsoft Teams')")
    parser.add_argument("--start_date", type=str, required=False, 
                       help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, required=False, 
                       help="End date in YYYY-MM-DD format")
    parser.add_argument("--source", type=str, required=False, 
                       choices=["g2", "capterra", "trustpilot"], 
                       help="Review source: g2, capterra, or trustpilot")
    parser.add_argument("--max_pages", type=int, default=10, 
                       help="Maximum pages to scrape (default: 10)")
    parser.add_argument("--show-examples", action="store_true", 
                       help="Show usage examples and exit")
    
    args = parser.parse_args()
    
    # Show examples if requested
    if args.show_examples:
        print_banner()
        print_usage_examples()
        return
    
    # Check if required arguments are provided
    if not all([args.company, args.start_date, args.end_date, args.source]):
        print("❌ Error: Missing required arguments")
        print("   Use --show-examples to see usage examples")
        return
    
    print_banner()
    
    company = args.company
    start_date = args.start_date
    end_date = args.end_date
    source = args.source
    max_pages = args.max_pages
    
    # Validate date format
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        print("❌ Error: Invalid date format. Please use YYYY-MM-DD")
        print("   Example: --start_date 2023-01-01 --end_date 2023-12-31")
        return
    
    # Validate date range
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if start_dt > end_dt:
            print("❌ Error: Start date must be before end date")
            return
    except ValueError:
        print("❌ Error: Invalid date format. Please use YYYY-MM-DD")
        return
    
    print(f"🎯 Target: {company}")
    print(f"🌐 Source: {source.upper()}")
    print(f"📅 Date Range: {start_date} to {end_date}")
    print(f"📄 Max Pages: {max_pages}")
    print("-" * 80)
    
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    try:
        print(f"🔍 Starting to scrape reviews from {source.upper()}...")
        print("   This may take a few minutes depending on the website...")
        
        # Scrape reviews based on source
        if source == "g2":
            reviews = scrape_g2_reviews_advanced(company)
        elif source == "capterra":
            reviews = scrape_capterra_reviews_advanced(company)
        elif source == "trustpilot":
            reviews = scrape_trustpilot_reviews_advanced(company)
        else:
            print("❌ Invalid source")
            return
        
        if not reviews:
            print("❌ No reviews found. This could be due to:")
            print("   • Company name not found on the platform")
            print("   • No reviews available for the specified time period")
            print("   • Website structure changes or anti-bot protection")
            print("   • Try different company name variations")
            print("\n💡 Suggestions:")
            print("   • Try: 'Microsoft' instead of 'Microsoft Teams'")
            print("   • Try: 'Zoom' instead of 'Zoom Video Communications'")
            print("   • Try: 'Slack' instead of 'Slack Technologies'")
            return
        
        print(f"✅ Found {len(reviews)} total reviews before date filtering")
        
        # Filter reviews by date
        reviews_filtered = filter_reviews_by_date(reviews, start_date, end_date)
        
        print(f"📅 After date filtering: {len(reviews_filtered)} reviews")
        
        if not reviews_filtered:
            print("⚠️  No reviews found in the specified date range")
            print("   Try expanding your date range or check if the company has reviews")
            return
        
        # Save to JSON file
        output_file = f"outputs/reviews_{company.replace(' ', '_')}_{source}_{start_date}_{end_date}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(reviews_filtered, f, indent=4, ensure_ascii=False)
        
        print(f"💾 Successfully saved {len(reviews_filtered)} reviews to {output_file}")
        
        # Print summary
        print("\n📊 REVIEW SUMMARY:")
        print("-" * 50)
        if reviews_filtered:
            sample = reviews_filtered[0]
            print("📝 Sample Review:")
            for key, value in sample.items():
                if value:
                    display_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    print(f"   {key.upper()}: {display_value}")
        
        print(f"\n🎉 Scraping completed successfully!")
        print(f"📁 Output file: {output_file}")
        print(f"📊 Total reviews: {len(reviews_filtered)}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
        return
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        print("\n🔧 Debug information:")
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
