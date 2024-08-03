from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
text = base64.b64decode(b'xBGaj4JgCA8HQEES15e8KvldcFrOkoZOwKGGkqTOnBKxqDznkmwOk53hkvL9wrrz')
key = bytes.fromhex('645066095236262de0b476fa7e079d54')
flag = b''
for x in range(0,len(text)):
    flag += (text[x] ^ key[x % len(key)]).to_bytes()


print(flag)
