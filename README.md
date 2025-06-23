You can download my model at my hugging face: https://huggingface.co/Lytchbaball/llama-3.2-3b-it-Ecommerce-ChatBot-Q4_K_M-GGUF

This project uses a LLaMA model that has been fine-tuned on a specific dataset to assist in answering questions related to commerce (e.g., customer support). 

Since the fine-tuned data is limited, I’ve added a Google Web Search feature to fetch external information and enable the chatbot to respond to real-time queries. To enable this functionality, please provide the necessary credentials such as GOOGLE_API_KEY and SEARCH_ENGINE_ID. 

GOOGLE_API_KEY: https://console.cloud.google.com/welcome?inv=1&invt=Ab02rg&project=langchain-2025-a4bdd-462307
SEARCH_ENGINE_ID: https://programmablesearchengine.google.com/about/

Additionally, to keep track of user interactions, I’ve integrated Google Sheets to log both the user’s questions and the chatbot’s responses.
