import os
import json
import random
import replicate
import praw
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load config.json
with open("config.json", "r") as f:
    config = json.load(f)

# --- Setup APIs ---
# Replicate API
replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

# Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=config["reddit_api"]["user_agent"]
)

# --- Pick a theme from config.json ---
theme_name, theme_prompt = random.choice(list(config["themes"].items()))

print(f"✨ Generating wallpaper for theme: {theme_name}")

# Call Replicate (example: stable-diffusion model)
image = replicate_client.run(
    "stability-ai/stable-diffusion:latest",
    input={"prompt": theme_prompt}
)

# Replicate returns a URL for the generated image
image_url = image[0]
print(f"🖼 Wallpaper generated: {image_url}")

# --- Post to Reddit ---
subreddits = config["reddit_api"]["subreddits"]
target_sub = random.choice(subreddits)

title = f"{theme_name.capitalize()} Wallpaper ✨"
reddit.subreddit(target_sub).submit(title, url=image_url)

print(f"✅ Posted to r/{target_sub}: {title}")