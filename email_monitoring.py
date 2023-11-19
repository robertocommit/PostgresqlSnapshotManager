import os
import yagmail

gmail = os.getenv("GMAIL")
gmailpw = os.getenv("GMAILPW")

def send_email(subject):
    try:
        content = ['']
        with yagmail.SMTP(gmail, gmailpw) as yag:
            yag.send(gmail, subject, content)
        print("Email sent successfully")
    except:
        print("Error in sending email")
