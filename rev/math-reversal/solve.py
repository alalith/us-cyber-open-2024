flag = [ 0x2d, 0x37, 0x2a, 0x3e, 0x39, 0x2e, 0x05, 0x0a, 0x4d, 0x0e, 0x07, 0x21, 0x1c, 0x4f, 0x1a, 0x1a, 0x4f, 0x1d, 0x0b, 0x14, 0x0c, 0x21, 0x10, 0x1f, 0x0d, 0x0d, 0x09, 0x50, 0x0e, 0x1c, 0x03 ]

str_flag = ''

for i in flag:
    str_flag += chr(0x80-i)

print(str_flag)