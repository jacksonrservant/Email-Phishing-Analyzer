# src/email_parser.py
import email
from email import policy
from email.parser import BytesParser
import re

def extract_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)

def parse_email(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg['subject']
    sender = msg['from']
    recipient = msg['to']
    date = msg['date']

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    urls = extract_urls(body)

    parsed_data = {
        "subject": subject,
        "from": sender,
        "to": recipient,
        "date": date,
        "body_snippet": body[:500],  # Limit output
        "urls_found": urls
    }

    return parsed_data
