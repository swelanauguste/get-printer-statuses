import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    # 👇 Ignore certificate errors
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")

    driver = webdriver.Chrome(options=options)
    return driver


# List of printer IPs / hostnames
printers = [
    "http://10.137.8.7",
]

driver = get_driver()

for printer in printers:
    try:
        driver.get(printer)
        time.sleep(5)  # wait for page load & AJAX

        filename = f"printers/printer_status_{printer.split('//')[-1].replace(':', '_')}.png"
        driver.save_screenshot(filename)
        print(f"Saved screenshot for {printer} → {filename}")

    except Exception as e:
        print(f"Failed to capture {printer}: {e}")

driver.quit()
