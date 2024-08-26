from datetime import datetime, timedelta
import email
from contextlib import closing
import os
from utils.imap import decode_header_field, decode_folder_name, imap_login

# Göz ardı edilecek klasörler
IGNORED_FOLDERS = os.getenv("IGNORED_FOLDERS").split(",")

def check_env_variables():
    required_vars = ["USERNAME", "PASSWORD", "IMAP_SERVER", "IMAP_PORT", "IGNORED_FOLDERS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Eksik çevresel değişkenler: {', '.join(missing_vars)}")

def get_folders(mail):
    _, folders = mail.list()
    return [decode_folder_name(folder) for folder in folders 
            if not any(ignored in decode_folder_name(folder) for ignored in IGNORED_FOLDERS)]

def process_email(mail, num):
    _, msg = mail.fetch(num, "(RFC822)")
    email_message = email.message_from_bytes(msg[0][1])
    
    subject = decode_header_field(email_message["Subject"])
    from_ = decode_header_field(email_message.get("From"))
    date = email_message["Date"]
    
    print(f"Konu: {subject}")
    print(f"Gönderen: {from_}")
    print(f"Tarih: {date}")
    print("-" * 30)

def process_folder(mail, folder_name):
    mail.select(f'"{folder_name}"')
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
    _, message_numbers = mail.search(None, f'(UNSEEN) (ON "{yesterday}")')
    
    if message_numbers[0]:
        print(f"\nKlasör: {folder_name}")
        print("=" * 30)
        for num in message_numbers[0].split():
            process_email(mail, num)

def get_unread_emails():
    with closing(imap_login()) as mail:
        if not mail:
            return
        
        folders = get_folders(mail)
        for folder_name in folders:
            process_folder(mail, folder_name)

if __name__ == "__main__":
    check_env_variables()
    get_unread_emails()