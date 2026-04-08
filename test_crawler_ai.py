import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append('src')
import random
from scraper import fetch_rss_feeds
from ai_translator import generate_social_post

print("Starting Scraper Test (Max 1 article per feed for fast testing)...")
# Temporarily override max_entries to 1 for a quick test
articles = fetch_rss_feeds(max_entries=1)

print(f"\nTotal articles scraped: {len(articles)}")
for i, art in enumerate(articles):
    print(f"{i+1}. [{art['source']}] {art['title']}")

if articles:
    # Pick a random article from the scraped list
    chosen = random.choice(articles)
    print(f"\n--- Randomly selected article for AI Processing ---")
    print(f"Source: {chosen['source']}")
    print(f"Title: {chosen['title']}")
    print("---------------------------------------------------\n")
    
    print("Sending to Gemini AI...")
    post_data = generate_social_post(chosen)
    
    if post_data:
        print("\n\n====== FINAL GENERATED X POST ======")
        print(post_data.get("post_text"))
        print("\nLink:", post_data.get('source_url', ''))
        print("Image URL:", post_data.get('main_image', '(None)'))
        print("====================================")
    else:
        print("AI Processing returned None or failed.")
else:
    print("No articles fetched.")
