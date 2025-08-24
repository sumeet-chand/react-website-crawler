# React Website Internal Route Crawler
# Usage:
#   1. Install Python and ensure it's in PATH
#   2. pip install requests beautifulsoup4
#   3. python main.py https://yourwebsite.com

import requests
from bs4 import BeautifulSoup, Tag
import re
import argparse
import time

# ------------------ Proxy Utilities ------------------
def get_free_proxies() -> list[str]:
    """
    Fetches a list of free HTTP proxies from an online API to bypass IP restrictions.
    Returns:
        list[str]: A list of proxy URLs in the format 'http://ip:port'.
    """
    try:
        resp = requests.get("https://www.proxy-list.download/api/v1/get?type=http")
        proxies = resp.text.strip().split('\r\n')
        return [f"http://{proxy}" for proxy in proxies if proxy]
    except Exception:
        return []

def fetch_with_fallback(session: requests.Session, url: str) -> requests.Response | None:
    """
    Attempts to fetch a URL using the provided session.
    If the direct request fails, tries up to 10 free proxies as a fallback.
    """
    try:
        return session.get(url, timeout=10)
    except Exception:
        proxies = get_free_proxies()
        for proxy_url in proxies[:10]:
            proxy = {"http": proxy_url, "https": proxy_url}
            try:
                resp = session.get(url, proxies=proxy, timeout=10)
                if resp.status_code == 200:
                    print(f"Fetched with proxy: {proxy_url}")
                    return resp
            except Exception:
                continue
        print("All proxy attempts failed.")
        return None

# ------------------ JS & Route Extraction ------------------
from typing import List

def extract_js_urls(soup: BeautifulSoup, homepage: str) -> List[str]:
    """
    Finds all JS bundle URLs from the homepage soup.
    """
    js_urls: List[str] = []
    for script in soup.find_all('script', src=True):
        if isinstance(script, Tag):
            src = str(script.get('src'))
            if src.endswith('.js') or '.js?' in src:
                if src.startswith('http'):
                    js_urls.append(src)
                else:
                    js_urls.append(homepage + src.lstrip('/'))
    return js_urls

def extract_routes_from_js(js_urls: list[str], session: requests.Session, route_regex: re.Pattern[str]) -> set[str]:
    """
    Downloads and scans each JS file for route patterns.
    """
    found_routes: set[str] = set()
    for url in js_urls:
        resp = fetch_with_fallback(session, url)
        if not resp:
            print('Failed to fetch:', url)
            continue
        matches = route_regex.findall(resp.text)
        for match in matches:
            found_routes.add(match.strip('"\''))
        time.sleep(1) # to bypass rate limits
    return found_routes

# ------------------ Main Entry Point ------------------
def main():
    parser = argparse.ArgumentParser(
        description='Crawl a React website for possible internal routes.',
        epilog="""Example:
  python main.py https://www.sumeet-singh.com

Possible internal routes:
  /biography
  /books
  /contactus
  /news
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('homepage', help='Homepage URL (e.g., https://example.com/)')
    args = parser.parse_args()

    homepage = args.homepage.rstrip('/') + '/'
    route_regex = re.compile(r'["]\/[a-zA-Z0-9\-_\/]+["]')
    session = requests.Session()

    # 1. Get homepage HTML (with fallback)
    resp = fetch_with_fallback(session, homepage)
    if not resp:
        print("Failed to fetch homepage.")
        return
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 2. Find all JS bundle URLs
    js_urls = extract_js_urls(soup, homepage)

    # 3. Download and scan each JS file for route patterns (with fallback)
    found_routes = extract_routes_from_js(js_urls, session, route_regex)

    # 4. Print possible internal routes (formatted)
    print('Possible internal routes:')
    for route in sorted(found_routes):
        print(route)

if __name__ == '__main__':
    main()