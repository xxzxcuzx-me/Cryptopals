import random
import math
from Crypto.Hash import SHA256
import base64

def modexp(g, u, p):
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

def generatePrime(bits):
	p = 0
	while (p%2 == 0 or pow(2, (p-1), p) != 1):
		p = random.randint(2**(bits-1), 2**bits-1)
	return p

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

def oracle(ciphertext, d, n):
	decrypted = decrypt(ciphertext, d, n)
	return decrypted%2

numberOfBits=1024
e=3
p, q, n, et, d = 0, 0, 0, 0, 0
errorFlag=True
while errorFlag:
	errorFlag=False
	p=generatePrime(numberOfBits)
	q=generatePrime(numberOfBits)
	n=p*q
	et=(p-1)*(q-1)
	try:
		d=invmod(e, et)
	except ValueError:
		errorFlag=True



message="VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=="
message=base64.b64decode(message)
message=int.from_bytes(message, "big")
encrypted=encrypt(message, e, n)

print("Starting decrypting...")
low = 0
high = 1
denom = 1
c = encrypted
k = pow(2, e, n)
for _ in range(n.bit_length()):
    c  = (c * k) % n
    h = oracle(c, d, n)
    l = high - low
    low *= 2
    high *= 2
    denom *= 2
    if h == 0:
        high -= l
    else:
        low += l
    hightext = n * high // denom
    print(hightext.to_bytes(len(str(hightext)), "big"))	

print("Decrypted:", hightext.to_bytes(len(str(hightext)), "big").decode("UTF-8").lstrip(chr(0)))