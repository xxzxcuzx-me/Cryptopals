import random
import math
from Crypto.Hash import SHA256
import base64
from math import ceil
from os import urandom
import challenge39

def modexp(g, u, p):
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

def extendedGCD(a, b):
	lastRemainder=abs(a)
	remainder=abs(b)
	x, lastX, y, lastY = 0, 1, 1, 0

	while remainder:
		lastRemainder, (quotient, remainder) = remainder, divmod(lastRemainder, remainder) 
		x, lastX = lastX - quotient*x, x
		y, lastY = lastY - quotient*y, y

	return lastRemainder, lastX*(-1 if a < 0 else 1), lastY*(-1 if b < 0 else 1)

def invmod(a, m):
	g, x, y = extendedGCD(a, m)
	if g != 1:
		raise ValueError
	return x % m

def encrypt(message, e, n):
	return modexp(message, e, n)

def decrypt(message, d, n):
	return modexp(message, d, n)

def floorRoot(n, s):
    b = n.bit_length()
    p = math.ceil(b/s)
    x = 2**p
    while x > 1:
        y = (((s - 1) * x) + (n // (x**(s-1)))) // s
        if y >= x:
            return x
        x = y
    return 1

def oracle(ciphertext):
	decrypted = decrypt(ciphertext, d, n)
	decrypted = decrypted.to_bytes(ceil(n.bit_length()/8), "big")
	return (decrypted[0] == 0 and decrypted[1] == 2)
	
def pad(message, k):
	prepend=bytearray([0, 2])
	bmessage=bytearray(message, "UTF-8")
	bmessage= bytearray([0]) + bmessage
	padding=urandom(k-2-len(bmessage))
	return prepend+padding+bmessage

def findFirstS(c0):
	s1 = (n + 3*B - 1) // (3*B)
	multiplier=encrypt(s1, e, n)
	while not oracle((multiplier*c0)%n):
		s1+=1
		multiplier=encrypt(s1, e, n)
	return s1

def findNextS(c0, a, b, lastS):
	r = (2 * (b * lastS - 2 * B) + n - 1) // n
	while True:
		lower = (2*B + r*n + b - 1) // b
		upper = (3*B + r*n + a - 1) // a
		for s in range(lower, upper):
			multiplier=encrypt(s, e, n)
			if oracle((multiplier*c0)%n):
				return s
		r+=1

def findNextInterval(s, a, b):
	r = (a * s - 3 * B + 1 + n - 1) // n
	lower=max(a, (2*B + r*n + s - 1) // s)
	upper=min(b, (3*B - 1 + r*n) // s)
	return (lower, upper)

pub, priv = challenge39.genKey(256)
e, n = pub
d, n = priv

k=ceil(n.bit_length()/8)
message="kick it, CC"
message=pad(message, k)
encrypted=encrypt(int.from_bytes(message, "big"), e, n)

B=2**(8*(k-2))
M=(2*B, 3*B-1)
s=findFirstS(encrypted)
M=findNextInterval(s, M[0], M[1])
while M[0] != M[1]:
	s=findNextS(encrypted, M[0], M[1], s)
	M=findNextInterval(s, M[0], M[1])

print(M[0].to_bytes(k, "big"))
		