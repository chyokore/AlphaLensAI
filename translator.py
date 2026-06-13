from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("QWEN_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["QWEN_API_KEY"]
    except Exception:
        api_key = None

client = None

if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://hackathon.bitgetops.com/v1"
    )

@st.cache_data(ttl=3600)
def translate_text(text, language):

    if language == "English":
        return text

    if not text.strip():
        return text

    if client is None:
        return text

    try:

        response = client.chat.completions.create(
            model="qwen3.6-plus",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are a professional translator.

Translate ALL text into {language}.

Rules:
- Translate every heading.
- Translate every paragraph.
- Preserve formatting.
- Return ONLY the translation.
- No explanations.
- No commentary.
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        result = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        if "</think>" in result:
            result = (
                result
                .split("</think>")[-1]
                .strip()
            )

        return result

    except Exception:
        return text