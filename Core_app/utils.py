from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import io

def encrypt_file(file, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    file_content = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(file_content)

    output = io.BytesIO()
    output.write(salt)
    output.write(nonce)
    output.write(tag)
    output.write(ciphertext)
    output.seek(0)

    return output

def decrypt_file(encrypted_file, password):
    encrypted_file.seek(0)
    salt = encrypted_file.read(16)
    nonce = encrypted_file.read(16)
    tag = encrypted_file.read(16)
    ciphertext = encrypted_file.read()

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
