import random
import math
from Crypto.Hash import SHA1

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

def validateCertificate(message, q, y, r, s):
	hashMachine=SHA1.new()
	hashMachine.update(bytearray(message, "UTF-8"))
	hashed=hashMachine.digest()
	hashed=int.from_bytes(hashed, "big")

	w=invmod(s, q)%q
	u1=(hashed*w)%q
	u2=(r*w)%q

	v=((modexp(g, u1, p)*modexp(y, u2, p))%p)%q
	if v == r:
		print("Certificate is valid")
		return True
	else:
		print("Certificate is not valid")	
		return False

def createCertificate(message, p, q, g, x):
	hashMachine=SHA1.new()
	hashMachine.update(bytearray(message, "UTF-8"))
	hashed=hashMachine.digest()
	hashed=int.from_bytes(hashed, "big")

	k=random.randint(2, q-1)
	r=modexp(g, k, p)%q

	s=(invmod(k, q)*(hashed+x*r))%q
	return (r, s)

def retrievePrivateKey(hashed, q, k, s, r):
	return ((s*k-hashed)*invmod(r, q))%q

#parameter generation
p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0
#private
x=random.randint(0, q)
#public
y=modexp(g, x, p)

message="hi mom"
(r, s)=createCertificate(message, p, q, g, x)
validateCertificate("bye mom", q, y, r, s)
#actual challenge

g=p+1
x=random.randint(0, q)
y=modexp(g, x, p)
z=2
r = modexp(y, z, p) % q

s = (r * invmod(z, q))%q

validateCertificate("Hello, world", q, y, r, s)
validateCertificate("Goodbye, world", q, y, r, s)