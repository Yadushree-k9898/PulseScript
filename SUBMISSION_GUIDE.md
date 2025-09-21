# Pulse Coding Assignment - Submission Package

## 🎯 Assignment Requirements Fulfilled

### ✅ 1. Script Requirements

**Input Parameters:**
- ✅ Company Name: `--company` parameter
- ✅ Start Date: `--start_date` parameter (YYYY-MM-DD format)
- ✅ End Date: `--end_date` parameter (YYYY-MM-DD format)
- ✅ Source: `--source` parameter (g2, capterra, trustpilot)

**Output:**
- ✅ JSON file with array of reviews
- ✅ Each review includes:
  - ✅ `title`: Review title
  - ✅ `description`: Review text content
  - ✅ `date`: Review posting date
  - ✅ `rating`: Star rating
  - ✅ `reviewer`: Reviewer name
  - ✅ `source`: Review source platform

### ✅ 2. Script Functionality

**Core Features:**
- ✅ Scrapes reviews from specified source based on company name
- ✅ Parses reviews into required JSON structure
- ✅ Handles pagination (max_pages parameter)
- ✅ Validates and handles errors gracefully
- ✅ Date filtering within specified time period

**Error Handling:**
- ✅ Invalid company names
- ✅ Out-of-range dates
- ✅ Network errors
- ✅ Website structure changes
- ✅ Anti-bot protection

### ✅ 3. Bonus Points

**Third Source Integration:**
- ✅ **Trustpilot** - Specialized in customer reviews and business ratings
- ✅ Same functionality as G2 and Capterra
- ✅ Universal scraper handles all three sources

### ✅ 4. Evaluation Criteria

**Time Efficiency:**
- ✅ Uses requests library for faster scraping when possible
- ✅ Falls back to Selenium only when needed
- ✅ Optimized selectors and parsing

**Code Quality:**
- ✅ Clean, well-commented code
- ✅ Modular design with separate classes
- ✅ Comprehensive error handling
- ✅ Type hints and documentation

**Novelty:**
- ✅ Universal URL detection for any company
- ✅ Multiple fallback strategies
- ✅ Anti-detection measures
- ✅ Dynamic selector detection
- ✅ Smart content extraction

**Output Accuracy:**
- ✅ Comprehensive data extraction
- ✅ Date filtering and validation
- ✅ Clean JSON structure
- ✅ Sample output provided

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Usage
```bash
python main.py --company "Zoom" --start_date "2023-01-01" --end_date "2023-12-31" --source g2
```

### Examples
```bash
# G2 Reviews
python main.py --company "Zoom" --start_date "2023-01-01" --end_date "2023-12-31" --source g2

# Capterra Reviews
python main.py --company "Slack" --start_date "2023-06-01" --end_date "2023-12-31" --source capterra

# Trustpilot Reviews (Bonus Third Source)
python main.py --company "Microsoft" --start_date "2023-01-01" --end_date "2023-12-31" --source trustpilot
```

## 📁 File Structure

```
PulseScript/
├── main.py                    # Main entry point
├── README.md                  # Comprehensive documentation
├── requirements.txt           # Dependencies
├── SUBMISSION_GUIDE.md        # This file
├── src/
│   ├── __init__.py
│   ├── advanced_scraper.py    # Core scraping engine
│   └── utils.py              # Utility functions
└── outputs/
    └── sample_output.json    # Sample JSON output
```

## 🎯 Key Features

1. **Universal Compatibility**: Works with any company name
2. **Three Sources**: G2, Capterra, and Trustpilot (bonus)
3. **Smart Detection**: Adapts to different website structures
4. **Date Filtering**: Precise time period filtering
5. **Error Handling**: Graceful error management
6. **Anti-Detection**: Bypasses common bot protection
7. **Rich Output**: Comprehensive review data extraction

## 📊 Sample Output

See `outputs/sample_output.json` for the exact JSON format with all required fields.

## 🔧 Technical Implementation

- **Selenium WebDriver**: For dynamic content scraping
- **BeautifulSoup**: For HTML parsing
- **Requests**: For faster HTTP requests
- **DateParser**: For flexible date parsing
- **Anti-Detection**: Random user agents, stealth mode
- **Fallback Strategies**: Multiple extraction methods

## ✅ Assignment Completion Status

- [x] All required input parameters
- [x] Complete JSON output format
- [x] G2 and Capterra support
- [x] Third source (Trustpilot) integration
- [x] Pagination handling
- [x] Error validation and handling
- [x] Clean, maintainable code
- [x] Comprehensive documentation
- [x] Sample output provided
- [x] Installation instructions
- [x] Usage examples

**Ready for submission! 🎉**
