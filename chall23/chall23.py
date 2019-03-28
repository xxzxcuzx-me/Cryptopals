import random
import time

MT=[0]*624
index=0

def initializeGenerator(seed):
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

def invExtractNumbers(num):
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

seedTime=int(time.time())
initializeGenerator(seedTime)
a=extractNumber()
b=invExtractNumbers(a)

randomNums=[0]*624
for i in range(624):
	randomNums[i]=extractNumber()
for i in range(624):
	MT[i]=invExtractNumbers(randomNums[i])

index=1
for i in range(1, 624):
	if randomNums[i]!=extractNumber():
		print("Nah, wasn't the same")
		break
else:
	print("Every generated 'random' number was the same")

