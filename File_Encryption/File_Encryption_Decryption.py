import os
import re
import getpass
import secrets
import pickle
import argon2
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Function to create an empty text file
def create_text_file():
    file_name = input("Enter the name of the text file to create: ")
    if os.path.exists(file_name):
        print(f"A file with the name '{file_name}' already exists.")
        return
    
    with open(file_name, 'w') as file:
        file.write("")  # Create an empty text file
    print(f"File '{file_name}' created successfully.")

# Function to edit a text file
def edit_text_file():
    file_name = input("Enter the name of the text file to edit: ")
    if not os.path.exists(file_name):
        print(f"File '{file_name}' does not exist.")
        return

    with open(file_name, 'a') as file:
        while True:
            new_line = input("Enter a line to add (or press Enter to finish editing): ")
            if not new_line:
                break
            file.write(new_line + '\n')
    print(f"Editing of '{file_name}' completed.")

# Function to perform file encryption
def perform_encryption():
    input_file = input("Enter the name of the file to encrypt: ")
    if not os.path.exists(input_file):
        print(f"File '{input_file}' does not exist.")
        return
    
    encrypted_file = input("Enter the name of the encrypted file: ")
    if os.path.exists(encrypted_file):
        print(f"A file with the name '{encrypted_file}' already exists.")
        return
    
    password = getpass.getpass("Enter a password: ")
    
    encrypt_file(input_file, encrypted_file, password)
    print(f"Encryption of '{input_file}' completed and saved as '{encrypted_file}'.")

# Function to perform file decryption
def perform_decryption():
    encrypted_file = input("Enter the name of the encrypted file: ")
    if not os.path.exists(encrypted_file):
        print(f"File '{encrypted_file}' does not exist.")
        return
    
    decrypted_file = input("Enter the name of the decrypted file: ")
    if os.path.exists(decrypted_file):
        print(f"A file with the name '{decrypted_file}' already exists.")
        return
    
    password = getpass.getpass("Enter the password: ")
    
    decrypt_file(encrypted_file, decrypted_file, password)
    print(f"Decryption of '{encrypted_file}' completed and saved as '{decrypted_file}'.")

# Function to check if a password is strong
def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

# Function to hash a password
def hash_password(password):
    hasher = argon2.PasswordHasher()
    password_hash = hasher.hash(password)
    return password_hash

# Function to store a password hash in a file
def store_password(password, file_path):
    password_hash = hash_password(password)

    try:
        with open(file_path, 'w') as f:
            f.write(password_hash)

        print("Password securely stored in", file_path)
    except Exception as e:
        print("Password storage failed:", str(e))

# Function to serialize user data
def serialize_user(user):
    return pickle.dumps(user)

# Function to deserialize user data
def deserialize_user(data):
    return pickle.loads(data)

# Function to get a strong password from the user
def get_password():
    while True:
        password = getpass.getpass("Enter your password: ")
        if is_strong_password(password):
            return password.encode('utf-8')
        else:
            print("Password is weak. Please choose a stronger password.")

# Function to store user data in a file
def store_user(user):
    try:
        with open("user_profile", 'ab') as f:  # Append binary mode
            serialized_user = serialize_user(user)
            f.write(serialized_user)
        print("User data stored successfully.")
    except Exception as e:
        print("User data storage failed:", str(e))

# Function to load users from a file
def load_users():
    users = []
    try:
        with open("user_profile", 'rb') as f:  # Read binary mode
            while True:
                serialized_user = f.read()
                if not serialized_user:
                    break
                user = deserialize_user(serialized_user)
                users.append(user)
        print("User data loaded successfully.")
    except Exception as e:
        print("User data loading failed:", str(e))
    return users

# User class to represent user data
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


# Function to create a new user
def create_user(users_db):
    username = input("Enter a username: ")
    
    # Check if a user with the same username already exists
    for user in users_db:
        if user.username == username:
            print("Username already exists. Please choose a different one.")
            return
    
    while True:
        password = getpass.getpass("Enter a password: ")
        
        if is_strong_password(password):
            # Hash the password before storing it
            password_hash = hash_password(password)
            
            user = User(username, password_hash)
            store_user(user)
            users_db.append(user)  # Add the new user to the in-memory database
            print("Registration successful.")
            return user  # Return the created user
        else:
            print("Password is weak. Please choose a stronger password.")

# Function to verify a password against a stored hash
def verify_password(stored_hash, password):
    hasher = argon2.PasswordHasher()
    try:
        return hasher.verify(stored_hash, password)
    except argon2.exceptions.VerifyMismatchError:
        return False

