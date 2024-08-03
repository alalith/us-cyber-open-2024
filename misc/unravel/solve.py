key = b'856abadb45ad7751'
cipher = bytes.fromhex('4d5b44001404081952590003680107050b0d060551515d570d51055d014a')
chosen = b'unravel{flag_8b78637202c1c0ed}'

plaintext = b''
for i in range(0,len(cipher)):
    plaintext += (cipher[i] ^ key[i % len(key)]).to_bytes()


sus_key = b''
for i in range(0,len(cipher)):
    sus_key += (cipher[i] ^ chosen[i]).to_bytes()
print(len(chosen))
print(len(key))
print(plaintext)
print(sus_key)
