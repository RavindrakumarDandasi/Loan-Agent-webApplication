import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    AWS_BEARER_TOKEN_BEDROCK = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    DECISION_RULES = {
        "auto_approve_dti": 0.30,
        "auto_reject_dti": 0.60,
        "auto_approve_credit": 750,
        "auto_reject_credit": 500,
    }
