"""
Translates and summarizes articles into social media friendly format using Gemini API.
"""
import os
import logging
from google import genai
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env")
load_dotenv(env_path)

logger = logging.getLogger(__name__)

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
5. Focus on the ONE most important issue in the article. Explain WHY it matters to the industry or market.
6. CRITICAL: The ENTIRE post (including hashtags) MUST be UNDER 240 CHARACTERS. Use abbreviations to save space.
7. Do not use emojis unless absolutely necessary.
8. Add 2-3 highly relevant hashtags at the end (e.g., #Semiconductor, #DeepTech, #AI).

[Example]
TSMC 2nm mass production pushed to next yr due to GAA thermal issues. Hurts Apple/Nvidia roadmaps while giving Intel and Samsung breathing room to catch up.
#TSMC #Semiconductor
"""

STUB_POST = """TSMC N2 yields reportedly above 70% — if accurate, this accelerates Apple A20 and Nvidia Blackwell Next timelines significantly. Watch for capacity allocation battles in H2.
#TSMC #Semiconductor #AI"""


def generate_social_post(article):
    api_key_env = os.getenv("GEMINI_API_KEY")
    if not api_key_env or api_key_env == "your_gemini_api_key_here":
        logger.warning("GEMINI_API_KEY is missing. Returning stub post.")
        return {
            "post_text": STUB_POST,
            "source_url": article.get('link'),
            "main_image": article.get('main_image')
        }

    try:
        content = f"Title: {article.get('title')}\nSource: {article.get('summary')}\nLink: {article.get('link')}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[SYSTEM_PROMPT.strip(), content]
        )
        return {
            "post_text": response.text.strip(),
            "source_url": article.get("link"),
            "main_image": article.get("main_image")
        }
    except Exception as e:
        logger.error(f"Error during AI processing: {e}")
        return None


def shorten_social_post(text):
    api_key_env = os.getenv("GEMINI_API_KEY")
    if not api_key_env or api_key_env == "your_gemini_api_key_here":
        return text[:200]

    prompt = """
    The following social media post is too long for a single tweet.
    Rewrite it to be MUCH shorter (strictly under 200 characters), keeping the core message.
    Do NOT use ellipses (...). Finish the thought completely.
    Keep the dry, factual, concise tech insider tone. NO markdown.
    Include 1-2 hashtags at the end.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt.strip(), text]
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error during AI shortening: {e}")
        return text[:200]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
    logger.info("Testing AI Translator...")
    test_article = {
        "title": "TSMC 2nm Process Yields Exceed Expectations",
        "link": "https://example.com/tsmc-2nm",
        "summary": "TSMC's upcoming N2 process has reportedly achieved trial yields over 70%.",
        "main_image": "https://example.com/image.jpg"
    }
    result = generate_social_post(test_article)
    if result:
        print(result.get("post_text"))
