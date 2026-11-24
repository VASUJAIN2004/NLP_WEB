import json
from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().with_name(".env"))

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



MODEL = "openai/gpt-oss-20b"


def call_groq(prompt, max_tokens=1024):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0
    )
    return response.choices[0].message.content


def clean_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()


class NLPApi:

    def __init__(self, api_key=None):
        pass

    # ── 1. NER ──────────────────────────────────────────────────────────
    def ner(self, text, search_term=None):
        try:
            prompt = f"""You are a Named Entity Recognition engine.
Extract all named entities from the text below.
Return ONLY a valid JSON array. No explanation. No markdown.
Each item must have:
  "text" - the entity as it appears
  "type" - one of: PERSON, ORG, GPE, LOC, DATE, TIME, MONEY, PRODUCT, EVENT, OTHER

Text: {text}"""
            entities = json.loads(clean_json(call_groq(prompt)))
            if search_term:
                entities = [e for e in entities if search_term.lower() in e["text"].lower()]
            return {"ok": True, "data": entities}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 2. Sentiment Analysis ────────────────────────────────────────────
    def sentiment_analysis(self, text):
        try:
            prompt = f"""You are a sentiment analysis engine.
Return ONLY valid JSON. No explanation. No markdown.
Format:
{{"scored_labels": [{{"label": "POSITIVE", "score": 0.0}}, {{"label": "NEGATIVE", "score": 0.0}}, {{"label": "NEUTRAL", "score": 0.0}}]}}
Scores must sum to 1.0.
Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 256)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 3. Abuse Detection ───────────────────────────────────────────────
    def abuse_detection(self, text):
        try:
            prompt = f"""You are a content moderation engine.
Return ONLY valid JSON. No explanation. No markdown.
Format:
{{"labels": ["abusive", "not abusive"], "scores": [0.0, 0.0], "best_label": "not abusive"}}
Scores must sum to 1.0.
Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 256)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 4. Text Summarization ────────────────────────────────────────────
    def summarize(self, text):
        try:
            prompt = f"""Summarize the following text in 2-3 clear, concise sentences.
Return ONLY a JSON object. No explanation. No markdown.
Format: {{"summary": "your summary here", "word_count_original": 0, "word_count_summary": 0}}

Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 512)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 5. Language Detection ────────────────────────────────────────────
    def detect_language(self, text):
        try:
            prompt = f"""Detect the language of the following text.
Return ONLY a JSON object. No explanation. No markdown.
Format: {{"language": "English", "code": "en", "confidence": 0.99, "script": "Latin"}}

Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 128)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 6. Text Translation ──────────────────────────────────────────────
    def translate(self, text, target_language="English"):
        try:
            prompt = f"""Translate the following text to {target_language}.
Return ONLY a JSON object. No explanation. No markdown.
Format: {{"translated_text": "translation here", "source_language": "detected language", "target_language": "{target_language}"}}

Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 512)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 7. Spam Detection ────────────────────────────────────────────────
    def spam_detection(self, text):
        try:
            prompt = f"""You are a spam detection engine.
Classify the text as spam or not spam.
Return ONLY a JSON object. No explanation. No markdown.
Format: {{"labels": ["spam", "not spam"], "scores": [0.0, 0.0], "best_label": "not spam", "reasons": ["reason1", "reason2"]}}
Scores must sum to 1.0.

Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 256)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 8. Grammar Correction ────────────────────────────────────────────
    def grammar_correction(self, text):
        try:
            prompt = f"""You are a grammar correction engine.
Fix all grammar, spelling, and punctuation errors in the text.
Return ONLY a JSON object. No explanation. No markdown.
Format: {{"corrected_text": "fixed text here", "errors_found": [{{"original": "wrong word", "corrected": "right word", "type": "spelling/grammar/punctuation"}}], "error_count": 0}}

Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 512)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ── 9. Keyword Extraction ────────────────────────────────────────────
    def keyword_extraction(self, text):
        try:
            prompt = f"""You are a keyword extraction engine.
Extract the most important keywords and phrases from the text.
Return ONLY a JSON object. No explanation. No markdown.
Format: {{"keywords": [{{"word": "keyword", "score": 0.9, "frequency": 2}}], "top_keywords": ["word1", "word2", "word3"]}}
Score should be between 0 and 1 based on importance.

Text: {text}"""
            data = json.loads(clean_json(call_groq(prompt, 512)))
            return {"ok": True, "data": data}
        except Exception as e:
            return {"ok": False, "error": str(e)}
