"""Test SMTP email delivery"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
STORE_EMAIL = os.environ.get('STORE_EMAIL', 'info@giantpro.com')

print(f"SMTP Host: {SMTP_HOST}:{SMTP_PORT}")
print(f"SMTP User: {SMTP_USER}")
print(f"Send To:   {STORE_EMAIL}")
print()

msg = MIMEMultipart('alternative')
msg['Subject'] = 'EZ-UP Atlantic - Email Test OK'
msg['From'] = f'EZ-UP Atlantic <{SMTP_USER}>'
msg['To'] = STORE_EMAIL

html = """<html><body style="font-family:Arial,sans-serif;">
<h2 style="color:#003B71;">Email notifications are working!</h2>
<p>Quote request notifications from the EZ-UP Atlantic website will now be delivered to this inbox automatically.</p>
<p style="color:#666;">This is a test email — you can ignore it.</p>
</body></html>"""

msg.attach(MIMEText(html, 'html'))

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, STORE_EMAIL, msg.as_string())
    print("SUCCESS — Email sent!")
    print(f"Check the inbox at {STORE_EMAIL}")
except Exception as e:
    print(f"FAILED — {e}")
