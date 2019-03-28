import sys
import argparse
import base64

parser = argparse.ArgumentParser(description='Convert hex to base64')
parser.add_argument("-v", "--value", help="Hex value", required=True, action="store")
args=parser.parse_args()

bytesarray=bytearray.fromhex(args.value)
base=base64.b64encode(bytesarray)
print(base)