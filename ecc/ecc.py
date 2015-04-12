
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
        kinv = self.nfield.inv(k)
        digest = hashlib.sha256(message).hexdigest()
        digest = long(digest, 16)
        digest = digest >> (digest.bit_length()-163)
        digest = self.nfield.mod(digest)        
        s = self.nfield.mul(kinv, (self.nfield.mul(r, self.privateKey) + digest))        
        return r, s
    
    def verify(self, message, Q, r, s):
        if self.curve.isNotPoint(Q):
            print 'Public key is not valid'
            return -1
        
        digest = hashlib.sha256(message).hexdigest()
        digest = long(digest, 16)
        digest = digest >> (digest.bit_length()-163)
        digest = self.nfield.mod(digest)   
        
        w = self.nfield.inv(s)
        u1 = self.nfield.mul(digest, w)
        u2 = self.nfield.mul(r, w)
        u1G = self.curve.scalerMul(self.curve.get_G(), u1)
        u2Q = self.curve.scalerMul(Q, u2)
        P = self.curve.add(u1G, u2Q)
        if r == P.x:
            print 'Signature is valid'
            return 0
        else:
            print 'Signature is invalid'
        return -1        