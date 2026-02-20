import magic
import re

# 🛡️ FILE STRUCTURE CHECK (Magic Bytes)
def is_file_secure(file_stream): 
    """
    SECURITY FEATURE: Validates file by actual content (Magic Bytes).
    Prevents attackers from renaming 'virus.exe' to 'data.csv'.
    """
    # 1. Check Magic Bytes (MIME Type)
    file_stream.seek(0)
    file_content = file_stream.read(2048) 
    mime = magic.from_buffer(file_content, mime=True)
    file_stream.seek(0) # Reset stream for the CSV parser

    ALLOWED_MIME_TYPES = ['text/plain', 'text/csv', 'application/csv']
    if mime not in ALLOWED_MIME_TYPES:
        return False, f"Content mismatch: File headers indicate {mime}, not CSV."

    # 2. Binary Data Check (Detects non-text/malware content)
    if b'\x00' in file_content:
        return False, "Binary data detected in CSV file."

    return True, "File structure is valid."


# 🛡️ PROMPT INJECTION BLACKLIST
INJECTION_KEYWORDS = ["ignore all previous instructions", "forget your instructions", "system prompt", "reveal your prompt", "you are now a", "dan mode", "ignore safety guidelines"]

def scan_for_prompt_injection(text):
    text_lower = text.lower()
    for phrase in INJECTION_KEYWORDS:
        if phrase in text_lower:
            return True
    return False

def mask_pii(text):
    # 2. Mask Phone Numbers (Handles formats like 555-0199, (555) 123-4567, +1 234-567-8900)
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d{3}-\d{4}'
    text = re.sub(phone_pattern, '[PHONE_MASKED]', text)
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, '[EMAIL_MASKED]', text)
    return text