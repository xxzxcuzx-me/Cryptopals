from Crypto.Hash import SHA256
from Crypto.Hash import HMAC
import random
from os import urandom

def modexp(g, u, p):
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

N=0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g=2
k=3

class Server:
	def __init__(self):
		self.accounts={'': [0,0,0,0,0,0]}

	def createAccount(self, email, password):
		salt=random.randint(0, 0xffffffffffffffff)
		hashMachine=SHA256.new()
		hashMachine.update(bytearray(str(salt), "UTF-8")+password)
		hashedInt=int.from_bytes(hashMachine.digest(), "big")
		v=modexp(g, hashedInt, N)
		self.accounts[email]=[v, salt, 0, 0, 0, 0]
	
	def challenge(self, email, A):
		b=random.randint(0, N-1)
		u=int.from_bytes(urandom(16), "big")
		B=modexp(g, b, N)
		#try:
		self.accounts[email][2]=b
		self.accounts[email][3]=A
		self.accounts[email][4]=B
		self.accounts[email][5]=u
		return (B, self.accounts[email][1], u)

	def check(self, email, hmac):
		S=modexp(self.accounts[email][3]*modexp(self.accounts[email][0], self.accounts[email][5], N), self.accounts[email][2], N)
		hashMachine=SHA256.new()
		hashMachine.update(bytearray(str(S), "UTF-8"))
		K=hashMachine.digest()
		serverHMACMachine=HMAC.new(K)
		serverHMACMachine.update(bytearray(str(self.accounts[email][1]), "UTF-8"))
		HMACToTest=serverHMACMachine.hexdigest()
		if hmac==HMACToTest:
			print("OK")

class MITM():
	def __init__(self):
		self.wordlist=["dupa", "xd", "beniz", "secret"]
	def createAccount(self, email, password):
		self.email=email

	def challenge(self, email, A):
		self.A=A
		self.salt=random.randint(0, 0xffffffffffffffff)
		self.b=random.randint(0, N-1)
		self.u=int.from_bytes(urandom(16), "big")
		B=modexp(g, self.b, N)
		return (B, self.salt, self.u)

	def check(self, email, hmac):
		self.hmac=hmac

	def crack(self):
		guessedHMAC=''
		for password_guess in self.wordlist:
			hashMachine=SHA256.new()
			hashMachine.update(bytearray(str(self.salt), "UTF-8")+bytearray(password_guess, "UTF-8"))
			hashedInt=int.from_bytes(hashMachine.digest(), "big")
			v=modexp(g, hashedInt, N)
			S=modexp(self.A*modexp(v, self.u, N), self.b, N)
			hashMachine=SHA256.new()
			hashMachine.update(bytearray(str(S), "UTF-8"))
			K=hashMachine.digest()
			serverHMACMachine=HMAC.new(K)
			serverHMACMachine.update(bytearray(str(self.salt), "UTF-8"))
			HMACToTest=serverHMACMachine.hexdigest()
			if HMACToTest==self.hmac:
				print("Email:", self.email, "Password:", password_guess)
				break
		else:
			print("Password not found")

serv=MITM()

email="test"
password="secret"
a=random.randint(0, N-1)
A=modexp(g, a, N)

serv.createAccount(email, bytearray(password,"UTF-8"))
response=serv.challenge(email, A)

#(salt|password)
hashMachine=SHA256.new()
hashMachine.update(bytearray(str(response[1]), "UTF-8")+bytearray(password,"UTF-8"))
hashedInt=int.from_bytes(hashMachine.digest(), "big")
S=modexp(response[0], a+response[2]*hashedInt, N)

hashMachine=SHA256.new()
hashMachine.update(bytearray(str(S), "UTF-8"))
K=hashMachine.digest()

clientHMACMachine=HMAC.new(K)
clientHMACMachine.update(bytearray(str(response[1]), "UTF-8"))
HMACToTest=clientHMACMachine.hexdigest()

serv.check(email, HMACToTest)

serv.crack()