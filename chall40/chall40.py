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

assert(invmod(17, 3120)==2753)

numberOfBits=256
e=3
message="Fck da polize cumming str8 from da unde'ground"
pubKeys=[]
ciphertexts=[]
for i in range(3):
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
	pubKeys.append([e, n])
	ciphertexts.append(encrypt(int.from_bytes(bytearray(message, "UTF-8"), "big"), e, n))

c0=ciphertexts[0]
c1=ciphertexts[1]
c2=ciphertexts[2]

n0=pubKeys[0][1]
n1=pubKeys[1][1]
n2=pubKeys[2][1]

ms0=n1*n2
ms1=n0*n2
ms2=n0*n1

N=n0*n1*n2

r0=(c0*ms0*invmod(ms0, n0))
r1=(c1*ms1*invmod(ms1, n1))
r2=(c2*ms2*invmod(ms2, n2))

result=(r0+r1+r2)%N

decrypted=floorRoot(result, 3)
print(decrypted)
decrypted=decrypted.to_bytes(len(str(decrypted)), "big").decode("UTF-8").lstrip(chr(0))
print('Decrypted:', decrypted)