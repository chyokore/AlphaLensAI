from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://hackathon.bitgetops.com/v1"
)

def translate_text(text, language):

    if language == "English":
        return text

    if not text.strip():
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

Translate all text into {language}.

Rules:
- Return ONLY the translation.
- No explanations.
- No commentary.
- No notes.
- Preserve formatting exactly.
- If the text is already in the target language, return it unchanged.
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        result = response.choices[0].message.content.strip()

        if "</think>" in result:
            result = result.split("</think>")[-1].strip()

        return result

    except Exception as e:
        print("Translation error:", e)
        return text