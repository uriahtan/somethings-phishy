import difflib
import nltk
# nltk.download('words', download_dir='.')
nltk.data.path.append('.')  
from nltk.corpus import words


dictionary = words.words()  # This is a list of English words
# print(len(dictionary))


def open_email(email):
    with open(email, "r", encoding = "utf-8") as f:
        content = f.read()
        lower = content.lower()
        # detect_suspicious_keywords(lower)
        detect_spelling_errors(lower)

suspicious_keywords = ['immediately','as soon as possible','asap','urgent',
                       'bank','transfer','payment',]
detected_suspicious_keywords = []
sus_count = 0
total_sus_count = 0
headers = ['from:','sent:','to:','subject:'
           ,'date:','cc:','bcc:']
symbols = [".", ",", "(", ")","/","$"]
spelling_mistakes = []

def detect_suspicious_keywords(lower):
    # print(f"lower content: {lower}")
    global sus_count
    global total_sus_count
    global detected_suspicious_keywords
    for sus in suspicious_keywords:
        sus_count = lower.count(sus)
        if sus_count > 0:
            detected_suspicious_keywords.append(sus)
        total_sus_count += sus_count
        # print(f"{sus} count: {sus_count}")
    print("")
    print(f"Suspicious keywords: {detected_suspicious_keywords}")
    # print(f"total sus count: {total_sus_count}")


def detect_spelling_errors(lower):
    global headers
    global symbols
    global spelling_mistakes
    filtered_lines = [
        line for line in lower.splitlines()
        if not any(substring in line for substring in headers)
    ]

    filtered_lines = ("\n".join(filtered_lines)).split()
    print(filtered_lines)
    for clean in filtered_lines:
        for symbol in symbols:
            clean = clean.replace(symbol, "")
        matches = difflib.get_close_matches(clean, dictionary, n=3, cutoff=0.6)
        if matches:
            if clean == matches[0]:
                # print(f"{matches[0]} no problem")
                pass
            else:
                spelling_mistakes.append(clean)
                # print(f"{clean}. Did you mean {matches[0]}")
        else:
            print(f"No match found for {clean}")
    print(f"Spelling mistakes: {spelling_mistakes}")



open_email('sample.txt')