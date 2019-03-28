import argparse
import base64

parser = argparse.ArgumentParser(description='Detect AES ECB encrypted text in file')
parser.add_argument("-f", "--filename", help="File name", required=True, action="store")
args=parser.parse_args()

file=open(args.filename)

for line in file:
	decoded=base64.b64decode(line)
	count=round(len(decoded)/16)
	tab=[]
	for i in range(count-1):
		tab.append(decoded[i*16:(i+1)*16])
	repeated=False
	for i in range(len(tab)):
		for j in range(i+1, len(tab)-1):
			if tab[i]==tab[j]:
				repeated=True
				break
	if repeated:
		print(line)
