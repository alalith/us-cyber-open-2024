from collections import deque 
starmap1 = [0] * 1600
starmap2 = [0] * 1601
starmap1[8] = 0xce
starmap1[2] = 0xb5
starmap1[410] = 0x590
starmap1[1479] = 0x62c
starmap1[1556] = 0x633
starmap1[1287] = 0x565
starmap1[1006] = 0x621
starmap1[369] = 400
starmap1[1426] = 0x639
starmap1[208] = 0x324
starmap1[884] = 0x5dd
starmap1[897] = 0x619
starmap1[561] = 0x4f6
starmap1[1422] = 0x600
starmap1[160] = 0x4db
starmap1[209] = 0x3b1
starmap1[717] = 0x3dd
starmap1[606] = 0x3e5
starmap1[18] = 0x55a
starmap1[981] = 0x59c
starmap1[280] = 0x518
starmap1[587] = 0x2d8
starmap1[1430] = 0x5d5
starmap1[389] = 0x510
starmap1[1460] = 0x62d
starmap1[1348] = 0x622
starmap1[626] = 0x424
starmap1[1451] = 0x5d2
starmap1[383] = 0x2a4
starmap1[1509] = 0x61c
starmap1[675] = 0x313
starmap1[467] = 0x574
starmap1[568] = 0x5e2
starmap1[1104] = 0x4a7
starmap1[856] = 0x413
starmap1[832] = 0x46e
starmap1[928] = 0x52a
starmap1[1549] = 0x61f
starmap1[476] = 0x1e9
starmap1[986] = 0x43d
starmap1[1274] = 0x597
starmap1[399] = 0x624
starmap1[140] = 0x132
starmap1[765] = 0x54c
starmap1[705] = 0x4cc
starmap1[1547] = 0x632
starmap1[1291] = 0x561
starmap1[1435] = 0x5b8
starmap1[132] = 0x416
starmap1[1213] = 0x588
starmap1[978] = 0x4ed
starmap1[275] = 0x62a
starmap1[246] = 0x36e
starmap1[104] = 0x45c
starmap1[1489] = 0x5f0
starmap1[67] = 0x317
starmap1[841] = 0x51f
starmap1[638] = 0x28b
starmap1[370] = 0x331
starmap1[288] = 0x440
starmap1[996] = 0x4e2
starmap1[1076] = 0x620
starmap1[1295] = 0x63b
starmap1[1443] = 0x5c3
starmap1[1535] = 0x624
starmap1[747] = 0x378
starmap1[1227] = 0x5f8
starmap1[139] = 0x3df
starmap1[77] = 0x1e9
starmap1[818] = 0x4fc
starmap1[1074] = 0x457
starmap1[1121] = 0x55d
starmap1[1498] = 0x613
starmap1[1234] = 0x5b2
starmap1[795] = 0x3db
starmap1[1183] = 0x63e
starmap1[1266] = 0x611
starmap1[376] = 0x584
starmap1[1126] = 0x544
starmap1[322] = 0x45b
starmap1[404] = 0x5c1
starmap1[81] = 0x2df
starmap1[916] = 0x3fc
starmap1[499] = 0x400
starmap1[91] = 0x4d0
starmap1[1084] = 0x54b
starmap1[514] = 0x214
starmap1[270] = 0x501
starmap1[1066] = 0x4df
starmap1[953] = 0x59b
starmap1[125] = 900
starmap1[301] = 0x514
starmap1[1200] = 0x638
starmap1[1196] = 0x52c
starmap1[1223] = 0x550
starmap1[865] = 0x39e
starmap1[156] = 0x5c7
starmap1[118] = 0x32a
starmap1[966] = 0x4c1
starmap1[250] = 0x5df
starmap1[1557] = 0x631
starmap1[16] = 0x51c
starmap1[334] = 0x3fa
starmap1[284] = 0x4ae
starmap1[1298] = 0x595
starmap1[1162] = 0x4d0
starmap1[793] = 0x49a
starmap1[236] = 0x539
starmap1[896] = 0x3b9
starmap1[291] = 0x4a8
starmap1[1301] = 0x5b6
starmap1[279] = 0x520
starmap1[678] = 0x440
starmap1[954] = 0x4d2
starmap1[1456] = 0x5ce
starmap1[779] = 0x61f
starmap1[124] = 0x2ab
starmap1[725] = 0x60a
starmap1[1358] = 0x5e0
starmap1[946] = 0x484
starmap1[634] = 0x58d
starmap1[864] = 0x600
starmap1[773] = 0x376
starmap1[1141] = 0x4b5
starmap1[298] = 0x298
starmap1[1305] = 0x61a
starmap1[1463] = 0x628
starmap1[677] = 0x43f
starmap1[639] = 0x28b
starmap1[1243] = 0x596
starmap1[1270] = 0x5f3
starmap1[848] = 0x3f0
starmap1[1165] = 0x4b6
starmap1[1500] = 0x62a
starmap2[618] = 0x1b3
starmap2[1298] = 0x118
starmap2[93] = 0x19
starmap2[1050] = 0x1ce
starmap2[850] = 0x3b
starmap2[242] = 0xcd
starmap2[222] = 0x2d
starmap2[1038] = 0x115
starmap2[1504] = 0x3a
starmap2[262] = 0x3f
starmap2[664] = 0x219
starmap2[194] = 0x65
starmap2[225] = 0x2b
starmap2[953] = 0x11f
starmap2[663] = 400
starmap2[1073] = 0x408
starmap2[15] = 2
starmap2[928] = 0xa7
starmap2[72] = 3
starmap2[412] = 0x27
starmap2[1562] = 0x3f3
starmap2[911] = 0x26f
starmap2[318] = 0xf8
starmap2[1409] = 0x2a4
starmap2[972] = 0x16e
starmap2[615] = 0xc3
starmap2[277] = 0x10a
starmap2[361] = 0xce
starmap2[101] = 0x13
starmap2[1454] = 0x41d
starmap2[98] = 0x2b
starmap2[1031] = 0x172
starmap2[551] = 0x205
starmap2[446] = 0x18e
starmap2[1471] = 0x4a8
starmap2[79] = 0x42
starmap2[996] = 0x8b
starmap2[542] = 0x205
starmap2[1125] = 0x116
starmap2[973] = 0x10a
starmap2[111] = 0xc
starmap2[581] = 0x14f
starmap2[259] = 0x5f
starmap2[1134] = 0x2a3
starmap2[571] = 0x21d
starmap2[1096] = 0x27d
starmap2[606] = 0x244
starmap2[26] = 10
starmap2[1412] = 0x1ff
starmap2[1519] = 0x3e4
starmap2[127] = 0x55
starmap2[1018] = 0x219
starmap2[215] = 0x20
starmap2[97] = 0x4e
starmap2[494] = 0x9f
starmap2[992] = 0x202
starmap2[1380] = 0x27c
starmap2[701] = 0x253
starmap2[295] = 0x4c
starmap2[1089] = 0x2c0
starmap2[1203] = 0x3d2
starmap2[1600]  = 0x228
starmap2[309] = 0x108
starmap2[1237] = 0x435
starmap2[139] = 3
starmap2[298] = 0x10
starmap2[1239] = 4
starmap2[1492] = 0xe1
starmap2[703] = 0xb0
starmap2[1313] = 0x5e
starmap2[1094] = 0x2b2
starmap2[1264] = 0x26d
starmap2[797] = 0x22
starmap2[338] = 0xa2
starmap2[1047] = 0x398
starmap2[782] = 0x2f7
starmap2[806] = 0x1e7
starmap2[528] = 0x16c
starmap2[300] = 0x9c
starmap2[1257] = 0x1e7
starmap2[858] = 0x1b6
starmap2[401] = 0xc9
starmap2[329] = 0xf1
starmap2[1434] = 0x3b6
starmap2[462] = 0x17f
starmap2[143] = 0x57
starmap2[286] = 199
starmap2[254] = 0xdd
starmap2[1027] = 0x1b
starmap2[179] = 99
starmap2[57] = 0x25
starmap2[1379] = 0x1c2
starmap2[772] = 0x1e3
starmap2[811] = 0x9b
starmap2[1110] = 0x2a1
starmap2[132] = 0x37
starmap2[1211] = 0x490
starmap2[1175] = 0x30a
starmap2[1210] = 0x113
starmap2[661] = 0x179
starmap2[178] = 0x43
starmap2[970] = 0x224
starmap2[1522] = 0x415
starmap2[1462] = 0x1a9
starmap2[1491] = 0x331
starmap2[1119] = 0xf2
starmap2[1147] = 0x210
starmap2[1287] = 0x28a
starmap2[1354] = 0x21e
starmap2[652] = 199
starmap2[641] = 0x1db
starmap2[1483] = 0x4da
starmap2[270] = 0xe9
starmap2[1155] = 0x44d
starmap2[940] = 0x394
starmap2[1227] = 0x46b
starmap2[1448] = 0x372
starmap2[171] = 0x76
starmap2[632] = 0x19a
starmap2[948] = 0x344
starmap2[415] = 0x170
starmap2[76] = 0x11
starmap2[835] = 0x29
starmap2[1384] = 0x288
starmap2[1112] = 0x2cf
starmap2[207] = 0x5a
starmap2[1532] = 0x72
starmap2[469] = 0x58
starmap2[252] = 0xd8
starmap2[1441] = 0x369


