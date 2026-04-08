"""
Auto-generated module: ai_translator.py
Translates and summarizes articles into social media friendly format using OpenAI API.
"""
import os
import json
from google import genai
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
load_dotenv(env_path)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
[System]
You are a jaded tech researcher/engineer scanning deeptech and stock market trends. 
Read the provided tech/semiconductor article and write an X (Twitter) post IN ENGLISH.

[Constraints - STRICT RULES]
1. MUST write in English only. Do not translate to Korean.
2. Absolutely NO markdown formatting like `**` or `__`.
3. NO AI-like phrasing (e.g., "In conclusion," "According to the article").
4. Use a dry, factual, concise, and slightly cynical tone typical of a tech insider.
5. Focus on the ONE most important issue in the article. Explain WHY it matters to the industry or market, giving a bit of depth rather than just listing shallow bullet points.
6. CRITICAL: The ENTIRE post (including hashtags) MUST be UNDER 240 CHARACTERS. Stay within the limit to prevent API truncation. Omit articles like 'the', 'a' and use abbreviations to save space.
7. Do not use emojis unless absolutely necessary.
8. Add 2-3 highly relevant hashtags at the end (e.g., #Semiconductor, #DeepTech, #AI).

[Example]
TSMC 2nm mass production pushed to next yr due to GAA thermal issues. This delay could seriously hurt Apple/Nvidia roadmaps while giving Intel and Samsung foundries breathing room they desperately need to catch up.
#TSMC #Semiconductor
"""

def generate_social_post(article):
    """
    Generates a summarized and translated social media post using the AI API.
    """
    api_key_env = os.getenv("GEMINI_API_KEY")
    if not api_key_env or api_key_env == "your_gemini_api_key_here":
        print("Warning: GEMINI_API_KEY is missing. Returning stub post.")
        return {
            "post_text": f"🚨 {article.get('title')}\n\n"
                         f"🔹 Point 1 highlights the main breakthrough.\n"
                         f"🔹 Point 2 explains the industry impact.\n"
                         f"🔹 Point 3 breaks down the technical details.\n\n"
                         f"#Semiconductor #AI #TechNews",
            "source_url": article.get('link'),
            "main_image": article.get('main_image')
        }
        
    try:
        content = f"Title: {article.get('title')}\nSource: {article.get('summary')}\nLink: {article.get('link')}"
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[SYSTEM_PROMPT.strip(), content]
        )
        
        ai_response = response.text.strip()
        
        # In a real scenario, you'd parse ai_response into separate fields if needed,
        # but for simple uploading we can just return the raw text.
        return {
            "post_text": ai_response,
            "source_url": article.get("link"),
            "main_image": article.get("main_image")
        }
    except Exception as e:
        print(f"Error during AI processing: {e}")
        return None

def shorten_social_post(text):
    """
    If the text is too long for Twitter, ask AI to aggressively shorten it without using truncation dots.
    """
    api_key_env = os.getenv("GEMINI_API_KEY")
    if not api_key_env or api_key_env == "your_gemini_api_key_here":
        return text[:200]
        
    prompt = """
    The following social media post is too long for a single tweet. 
    Rewrite it to be MUCH shorter (strictly under 200 characters), while keeping the core message exactly the same.
    Do NOT use ellipses (...) to cut off sentences. Finish the thought completely.
    Keep the dry, factual, concise tech insider tone. NO markdown.
    Include 1-2 hashtags at the end.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt.strip(), text]
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error during AI shortening: {e}")
        return text[:200]

if __name__ == "__main__":
    # Test script with dummy data if run directly
    print("Testing AI Translator...")
    test_article = {
        "title": "TSMC 2nm Process Yields Exceed Expectations",
        "link": "https://example.com/tsmc-2nm",
        "summary": "TSMC's upcoming N2 process has reportedly achieved trial yields over 70%, suggesting stable mass production timeline for Apple and Nvidia.",
        "main_image": "https://example.com/image.jpg"
    }
    result = generate_social_post(test_article)
    if result:
        print("\nGenerated Post:")
        print(result.get("post_text") if "post_text" in result else result)
