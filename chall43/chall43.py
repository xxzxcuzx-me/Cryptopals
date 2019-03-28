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
	if r <=0 or r >= q or s <=0 or s >= q:
		print("Certificate is not valid")
		return False
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
	s=0
	while s==0:
		k=random.randint(2, q-1)
		r=modexp(g, k, p)%q
		while r == 0:
			k=random.randint(2, q-1)
			r=modexp(g, k, p)%q

		s=(invmod(k, q)*(hashed+x*r))%q
	return (r, s)

def retrievePrivateKey(hashed, q, k, s, r):
	return ((s*k-hashed)*invmod(r, q))%q

#parameter generation
p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

#private
x=random.randint(0, q)
#public
y=modexp(g, x, p)

message="hi mom"
(r, s)=createCertificate(message, p, q, g, x)
validateCertificate(message, q, y, r, s)
#actual challenge

y = 0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17
message="""For those that envy a MC it can be hazardous to your health
So be friendly, a matter of life and death, just like a etch-a-sketch
"""

r = 548099063082341131477253921760299949438196259240
s = 857042759984254168557880549501802188789837994940
hashMachine=SHA1.new()
hashMachine.update(bytearray(message, "UTF-8"))
hashed=hashMachine.digest()
hashed=int.from_bytes(hashed, "big")
priv=0
if validateCertificate(message, q, y, r, s):
	for k in range(1, 65537):
		print(k)
		priv=retrievePrivateKey(hashed, q, k, s, r)
		if y == modexp(g, priv, p):
			print("Private key is" , priv)
			break
		
	else:
		print("Private key not found")
(r, s)=createCertificate(message, p, q, g, priv)
validateCertificate(message, q, y, r, s)