# Global variable to store the logged-in user
logged_in_user = None

# Main program
def main():
    # Load existing users from the "user_profile" file
    users_db = load_users()
    
    global logged_in_user  # Declare logged_in_user as a global variable
    
    while True:
        if logged_in_user is None:
            print("1. Register")
            print("2. Login")
            print("3. Quit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                user = create_user(users_db)
                store_user(user)
                users_db.append(user)  # Add the new user to the in-memory database
            elif choice == "2":
                username = input("Enter your username: ")
                password = getpass.getpass("Enter a password: ")
                
                user_found = False
                for user in users_db:
                    if user.username == username and verify_password(user.password_hash, password):
                        user_found = True
                        logged_in_user = user  # Set the logged-in user
                        print("Login successful.")
                        break
                
                if not user_found:
                    print("Login failed. Invalid username or password.")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Logged in as:", logged_in_user.username)
            print("4. Create Text File")
            print("5. Edit Text File")
            print("6. Encrypt File")
            print("7. Decrypt File")
            print("8. Logout")
            
            choice = input("Enter your choice: ")
            
            if choice == "4":
                create_text_file()
            elif choice == "5":
                edit_text_file()
            elif choice == "6":
                perform_encryption()
            elif choice == "7":
                perform_decryption()
            elif choice == "8":
                logged_in_user = None  # Logout the user
                print("Logged out.")
            else:
                print("Invalid choice. Please try again.")

    # Store all users back to the "user_profile" file
    with open("user_profile", 'wb') as f:
        for user in users_db:
            serialized_user = serialize_user(user)
            f.write(serialized_user)

# Function to generate a salt
def generate_salt():
    return secrets.token_bytes(16)

# Function to generate an initialization vector (IV)
def generate_iv():
    return secrets.token_bytes(16)

# Function to derive a key from a password and salt
def derive_key(password, salt):
    # Encode the password as bytes using UTF-8 encoding
    password_bytes = password.encode('utf-8')
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password_bytes)

# Function to derive an HMAC key from a password and salt
def derive_hmac_key(password, salt):
    # Encode the password as bytes using UTF-8 encoding
    password_bytes = password.encode('utf-8')
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password_bytes)

# Function to add a MAC (Message Authentication Code) to encrypted data
def add_mac(encrypted_data, hmac_key):
    h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
    h.update(encrypted_data)
    mac = h.finalize()
    return encrypted_data + mac

# Function to verify the MAC of encrypted data
def verify_mac(encrypted_data_with_mac, hmac_key):
    encrypted_data = encrypted_data_with_mac[:-32]
    received_mac = encrypted_data_with_mac[-32:]
    h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
    h.update(encrypted_data)
    try:
        h.verify(received_mac)
        return True
    except Exception as e:
        print("MAC verification failed:", str(e))
        return False

# Function to encrypt a file
def encrypt_file(input_file, output_file, password):
    # Check if the output file already exists
    if os.path.exists(output_file):
        overwrite = input(f"File '{output_file}' already exists. Do you want to overwrite it? (Yes or No): ").strip().lower()
        if overwrite != "yes":
            print("Encryption canceled.")
            return

    salt = generate_salt()
    iv = generate_iv()
    
    key = derive_key(password, salt)
    hmac_key = derive_hmac_key(password, salt)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    try:
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        encrypted_data_with_mac = add_mac(ciphertext, hmac_key)

        with open(output_file, 'wb') as f:
            f.write(salt)
            f.write(iv)
            f.write(encrypted_data_with_mac)

        print("File encrypted successfully.")
    except Exception as e:
        print("Encryption failed:", str(e))

# Function to decrypt a file
def decrypt_file(input_file, output_file, password):
    # Check if the output file already exists
    if os.path.exists(output_file):
        overwrite = input(f"File '{output_file}' already exists. Do you want to overwrite it? (Yes or No): ").strip().lower()
        if overwrite != "yes":
            print("Decryption canceled.")
            return

    try:
        with open(input_file, 'rb') as f:
            salt = f.read(16)
            iv = f.read(16)
            encrypted_data_with_mac = f.read()

        key = derive_key(password, salt)
        hmac_key = derive_hmac_key(password, salt)
        
        if not verify_mac(encrypted_data_with_mac, hmac_key):
            print("\nMAC verification failed. The data may be tampered.")
            return
        
        encrypted_data = encrypted_data_with_mac[:-32]
        
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

        with open(output_file, 'wb') as f:
            f.write(plaintext)

        print("File decrypted successfully.")
    except Exception as e:
        print("Decryption failed:", str(e))

if __name__ == "__main__":
    main()
