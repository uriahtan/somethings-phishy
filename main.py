import re
from spellchecker import SpellChecker
dictionary = SpellChecker()
from bs4 import BeautifulSoup


def open_email(email):
    with open(email, "r", encoding = "utf-8") as f:
        content = f.read()
        lower = content.lower()
        detect_suspicious_keywords(lower)
        detect_spelling_errors(lower)
        print("")
        detect_attachments(lower)


suspicious_keywords = ['immediately', 'as soon as possible', 'asap', 'urgent', '!',
                       'bank', 'transfer', 'payment', 'invoice',
                       'action required', 'verify', 'click', 'link', 'attachment',
                       'ic', 'credit card', 'bank account']

headers = ['from:', 'sent:', 'to:', 'subject:',
           'date:', 'cc:', 'bcc:', 'attachments:', 
           'content-type:']

symbols = [".", ",", "(", ")","/","$"]

def detect_suspicious_keywords(lower):
    detected_suspicious_keywords = []
    pattern = r'\b(?:' + '|'.join(re.escape(sus) for sus in suspicious_keywords) + r')\b'
    detected_suspicious_keywords = re.findall(pattern, lower, flags=re.IGNORECASE)
    print("")
    print(f"Suspicious keywords: {detected_suspicious_keywords}")


def detect_spelling_errors(lower):
    global headers
    global symbols
    spelling_mistakes = []
    filtered_lines = [
        line for line in lower.splitlines()
        if not any(substring in line for substring in headers)
    ]

    filtered_lines = ("\n".join(filtered_lines)).split()
    for clean in filtered_lines:
        for symbol in symbols:
            clean = clean.replace(symbol, "")
        if clean.isalpha():
            if clean not in dictionary:
                spelling_mistakes.append(clean)

    print(f"Spelling mistakes: {spelling_mistakes}")


def detect_attachments(lower):
    for line in lower.splitlines():
        if "attachments:" in line:
            attachment = line.split(":", 1)[1].strip()
    attachment_list = attachment.split(";")
    print(f"Attachments found: {attachment_list}")


def detect_links(html):
    with open(html, "r", encoding = "utf-8", errors="replace") as f:
        raw_html = f.read()
    html_src_code = BeautifulSoup(raw_html, 'html.parser')
    links = [a['href'] for a in html_src_code.find_all('a', href=True)]
    clean_links = []
    for l in links:
        if "mailto:" in l:
            pass
        else:
            clean_links.append(l)
    print(clean_links)


open_email('sample.txt')
detect_links("email.html")