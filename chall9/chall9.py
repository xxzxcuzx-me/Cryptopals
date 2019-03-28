import argparse
import base64

parser = argparse.ArgumentParser(description='Pad plaintext PKCS#7 style')
parser.add_argument("-p", "--plaintext", help="Plaintext to be padded", required=True, action="store")
parser.add_argument("-b", "--blocksize", help="Size to which block should be padded", required=True, action="store")
args=parser.parse_args()

args.blocksize=int(args.blocksize)
howmanytopad=args.blocksize-(len(args.plaintext)%args.blocksize)
padbyte=hex(howmanytopad)
for i in range(howmanytopad):
	args.plaintext+=padbyte
print(args.plaintext)