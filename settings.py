import os

# Tokens
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Variables
DEFAULT_LLM_NAME = "llama3-70b-8192"
DEFAULT_LLM_PROVIDER = "groq"
DEFAULT_LLM = {
    "llm_provider": DEFAULT_LLM_PROVIDER,
    "llm_name": DEFAULT_LLM_NAME,
}

# paths
CONVERSATIONS_FILE = "./conversations/saved_conversations.json"
