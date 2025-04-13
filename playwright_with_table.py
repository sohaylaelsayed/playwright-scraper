from playwright.sync_api import sync_playwright

def scrape_expanding_table(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Step 1: Click to expand the table (adjust selector as needed)
        try:
            page.click("text='Expand Table'")  # Adjust selector if needed
            page.wait_for_timeout(2000)  # wait for content to expand
        except Exception as e:
            print("Expand button not found or not clickable:", e)

        # Step 2: Extract the table
        rows = page.query_selector_all("table tr")

        table_data = []
        for row in rows:
            cells = row.query_selector_all("th, td")
            cell_contents = []

            for cell in cells:
                # Check for a link inside the cell
                link = cell.query_selector("a")
                if link:
                    text = link.inner_text().strip()
                    href = link.get_attribute("href")
                    cell_contents.append(f"{text} ({href})")
                else:
                    text = cell.inner_text().strip()
                    cell_contents.append(text)

            if cell_contents:
                table_data.append(cell_contents)

        # Step 3: Print or save
        for row in table_data:
            print(row)

        # Optional: Save to CSV
        import csv
        with open("table_data2.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(table_data)

        browser.close()

# Replace with your real URL
scrape_expanding_table("https://www.qu.edu.qa/en-us/students/admission/undergraduate/Pages/academic-programs.aspx")
