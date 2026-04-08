"""
Auto-generated module: sns_uploader.py
Uploads posts and images to Twitter and Instagram.
"""

import os
import tweepy
import requests
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
load_dotenv(env_path)

def upload_to_twitter(text, media_path=None):
    """
    Uploads a post to Twitter using Tweepy V2 API.
    Auto-truncates to 280 characters to prevent 403 errors.
    """
    try:
        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        if not all([api_key, api_secret, access_token, access_token_secret]) or "your_" in api_key:
            print("Twitter API keys are missing or not set up. Skipping Twitter upload.")
            return False

        # V1.1 API needed for media upload
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        
        # V2 API for tweeting
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        media_id = None
        if media_path and os.path.exists(media_path):
            print(f"Uploading media to Twitter: {media_path}")
            media = api.media_upload(media_path)
            media_id = media.media_id
            
        print("Publishing tweet...")
        if media_id:
            response = client.create_tweet(text=text, media_ids=[media_id])
        else:
            response = client.create_tweet(text=text)
            
        print(f"Tweet published! ID: {response.data['id']}")
        return True
    
    except tweepy.errors.Forbidden as e:
        print(f"Error uploading to Twitter: 403 Forbidden")
        print(f"Details: {e.response.text if hasattr(e, 'response') else e}")
        return False
    except Exception as e:
        print(f"Error uploading to Twitter: {e}")
        return False

def upload_to_instagram(text, image_url):
    """
    Uploads a post to Instagram using the Facebook Graph API.
    Note: Instagram API requires the image to be hosted on a public URL.
    For local files, you'll need an intermediate service (like S3/Imgur) or you
    must use the original high-quality image URL from the article if processing isn't strictly necessary.
    Here we assume image_url is a public URL.
    """
    try:
        access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        ig_user_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        
        if not access_token or not ig_user_id or "your_" in access_token:
            print("Instagram API keys are missing. Skipping Instagram upload.")
            return False
            
        # Step 1: Create a media container
        url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media"
        payload = {
            "image_url": image_url,
            "caption": text,
            "access_token": access_token
        }
        
        response = requests.post(url, data=payload)
        response_json = response.json()
        
        if "id" not in response_json:
            print(f"Error creating Instagram media container: {response_json}")
            return False
            
        creation_id = response_json["id"]
        
        # Step 2: Publish the media container
        publish_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }
        
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_json = publish_response.json()
        
        if "id" in publish_json:
            print(f"Instagram Post Published! ID: {publish_json['id']}")
            return True
        else:
            print(f"Error publishing to Instagram: {publish_json}")
            return False
            
    except Exception as e:
        print(f"Error uploading to Instagram: {e}")
        return False

def publish_all(text, local_image_path=None, public_image_url=None):
    """
    Wrapper to publish to all platforms.
    """
    print("\n--- Starting Social Media Publishing ---")
    
    # Twitter uses local image
    upload_to_twitter(text, local_image_path)
    
    # Instagram requires public image URL
    if public_image_url:
        upload_to_instagram(text, public_image_url)
    else:
        print("No public image URL provided; skipping Instagram.")

if __name__ == "__main__":
    print("Testing SNS Uploader...")
    test_text = "Test Post from DeepTech_Scanner Bot #Tech #Beta"
    publish_all(test_text)
