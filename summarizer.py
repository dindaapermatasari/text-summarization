import requests
from bs4 import BeautifulSoup
import re
from transformers import T5ForConditionalGeneration, T5Tokenizer


def preprocess_text(text):
    text = text.lower()
    return text


def fetch_and_clean_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error saat mengambil data: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.find_all("p")
    if not paragraphs:
        paragraphs = soup.find_all("div")
    raw_article = " ".join([p.get_text() for p in paragraphs])

    if not raw_article.strip():
        raise Exception("Tidak dapat menemukan teks di halaman.")

    clean_article = preprocess_text(raw_article)
    return clean_article


def summarize_text(text, max_length=150, min_length=30):
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    input_text = "summarize: " + text
    inputs = tokenizer.encode(
        input_text, return_tensors="pt", max_length=1024, truncation=True
    )

    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


if __name__ == "__main__":
    url = input("Masukkan URL artikel berita: ")
    try:
        article = fetch_and_clean_article(url)
        print("\nTeks Artikel yang Dibersihkan:")
        print(article)
        summary = summarize_text(article)
        print("\nRingkasan:")
        print(summary)
    except Exception as e:
        print(f"Terjadi error: {e}")
