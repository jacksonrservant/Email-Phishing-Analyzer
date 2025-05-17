# src/url_checker.py

from urllib.parse import urlparse

# Basic list of suspicious domains or TLDs (examples)
SUSPICIOUS_TLDS = ['.ru', '.cn', '.tk', '.ml']
SUSPICIOUS_PATTERNS = [
    "login", "secure", "verify", "update", "account", "bank", "paypal", "signin"
]

def analyze_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    reasons = []

    # Check suspicious TLDs
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            reasons.append(f"Suspicious TLD detected: {tld}")

    # Look for phishing-related keywords in path or domain
    for keyword in SUSPICIOUS_PATTERNS:
        if keyword in domain or keyword in path:
            reasons.append(f"Contains keyword: '{keyword}'")

    return {
        "url": url,
        "suspicious": bool(reasons),
        "reasons": reasons
    }

def analyze_urls(url_list):
    return [analyze_url(url) for url in url_list]
