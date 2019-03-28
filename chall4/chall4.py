import argparse
from string import ascii_lowercase, ascii_letters, printable, punctuation

parser = argparse.ArgumentParser(description='Find in filestring XORed with single letter')
parser.add_argument("-f", "--filename", help="filename", required=True, action="store")
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

def rate(stringtorate):
	result=0
	for c in ascii_lowercase:
		count=0
		stringtorate=stringtorate.lower()
		for d in stringtorate:
			if d in ascii_letters or d in punctuation or d == ' ':
				if d==c:
					count+=1
			else:
				return 1002
		result+=pow(frequencies[c]-(count/len(stringtorate)), 2)	
	return result

file=open(args.filename)
lines = file.read().splitlines()
file.close()
best_decrypted=''
best_score=1000
for line in lines:
	best_decrypted_locally=''
	best_score_locally=1001
	bytesarray=bytearray.fromhex(line)
	for c in ascii_letters:
		xor=''
		for byte in bytesarray:
			xor+=chr(byte^ord(c))
		current_rate=rate(xor)
		if(current_rate<best_score_locally):
			best_score_locally=current_rate
			best_decrypted_locally=xor
	if(best_score_locally<best_score):
		best_score=best_score_locally
		best_decrypted=best_decrypted_locally
print(best_decrypted)