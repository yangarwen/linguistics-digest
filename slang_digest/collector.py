import random
import re
from typing import Dict, List

import requests


URBAN_DICTIONARY_RANDOM_URL = "https://api.urbandictionary.com/v0/random"
QUOTABLE_RANDOM_URL = "https://api.quotable.io/random?tags=famous-quotes|inspirational|wisdom"
FALLBACK_SLANG = [
    {
        "word": "glow-up",
        "definition": "A positive transformation in appearance, confidence, or life circumstances.",
    },
    {
        "word": "rent-free",
        "definition": "When something is stuck in your head or influencing you without effort.",
    },
    {
        "word": "no cap",
        "definition": "A phrase meaning 'no lie' or 'I'm serious.'",
    },
    {
        "word": "low-key",
        "definition": "Something done quietly or subtly, without drawing attention.",
    },
    {
        "word": "main character energy",
        "definition": "A confident attitude like you are the lead in your own story.",
    },
    {
        "word": "vibe check",
        "definition": "An informal way to evaluate the mood or energy of a person or place.",
    },
]


def clean_text(text: str) -> str:
    text = re.sub(r"\[|\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_urban_dictionary_random() -> List[Dict[str, str]]:
    response = requests.get(URBAN_DICTIONARY_RANDOM_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("list", []):
        word = clean_text(item.get("word", "")).strip()
        definition = clean_text(item.get("definition", "")).strip()
        example = clean_text(item.get("example", "")).strip()

        if not word or not definition:
            continue

        display_definition = definition
        if example:
            display_definition += f"\nExample: {example}"

        results.append({"word": word, "definition": display_definition})

    return results


def get_trending_slang(count: int = 5) -> List[Dict[str, str]]:
    slang_items = []
    try:
        random_items = fetch_urban_dictionary_random()
        unique_terms = {}
        for item in random_items:
            if len(slang_items) >= count:
                break
            word = item["word"].lower()
            if word in unique_terms:
                continue
            unique_terms[word] = True
            slang_items.append(item)

    except Exception:
        slang_items = []

    if len(slang_items) < count:
        fallback = [item for item in FALLBACK_SLANG if item["word"] not in {x["word"] for x in slang_items}]
        random.shuffle(fallback)
        while len(slang_items) < count and fallback:
            slang_items.append(fallback.pop())

    return slang_items


def get_daily_quote() -> Dict[str, str]:
    try:
        response = requests.get(QUOTABLE_RANDOM_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "text": clean_text(data.get("content", "")),
            "author": clean_text(data.get("author", "Unknown")),
        }
    except Exception:
        return {
            "text": "A true quote source could not be reached today.",
            "author": "Quote service unavailable",
        }
