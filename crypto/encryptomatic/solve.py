from pwn import *
from Crypto.Util.Padding import pad



r = remote('0.cloud.chals.io', 28962)

charset = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890-=!@#$%^&*()_+{}'
flag = b''

for x in range(0,16):
    for c in charset:
        payload = b"A"*(15-len(flag)) +flag + c.to_bytes() 
        #print(len(payload))
        payload += b"A"*(15-len(flag))
        #print(len(payload))
        #print(payload)
        r.recvuntil(b'> ')
        #print(payload)
        r.sendline(payload)
        r.recvuntil(b'Encrypted: ')
        enc = r.recvline().rstrip()
        #print(len(enc))
        #print(len(enc))
        my_enc = enc[0:32]
        their_enc = enc[32:64]

        #input()
        if my_enc == their_enc:
            flag += (c).to_bytes()
            break
            #print(flag)

flag2 = b''
for x in range(0,16):
    for c in charset:
        payload = b"A"*(15-len(flag2)) +flag + flag2 + c.to_bytes() 
        #print(len(payload))
        payload += b"A"*(15-len(flag2))
        #print(len(payload))
        print(payload)
        r.recvuntil(b'> ')
        #print(payload)
        r.sendline(payload)
        r.recvuntil(b'Encrypted: ')
        enc = r.recvline()
        print(enc)
        #print(len(enc))
        my_enc = enc[32:64]
        their_enc = enc[96:128]
        print(my_enc)
        print(their_enc)

        #input()
        if my_enc == their_enc:
            flag2 += (c).to_bytes()
            break
            #print(flag)


