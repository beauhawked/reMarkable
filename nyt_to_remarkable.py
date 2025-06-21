#!/usr/bin/env python3
"""Download NYT top stories and upload them to reMarkable."""
import os
import requests
import subprocess
import pdfkit
from readability import Document
from datetime import datetime

NYT_API_KEY = os.environ.get("NYT_API_KEY")
NYT_SECTION = os.environ.get("NYT_SECTION", "home")
MAX_ARTICLES = int(os.environ.get("MAX_ARTICLES", 5))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "nyt_pdfs")


def slugify(text: str) -> str:
    """Simplistic slugify function."""
    return "".join(c if c.isalnum() else "-" for c in text).strip("-").lower()


def fetch_top_articles():
    url = f"https://api.nytimes.com/svc/topstories/v2/{NYT_SECTION}.json"
    resp = requests.get(url, params={"api-key": NYT_API_KEY})
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])[:MAX_ARTICLES]


def fetch_article_html(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def html_to_pdf(html: str, output_path: str):
    pdfkit.from_string(html, output_path)


def upload_to_remarkable(path: str):
    subprocess.run(["rmapi", "put", path], check=True)


def main():
    if not NYT_API_KEY:
        raise SystemExit("NYT_API_KEY environment variable not set")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    articles = fetch_top_articles()
    for article in articles:
        html = fetch_article_html(article["url"])
        doc = Document(html)
        content = f"<h1>{article['title']}</h1>" + doc.summary()
        pdf_name = f"{datetime.now().date()}_{slugify(article['title'])}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
        html_to_pdf(content, pdf_path)
        upload_to_remarkable(pdf_path)


if __name__ == "__main__":
    main()
