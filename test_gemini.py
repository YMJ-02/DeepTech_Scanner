import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('src')
import os
from dotenv import load_dotenv
from ai_translator import generate_social_post

# Load the environment precisely
env_path = os.path.join(os.path.dirname(__file__), "config", ".env")
load_dotenv(env_path)

print(f"Loaded GEMINI_API_KEY: {'Yes' if os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here' else 'No'}")

test_article = {
    "title": "Nvidia reveals 'Blackwell' B200 GPU, claiming it is the world's most powerful AI chip",
    "link": "https://example.com/nvidia-blackwell",
    "summary": "Nvidia has officially unveiled its next-generation Blackwell B200 GPU, packing 208 billion transistors and offering up to 20 petaflops of FP4 computing power. CEO Jensen Huang announced the chip will power the next era of AI datacenters, reducing cost and energy consumption by up to 25x compared to the previous Hopper generation.",
    "main_image": "https://example.com/nvidia-image.jpg"
}

print("\n--- Sending request to Gemini ---")
post_data = generate_social_post(test_article)

if post_data:
    print("\n[SUCCESS] AI processing completed! Below is the generated post text:\n")
    print(post_data.get("post_text", ""))
else:
    print("\n[FAILED] AI returned None.")
