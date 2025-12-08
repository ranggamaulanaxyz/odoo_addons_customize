from odoo.tools import config
from cryptography.fernet import Fernet

key = config.get('secret_key', 'jk42kjb42kb4k2b4kj24k3')

def encrypt_string(string: str) -> bytes:
    """
    Encrypts a string message using the provided Fernet key.
    
    Args:
        string: The plaintext string to encrypt.
        key: The Fernet key (as a string).
        
    Returns:
        The encrypted message as bytes.
    """
    # Instantiate the Fernet object with the key
    f = Fernet(key.encode())
    
    # Encrypt the message (must be in bytes)
    encrypted_message = f.encrypt(string.encode())
    
    return encrypted_message

def decrypt_bytes(encrypted: bytes) -> str:
    """
    Decrypts a bytes message using the provided Fernet key.
    
    Args:
        encrypted: The encrypted data as bytes.
        key: The Fernet key (as a string).
        
    Returns:
        The decrypted plaintext message as a string.
    """
    # Instantiate the Fernet object with the key
    f = Fernet(key.encode())
    
    # Decrypt the message
    decrypted_message = f.decrypt(encrypted)
    
    # Decode the result back to a string
    return decrypted_message.decode()