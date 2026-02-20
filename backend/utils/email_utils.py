import smtplib
from email.message import EmailMessage
from backend.config import Config

def send_otp_email(to_email, otp):
    print("EMAIL USER:", Config.EMAIL_USER)
    print("EMAIL PASS:", Config.EMAIL_PASSWORD)

    msg = EmailMessage()
    msg["Subject"] = "Your OTP Verification Code"
    msg["From"] = Config.EMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
        server.send_message(msg)


# In email_utils.py
import os
import smtplib
from email.message import EmailMessage

def send_reset_email(target_email, reset_link):
    msg = EmailMessage()
    msg.set_content(f"Click the link below to reset your SalesMind AI password:\n\n{reset_link}")
    msg["Subject"] = "Reset Your Password - SalesMind AI"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = target_email

    # Use port 587 with STARTTLS (more reliable for Gmail)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Upgrade to secure connection
            # Match the variable name in your .env exactly!
            smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD")) 
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"SMTP Error: {e}")
        raise e