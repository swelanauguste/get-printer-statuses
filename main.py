from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# List of printer IPs or web URLs
printers = [
  'http://10.137.8.90/'
]

# Setup Chrome options
options = Options()
options.headless = True  # run in background, no visible browser
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

for printer in printers:
    try:
        driver.get(printer)

        # wait for AJAX/JS to load (tweak timing as needed)
        time.sleep(5)

        # Screenshot entire page
        filename = f"printer_status_{printer.split('//')[-1].replace(':', '_')}.png"
        driver.save_screenshot(filename)
        print(f"Saved screenshot for {printer} → {filename}")

    except Exception as e:
        print(f"Failed to capture {printer}: {e}")

driver.quit()
