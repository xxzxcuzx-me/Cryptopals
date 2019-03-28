import random
import math

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

assert(invmod(17, 3120)==2753)

numberOfBits=512
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

message="Fck da polize cumming str8 from da unde'ground"
print('Before:', message)
message=int.from_bytes(bytearray(message, "UTF-8"), "big")
encrypted=encrypt(message, e, n)
print('Encrypted:', encrypted)
decrypted=decrypt(encrypted, d, n)
decrypted=decrypted.to_bytes(len(str(decrypted)), "big").decode("UTF-8").lstrip(chr(0))

print('Decrypted:', decrypted)