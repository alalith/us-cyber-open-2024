#!/usr/bin/env python3

'''
	GOAL : Pure python solution for RSA small exponent attack

	since cipher is a very large integer python generally throws
	overflow error, to solve that I have used decimal module which is
	part of the standard python library

	decimal module offers user defined precision which can be increased
	as much as we want

	here precision = number of decimal places

	default value is 28 but that wont be enough for larger integers
	such as our cipher text but we dont know at what precision we will
	get perfect cube root so we can bruteforce precision and round it off
'''

from decimal import *

e = 3
c = 24169313728564942442211774792718133649505303766122840641824238947925887523809659286479788261358160947897827563877730687191196979635981766007541262794064747436339518434662376001187909548541032912960261470378632234919864504416430112988325282635602076675727609986764939035311005911495050936123288502045541159782290557092166459385730265169804173086982862520503253166994397834568988061050489364671603850794860660038045636906752404250094067941258320535890143754097216
i = 100

while i < 2000:
	# set precision
	getcontext().prec = i

	# calculate cube root with values wrapped in decimal
	# it is then rounded off using Decimal.to_integral_exact()
	cube_root = int((Decimal(c) ** (Decimal(1) / Decimal(3))).to_integral_exact())

	# remove 0x from start of string
	hex_str = hex(cube_root)[2:]
	try:
		dehex = bytes.fromhex(hex_str).decode()
		flag = bytes.fromhex(dehex).decode()
		if flag.startswith('twc{') and flag.endswith('}'):
			print('Precision :', i)
			print('FLAG      :', flag)
			break
	except UnicodeDecodeError:
		pass
	except ValueError:
		pass
	i += 1
