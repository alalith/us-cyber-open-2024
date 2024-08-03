cipher = [196, 251, 231, 169, 250, 224, 179, 231, 251, 246, 179, 245, 255, 242, 244, 172, 179, 153 ,153]
cipher_flag = [32, 60, 38, 48, 33, 28, 52, 30, 6, 31, 85,0,110,4,11,77,51,110,86,7,89,1,81,4,69]
key = [115,117,112,101,114,95,115,101,99,114,101,116,95,107,101,121,95,49,50,51,52,53,54,55,56]

flag = b''
for x in cipher:
    flag += (x ^ 147).to_bytes()


print(flag)
flag = b''
for x in range(0,len(cipher_flag)):
    flag += (key[x] ^ cipher_flag[x]).to_bytes()
print(len(key))
print(len(cipher_flag))
print(flag)
