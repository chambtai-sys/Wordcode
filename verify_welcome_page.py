import os
from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8000/website/")
    page.wait_for_timeout(1000)

    # Copy quick start command
    copy_buttons = page.query_selector_all(".copy-btn")
    if copy_buttons:
        copy_buttons[0].click()
        page.wait_for_timeout(600)

    # Scroll down to Quick Start
    page.evaluate("window.scrollTo(0, 450)")
    page.wait_for_timeout(800)

    # Scroll down to Features
    page.evaluate("window.scrollTo(0, 950)")
    page.wait_for_timeout(800)

    # Scroll down to Interactive Examples
    page.evaluate("window.scrollTo(0, 1500)")
    page.wait_for_timeout(800)

    # Click fizzbuzz tab
    fizzbuzz_tab = page.query_selector("button[data-example='fizzbuzz']")
    if fizzbuzz_tab:
        fizzbuzz_tab.click()
        page.wait_for_timeout(600)

    # Click Run Sample
    run_btn = page.query_selector("#run-sample-btn")
    if run_btn:
        run_btn.click()
        page.wait_for_timeout(800)

    # Scroll back to top hero section for final hero state screenshot
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)

    os.makedirs("/tmp/verification/screenshots", exist_ok=True)
    screenshot_path = "/tmp/verification/screenshots/verification.png"
    page.screenshot(path=screenshot_path)
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/tmp/verification/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/tmp/verification/videos",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
