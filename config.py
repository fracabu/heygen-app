# HeyGen API Configuration
# Get your API key from: https://app.heygen.com/settings > API tab

import os
from dotenv import load_dotenv

load_dotenv()

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

# API Base URL
BASE_URL = "https://api.heygen.com"

# Headers for all requests
def get_headers():
    return {
        "X-Api-Key": HEYGEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
