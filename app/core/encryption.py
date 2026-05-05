from cryptography.fernet import Fernet
from app.core.config import settings

fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(raw: str) -> bytes:
    return fernet.encrypt(raw.encode())

def decrypt_data(blob: bytes) -> str:
    return fernet.decrypt(blob).decode()