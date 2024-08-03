import zlib
from Crypto.Cipher import ChaCha20
import string
import random


charset = string.ascii_letters+string.digits + '_'

flag_str = "".join(random.sample(charset,23))
secret = "SIVUSCG{"+flag_str+"}"
data = "t"
nonce = bytes.fromhex("4e028ccfa58ef2e7")
ciphertext = bytes.fromhex("e4d743a6b9d6798cadc39fbad3b13c1dc67f6270d773bb1f79796f3633c9bb511399f532da43860b0b07cb98")


signed = secret+data+secret
compressed = zlib.compress(signed.encode())
cipher = ChaCha20.new(key=secret.encode(),nonce=nonce)
encrypted = cipher.encrypt(compressed)

#for i in range(0,len(ciphertext

key = b''
for i in range(0,len(secret)):
    key += (ord(secret[i]) ^ encrypted[i]).to_bytes()



print(len(compressed))
print(len(ciphertext))
print(len(key))
print(secret)


print(key.hex())





