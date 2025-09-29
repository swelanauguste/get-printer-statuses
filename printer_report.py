import json
import os
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv() 


# === LOAD JSON ===
# with open("printers_test.json", "r") as f:
with open("printers.json", "r") as f:
    printers = json.load(f)


# === BUILD HTML TABLE FOR EMAIL ===
def build_printer_table(printers):
    rows = ""
    for p in printers:
        rows += f"""
        <tr>
          <td>{p['id']}</td>
          <td>{p['model']}</td>
          <td>{p['department']}</td>
          <td>{p['location']}</td>
          <td>{p['ip']}</td>
          <td></td>
        </tr>
        """
    html = f"""
    <html>
      <body>
        <p>Attached are the latest printer status screenshots.</p>
        <table border="1" cellspacing="0" cellpadding="5">
          <tr>
            <th>Serial / ID</th>
            <th>Printer Model</th>
            <th>Department</th>
            <th>Location</th>
            <th>IP Address</th>
            <th>Message</th>
          </tr>
          {rows}
        </table>
      </body>
    </html>
    """
    return html


# === CONFIGURATION ===
OUTPUT_FOLDER = "printers"

SMTP_SERVER = "mail.govt.lc"
SMTP_PORT = 587
SMTP_USER = "ict.infrastructure@govt.lc"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TO_EMAILS = ["ict.infrastructure@govt.lc"]
# TO_EMAILS = ["swelan.auguste@govt.lc"]


# === BROWSER SETUP (ignores SSL errors, runs headless) ===
def get_driver():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)


# === CAPTURE PRINTER SCREENS ===
def capture_printer_screenshots():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    driver = get_driver()

    for p in printers:
        url = f"http://{p['ip']}"
        try:
            driver.get(url)
            time.sleep(8)  # wait for page + AJAX
            filename = os.path.join(
                OUTPUT_FOLDER,
                f"{p['model'].replace(' ', '_').replace('-', '').lower()}_{p['department'].replace(' ', '_').replace('-', '').lower()}_{p['location'].replace(' ', '_').replace(',', '').lower()}.png",
            )
            driver.save_screenshot(filename)
            print(f"✅ Saved screenshot for {p['model']} ({p['ip']}) → {filename}")
        except Exception as e:
            print(f"❌ Failed to capture {url}: {e}")

    driver.quit()


# === SEND EMAIL WITH TLS ===
def send_email_with_screenshots():
    today = datetime.now().strftime("%d-%m-%Y")
    msg = EmailMessage()
    msg["Subject"] = f"Daily Printer Status Screenshots – {today}"
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(TO_EMAILS)
    msg.set_content("Attached are the latest printer status screenshots.")
    msg.add_alternative(build_printer_table(printers), subtype="html")

    for file_name in os.listdir(OUTPUT_FOLDER):
        if file_name.lower().endswith(".png"):
            file_path = os.path.join(OUTPUT_FOLDER, file_name)
            with open(file_path, "rb") as f:
                file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="image",
                subtype="png",
                filename=file_name,
            )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    print("📧 Email sent successfully with screenshots attached!")


# === MAIN ===
if __name__ == "__main__":
    capture_printer_screenshots()
    send_email_with_screenshots()
