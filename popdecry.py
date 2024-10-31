import os
from pathlib import Path
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Function to load an existing encryption key
def load_key(key_path='encryption_key.key'):
    with open(key_path, 'rb') as key_file:
        return key_file.read()

# Decrypt a file with a given key
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)
    print(f"Decrypted {file_path}")

# Function to decrypt all files in the Downloads folder
def decrypt_downloads_folder(key):
    downloads_folder = Path.home() / 'Downloads'  # Gets the Downloads folder of the current user

    if downloads_folder.exists():
        for file_path in downloads_folder.iterdir():
            if file_path.is_file():  # Ensure it's a file
                decrypt_file(file_path, key)
    else:
        print(f"Downloads folder does not exist: {downloads_folder}")

# Function to display a decryption success popup
def show_decryption_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Decryption Complete", "Your files have been successfully decrypted.")
    root.destroy()  # Close the Tkinter window

# Example usage
# Load encryption key
key_path = 'encryption_key.key'
key = load_key(key_path)

# Decrypt files in the Downloads folder
decrypt_downloads_folder(key)

# Show the decryption success popup
show_decryption_popup()
