import smtplib
import os
from email.message import EmailMessage

# === CONFIGURATION ===
SMTP_SERVER = "172.20.20.40"
SMTP_PORT = 587
SMTP_USER = "ict.infrastructure@govt.lc"
SMTP_PASSWORD = "!T Em@1l"   # Use an app password, not your main one
PRINTERS_FOLDER = "printers"          # Folder with screenshots
TO_EMAILS = ["ict.infrastructure@govt.lc",]
EMAIL_USE_TLS = True

def send_printer_screenshots():
    # Create email
    msg = EmailMessage()
    msg["Subject"] = "Daily Printer Status Screenshots"
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(TO_EMAILS)
    msg.set_content("Attached are the latest printer status screenshots.")

    # Attach all PNGs in folder
    for file_name in os.listdir(PRINTERS_FOLDER):
        if file_name.lower().endswith(".png"):
            file_path = os.path.join(PRINTERS_FOLDER, file_name)
            with open(file_path, "rb") as f:
                file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="image",
                subtype="png",
                filename=file_name,
            )

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully with screenshots!")

if __name__ == "__main__":
    send_printer_screenshots()
