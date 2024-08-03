from pwn import *

r = remote('167.99.118.184',31340)

r.recvuntil(b'>:)\n')
while True:
    problem = r.recvline().rstrip()
    print(problem)
    solve = eval(problem)
    print(solve)
    r.sendline(str(solve))
    r.recvline()

r.interactive()
