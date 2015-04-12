
import gmpy2
from gmpy2 import mpz
import curve
import field
import numpy as np
import hashlib

class ECDSA:
    def __init__(self, curve_string = 'NIST K-163'):
        if curve_string == 'NIST K-163':
            p    = 0x800000000000000000000000000000000000000C9 #t^163 + t^7 + t^6 + t^3 + 1 
            a    = 1
            G_x  = 0x2fe13c0537bbc11acaa07d793de4e6d5e5c94eee8
            G_y  = 0x289070fb05d38ff58321f2e800536d538ccdaa3d9
            G    = 0x0402fe13c0537bbc11acaa07d793de4e6d5e5c94eee80289070fb05d38ff58321f2e800536d538ccdaa3d9 
            n    = 5846006549323611672814741753598448348329118574063
            h    = 2
            self.curve = curve.curve(A = a, B = 1, Polynomial = p, Generator = G, Order = n)
            self.Order = n
            self.nfield = field.nfield(n)
            
            
    def setPrivateKey(self, key = 0):
        self.privateKey = mpz(key)
        self.publicKey = self.curve.scalerMul(self.curve.get_G(), key)
        return self.publicKey
        
        
    def sign(self, message, k):
        Q = self.curve.scalerMul(self.curve.get_G(), k)
        r = Q.x
        print hex(r)
        kinv = self.nfield.inv(k)
        print hex(k)
        print hex(kinv)
        print hex(self.privateKey)
        
        digest = hashlib.sha256(message).hexdigest()
        digest = long(digest, 16)
        digest = digest >> (digest.bit_length()-163)
        digest = self.nfield.mod(digest)
        print hex(digest)
        
        s = self.nfield.mul(kinv, (self.nfield.mul(r, self.privateKey) + digest))
        
        print hex(s)
        print '$$$$$$$$$$$$$$$$$'
        s = 0x1313A2E03F5412DDB296A22E2C455335545672D9F
        print hex(s)
        digest = self.nfield.mul(k, s) ^ self.nfield.mul(r, self.privateKey)
        print hex(digest)
        print digest.bit_length()
        return digest
    
    def verify(self, message, r, s):
        sinv = self.curve.Field.inv(s)
        print hex(sinv)
        digest = hashlib.sha1(message).hexdigest()
        print digest
        digest = long(digest, 16)
        digest = mpz(digest)
        print hex(digest)
        digest = digest >> (digest.bit_length()-163)
        print digest.bit_length()
        print hex(digest)
        print hex(digest)
        #s = self.curve.Field.mul(kinv, (self.curve.Field.mul(r, self.privateKey) ^ digest))
        #print hex(s)
        return digest
        