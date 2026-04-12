"""
Crawler for fetching deeptech news from RSS feeds.
"""

import feedparser
import json
import os
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

RSS_FEEDS = {
    "Tom's Hardware": "https://www.tomshardware.com/feeds/all",
    "Wccftech": "https://wccftech.com/feed/",
    "TechCrunch": "https://techcrunch.com/feed/",
    "VentureBeat": "https://feeds.feedburner.com/venturebeat/SZYF"
}


def get_main_image(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    except Exception as e:
        logger.warning(f"Failed to fetch image for {url}: {e}")
    return None


def _fetch_single_feed(source, url, max_entries):
    """Fetches a single RSS feed and returns a list of article dicts."""
    articles = []
    try:
        feed = feedparser.parse(url)
        if getattr(feed, 'bozo', False) and getattr(feed, 'bozo_exception', None):
            logger.warning(f"Issue parsing feed {source}: {feed.bozo_exception}")

        entries = feed.entries[:max_entries]
        links = [entry.get("link", "") for entry in entries]

        # Fetch images in parallel per feed
        with ThreadPoolExecutor(max_workers=5) as executor:
            image_futures = {executor.submit(get_main_image, link): link for link in links if link}
            image_map = {}
            for future in as_completed(image_futures):
                link = image_futures[future]
                try:
                    image_map[link] = future.result()
                except Exception:
                    image_map[link] = None

        for entry in entries:
            link = entry.get("link", "")
            articles.append({
                "source": source,
                "title": entry.get("title", ""),
                "link": link,
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "main_image": image_map.get(link)
            })
    except Exception as e:
        logger.error(f"Error fetching {source}: {e}")
    return articles


def fetch_rss_feeds(max_entries=10):
    """
    Fetches the latest articles from all predefined RSS feeds in parallel.
    Returns a list of article dicts.
    """
    all_articles = []
    with ThreadPoolExecutor(max_workers=len(RSS_FEEDS)) as executor:
        futures = {
            executor.submit(_fetch_single_feed, source, url, max_entries): source
            for source, url in RSS_FEEDS.items()
        }
        for future in as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                logger.info(f"Fetched {len(result)} articles from {source}")
                all_articles.extend(result)
            except Exception as e:
                logger.error(f"Unexpected error from {source}: {e}")
    return all_articles


def save_articles(articles):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(data_dir, f"raw_articles_{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    logger.info(f"Saved {len(articles)} articles to {file_path}")


def cleanup_old_articles(days=7):
    """Removes raw_articles_*.json files older than `days` days."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    cutoff = datetime.now() - timedelta(days=days)
    removed = 0
    for fname in os.listdir(data_dir):
        if fname.startswith("raw_articles_") and fname.endswith(".json"):
            fpath = os.path.join(data_dir, fname)
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
            if mtime < cutoff:
                os.remove(fpath)
                removed += 1
    if removed:
        logger.info(f"Cleaned up {removed} old article file(s).")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
    logger.info("Starting DeepTech News Scraper...")
    scraped_articles = fetch_rss_feeds(max_entries=10)
    if scraped_articles:
        save_articles(scraped_articles)
        print(json.dumps(scraped_articles[0], indent=2, ensure_ascii=False))
    else:
        logger.warning("No articles fetched.")
