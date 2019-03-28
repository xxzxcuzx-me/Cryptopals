import argparse
from string import ascii_lowercase, ascii_letters, printable, punctuation
import base64

parser = argparse.ArgumentParser(description='Crack a string XORed with key of unknown size')
parser.add_argument("-f", "--filename", help="File with base64 encoded XORed string", required=True, action="store")

args=parser.parse_args()

frequencies = {
	'a':0.08167,	
	'b':0.01492,
	'c':0.02782,	
 	'd':0.04253,	
	'e':0.12702,	
	'f':0.02228,	
 	'g':0.02015,	
 	'h':0.06094,	
 	'i':0.06966,	
 	'j':0.00153,	
 	'k':0.00772,	
 	'l':0.04025,	
 	'm':0.02406,	
 	'n':0.06749,	
 	'o':0.07507,	
 	'p':0.01929,	
 	'q':0.00095,	
 	'r':0.05987,	
 	's':0.06327,	
	't':0.09056,	
 	'u':0.02758,	
	'v':0.00978,	
	'w':0.02360,	
 	'x':0.00150,	
	'y':0.01974,	
	'z':0.00074	
}

def calculatedistance(first, second):
	binfirst=''.join(format(x, 'b').zfill(8) for x in bytearray(first, "UTF-8"))
	binsecond=''.join(format(x, 'b').zfill(8) for x in bytearray(second, "UTF-8"))
	if(len(binfirst)<len(binsecond)):
		binfirst=(len(binsecond)-len(binfirst))*"0"+binfirst
	elif(len(binsecond)<len(binfirst)):
		binsecond=(len(binfirst)-len(binsecond))*"0"+binsecond
	distance=len(list(filter(lambda xy: xy[0]!=xy[1], zip(binfirst, binsecond))))
	return distance

def rate(stringtorate):
	result=0
	for c in ascii_lowercase:
		count=0
		stringtorate=stringtorate.lower()
		for d in stringtorate:
			if d in ascii_letters or d in punctuation or d == ' ':
				if d==c:
					count+=1
		result+=pow(frequencies[c]-(count/len(stringtorate)), 2)	
	return result

content = "JwxTBxELMFxDRUoaFU8BBwkAZz0tNjciQkZFMhEzQlpeEgMSBlQjFEoQXQAGEBYGDytLEFxdGhJfUxYSRSg6YzQ8KkNGUDQKdl8fRQNMAxhVcRNdRBgLEx8MHRI2XFcRTBMEClIWAhA1PTcucyNWVUEyDCURDlkVV1E+SSMDTRddGwIXQxAPLFFfR10JBE4PUzMKJTExI3MTUkNUMBZ2fBVDBkoC"
base64decoded=base64.b64decode(content).decode("UTF-8")
#finding key size
realkeysize=0
smallestdistance=100
for keysize in range(2, 40):
	firsttab=base64decoded[:keysize]
	secondtab=base64decoded[keysize:2*keysize]
	thirdtab=base64decoded[2*keysize:3*keysize]
	fourthtab=base64decoded[3*keysize:4*keysize]
	fifthtab=base64decoded[4*keysize:5*keysize]
	sixthtab=base64decoded[5*keysize:6*keysize]
	seventh=base64decoded[6*keysize:7*keysize]
	dist=0
	dist+=calculatedistance(firsttab, secondtab)/keysize
	dist+=calculatedistance(firsttab, thirdtab)/keysize
	dist+=calculatedistance(firsttab, fourthtab)/keysize
	dist+=calculatedistance(firsttab, fifthtab)/keysize
	dist+=calculatedistance(firsttab, sixthtab)/keysize
	dist+=calculatedistance(firsttab, seventh)/keysize
	dist+=calculatedistance(secondtab, thirdtab)/keysize
	dist+=calculatedistance(secondtab, fourthtab)/keysize
	dist+=calculatedistance(secondtab, fifthtab)/keysize
	dist+=calculatedistance(secondtab, sixthtab)/keysize
	dist+=calculatedistance(secondtab, seventh)/keysize
	dist+=calculatedistance(thirdtab, fourthtab)/keysize
	dist+=calculatedistance(thirdtab, fifthtab)/keysize
	dist+=calculatedistance(thirdtab, sixthtab)/keysize
	dist+=calculatedistance(thirdtab, seventh)/keysize
	dist+=calculatedistance(fourthtab, fifthtab)/keysize
	dist+=calculatedistance(fourthtab, sixthtab)/keysize
	dist+=calculatedistance(fourthtab, seventh)/keysize
	dist+=calculatedistance(fifthtab, sixthtab)/keysize
	dist+=calculatedistance(fifthtab, seventh)/keysize
	dist+=calculatedistance(sixthtab, seventh)/keysize
	dist/=21
	if(dist<smallestdistance):
		smallestdistance=dist
		realkeysize=keysize

i=0
sliced=[]
realkeysize=33
while i<len(base64decoded):
	sliced.append(base64decoded[i:i+realkeysize])
	i+=realkeysize
sliced.pop()
positions=[[]]
for i in range(0, realkeysize):
	tmp=[]
	for s in sliced:
		tmp.append(s[i])
	positions.append(tmp)
positions.pop(0)
key=""
for bytesarray in positions:
	best_letter=''
	best_score=1000
	for c in printable:
		xor=''
		for byte in bytesarray:
			xor+=chr(ord(byte)^ord(c))
		current_rate=rate(xor)
		if(current_rate<best_score):
			best_score=current_rate
			best_letter=c
	key+=best_letter
print(key)