import random
import time
import os

MT=[0]*624
index=0

def initializeGenerator(seed):
	global index
	global MT
	index=0
	MT[0]=seed
	for i in range(1, 624):
		MT[i]=(1812433253*(MT[i-1]^(MT[i-1]>>30))+i)%4294967296

def extractNumber():
	global index
	global MT	
	if index==0:
		generateNumbers()

	y=MT[index]
	y=y^(y>>11)
	y=y^((y<<7)&2636928640)
	y=y^((y<<15)&4022730752)
	y=y^(y>>18)
	index=(index+1)%624
	return y

def generateNumbers():
	global MT
	for i in range(624):
		y=MT[i]&0x80000000+MT[(i+1)%624]&0x7fffffff
		MT[i]=MT[(i+397)%624]^(y>>1)
		if y%2==1:
			MT[i]=MT[i]^2567483615

def invExtractNumber(num):
	num=(num&0xFFFFC000)|((num>>18)^(num&0x3FFF))
	num=((num<<15)&0xEFC60000)^(num&0xFFFE0000)|(num&0x1FFFF)
	#second step
	seven5=num&0x7F
	seven4=(num&0x3F80)^((seven5<<7)&2636928640)
	seven3=(num&0x1FC000)^((seven4<<7)&2636928640)
	seven2=(num&0xFE00000)^((seven3<<7)&2636928640)
	seven1=(num&0xF0000000)^((seven2<<7)&2636928640)
	num=seven1|seven2|seven3|seven4|seven5
	#first step
	eleven1=num&0xFFE00000
	eleven2=(eleven1>>11)^(num&0x1FFC00)
	last=(eleven2>>11)^(num&0x3FF)
	num=eleven1|eleven2|last
	return num

def generateKeyStream(length, seed):
	initializeGenerator(seed)
	keyStream=[]
	i=0
	while i<length:
		gen=extractNumber()
		keyStream.append(gen&0xFF)
		keyStream.append((gen&0xFF00)>>8)
		keyStream.append((gen&0xFF0000)>>16)
		keyStream.append((gen&0xFF000000)>>24)
		i+=4
	return keyStream

def xorWithKeyStream(text, seed):
	keyStream=generateKeyStream(len(text), seed)
	i=0
	output=[]
	while i<len(text):
		output.append(keyStream[i]^text[i])
		i+=1
	return output

knownPlaintext='A'*14
randomLength=random.randint(14, 256)
randomPlaintext=''
for i in range(randomLength):
	randomPlaintext+=chr(random.randint(65, 90))

plaintext=randomPlaintext+knownPlaintext
seed=random.randint(0, 0xffff)
encrypted=xorWithKeyStream(bytearray(plaintext, "UTF-8"), seed)

for i in range(0x10000):
	decrypted=bytearray(xorWithKeyStream(encrypted, i))
	if decrypted[-len(knownPlaintext):]==bytearray(knownPlaintext, "UTF-8"):
		print("Found correct seed", i)
		print("Decrypted ciphertext", decrypted.decode("UTF-8"))
		break