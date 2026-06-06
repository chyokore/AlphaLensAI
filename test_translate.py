from translator import translate_text

analysis = """
Bitcoin sentiment is cautiously bullish.
Risk remains elevated.
"""

languages = [
    "Chinese",
    "Spanish",
    "Portuguese",
    "French"
]

for lang in languages:
    print(f"\n--- {lang} ---")
    print(translate_text(analysis, lang))