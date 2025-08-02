# React Website Sitemapper

This Python script crawls a JavaScript-based React website to find all possible internal routes, including those that may be hidden or commented out in the source code.

## Features

- Scans the homepage and all linked JavaScript bundles for route-like strings
- Outputs a formatted list of possible internal routes
- Handles both absolute and relative JS bundle URLs

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
python crawler.py https://test.com
```
