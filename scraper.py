from playwright.sync_api import sync_playwright
import json
from bs4 import BeautifulSoup

def extract_data_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    elements = []
    for el in soup.body.descendants:
        if el.name:
            if el.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                elements.append({"type": "heading", "tag": el.name, "text": el.get_text(strip=True)})
            elif el.name == "p":
                elements.append({"type": "paragraph", "text": el.get_text(strip=True)})
            elif el.name == "img" and el.get("src"):
                elements.append({"type": "image", "src": el["src"], "alt": el.get("alt", "")})
            elif el.name == "a" and el.get("href"):
                elements.append({"type": "link", "text": el.get_text(strip=True), "href": el["href"]})
            elif el.name == "table":
                elements.append({"type": "table", "html": str(el)})
            else:
                text = el.get_text(strip=True)
                if text:
                    elements.append({"type": "other", "tag": el.name, "text": text})
    return elements

def scrape_page(url, output_json="page_content.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        data = extract_data_from_html(html)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Extracted content saved to {output_json}")
        browser.close()

# 👉 Replace this with your target URL
scrape_page("https://www.qu.edu.qa/en-us/students/admission/undergraduate/Pages/academic-programs.aspx")
