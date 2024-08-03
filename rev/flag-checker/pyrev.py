enc_flag = [55, 33, 52, 40, 35, 56, 86, 90, 66, 111, 81, 26, 23, 75, 109, 26, 88, 90, 75, 67, 92, 25, 87, 88, 92, 84, 23, 88]

flag_in = input("Enter the flag: ")
input_int = [ord(i) for i in flag_in]
input_len = len(input_int)
flag_len = len(enc_flag)



makeupRoof = []
tinRoyalty = []
if flag_len == input_len:
    for heartCool in input_int:
        makeupRoof.append(heartCool - 27)
    for angelStay in makeupRoof:
        tinRoyalty.append(angelStay ^ 15)
    
    #swap 6 and 9
    franchisePath = tinRoyalty[6]
    tinRoyalty[6] = tinRoyalty[9]
    tinRoyalty[9] = franchisePath

    #swap 8 and 10
    eastGhostwriter  = tinRoyalty[10]
    tinRoyalty[10] = tinRoyalty[8]
    tinRoyalty[8] = eastGhostwriter

    #swap 17 and 12
    personPioneer = tinRoyalty[17]
    tinRoyalty[17] = tinRoyalty[12]
    tinRoyalty[12] = personPioneer

    lineMoon = tinRoyalty[0 : len(tinRoyalty) // 2]
    puddingCommission = tinRoyalty[len(tinRoyalty) // 2 : len(tinRoyalty)]

    # reverse last half
    furRegret = lineMoon + puddingCommission[::-1]
    tinRoyalty = furRegret

    if tinRoyalty == enc_flag:
        print("Correct!! :)")
    else:
        print("Incorrect flag :(")

else:
    print("Incorrect :(")
