from z3 import *
from decimal import Decimal, getcontext
import gmpy2
from Crypto.Util.number import *
import functools
import math


def egcd(a, b):
    """Extended gcd of a and b. Returns (d, x, y) such that
    d = a*x + b*y where d is the greatest common divisor of a and b."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def inverse(a, n):
    """Returns the inverse x of a mod n, i.e. x*a = 1 mod n. Raises a
    ZeroDivisionError if gcd(a,n) != 1."""
    d, a_inv, n_inv = egcd(a, n)
    if d != 1:
        raise ZeroDivisionError('{} is not coprime to {}'.format(a, n))
    else:
        return a_inv % n


def lcm(*x):
    """
    Returns the least common multiple of its arguments. At least two arguments must be
    supplied.
    :param x:
    :return:
    """
    if not x or len(x) < 2:
        raise ValueError("at least two arguments must be supplied to lcm")
    lcm_of_2 = lambda x, y: (x * y) // math.gcd(x, y)
    return functools.reduce(lcm_of_2, x)


def carmichael_pp(p, e):
    phi = pow(p, e - 1) * (p - 1)
    if (p % 2 == 1) or (e >= 2):
        return phi
    else:
        return phi // 2


def carmichael_lambda(pp):
    """
    pp is a sequence representing the unique prime-power factorization of the
    integer whose Carmichael function is to be computed.
    :param pp: the prime-power factorization, a sequence of pairs (p,e) where p is prime and e>=1.
    :return: Carmichael's function result
    """
    return lcm(*[carmichael_pp(p, e) for p, e in pp])

class LCG:
	def __init__(self, a, b, p, seed):
		self.a = a
		self.b = b
		self.p = p
		self.seed = seed

	def next(self):
		self.seed = (self.a*self.seed + self.b) % self.p
		return self.seed

def modinv(x,p):
    return pow(x, -1 ,p)
x1 = 5817979666070064699383212732256070495
x2 = 122803915435033307307080628491122907417
x3 = 96413833466614190818049520251833161905

m = 186635132765484126250996539793206145667



multiplier = (x3 - x2) * modinv(x2-x1, m) % m
increment = (x2 - x1 * multiplier) % m

x = x3

y =  (modinv(multiplier, m) * (x - increment)) % m

print(y)
z =  (modinv(multiplier, m) * (y - increment)) % m
print(z)
o5 =  (modinv(multiplier, m) * (x1 - increment)) % m
o4 =  (modinv(multiplier, m) * (o5 - increment)) % m
o3 =  (modinv(multiplier, m) * (o4 - increment)) % m
o2 =  (modinv(multiplier, m) * (o3 - increment)) % m
o1 =  (modinv(multiplier, m) * (o2 - increment)) % m
o0 =  (modinv(multiplier, m) * (o1 - increment)) % m
seed =  (modinv(multiplier, m) * (o0 - increment)) % m

outputs = [o0,o1,o2,o3,o4,o5]
print(outputs)
print(seed)

lcg = LCG(multiplier,increment,m,seed)

for i in range(0,9):
    print(lcg.next())

cipher1 = bytes_to_long(b'\x19\x8b\x06<a\xfa\x00*\x8b\x9d\xabf\x0b\x84]!{,\x0f\x00\xf1\x11c\x15~Ax\x84$\xb3\xabn\xc9\xd4f\x7fa\x0b7z\xd7\xe7\xaf')
cipher1 = 3575621442076514417844667434041008118318918838370776314935631750400935086310559330079610560846371481518
#cipher1 = 24623982103864037902592261524731176908146265129794195723565319004348368246080900349707205949305813109529
#cipher1 = 0x198b063c61fa002a8b9dab660b845d217b2c0f00f11163157e41788424b3ab6ec9d4667f610b377ad7e7af
#cipher2 = bytes_to_long(b'\n;RG\xbe\xd9\xfa\x1cN\x9a\x9c \xa5\x08\x8b\xa3\xea\xe0)\x9d\xd1V7f\xfd\xf2\xf2#>H\xe9\x0e\xb6hJ\xff\x99\xa0\xd0\x01\xcf\xc9F')
#cipher2= 0x0a3b5247bed9fa1c4e9a9c20a5088ba3eae0299dd1563766fdf2f2233e48e90eb6684aff99a0d001cfc946
cipher2 = 1432278161611618120085753481769153031750119452195934781170091281038648483403852034747517731898647365958
#cipher3 = bytes_to_long(b'\x17\\\xfaRO\x14\x965\x9eG\x17\xbcu\xb8q\xdd\xc7v\x0e\\\x93\xfdqN\xec\xf7U\x14l\xfdn\xa6\xf7\x05Z\x1e\xee\xc3\xb8\xdc:i\x15')
#cipher3 = 0x175cfa524f1496359e4717bc75b871ddc7760e5c93fd714eecf755146cfd6ea6f7055a1eeec3b8dc3a6915
cipher3 = 3270474517070364969579219971129298269784593302833331160969961538642009310938547772704007052184293894421

d1 = cipher1 + cipher2 + cipher3 - outputs[1] - outputs[3] - outputs[5]
d2 = outputs[0]+outputs[2]+outputs[4]

getcontext().prec = 670

print(d1)
print(d2)
N = 58875529304338905505953736667221291201023306734480969247806744848754691476474059614663016432386992446676367074190570583945448346734199513681690392081616727023248926447123883344310985916849639888321099825559426707949564522612871413289064362345332045923908212157578793253630638285901734823301475623394385357159

print(modinv(45714565771547930229226359824324184612765804704488147361405122171431410830457625531894507696079301820876695796609440647494597444433096375990065249515774077523541239928616914554861842429334485025363517166565849602924745902936379628721161367954518076487229592008473203339185677650566708246361459229275716576568,N))
#print(c1)
print(pow(cipher1,3,N))

c1 = 45714565771547930229226359824324184612765804704488147361405122171431410830457625531894507696079301820876695796609440647494597444433096375990065249515774077523541239928616914554861842429334485025363517166565849602924745902936379628721161367954518076487229592008473203339185677650566708246361459229275716576568
c2 = 2938205115049708668056485138176403871361086853648934101627506232566239668541574581519458081557120773367632388591435452676969637296270182244964860487777690358171660162952614090569560548502878423451486434716376263912348986733178496729565668523867452903707337375044080831942666690338685816022188990893636320298
c3 = 349810070997348372385332997581386496446517880511047718646911067249375009331456488744287210150453793419941100645233658751502454879549553237101928125595322349868735114829942294943478410438857945193882279241133

        
print(gmpy2.iroot(modinv(c1,N),3))
print((2999924083994519625895112672845090820639808672720177419859247265639235799353095814303574547902147887067-outputs[1])//outputs[0])
print(long_to_bytes(417732898165270131822121709109999740174737144440970544871744683768))
#print(d1/d2)
#print(cipher1-outputs[1])
#print(long_to_bytes(gmpy2.f_div(d1,d2)))
#print(long_to_bytes(gmpy2.f_div(cipher1-outputs[1],outputs[0])))
##print(cipher1-outputs(1)
#print(Decimal(cipher2-outputs[3])/Decimal(outputs[2]))
#print(Decimal(cipher3-outputs[5])/Decimal(outputs[4]))
#lcg = LCG(multiplier,increment,m,seed)

#print(long_to_bytes(497897502043332906273675113686101822792064792234516238510719961870))
#print(multiplier)
#print(increment)

print(outputs[0],outputs[2],outputs[4])
print(outputs[1],outputs[3],outputs[5])
#print(outputs[1])

