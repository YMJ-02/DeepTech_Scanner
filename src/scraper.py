"""
Auto-generated module: scraper.py
Basic Crawler for fetching deeptech news from RSS feeds.
"""

import feedparser
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define target RSS feeds
RSS_FEEDS = {
    "Tom's Hardware": "https://www.tomshardware.com/feeds/all",
    "Wccftech": "https://wccftech.com/feed/",
    "TechCrunch": "https://techcrunch.com/feed/",
    "VentureBeat": "https://feeds.feedburner.com/venturebeat/SZYF"
}

def get_main_image(url):
    """
    Fetches the article URL and extracts the main image (og:image).
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    except Exception as e:
        print(f"Failed to fetch image for {url}: {e}")
    return None

def fetch_rss_feeds(max_entries=5):
    """
    Fetches the latest articles from the predefined RSS feeds.
    Returns a list of dictionaries containing article metadata.
    """
    articles = []
    
    for source, url in RSS_FEEDS.items():
        print(f"Fetching RSS feed from {source}...")
        try:
            feed = feedparser.parse(url)
            
            if getattr(feed, 'bozo', False) and getattr(feed, 'bozo_exception', None):
                print(f"Warning: Issue parsing feed {source} -> {feed.bozo_exception}")
                
            for entry in feed.entries[:max_entries]:
                link = entry.get("link", "")
                main_image = get_main_image(link) if link else None
                
                article = {
                    "source": source,
                    "title": entry.get("title", ""),
                    "link": link,
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "main_image": main_image
                }
                articles.append(article)
        except Exception as e:
            print(f"Error fetching {source}: {e}")
            
    return articles

def save_articles(articles):
    """
    Saves fetched articles to the data directory as a JSON file.
    """
    # Find the data directory relative to this script's path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(data_dir, f"raw_articles_{timestamp}.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully saved {len(articles)} articles to {file_path}")

if __name__ == "__main__":
    print("Starting DeepTech News Scraper...")
    scraped_articles = fetch_rss_feeds(max_entries=5)
    
    if scraped_articles:
        save_articles(scraped_articles)
        print("\nScraping Sample Output (First Article):")
        print(json.dumps(scraped_articles[0], indent=2, ensure_ascii=False))
    else:
        print("No articles fetched.")
