import os
import email
from email import policy
from email.parser import BytesParser

def load_eml_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        return msg
    except Exception as e:
        print(f"[!] Failed to load EML file: {e}")
        return None

def extract_email_metadata(msg):
    metadata = {
        'From': msg['From'],
        'To': msg['To'],
        'Subject': msg['Subject'],
        'Date': msg['Date'],
        'Reply-To': msg['Reply-To'],
        'Return-Path': msg['Return-Path'],
        'Received-SPF': msg['Received-SPF'],
        'Authentication-Results': msg['Authentication-Results'],
    }
    return metadata

def extract_auth_results(auth_header):
    results = {'SPF': None, 'DKIM': None, 'DMARC': None}
    if not auth_header:
        return results

    value_lower = auth_header.lower()
    if 'spf=' in value_lower:
        results['SPF'] = value_lower.split('spf=')[1].split()[0]
    if 'dkim=' in value_lower:
        results['DKIM'] = value_lower.split('dkim=')[1].split()[0]
    if 'dmarc=' in value_lower:
        results['DMARC'] = value_lower.split('dmarc=')[1].split()[0]

    return results

def analyze_phishing_indicators(msg):
    indicators = []

    from_addr = msg.get('From', '')
    reply_to = msg.get('Reply-To', '')

    if reply_to and reply_to != from_addr:
        indicators.append("Reply-To address does not match From address.")

    payload = msg.get_body(preferencelist=('plain', 'html'))
    if payload:
        content = payload.get_content()
        if 'http://' in content or 'https://' in content:
            indicators.append("Contains suspicious links.")
        if 'bit.ly' in content or 'tinyurl' in content:
            indicators.append("Contains shortened URLs.")
        if 'password' in content.lower() or 'verify account' in content.lower():
            indicators.append("Contains language asking for credentials.")

    return indicators

def print_analysis_report(file_path, metadata, auth_results, indicators):
    print(f"\n📨 Analyzing: {file_path}")
    print("\n--- Email Metadata ---")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("\n--- Authentication Results ---")
    for method, result in auth_results.items():
        print(f"{method}: {result if result else 'Not found'}")

    print("\n--- Phishing Indicators ---")
    if indicators:
        for ind in indicators:
            print(f"[!] {ind}")
    else:
        print("[✓] No strong phishing indicators found.")

    print("\n--- Verdict ---")
    if indicators or any(v != 'pass' for v in auth_results.values() if v):
        print(" Suspicious email detected. Proceed with caution.")
    else:
        print(" Email appears safe based on current analysis.")

def main():
    file_path = "input_samples/suspicious_email.eml"  # change to your file path
    msg = load_eml_file(file_path)

    if not msg:
        return

    metadata = extract_email_metadata(msg)
    auth_results = extract_auth_results(metadata.get('Authentication-Results', ''))
    indicators = analyze_phishing_indicators(msg)

    print_analysis_report(file_path, metadata, auth_results, indicators)

if __name__ == "__main__":
    main()



