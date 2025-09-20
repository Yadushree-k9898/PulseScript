import requests

urls_to_try = [
    "https://www.g2.com/products/zoom-workplace/reviews",
    "https://www.g2.com/products/zoom-workplace",
    "https://www.g2.com/software/zoom-workplace",
    "https://www.g2.com/products/zoom-workplace/details",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.g2.com/',
    'DNT': '1'
}

for url in urls_to_try:
    print(f"\nTrying URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Title: {response.text.split('<title>')[1].split('</title>')[0] if '<title>' in response.text else 'No title found'}")
    except Exception as e:
        print(f"Error: {str(e)}")