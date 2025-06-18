import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# Basic quota tracking
CALL_COUNT = 0
MAX_CALLS_PER_DAY = 100

def search_google(query):
    global CALL_COUNT
    if CALL_COUNT >= MAX_CALLS_PER_DAY:
        return "❗ API call limit reached for today. Please try again tomorrow."

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 2
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        CALL_COUNT += 1

        if "items" not in data:
            return "❗ No results found."

        results = [item["snippet"] for item in data["items"]]
        return "\n\n".join(results)

    except Exception as e:
        return f"❗ Error during search: {e}"


# # ✅ Test thử khi chạy trực tiếp
# if __name__ == "__main__":
#     print(search_google("What is the capital of Vietnam?"))
