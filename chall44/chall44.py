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

def retrievePrivateKey(hashed, q, k, s, r):
	return ((s*k-hashed)*invmod(r, q))%q

#parameter generation
p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

y = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

file = open('44.txt', 'r')

cryptograms=[]
oneCrypto=[]
i=0
for line in file:
	line=line[:-1]
	oneCrypto.append(line.split(': ')[1])
	i+=1
	if i == 4:
		cryptograms.append(oneCrypto)
		i=0
		oneCrypto=[]
file.close()

m1, m2, s1, s2, r1 = 0, 0, 0, 0, 0

for i in range(len(cryptograms)):
	for j in range(i+1, len(cryptograms)):
		if cryptograms[i][2] == cryptograms[j][2]:
			s1=int(cryptograms[i][1])
			r1=int(cryptograms[i][2])
			m1=int(cryptograms[i][3], 16)
			s2=int(cryptograms[j][1])
			m2=int(cryptograms[j][3], 16)
			break
	else:
		continue
	break

k=(((m1-m2)%q)*invmod((s1-s2)%q, q))%q

priv=retrievePrivateKey(m1, q, k, s1, r1)

if y == modexp(g, priv, p):
	print("k:", k)
	print("Private key:", priv)
else:
	print("Something went wrong")

