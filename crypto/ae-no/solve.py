from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom

def main():
  first_16_pt = b'Here is the flag'
  first_16_ct = b'\x96\xa0\x29\x9d\x6c\x60\xcd\x0f\x40\x21\x8b\x73\xab\x5f\xc4\xb7'

  iv = b''
  for x in range(0,len(first_16_pt)):
      iv += (first_16_pt[x] ^ first_16_ct[x]).to_bytes()

  print(iv)
  key = b'SecretKey1234567'
  msg = bytes.fromhex('96a0299d6c60cd0f40218b73ab5fc4b710b8951bd0ed8977a1382328454a2ce68106660bb48808c2fa7a141ac863732f66f9032d00cf2c0ecc3a6871683911a6')
  cipher = AES.new(key, AES.MODE_CBC, iv)
  enc = cipher.decrypt(pad(msg,16))
  print("Key: " + key.decode())
  print("Encoded Flag: " + enc.hex())

if __name__ == '__main__': main()
