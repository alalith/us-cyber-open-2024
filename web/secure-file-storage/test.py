import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging
import os


SECRET_KEY = os.urandom(16)

def encrypt(plaintext):
    try:
        
        if type(plaintext) == str:
            plaintext = plaintext.encode()

        cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
        enc = cipher.encrypt(pad(plaintext, AES.block_size))
        return cipher.iv+enc
    except Exception as e:
        logging.error(e)
        return None

def decrypt(ciphertext):
    try:
        iv,ciphertext = ciphertext[:16],ciphertext[16:]
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC,iv=iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size)
    except Exception as e:
        logging.error(e)
        return None


plaintext = b'A'*16 + b'B'*16

enc = encrypt(plaintext)

enc_list = list(enc)
enc_list[16] = ord('B')
new_enc = bytes(enc_list)
print(enc_list)
pt = decrypt(new_enc[16:])


print(enc)
print(pt)


