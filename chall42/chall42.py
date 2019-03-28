import random
import math
from Crypto.Hash import SHA256

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

def validateCertificate(certificate, message, e, n):
	decrypted=decrypt(certificate, e, n)
	certificate=decrypted.to_bytes(128, "big")
	if certificate[:3] == bytearray([0x00, 0x01, 0xff]):
		j=0
		for i in range(3, len(certificate)):
			if certificate[i] == 0x00:
				j=i
				break
		else:
			print("Certificate not valid - no 0 byte")
			return

		hashMachine=SHA256.new()
		hashMachine.update(bytearray(message, "UTF-8"))
		calculatedHash=hashMachine.digest()
		if calculatedHash==certificate[j+1:j+33]:
			print("Certificate is valid")
		else:
			print("Certificate not valid - wrong hash")
	else:
		print("Certificate not valid - wrong first 3 bytes")
		return

def createCertificate(message, d, n):
	hashMachine=SHA256.new()
	hashMachine.update(bytearray(message, "UTF-8"))
	calculatedHash=hashMachine.digest()
	preparedMessage=bytearray([0x00, 0x01] + [0xff]*(128-len(calculatedHash)-3) + [0x00]) + calculatedHash
	preparedMessage=int.from_bytes(preparedMessage, "big")
	return encrypt(preparedMessage, d, n)

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

def forgeFakeCertificate(message):
	hashMachine=SHA256.new()
	hashMachine.update(bytearray(message, "UTF-8"))
	calculatedHash=hashMachine.digest()
	preparedMessage=bytearray([0x00, 0x01] + [0xff] + [0x00]) + calculatedHash + bytearray([0x0]*(128-len(calculatedHash)-4))
	preparedMessage=int.from_bytes(preparedMessage, "big")
	return floorRoot(preparedMessage, 3)+1

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

message="hi mom"
cert=createCertificate(message, d, n)
validateCertificate(cert, message, e, n)
forged=forgeFakeCertificate(message)
validateCertificate(forged, message, e, n)