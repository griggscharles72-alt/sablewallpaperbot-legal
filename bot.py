import os
import json
import random
import replicate
import praw
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Load config.json safely ---
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("config.json not found!")

# Validate themes
themes = config.get("themes", {})
if not themes:
    raise ValueError("No themes found in config.json")

# --- Setup APIs ---
replicate_token = os.getenv("REPLICATE_API_TOKEN")
assert replicate_token, "REPLICATE_API_TOKEN not set!"
replicate_client = replicate.Client(api_token=replicate_token)

reddit_config = config.get("reddit_api", {})
subreddits = reddit_config.get("subreddits", [])
user_agent = reddit_config.get("user_agent", "WallpaperBot/0.1")

# Check Reddit env variables
required_envs = ["REDDIT_CLIENT_ID", "REDDIT_SECRET", "REDDIT_USER", "REDDIT_PASSWORD"]
for env in required_envs:
    assert os.getenv(env), f"{env} not set!"

if not subreddits:
    raise ValueError("No subreddits configured!")

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=user_agent
)

# --- Pick a theme ---
theme_name, theme_prompt = random.choice(list(themes.items()))
print(f"✨ Generating wallpaper for theme: {theme_name}")

# --- Call Replicate ---
try:
    image = replicate_client.run(
        "stability-ai/stable-diffusion:latest",
        input={"prompt": theme_prompt}
    )
    if not image:
        raise ValueError("No image returned from Replicate API")
    image_url = image[0]
    print(f"🖼 Wallpaper generated: {image_url}")
except Exception as e:
    print(f"❌ Error generating image: {e}")
    image_url = None

# --- Post to Reddit ---
target_sub = random.choice(subreddits)
title = f"{theme_name.capitalize()} Wallpaper ✨"

if image_url:
    try:
        reddit.subreddit(target_sub).submit(title, url=image_url)
        print(f"✅ Posted to r/{target_sub}: {title}")
    except Exception as e:
        print(f"❌ Reddit submission failed: {e}")
else:
    print("❌ Skipping Reddit post because image_url is None")