#print(starmap1)
#print(starmap2)

# get the potential next step, and then the potential state afterwards
def getAdjacents(node):
    adjacent = []
    curr_starmap1 = node['starmap1']
    curr_starmap2 = node['starmap2']
    curr_index = node['curr_index']
    
    for i in range (1,9):
        if curr_index+i == 1600:
            roll = { 'curr_index': curr_index+i, 'increment': i,  'starmap1': curr_starmap1.copy(), 'starmap2': curr_starmap2.copy() }
            adjacent.append(roll)
            continue
        if curr_index+i > 1600:
            continue
        roll = { 'curr_index': curr_index+i, 'increment': i,  'starmap1': curr_starmap1.copy(), 'starmap2': curr_starmap2.copy() }
        if curr_starmap1[curr_index+i] != 0:
            new_starmap1 = curr_starmap1.copy()
            new_starmap1[curr_index+i] = 0
            roll = { 'curr_index': curr_starmap1[curr_index+i], 'increment': i,  'starmap1': new_starmap1, 'starmap2': curr_starmap2.copy() }
        elif curr_starmap2[curr_index+i+1] != 0:
            new_starmap2 = curr_starmap2.copy()
            new_starmap2[curr_index+i+1] = 0
            roll = { 'curr_index': curr_starmap2[curr_index+i+1], 'increment': i,  'starmap1': curr_starmap1.copy(), 'starmap2': new_starmap2 }
        adjacent.append(roll)

    return adjacent


def bfs(start, end):

    initial_node = { 'curr_index': start, 'increment': 0,  'starmap1': starmap1.copy(), 'starmap2': starmap2.copy() }
    queue = deque([[initial_node]])

    visited = set()

    queue.append([initial_node])
    while queue:
        path = queue.popleft()
        
        node = path[-1]
        
        if node['curr_index'] == end:
            return path

        if node['curr_index'] not in visited:
            visited.add(node['curr_index'])

            for adjacent in getAdjacents(node):
                #print(f'path: {path}')
                #input()
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
    return None

path = bfs(0, 1600)

node = path[-1]

print(f'fuel required: {len(path)-1}')
for i in path:
    print(f'{i["curr_index"]} +{i["increment"]}')

starmap1 = node['starmap1']
starmap2 = node['starmap2']

new_path = bfs(0,1600)

print(f'fuel required: {len(new_path)-1}')
for i in new_path:
    print(f'{i["curr_index"]} +{i["increment"]}')
