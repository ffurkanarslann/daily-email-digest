from datetime import datetime, timedelta
import imaplib
import email
from email.header import decode_header

from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = os.getenv("IMAP_PORT")

# Göz ardı edilecek klasörler
IGNORED_FOLDERS = os.getenv("IGNORED_FOLDERS").split(",")
 
def get_folders(mail):
    mail_folders = []

    # Tüm klasörleri al
    _, folders = mail.list()
    
    for folder in folders:
        # Klasör adını al ve decode et
        parts = folder.decode().split('"')
        folder_name = parts[-2].strip() if len(parts) > 3 else parts[-1].strip()

        # Göz ardı edilecek klasörleri kontrol et
        if not any(ignored in folder_name for ignored in IGNORED_FOLDERS):
            mail_folders.append(folder_name)
    
    return mail_folders

def get_unread_emails():
    # IMAP sunucusuna bağlan
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    
    # try:
        # Giriş yap
    mail.login(USERNAME, PASSWORD)

    folders = get_folders(mail)

    # Dünün tarihini al
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
    
    for folder_name in folders:
        folder_name = '"' + folder_name.strip() + '"'  # Klasör adını tırnak işaretleri içine alın ve boşlukları kırpın

        mail.select(folder_name)
        # Dün gönderilen ve okunmamış mailleri ara
        _, message_numbers = mail.search(None, f'(UNSEEN) (ON "{yesterday}")')
        
        if message_numbers[0]:
            print(f"\nKlasör: {folder_name}")
            print("=" * 30)
        
        for num in message_numbers[0].split():
            # Maili getir
            _, msg = mail.fetch(num, "(RFC822)")
            
            # Mail içeriğini parse et
            email_body = msg[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Konu, gönderen ve tarihi al
            subject, encoding = decode_header(email_message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            from_, encoding = decode_header(email_message.get("From"))[0]
            if isinstance(from_, bytes):
                from_ = from_.decode(encoding or "utf-8")
            date = email_message["Date"]
            
            print(f"Konu: {subject}")
            print(f"Gönderen: {from_}")
            print(f"Tarih: {date}")
            print("-" * 30)

    # except imaplib.IMAP4.error as e:
    #     print(f"Bir hata oluştu: {e}")
    
    # finally:
    #     # Bağlantıyı kapat
    #     # mail.close()
    mail.logout()
        
         # Gelen kutusu seç
            # mail.select("INBOX")

            # # Okunmamış mailleri ara
            # _, message_numbers = mail.search(None, "UNSEEN")

            # # Dünün tarihini al
            # yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

            # # Dün gönderilen mailleri ara
            # _, message_numbers = mail.search(None, f'(ON "{yesterday}")')
            
            # for num in message_numbers[0].split():
            #     # Maili getir
            #     _, msg = mail.fetch(num, "(RFC822)")
                
            #     # Mail içeriğini parse et
            #     email_body = msg[0][1]
            #     email_message = email.message_from_bytes(email_body)
                
            #     # Konu ve göndereni al
            #     subject, encoding = decode_header(email_message["Subject"])[0]
            #     if isinstance(subject, bytes):
            #         subject = subject.decode(encoding or "utf-8")
            #     from_, encoding = decode_header(email_message.get("From"))[0]
            #     if isinstance(from_, bytes):
            #         from_ = from_.decode(encoding or "utf-8")
            #     date = email_message["Date"]
                
            #     print(f"Konu: {subject}")
            #     print(f"Gönderen: {from_}")
            #     print(f"Tarih: {date}")
            #     print("-" * 30)
   

if __name__ == "__main__":
    get_unread_emails()