# File_Encryption_Decryption

Certainly! Here's a README file for the provided Python code:

# File Management and Encryption Command-Line Tool

This command-line tool is designed to provide basic file management capabilities, user authentication, and file encryption/decryption. It allows users to create and edit text files, secure their data with encryption, and manage user accounts.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Usage](#usage)
4. [File Encryption](#file-encryption)
5. [User Authentication](#user-authentication)
6. [Contributing](#contributing)
7. [Disclaimer](#disclaimer)

## Features<a name="features"></a>
- **Text File Management**: Create and edit text files from the command line.
- **File Encryption**: Encrypt sensitive files to protect their contents.
- **User Authentication**: Register and log in with a username and a strong password.
- **Password Hashing**: Securely hash user passwords using the Argon2 algorithm.
- **User Data Persistence**: Store user data and hashed passwords in a binary file.
- **MAC (Message Authentication Code) Verification**: Ensure the integrity of encrypted data.

## Prerequisites<a name="prerequisites"></a>
- Python 3.7 or higher.
- Required Python packages can be installed via pip:
  ```
  pip install cryptography argon2-cffi
  ```

## Usage<a name="usage"></a>
1. Clone or download this repository to your local machine.

2. Open a terminal and navigate to the project directory.

3. Run the program by executing the following command:
   ```
   python file_management.py
   ```

4. Follow the on-screen instructions to perform various actions.

## File Encryption<a name="file-encryption"></a>
- **Encrypt a File**: Choose option 6 from the main menu to encrypt an existing file. You will be prompted for the input file, output file, and a password. The file will be encrypted using AES-CFB encryption and saved securely.

- **Decrypt a File**: Choose option 7 from the main menu to decrypt an encrypted file. Provide the input encrypted file, output decrypted file, and the password used for encryption.

- **MAC Verification**: The program verifies the integrity of encrypted data using a Message Authentication Code (MAC). If the data has been tampered with, decryption will fail.

## User Authentication<a name="user-authentication"></a>
- **Register**: Choose option 1 from the main menu to create a new user account. You will be prompted to choose a unique username and a strong password.

- **Login**: Select option 2 from the main menu to log in with an existing username and password. If authentication is successful, you can access additional features such as file creation and encryption.

- **Logout**: Choose option 8 to log out of the current user session.

## Contributing<a name="contributing"></a>
Contributions to this project are welcome! If you have suggestions for improvements or bug fixes, please open an issue or create a pull request.


## Disclaimer<a name ="disclaimer"></a>
The File Management and Encryption Command-Line Tool ("the Tool") is provided for educational and demonstration purposes only. The Tool may involve cryptographic operations and handling of sensitive information, and it is your responsibility to use it responsibly and in accordance with applicable laws and regulations.

Use at Your Own Risk: The Tool is made available on an "as-is" basis, and the authors make no warranties or guarantees regarding its functionality, security, or fitness for a particular purpose. The use of this Tool is entirely at your own risk.

Data Security: While the Tool employs encryption techniques to protect sensitive data, no encryption system can be guaranteed to be completely secure. Users are encouraged to exercise caution and take appropriate measures to safeguard their data and credentials.

User Authentication: The Tool includes user authentication features. Users are responsible for choosing strong, unique passwords and keeping them confidential. The Tool stores password hashes, not plaintext passwords, but it is essential to use strong and secure passwords.

Data Backup: Before using the Tool to edit or encrypt files, it is recommended to make backup copies of your data. The authors are not responsible for any data loss or damage that may occur during the use of the Tool.

No Liability: The authors and contributors of this project shall not be liable for any direct or indirect damages or losses resulting from the use of the Tool, including but not limited to data loss, security breaches, or any other issues.

Legal Compliance: Users are responsible for complying with all applicable local, state, and federal laws and regulations when using this Tool. It is the user's responsibility to ensure that their use of the Tool is in compliance with all applicable laws.

---
