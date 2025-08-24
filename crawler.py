# This script scraps a JavaScript React Website to find all router links including any hidden/commented out.

# to use this script, run:
# 1. Install Python and ensure it's in PATH
# 2. in your CLI run: pip install requests beautifulsoup4
# 3. in your CLI run the following while including a webpage to target
# python crawler.py https://sumeet-singh.com


import requests           # For making HTTP requests to fetch web pages and JS files
from bs4 import BeautifulSoup   # For parsing HTML and extracting script tags
import re                 # For using regular expressions to find route patterns, part of the Python standard library
import argparse           # For parsing command-line arguments, part of the Python standard library

def main():
    parser = argparse.ArgumentParser(description='Crawl a React website for possible internal routes.')
    parser.add_argument('homepage', help='Homepage URL (e.g., https://example.com/)')
    args = parser.parse_args()

    homepage = args.homepage.rstrip('/') + '/'  # Ensure homepage ends with a single slash
    route_regex = re.compile(r'["\']\/[a-zA-Z0-9\-_\/]+["\']')  # Regex to match route-like strings
    found_routes: set[str] = set()  # Store unique routes

    # 1. Get homepage HTML
    resp = requests.get(homepage)  # Fetch homepage HTML
    soup = BeautifulSoup(resp.text, 'html.parser')  # Parse HTML

    # 2. Find all JS bundle URLs
    js_urls: list[str] = []
    for script in soup.find_all('script', src=True):  # Look for <script src="...">
        src: str = str(script.get('src'))
        if src.endswith('.js') or '.js?' in src:      # Only JS files
            if src.startswith('http'):                # Absolute URL
                js_urls.append(src)
            else:                                     # Relative URL
                js_urls.append(homepage + src.lstrip('/'))

    # 3. Download and scan each JS file for route patterns
    for url in js_urls:
        try:
            js_resp = requests.get(url)  # Fetch JS file
            matches = route_regex.findall(js_resp.text)  # Find all route-like strings
            for match in matches:
                found_routes.add(match.strip('"\''))     # Clean and add to set
        except Exception:
            print('Failed to fetch:', url)

    # 4. Print possible internal routes (formatted)
    print('Possible internal routes:')
    for route in sorted(found_routes):
        print(route)

if __name__ == '__main__':
    main()