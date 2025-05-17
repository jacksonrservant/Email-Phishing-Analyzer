# src/analyzer.py

SUSPICIOUS_KEYWORDS = [
    "verify your account",
    "update your payment information",
    "click here to login",
    "urgent action required",
    "account suspended",
    "security alert",
    "reset your password",
    "confirm your identity"
]

def analyze(parsed_data):
    flags = []

    # Check for suspicious keywords in body
    body = parsed_data.get("body_snippet", "").lower()
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in body]
    if found_keywords:
        flags.append(f"Suspicious keywords detected: {', '.join(found_keywords)}")

    # Check if 'From' and 'To' are the same (possible spoof)
    if parsed_data.get("from") and parsed_data.get("to"):
        if parsed_data["from"] == parsed_data["to"]:
            flags.append("Sender and recipient are the same — possible spoofing")

    # Check for multiple suspicious URLs
    if len(parsed_data.get("urls_found", [])) > 3:
        flags.append("Multiple URLs detected in email body")

    parsed_data["phishing_warnings"] = flags
    return parsed_data
