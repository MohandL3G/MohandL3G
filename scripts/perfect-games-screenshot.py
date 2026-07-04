from playwright.sync_api import sync_playwright
import subprocess, os

URL = "https://ach.mohandl3g.ly/"
OUTPUT = "assets/perfect-games.png"
SELECTOR = "div.flex.flex-wrap.justify-center.gap-5.py-5"

CAESIUM = "caesiumclt"
QUALITY = "85"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(URL, wait_until="networkidle")
    page.wait_for_selector(SELECTOR, timeout=15000)

    container = page.query_selector(SELECTOR)
    bbox = container.bounding_box()

    clip_height = page.evaluate("""() => {
        const container = document.querySelector('div.flex.flex-wrap.justify-center.gap-5.py-5');
        const cards = container.querySelectorAll(':scope > div');
        const containerRect = container.getBoundingClientRect();
        const count = Math.min(20, cards.length);
        if (count === 0) return 400;
        const lastRect = cards[count - 1].getBoundingClientRect();
        return lastRect.bottom - containerRect.top + 15;
    }""")

    page.screenshot(
        path=OUTPUT,
        full_page=True,
        clip={
            "x": bbox["x"],
            "y": bbox["y"],
            "width": bbox["width"],
            "height": clip_height
        }
    )
    browser.close()

subprocess.run([
    CAESIUM, "-q", QUALITY, "--same-folder-as-input", "--quiet", OUTPUT
], check=True)
