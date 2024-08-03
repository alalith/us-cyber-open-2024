enc_flag = [55, 33, 52, 40, 35, 56, 86, 90, 66, 111, 81, 26, 23, 75, 109, 26, 88, 90, 75, 67, 92, 25, 87, 88, 92, 84, 23, 88]


first_half = enc_flag[0 : len(enc_flag) // 2]
second_half = enc_flag[len(enc_flag) // 2 : len(enc_flag)]

enc_flag2 = first_half + second_half[::-1]

#swap 6 and 9
franchisePath = enc_flag2[6]
enc_flag2[6] = enc_flag2[9]
enc_flag2[9] = franchisePath

#swap 8 and 10
eastGhostwriter  = enc_flag2[10]
enc_flag2[10] = enc_flag2[8]
enc_flag2[8] = eastGhostwriter

#swap 17 and 12
personPioneer = enc_flag2[17]
enc_flag2[17] = enc_flag2[12]
enc_flag2[12] = personPioneer

str_flag = ''

for i in enc_flag2:
    str_flag += chr((i^15) + 27)

print(str_flag)

