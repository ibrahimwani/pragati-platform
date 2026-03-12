import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp():
    load_dotenv()
    sender = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    recipient = "ibrahimwani095@gmail.com"  # Hardcoded for test
    
    print(f"--- SMTP Diagnostic ---")
    print(f"Sender: {sender}")
    print(f"Password Check: Length {len(password) if password else 0}")
    
    if not sender or not password:
        print("ERROR: Missing credentials in .env")
        return

    try:
        print("Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)  # Show full SMTP logs
        server.starttls()
        
        print(f"Logging in as {sender}...")
        server.login(sender, password)
        
        print("Preparing message...")
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = "SMTP Test Message"
        msg.attach(MIMEText("This is a test email to verify SMTP configuration.", 'plain'))
        
        print(f"Sending to {recipient}...")
        server.send_message(msg)
        server.quit()
        print("\nSUCCESS: Email sent successfully!")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

if __name__ == "__main__":
    test_smtp()
