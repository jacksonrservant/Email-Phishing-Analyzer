# Phishing Email Analyzer

This project is for a Python-based phishing email analysis tool designed to assist cybersecurity analysts in identifying malicious characteristics within `.eml` or `.msg` email files. It extracts, parses, and evaluates email headers, links, attachments, and content to flag indicators of compromise (IOCs) commonly found in phishing attacks.

## Project Scope

This version of the tool focuses on:

- Parsing `.eml` files to extract metadata, headers, body text, links, and attachments.
- Analyzing headers for SPF, DKIM, and DMARC anomalies.
- Detecting suspicious URLs and keywords commonly used in phishing.
- Performing static analysis on attachments (e.g., hashing for lookup).
- Cross-referencing links and hashes with open-source threat intelligence sources.
- Generating structured reports in JSON, Excel, or HTML formats.

