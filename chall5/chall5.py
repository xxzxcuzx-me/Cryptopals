import argparse

parser = argparse.ArgumentParser(description='XOR string with key')
parser.add_argument("-s", "--string", help="String to encrypt", required=True, action="store")
parser.add_argument("-k", "--key", help="Encryption key", required=True, action="store")
args=parser.parse_args()

plaintext=bytearray(args.string, "ASCII")	
key=bytearray(args.key, "ASCII")

encrypted=''
i=0
for byte in plaintext:
	encrypted+=format(byte^key[i], "x")
	i+=1
	if i>=len(key):
		i=0
print(encrypted)