from playwright.sync_api import sync_playwright


# --------------------------------------------------
# 1. GET CUSTOM SEARCH NAME FROM USER
# --------------------------------------------------

search_name = input("Enter the Wikipedia search name: ").strip()


# --------------------------------------------------
# 2. VALIDATE USER INPUT
# --------------------------------------------------

# Check that input is not empty
if not search_name:

    print("ERROR: Search name cannot be empty.")
    exit()


# Check that every character is an alphabet or space
if not all(char.isalpha() or char.isspace() for char in search_name):

    print("ERROR: Please enter alphabets and spaces only.")
    exit()


# --------------------------------------------------
# 3. CREATE SCREENSHOT FILE NAME
# --------------------------------------------------

screenshot_name = search_name.replace(" ", "_") + ".png"


# --------------------------------------------------
# 4. START PLAYWRIGHT
# --------------------------------------------------

with sync_playwright() as p:

    # --------------------------------------------------
    # 5. LAUNCH BROWSER
    # --------------------------------------------------

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()


    # --------------------------------------------------
    # 6. NAVIGATION
    # --------------------------------------------------

    print("\nOpening Wikipedia...")

    page.goto("https://www.wikipedia.org/")

    print("Page title:", page.title())


    # --------------------------------------------------
    # 7. TYPING / FILLING
    # --------------------------------------------------

    print("\nSearching for:", search_name)

    search_box = page.locator("input[name='search']")

    search_box.fill(search_name)


    # --------------------------------------------------
    # 8. CLICKING
    # --------------------------------------------------

    print("Clicking Search...")

    search_button = page.locator("button[type='submit']")

    search_button.click()


    # --------------------------------------------------
    # 9. WAITING
    # --------------------------------------------------

    print("Waiting for search result...")

    page.locator("h1").wait_for(state="visible")

    print("Search result loaded.")


    # --------------------------------------------------
    # 10. EXTRACTING DATA
    # --------------------------------------------------

    print("\nExtracting information...")

    # Extract heading
    heading = page.locator("h1").inner_text()

    print("\nHeading:")
    print(heading)


    # Locate valid paragraphs
    paragraphs = page.locator(
        "div.mw-content-ltr p:not(.mw-empty-elt)"
    )

    # Count matching elements
    paragraph_count = paragraphs.count()

    print("\nValid paragraphs found:", paragraph_count)


    # Check whether paragraphs exist
    if paragraph_count > 0:

        first_paragraph = paragraphs.first

        first_paragraph.wait_for(state="visible")

        paragraph_text = first_paragraph.inner_text()

        print("\nFirst paragraph:")
        print(paragraph_text)

    else:

        print("No valid paragraphs were found.")


    # --------------------------------------------------
    # 11. SCREENSHOT
    # --------------------------------------------------

    print("\nTaking screenshot...")

    page.screenshot(path=screenshot_name)

    print("Screenshot saved as:", screenshot_name)


    # --------------------------------------------------
    # 12. CLOSE BROWSER
    # --------------------------------------------------

    browser.close()

    print("\nwikipedia search completed successfully.") 
