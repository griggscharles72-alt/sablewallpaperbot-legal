import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load config.json
with open("config.json", "r") as f:
    config = json.load(f)

print("✅ Config loaded!")
print("Themes available:", ", ".join(config["themes"].keys()))

# Test environment variables
print("Replicate API Token:", os.getenv("REPLICATE_API_TOKEN"))
print("Reddit User:", os.getenv("REDDIT_USER"))
print("PayPal Email:", os.getenv("PAYPAL_EMAIL"))