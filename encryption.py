from cryptography.fernet import Fernet
import os

KEY_FILE = "encryption.key"


def create_key():
    """Create an encryption key if one doesn't already exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)


def load_key():
    """Load the existing encryption key."""
    with open(KEY_FILE, "rb") as file:
        return file.read()


def encrypt_file(input_path, output_path):
    """Encrypt a file and save the encrypted version."""

    create_key()

    key = load_key()
    cipher = Fernet(key)

    with open(input_path, "rb") as file:
        data = file.read()

    encrypted_data = cipher.encrypt(data)

    with open(output_path, "wb") as file:
        file.write(encrypted_data)


def decrypt_file(input_path, output_path):
    """Decrypt an encrypted file."""

    key = load_key()
    cipher = Fernet(key)

    with open(input_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    with open(output_path, "wb") as file:
        file.write(decrypted_data)