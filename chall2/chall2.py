import argparse
import base64

parser = argparse.ArgumentParser(description='XOR two strings')
parser.add_argument("-f", "--first", help="First string", required=True, action="store")
parser.add_argument("-s", "--second", help="Second string", required=True, action="store")
args=parser.parse_args()

if(len(args.first)!=len(args.first)):
	exit()

firstbytesarray=bytearray.fromhex(args.first)
secondbytesarray=bytearray.fromhex(args.second)
i=0
xor=''
while i<len(firstbytesarray):
	xor+=format(firstbytesarray[i]^secondbytesarray[i], 'x')
	i+=1
print(xor)