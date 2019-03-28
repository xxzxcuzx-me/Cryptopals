def validatePadding(bPlaintext, blockLength):
	paddingLength=bPlaintext[-1]
	if paddingLength<=blockLength:
		for s in bPlaintext[-paddingLength:]:
			if s != paddingLength:
				return False
		return True
	return False

def unpad(plaintext, blockLength):
	bPlaintext=bytearray(plaintext, "UTF-8")
	if validatePadding(bPlaintext, blockLength):
		print("Properly padded")
		paddingLength=bPlaintext[-1]
		return bPlaintext[:-paddingLength]
	else:
		print("String not padded")
		return bPlaintext

print(unpad("YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10", 16))