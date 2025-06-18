from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama
from datetime import datetime
import gspread
from dotenv import load_dotenv
import os
from google_search import search_google

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# 1. Google Sheets connection (optional logging)
gc = gspread.service_account(filename="langchain-2025-a4bdd-462307-649b4a58d244.json")
sheet_url = "https://docs.google.com/spreadsheets/d/1b_Tt-iUaR_xjmmq0dJnx7xZ2GYVzZiGBi1mkshCCWZc"
sheet = gc.open_by_url(sheet_url).sheet1

# 2. Load local LLaMA model
llm = Llama(
    model_path="llama-3.2-3b-it-ecommerce-chatbot-q4_k_m.gguf",
    n_ctx=1024,
    n_threads=4,
    temperature=0.7,
    use_mmap=True,
    use_mlock=False,
    low_vram=True
)

# 3. System prompt for chatbot persona
SYSTEM_PROMPT = (
    "You are a top-rated customer service agent named Lytch. "
    "Be polite, clear, and concise. "
    "When listing steps or multiple items, format them using bullet points or numbered lists (1., 2., 3.). "
    "Add line breaks (\\n) between each step for readability. "
    "Avoid long, dense paragraphs."
)

# 4. Home page route
@app.route("/")
def index():
    return render_template("index.html")

# 5. Chat API route
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "❗ You haven't entered anything."})

    # Step 1: Always try LLaMA first
    prompt = SYSTEM_PROMPT + f"\nUser: {user_input}\nLytch:"
    prompt = prompt.replace("\n", " ").replace("\r", "").strip()  # ✅ Thêm dòng này để xử lý lỗi '\n'
    prompt = ''.join([c for c in prompt if 32 <= ord(c) <= 126])  # chỉ giữ ký tự ASCII in được
    response = llm.create_completion(prompt=prompt, max_tokens=512, echo=False)
    raw_output = response["choices"][0]["text"].strip()
    bot_reply = raw_output.split("User:")[0].strip() if "User:" in raw_output else raw_output

    # Step 2: If LLaMA can't answer, fallback to Google Search
    fallback_phrases = [
        "i don't know", "i'm not sure", "i have no information",
        "cannot answer", "outside my knowledge", "i apologize",
        "i do not have any information", "i cannot provide",
        "unfortunately", "i'm unable to answer"
    ]

    if any(phrase in bot_reply.lower() for phrase in fallback_phrases):
        search_result = search_google(user_input)
        return jsonify({"reply": f"🌐 I couldn't answer directly, but here's what I found online:\n\n{search_result}"})

    # Step 3: Log to Google Sheets
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_input, bot_reply])

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
