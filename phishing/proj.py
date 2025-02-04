import imaplib
import email
from email.header import decode_header
from urllib.parse import urlparse
import re

# Function to check if a URL is suspicious
def is_suspicious_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if not domain:  # Invalid URL
        return True
    if re.search(r'\d+\.\d+\.\d+\.\d+', domain):  # IP address
        return True
    if len(domain.split('.')) > 3:  # Too many subdomains
        return True
    return False

# Function to detect phishing
def detect_phishing(subject, sender, body, urls):
    reasons = []
    # Check suspicious sender
    if sender.split('@')[-1] not in ['gmail.com', 'yahoo.com', 'outlook.com']:
        reasons.append("Suspicious sender domain.")
    # Check suspicious content
    phishing_phrases = ["urgent", "click here", "verify", "password reset"]
    if any(phrase in body.lower() or phrase in subject.lower() for phrase in phishing_phrases):
        reasons.append("Suspicious language detected.")
    # Check suspicious URLs
    for url in urls:
        if is_suspicious_url(url):
            reasons.append(f"Suspicious URL detected: {url}")
    return reasons if reasons else ["Safe"]

# Connect to the email server
def connect_to_email(username, password, imap_server):
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select("inbox")  # Connect to inbox
        return mail
    except Exception as e:
        print(f"Error connecting to email: {e}")
        return None

# Fetch and analyze emails
def fetch_emails(mail):
    try:
        # Search all emails
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        for email_id in email_ids[:10]:  # Fetch the first 10 emails for simplicity
            # Fetch email by ID
            res, msg = mail.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    # Parse email
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    subject = subject.decode() if isinstance(subject, bytes) else subject
                    sender = msg.get("From")
                    # Get email body
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    # Extract URLs
                    urls = re.findall(r'(https?://\S+)', body)
                    # Analyze the email
                    reasons = detect_phishing(subject, sender, body, urls)
                    print(f"\nEmail from: {sender}")
                    print(f"Subject: {subject}")
                    print(f"Analysis: {'; '.join(reasons)}")
    except Exception as e:
        print(f"Error fetching emails: {e}")

# Main function
if __name__ == "__main__":
    # Replace with your credentials
    username = "varunsiva88@gmail.com"
    password = "rockstarvarun@888"
    imap_server = "imap.gmail.com"  # IMAP server for Gmail

    mail = connect_to_email(username, password, imap_server)
    if mail:
        fetch_emails(mail)
        mail.logout()
