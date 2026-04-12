"""
Downloads and processes article images for X (Twitter).
"""

import os
import logging
import requests
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
from datetime import datetime

logger = logging.getLogger(__name__)

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def download_and_process_image(image_url):
    """
    Downloads an image from a URL, crops it to a 16:9 ratio suitable for X (Twitter),
    and saves it to the assets folder.
    Returns the path to the processed image, or None on failure.
    """
    if not image_url:
        logger.warning("No image URL provided.")
        return None

    try:
        logger.info(f"Downloading image from {image_url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')

        # Twitter recommended: 1200x675 (16:9)
        target_w, target_h = 1200, 675

        bg = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=30))

        img_fg = ImageOps.contain(img, (target_w, target_h), Image.Resampling.LANCZOS)
        x = (target_w - img_fg.width) // 2
        y = (target_h - img_fg.height) // 2
        bg.paste(img_fg, (x, y))

        os.makedirs(ASSETS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(ASSETS_DIR, f"tweet_image_{timestamp}.jpg")
        bg.save(filepath, "JPEG", quality=90)

        logger.info(f"Processed image saved to {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Error processing image {image_url}: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
    test_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1000"
    result_path = download_and_process_image(test_url)
    if result_path:
        logger.info(f"Success! Image saved at: {result_path}")
