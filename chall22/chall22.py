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

time.sleep(random.randint(40, 1000))
seedTime=int(time.time())
initializeGenerator(seedTime)
time.sleep(random.randint(40, 1000))
randomNum=extractNumber()
print(randomNum)

currentTime=int(time.time())
for i in range(2100):
	index=0
	MT=[0]*624
	guessedSeed=currentTime-i
	initializeGenerator(guessedSeed)
	num=extractNumber()
	if num==randomNum:
		print("Seed time was:", guessedSeed)
		print("It was", currentTime-guessedSeed, "seconds ago")
		if(guessedSeed==seedTime):
			print("And I was right!")
		break
		