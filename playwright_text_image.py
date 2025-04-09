from playwright.sync_api import sync_playwright


from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def extract_text_and_images(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Extract visible text from the page
        visible_text = page.inner_text("body")

        # Extract all image src URLs
        img_elements = page.query_selector_all("img")
        img_urls = [urljoin(url, img.get_attribute("src")) for img in img_elements if img.get_attribute("src")]

        # Print or save results
        print("\n--- TEXT PREVIEW ---\n")
        print(visible_text[:1000], "...")  # Just previewing first 1000 characters

        print("\n--- IMAGE URLs ---\n")
        for i, src in enumerate(img_urls, 1):
            print(f"{i}. {src}")

        # Save to files
        with open("page_text.txt", "w", encoding="utf-8") as f:
            f.write(visible_text)

        with open("image_urls.txt", "w", encoding="utf-8") as f:
            for img in img_urls:
                f.write(img + "\n")

        browser.close()

# Replace with your actual URL
extract_text_and_images("https://www.qu.edu.qa/en-us/students/admission/undergraduate/Pages/academic-programs.aspx")
