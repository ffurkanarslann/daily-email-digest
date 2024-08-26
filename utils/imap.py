from email.header import decode_header
import imaplib
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = os.getenv("IMAP_PORT")

# IMAP işlemleri
def imap_login():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(USERNAME, PASSWORD)
        return mail
    except (imaplib.IMAP4.error, OSError) as e:
        print(f"Giriş yapılırken bir hata oluştu: {e}")
        return None

def decode_header_field(field):
    decoded, encoding = decode_header(field)[0]
    return decoded.decode(encoding or "utf-8") if isinstance(decoded, bytes) else decoded

def decode_folder_name(folder):
    parts = folder.decode().split('"')
    return parts[-2].strip() if len(parts) > 3 else parts[-1].strip()
