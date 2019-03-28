import codecs
import struct

def leftrotate(i, n):
    return ((i << n) & 0xffffffff) | (i >> (32 - n))

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & y) | (x & z) | (y & z)

def H(x, y, z):
    return x ^ y ^ z

class MD4(object):
    def __init__(self, h0, h1, h2, h3, processed, data=b''):
        self.remainder = data
        self.count = processed
        self.h = [
                h0,
                h1,
                h2,
                h3
                ]

    def _add_chunk(self, chunk):
        self.count += 1
        X = list( struct.unpack("<16I", chunk) + (None,) * (80-16) )
        h = [x for x in self.h]
        # Round 1
        s = (3, 7, 11, 19)
        for r in range(16):
            i = (16-r)%4
            k = r
            h[i] = leftrotate( (h[i] + F(h[(i+1)%4], h[(i+2)%4], h[(i+3)%4]) + X[k]) % 2**32, s[r%4] )
        # Round 2
        s = (3, 5, 9, 13)
        for r in range(16):
            i = (16-r)%4 
            k = 4*(r%4) + r//4
            h[i] = leftrotate( (h[i] + G(h[(i+1)%4], h[(i+2)%4], h[(i+3)%4]) + X[k] + 0x5a827999) % 2**32, s[r%4] )
        # Round 3
        s = (3, 9, 11, 15)
        k = (0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15) #wish I could function
        for r in range(16):
            i = (16-r)%4 
            h[i] = leftrotate( (h[i] + H(h[(i+1)%4], h[(i+2)%4], h[(i+3)%4]) + X[k[r]] + 0x6ed9eba1) % 2**32, s[r%4] )

        for i, v in enumerate(h):
            self.h[i] = (v + self.h[i]) % 2**32

    def add(self, data):
        message = self.remainder + data
        r = len(message) % 64
        if r != 0:
            self.remainder = message[-r:]
        else:
            self.remainder = b''
        for chunk in range(0, len(message)-r, 64):
            self._add_chunk( message[chunk:chunk+64] )
        return self

    def finish(self):
        l = len(self.remainder) + 64 * self.count
        self.add( b'\x80' + b'\x00' * ((55 - l) % 64) + struct.pack("<Q", l * 8) )
        out = struct.pack("<4I", *self.h)
        self.__init__(0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0)
        return out

def checkIntegrity(message, password):
    hashToCheck=message[:16]
    messageToCheck=message[16:]
    hashed=MD4(0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0).add(bytearray(password, "UTF-8")+messageToCheck).finish()
    return hashed==hashToCheck

def calculatePadding(messageLen):
    padding=bytearray()
    padding.append(0x80)
    howMany=((56 - (messageLen + 1) % 64) % 64)
    for i in range(howMany):
        padding.append(0x00)
    length=bytearray((messageLen*8).to_bytes(8, "little"))
    for byte in length:
        padding.append(byte)
    return padding

message="comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
secretPassword="qwerty"
toAdd=";admin=true"
hashed=MD4(0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0).add(bytearray(secretPassword+message, "UTF-8")).finish()
for i in range(6, 7):
    gluePadding=calculatePadding(i+len(message))
    newMessage=bytearray(MD4(int.from_bytes(hashed[:4], "little"),
                            int.from_bytes(hashed[4:8], "little"),
                            int.from_bytes(hashed[8:12], "little"),
                            int.from_bytes(hashed[12:16], "little"), int((i+len(message)+len(gluePadding))/64)).add(bytearray(toAdd, "UTF-8")).finish())
    for byte in bytearray(message, "UTF-8"):
        newMessage.append(byte)
    for byte in gluePadding:
        newMessage.append(byte)
    for byte in bytearray(toAdd, "UTF-8"):
        newMessage.append(byte)
    if checkIntegrity(newMessage, secretPassword):
        print("Everything is right! The message really was:", newMessage[16:])
        break
else:
    print("It didn't work") 