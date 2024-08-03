from Crypto.Cipher import Salsa20
import base64
import json

with open('encrypted.txt','rb') as f:
    json_object = json.loads(f.read()) 

for i in json_object:
    key = b'\x45\x32\x46\x41\x43\x38\x41\x33\x39\x35\x37\x33\x46\x31\x46\x34\x31\x36\x41\x38\x43\x36\x38\x33\x34\x42\x46\x34\x39\x32\x31\x36'

    if 'Nonce' not in i:
        continue
    nonce = base64.b64decode(i['Nonce'])
    msg = base64.b64decode(i['Msg'])

    cipher = Salsa20.new(key=key, nonce=nonce)

    plaintext = cipher.decrypt(msg)
    print(plaintext)
