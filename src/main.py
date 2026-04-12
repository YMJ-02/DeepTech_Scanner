"""
Main Orchestrator for the DeepTech News Automation Bot.
Coordinates crawling, translating, image processing, and uploading.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import os
import re
import random
import logging
from datetime import datetime

# Import modules from src
from scraper import fetch_rss_feeds, save_articles, cleanup_old_articles
from ai_translator import generate_social_post, shorten_social_post
from image_maker import download_and_process_image
from sns_uploader import publish_all

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

KEYWORDS = [
    'chip', 'semiconductor', 'wafer', 'tsmc', 'nvidia', 'intel', 'amd',
    'arm', 'qualcomm', 'samsung', 'foundry', 'gpu', 'ai', 'cpu', 'fab', 'node'
]

POSTED_URLS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "posted_urls.txt"
)


def get_effective_length(text: str) -> int:
    urls = re.findall(r'(https?://[^\s]+)', str(text))
    effective_length = len(text)
    for url in urls:
        effective_length = effective_length - len(url) + 23
    return effective_length


def load_posted_urls() -> set:
    if os.path.exists(POSTED_URLS_FILE):
        with open(POSTED_URLS_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def save_posted_url(url: str):
    with open(POSTED_URLS_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")


def run_bot_job():
    logger.info("Starting Bot Workflow...")

    # 1. Scrape News
    logger.info("--- 1. Scraping News ---")
    articles = fetch_rss_feeds(max_entries=10)
    if not articles:
        logger.warning("No articles found in this run.")
        return

    save_articles(articles)
    cleanup_old_articles(days=7)
    logger.info(f"Scraped {len(articles)} articles.")

    # 2. Duplicate filtering
    posted_urls = load_posted_urls()
    unposted = [a for a in articles if a.get("link") not in posted_urls]

    if not unposted:
        logger.warning("All scraped articles were already posted! Falling back to full list.")
        unposted = articles

    deeptech = [
        a for a in unposted
        if any(kw in (a.get('title', '') + ' ' + a.get('summary', '')).lower() for kw in KEYWORDS)
    ]

    article_to_process = random.choice(deeptech) if deeptech else random.choice(unposted)
    logger.info(f"Selected Article: [{article_to_process.get('source')}] {article_to_process.get('title')}")

    # 3. AI Translation
    logger.info("--- 2. AI Summarization & Translation ---")
    post_data = generate_social_post(article_to_process)

    if not post_data:
        logger.error("AI processing failed. Aborting workflow.")
        return

    post_text = post_data.get("post_text", post_data.get("text", ""))
    final_caption = f"{post_text}\n\n🔗 Source: {post_data.get('source_url')}"

    # Safety catch: shorten if over 280 chars
    attempts = 0
    while get_effective_length(final_caption) > 280 and attempts < 2:
        logger.warning(f"Caption is {get_effective_length(final_caption)} chars. Shortening...")
        post_text = shorten_social_post(post_text)
        final_caption = f"{post_text}\n\n🔗 Source: {post_data.get('source_url')}"
        attempts += 1

    logger.info(f"Generated Text:\n{final_caption}")

    # 4. Image Processing
    logger.info("--- 3. Image Processing ---")
    main_image_url = post_data.get("main_image")
    local_image_path = None

    if main_image_url:
        local_image_path = download_and_process_image(main_image_url)
    else:
        logger.info("No main image found. Skipping image download.")

    # 5. Social Media Posting
    logger.info("--- 4. SNS Upload ---")
    success = publish_all(
        text=final_caption,
        local_image_path=local_image_path
    )

    # Only save URL to posted list if upload succeeded
    if success:
        save_posted_url(article_to_process.get("link", ""))
        logger.info("Workflow completed successfully.")
    else:
        logger.error("Upload failed. URL NOT saved to posted list — will retry next run.")


if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs"), exist_ok=True)
    run_bot_job()
