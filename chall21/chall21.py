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
	return MT

initializeGenerator(123)
print(extractNumber())
