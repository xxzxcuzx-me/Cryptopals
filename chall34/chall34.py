import random
from os import urandom
from Crypto.Hash import SHA1
from Crypto.Cipher import AES

def modexp(g, u, p):
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

class Bot:
	
	def setPublic(self, newP, newG, newA):
		self.p=newP
		self.g=newG
		self.b=random.randint(0, self.p-1)
		self.A=newA
		self.B=modexp(self.g, self.b, self.p)
		self.s=bytearray(str(modexp(self.A, self.b, self.p)), "UTF-8")
		return self.B

	def echo(self, msg, iv):
		hashObj=SHA1.new()
		hashObj.update(self.s)
		key=hashObj.digest()[:16]
		newIV=urandom(16)

		obj=AES.new(key, AES.MODE_CBC, iv)
		decrypted=obj.decrypt(msg)

		obj2=AES.new(key, AES.MODE_CBC, newIV)
		encrypted=obj2.encrypt(decrypted)
		return(encrypted, newIV)

class MITM:
	def __init__(self, bot):
		self.bot=bot

	def setPublic(self, newP, newG, newA):
		self.p=newP
		self.g=newG
		self.bot.setPublic(self.p, self.g, self.p)
		self.s=bytearray(str(modexp(self.p, a, self.p)), "UTF-8")
		return self.p

	def echo(self, msg, iv):
		hashObj=SHA1.new()
		hashObj.update(self.s)
		key=hashObj.digest()[:16]
		obj=AES.new(key, AES.MODE_CBC, iv)
		decrypted=obj.decrypt(msg)
		print("Decrypting client message: ", decrypted.decode("UTF-8"))

		(newEncrypted, newIV)=self.bot.echo(msg, iv)
		obj2=AES.new(key, AES.MODE_CBC, newIV)
		decrypted=obj2.decrypt(newEncrypted)
		print("Decrypting bot response: ", decrypted.decode("UTF-8"))

		obj3=AES.new(key, AES.MODE_CBC, newIV)
		encrypted=obj3.encrypt(decrypted)
		return(encrypted, newIV)

echoBot=Bot()
attacker=MITM(echoBot)

message=bytearray("testtesttesttest", "UTF-8")
p=0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g=2

a=random.randint(0, p-1)
A=modexp(g, a, p)
B=attacker.setPublic(p, g, A)
s=bytearray(str(modexp(B, a, p)), "UTF-8")

hashObj=SHA1.new()
hashObj.update(s)
key=hashObj.digest()[:16]
iv=urandom(16)

obj=AES.new(key, AES.MODE_CBC, iv)
encrypted=obj.encrypt(message)

(newEncrypted, newIV)=attacker.echo(encrypted, iv)
obj2=AES.new(key, AES.MODE_CBC, newIV)
decrypted=obj2.decrypt(newEncrypted)