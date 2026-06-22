import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BEDROCK_API_KEY = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6")

BEDROCK_URL = (
    f"https://bedrock-runtime.{BEDROCK_REGION}.amazonaws.com"
    f"/model/{MODEL_ID}/converse"
)


def call_bedrock(prompt: str) -> str:
    """
    Calls Amazon Bedrock Converse API using Bedrock API Key.
    """

    if not BEDROCK_API_KEY:
        raise ValueError("Missing AWS_BEARER_TOKEN_BEDROCK in .env file")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEDROCK_API_KEY}"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        BEDROCK_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"Bedrock API Error: {response.status_code} - {response.text}"
        )

    result = response.json()

    return result["output"]["message"]["content"][0]["text"]


def call_bedrock_json(prompt: str) -> dict:
    """
    Calls Bedrock and tries to parse JSON output.
    If parsing fails, returns safe fallback.
    """

    text = call_bedrock(prompt)

    try:
        return json.loads(text)
    except Exception:
        return {
            "decision": "MANUAL_REVIEW",
            "confidence": 0.5,
            "reason": "LLM response was not valid JSON",
            "raw_response": text
        }