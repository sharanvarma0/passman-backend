import cryptography.hazmat.primitives.hashes as hashes
import cryptography.hazmat.primitives.kdf.pbkdf2 as pbkdf2
import cryptography.fernet as fernet
import base64

GENERATED_KEY = ""

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

def encrypt_data(key, data):
    fer = fernet.Fernet(key)
    return fer.encrypt(data).decode()

def decrypt_data(key, data):
    enc_data = data.encode()
    fer = fernet.Fernet(key)
    try:
        dec_data = fer.decrypt(enc_data)
        return dec_data
    except fernet.InvalidToken:
        return "Invalid Key"
