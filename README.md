# React Website Crawler

Generic Javascript is simple to scrap, although with the React framework as JS is rendered on the client side it creates a problem for traditional web scrappers. This Python script crawls a JavaScript-based React website to find all possible internal routes, including those that may be hidden or commented out in the source code.

## Limitations

The following are limitations and considerations to take into when using this code.
- Captcha - Find a way to evade captcha e.g. from Cloudflare, possibly with the use of paid API's.

## Features

- Scans the homepage and all linked JavaScript bundles to output a formatted list of possible internal routes
- Handles rate limiting with request time delays
- Handles Honepot fake routes leading to IP Ban/IP retrictions by using free list of free updated proxies 

## Requirements

- Python 3.x installed and added to your system PATH
- The following Python packages:
  - `requests`
  - `beautifulsoup4`

## Installation

Open your terminal or command prompt and run:

```bash
pip install requests beautifulsoup4
```

## Usage

To use this script, run the following command in your CLI, replacing `https://test.com` with the webpage you want to target. Note that the `http://` or `https://` prefix is required.

```bash
python main.py https://test.com
```

![Example Screenshot](./example_screenshot_1.png "Example Screenshot")
