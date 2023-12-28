import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import AppName

sender_email = "noreply.kerstlan@gmail.com"
from_email = f"{AppName} <noreply.kerstlan@gmail.com>"
password = "lkfm ezcs sffw jkzm"

def email_forgot_password(email: str, new_password: str, username: str):
    subject = f"New password request for: {str.capitalize(username)}"
    receiver_email = email
    body = f"Hi {str.capitalize(username)},\n\nYour new password is: {new_password}"
    send_email(subject, body, [receiver_email])

def email_forgot_username(email: str, username: str):
    subject = f"Username request"
    receiver_email = email
    body = f"Hi ,\n\nYour username is: {username}"
    send_email(subject, body, [receiver_email])

def send_email(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender_email, password)
       smtp_server.sendmail(sender_email, recipients, msg.as_string())
    print("Message sent!")