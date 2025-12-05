from transformers import pipeline
from typing import Dict
from datetime import datetime
import re

#Underthesea tách từ
try:
    from underthesea import word_tokenize
    USE_UNDERSEA = True
except ImportError:
    USE_UNDERSEA = False

MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

sentiment_pipeline = pipeline(
    task="sentiment-analysis",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)

CORRECTION_DICT = {
    "rat": "rất",
    "rat vui": "rất vui",
    "rat buon": "rất buồn",
    "rat tot": "rất tốt",
    "rat te": "rất tệ",
}


def simple_vi_normalize(text: str) -> str:
    t = text.lower()
    for k, v in CORRECTION_DICT.items():
        t = t.replace(k, v)
    return t


def preprocess_text(text: str, max_chars: int = 50) -> str:
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()
    text = simple_vi_normalize(text)
    text = re.sub(r"\s+", " ", text)

    if len(text) > max_chars:
        text = text[:max_chars]

    if USE_UNDERSEA:
        text = word_tokenize(text, format="text")

    return text


def classify_sentiment(text: str) -> Dict:
    """
    Nhận câu tiếng Việt, trả về:
    {
      "text": <câu gốc>,
      "sentiment": "POSITIVE|NEUTRAL|NEGATIVE",
      "score": float,
      "timestamp": "YYYY-MM-DD HH:MM:SS"
    }

    Ràng buộc đề bài:
    - Câu nhập >= 5 ký tự -> nếu không: raise ValueError("Câu không hợp lệ, thử lại")
    - Nếu score < 0.5 -> gán nhãn NEUTRAL
    """
    if text is None:
        text = ""

    raw_input = text.strip()
    if len(raw_input) < 5:
        raise ValueError("Câu không hợp lệ, thử lại")

    cleaned = preprocess_text(raw_input)

    try:
        result = sentiment_pipeline(cleaned)[0]
    except Exception:
        raise ValueError("Câu không hợp lệ, thử lại")

    raw_label = result["label"].upper()   # NEG / POS / NEU
    score = float(result["score"])

    # Map sang 3 nhãn chuẩn
    if "NEG" in raw_label:
        label = "NEGATIVE"
    elif "POS" in raw_label:
        label = "POSITIVE"
    else:  # NEU hoặc khác
        label = "NEUTRAL"

    if score < 0.5:
        label = "NEUTRAL"

    return {
        "text": raw_input,
        "sentiment": label,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
