''' This module deals with all encryption and decryption of obtained and fed data to the passman api endpoints.
I have abstracted them in a seperate module here for reuse if needed in the future. '''

import cryptography.hazmat.primitives.hashes as hashes
import cryptography.hazmat.primitives.kdf.pbkdf2 as pbkdf2
import cryptography.fernet as fernet
import base64

# Generate a fernet key by derieving it from the user's hashed password. As this is available from the User model, I have used it here. It can undoubtedly be made much more complex but this has sufficed for now.
def generate_key(user):
    algorithm = hashes.SHA256()
    length = 32
    iterations = 10000
    salt = user.username[0] + user.username[:-1]
    salt = salt.encode()
    kdf = pbkdf2.PBKDF2HMAC(algorithm=algorithm, length=length, salt=salt, iterations=iterations)
    enc_key = kdf.derive(user.password.encode())
    key = base64.urlsafe_b64encode(enc_key)
    return key

# Take the key and encrypt the given data using the fernet key.
def encrypt_data(key, data):
    fer = fernet.Fernet(key)
    return fer.encrypt(data).decode()

# Take a key and decrypt the given data. The given data here is in bytes form.
def decrypt_data(key, data):
    enc_data = data.encode()
    fer = fernet.Fernet(key)
    try:
        dec_data = fer.decrypt(enc_data)
        return dec_data
    except fernet.InvalidToken:
        return "Invalid Key"
