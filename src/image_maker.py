"""
Auto-generated module: image_maker.py
Downloads and processes article images for Instagram (1:1 or 4:5 aspect ratio).
"""

import os
import requests
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
from datetime import datetime

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

def download_and_process_image(image_url):
    """
    Downloads an image from a URL, crops it to a 4:5 ratio (Instagram portrait size),
    and saves it to the assets folder.
    Returns the path to the processed image.
    """
    if not image_url:
        print("No image URL provided.")
        return None
        
    try:
        # 1. Download image
        print(f"Downloading image from {image_url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 2. Open image with Pillow
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary (e.g., PNG with alpha)
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
            
        # 3. Create a blurred background and fit the original image (4:5 ratio, 1080x1350)
        # Create a blurred background by stretching and strongly blurring the original image
        bg = img.resize((1080, 1350), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=50))
        
        # Resize original image to fit within the target dimensions while maintaining aspect ratio
        img_fg = ImageOps.contain(img, (1080, 1350), Image.Resampling.LANCZOS)
        
        # Calculate position to center the foreground image on the background
        x = (1080 - img_fg.width) // 2
        y = (1350 - img_fg.height) // 2
        
        # Paste foreground onto background
        bg.paste(img_fg, (x, y))
        img_resized = bg
        
        # 4. Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"feed_image_{timestamp}.jpg"
        filepath = os.path.join(ASSETS_DIR, filename)
        
        img_resized.save(filepath, "JPEG", quality=90)
        print(f"Processed image saved to {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"Error processing image {image_url}: {e}")
        return None

if __name__ == "__main__":
    # Test script with dummy data if run directly
    print("Testing Image Maker...")
    test_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1000&auto=format&fit=crop"
    result_path = download_and_process_image(test_url)
    if result_path:
        print(f"Success! Image saved at: {result_path}")
