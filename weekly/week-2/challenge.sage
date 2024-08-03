flag = "<REDACTED>"
n = 4
p = 257
F = GF(p)
ascii_values = [ord(char) for char in flag]
R.<x> = PolynomialRing(F)
P = sum(F(ascii_values[i]) * x^i for i in range(len(ascii_values)))
unity_poly = x^n - 1
roots_of_unity = unity_poly.roots(multiplicities=False)
Q = P * unity_poly
print(Q.list())

