from Crypto.PublicKey import RSA
from Crypto.Util.number import (long_to_bytes, bytes_to_long, GCD, inverse)
from base64 import (b64decode, b64encode)
import argparse
import sys

i = bytes_to_long(b'Bravo Le flag est Cryp7ogr4ph!eLeF3u')
key1 = RSA.importKey(open("private1.key").read())

c2 = pow(i, key1.e,key1.n)
c2 = long_to_bytes(c2)
print(c2)
print("\n")

"""m2 = bytes_to_long(c2)
m2 = pow(m2, key1.d, key1.n)
m2 = long_to_bytes(m2)
print(m2)"""
