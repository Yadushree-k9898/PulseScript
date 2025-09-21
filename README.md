# Universal Review Scraper

A powerful, universal web scraping tool that can extract product reviews from G2, Capterra, and Trustpilot for any company. This tool uses advanced techniques to adapt to different website structures and bypass common anti-bot measures.

## Features

- 🚀 **Universal Compatibility**: Works with any company name on supported platforms
- 🔍 **Smart Detection**: Automatically adapts to different website structures
- 📅 **Date Filtering**: Filter reviews by specific date ranges
- 🛡️ **Anti-Detection**: Uses multiple strategies to avoid bot detection
- 📊 **Rich Data**: Extracts title, description, date, rating, reviewer, and source
- 🎯 **Multiple Sources**: Supports G2, Capterra, and Trustpilot
- 📁 **JSON Output**: Clean, structured JSON output for easy processing

## Installation

1. **Clone or download the project**
```bash
git clone <repository-url>
cd PulseScript
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Chrome WebDriver**
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Make sure it's in your PATH or place it in the project directory

## Usage

### Basic Usage

```bash
python src/main.py --company "Zoom" --start_date "2023-01-01" --end_date "2023-12-31" --source g2
```

### Parameters

- `--company`: Company name (e.g., "Zoom", "Slack", "Microsoft Teams")
- `--start_date`: Start date in YYYY-MM-DD format
- `--end_date`: End date in YYYY-MM-DD format
- `--source`: Review source (g2, capterra, or trustpilot)
- `--max_pages`: Maximum pages to scrape (optional, default: 3)

### Examples

**Scrape Zoom reviews from G2:**
```bash
python src/main.py --company "Zoom" --start_date "2023-01-01" --end_date "2023-12-31" --source g2
```

**Scrape Slack reviews from Capterra:**
```bash
python src/main.py --company "Slack" --start_date "2023-06-01" --end_date "2023-12-31" --source capterra
```

**Scrape Microsoft Teams reviews from Trustpilot:**
```bash
python src/main.py --company "Microsoft Teams" --start_date "2023-01-01" --end_date "2023-12-31" --source trustpilot
```

## Output Format

The script generates a JSON file with the following structure:

```json
[
  {
    "title": "Great product for remote work",
    "description": "Zoom has been essential for our remote team. The video quality is excellent and the interface is intuitive...",
    "date": "2023-03-15",
    "rating": "5",
    "reviewer": "John Smith",
    "source": "G2"
  },
  {
    "title": "Reliable video conferencing",
    "description": "We've been using Zoom for over a year now. It's reliable and has all the features we need...",
    "date": "2023-02-28",
    "rating": "4",
    "reviewer": "Sarah Johnson",
    "source": "G2"
  }
]
```

## How It Works

### Universal Scraping Approach

1. **URL Discovery**: Automatically generates multiple possible URLs for the company
2. **Accessibility Testing**: Tests each URL to find the working one
3. **Dynamic Selector Detection**: Uses multiple strategies to find review containers
4. **Content Extraction**: Extracts review data using various fallback methods
5. **Date Filtering**: Filters reviews based on the specified date range
6. **JSON Export**: Saves results in a structured JSON format

### Anti-Detection Features

- Random user agents
- Realistic browser behavior simulation
- Dynamic scrolling patterns
- Multiple selector strategies
- Error handling and retry logic

## Supported Platforms

### G2 (g2.com)
- Business software reviews
- B2B SaaS applications
- Enterprise solutions

### Capterra (capterra.com)
- Software marketplace
- Business applications
- Industry-specific tools

### Trustpilot (trustpilot.com)
- Customer reviews
- Business ratings
- Consumer feedback

## Troubleshooting

### Common Issues

1. **No reviews found**
   - Check if the company name is correct
   - Try different variations of the company name
   - Verify the company exists on the platform

2. **ChromeDriver errors**
   - Ensure ChromeDriver is installed and in PATH
   - Check ChromeDriver version compatibility
   - Update Chrome browser to latest version

3. **Rate limiting**
   - The script includes delays to avoid rate limiting
   - If you encounter issues, try reducing max_pages
   - Consider running during off-peak hours

### Debug Mode

To see more detailed output, you can modify the script to run in debug mode by adding print statements or using logging.

## File Structure

```
PulseScript/
├── src/
│   ├── main.py                    # Main script entry point
│   ├── universal_review_scraper.py # Universal scraping logic
│   ├── utils.py                   # Utility functions
│   └── __init__.py
├── outputs/                       # Generated JSON files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver
- Internet connection

## Dependencies

- selenium>=4.8.0
- beautifulsoup4>=4.11.0
- requests>=2.28.0
- lxml>=4.9.0
- dateparser>=1.1.0

## Legal Notice

This tool is for educational and research purposes. Please ensure you comply with the terms of service of the websites you're scraping and respect their robots.txt files. Use responsibly and ethically.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is open source and available under the MIT License.
