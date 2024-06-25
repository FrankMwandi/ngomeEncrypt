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

    return {
        'salt': salt,
        'nonce': nonce,
        'ciphertext': ciphertext,
        'tag': tag,
    }
