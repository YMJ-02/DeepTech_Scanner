import sys
sys.path.append('src')
from sns_uploader import upload_to_twitter

text = "A" * 200 + "\n\n🔗 Source: https://venturebeat.com/orchestration/google-upgrades-gemini-for-workspace-allowing-it-to-pull-data-from-multiple-sources-and-documents-to-solve-problems"
image_path = "assets/feed_image_20260311_070121.jpg"

print(f"Attempting to post text+image to Twitter from {image_path}...")
success = upload_to_twitter(text, media_path=image_path)
print(f"Upload success block returned: {success}")
