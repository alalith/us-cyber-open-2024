from Crypto.Cipher import Salsa20
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json

with open('encrypted.txt','rb') as f:
    json_object = json.loads(f.read()) 


for i in json_object:
    key = b'\x1b\x1c\x9fS\x9e\\O\xf8\xdb\xcf\xfe\x99e\x92\xff\xd3\x9cc\xb6Af#\xd0=]\xbd\xc1\xab\xe4\x18\xffX'
    if 'Nonce' not in i:
        continue
    nonce = base64.b64decode(i['Nonce'])
    msg = base64.b64decode(i['Msg'])

    cipher = Salsa20.new(key=key, nonce=nonce)

    plaintext = cipher.decrypt(msg)
    print(plaintext)
