"""
Auto-generated module: main.py
Main Orchestrator for the DeepTech News Automation Bot.
Coordinates crawling, translating, image processing, and uploading.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import os
from datetime import datetime

# Import modules from src
from scraper import fetch_rss_feeds, save_articles
from ai_translator import generate_social_post
from image_maker import download_and_process_image
from sns_uploader import publish_all

def run_bot_job():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Bot Workflow...")
    
    # 1. Scrape News
    print("--- 1. Scraping News ---")
    articles = fetch_rss_feeds(max_entries=3)
    if not articles:
        print("No articles found in this run.")
        return
        
    save_articles(articles)
    print(f"Scraped {len(articles)} articles.")
    
    import random
    
    # Load previously posted urls to prevent duplicates
    posted_urls_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "posted_urls.txt")
    posted_urls = set()
    if os.path.exists(posted_urls_file):
        with open(posted_urls_file, "r", encoding="utf-8") as f:
            posted_urls = set(line.strip() for line in f.readlines())
            
    # Filter articles for deep tech/semiconductor keywords AND ensure they haven't been posted yet
    keywords = ['chip', 'semiconductor', 'wafer', 'tsmc', 'nvidia', 'intel', 'amd', 'arm', 'qualcomm', 'samsung', 'foundry', 'gpu', 'ai', 'cpu', 'fab', 'node']
    deeptech_articles = []
    unposted_articles = []
    
    for art in articles:
        if art.get("link") in posted_urls:
            continue  # Skip already posted articles
        
        unposted_articles.append(art)
        text = (art.get('title', '') + ' ' + art.get('summary', '')).lower()
        if any(kw in text for kw in keywords):
            deeptech_articles.append(art)
            
    # Fallback if everything was already posted in this batch
    if not unposted_articles:
        print("All scraped articles were already posted! Falling back to random choice just to keep the bot alive.")
        unposted_articles = articles
        deeptech_articles = [a for a in articles if any(kw in (a.get('title','')+' '+a.get('summary','')).lower() for kw in keywords)]
    
    # We will prioritize processing an article that specifically relates to deep tech
    if deeptech_articles:
        article_to_process = random.choice(deeptech_articles)
    else:
        article_to_process = random.choice(unposted_articles)
        
    print(f"Selected Article: [{article_to_process.get('source')}] {article_to_process.get('title')}")
    
    # Save the selected article to our posted list so we don't post it again
    with open(posted_urls_file, "a", encoding="utf-8") as f:
        f.write(article_to_process.get("link", "") + "\n")
    
    # 2. AI Translation
    print("\n--- 2. AI Summarization & Translation ---")
    post_data = generate_social_post(article_to_process)
    
    if not post_data:
        print("AI processing failed. Aborting workflow.")
        return
        
    post_text = post_data.get("post_text", post_data.get("text", "")) # Handle both real and mock return formats
    # Construct complete caption, AI response already contains hashtags and emojis
    final_caption = f"{post_text}\n\n🔗 Source: {post_data.get('source_url')}"
    
    import re
    from ai_translator import shorten_social_post
    def get_effective_length(text: str) -> int:
        urls = re.findall(r'(https?://[^\s]+)', str(text))
        effective_length = len(text)
        for url in urls:
            effective_length = effective_length - len(url) + 23
        return effective_length

    # Safety catch: if the AI rambled and broke length limits, ask it to summarize again
    attempts = 0
    while get_effective_length(final_caption) > 280 and attempts < 2:
        print(f"Caption is {get_effective_length(final_caption)} chars. Too long! Asking AI to shorten intelligently...")
        post_text = shorten_social_post(post_text)
        final_caption = f"{post_text}\n\n🔗 Source: {post_data.get('source_url')}"
        attempts += 1
        
    print("Generated Text:\n", final_caption)
    
    # 3. Image Processing
    print("\n--- 3. Image Processing ---")
    main_image_url = post_data.get("main_image")
    local_image_path = None
    
    if main_image_url:
        local_image_path = download_and_process_image(main_image_url)
    else:
        print("No main image found. Skipping image download.")
        
    # 4. Social Media Posting
    print("\n--- 4. SNS Upload ---")
    # For instagram, we need the public URL
    publish_all(
        text=final_caption,
        local_image_path=local_image_path,
        public_image_url=main_image_url
    )
    
    print("\nWorkflow completed successfully for the current iteration.")


if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs"), exist_ok=True)
    
    # GitHub Actions will handle scheduling, so just run once
    run_bot_job()
