
import gmpy2
from gmpy2 import mpz

def mul(a, b):
    #print '$$$$$$$$$$$$$$'
    #print hex(a), hex(b)
    if a >= b:
        l, h = mpz(b), mpz(a)
    else:
        l, h = mpz(a), mpz(b)
    shift = 0
    out = 0
    while l:
        shift = l.bit_scan1()
        l = l.bit_clear(shift)
        shifted_h = h * 2**shift
        out = out ^ shifted_h
    #print hex(out)
    #print '$$$$$$$$$$$$$$'
    return out

def squar(a):
    d = mpz(a)
    out = mpz(0)
    while d:
        dsize = d.bit_length()
        d = d.bit_clear(dsize-1)
        out = out.bit_set((dsize-1)*2)
    return out

def mod(a, poly):
    d = mpz(a)
    p = mpz(poly)
    while(True):
        dsize = d.bit_length()
        psize = p.bit_length()
        if dsize < psize:
            return mpz(d)
        else:
            #print bin(d)
            d = d ^ (p * (2**(dsize-psize)))

def inv(a, poly):
    d = mpz(a)
    p = mpz(poly)
    out = mpz(d)
    psize = p.bit_length()
    for i in range(psize-3):
        d = mod(squar(d), p)
        out = mod(mul(d, out), p)
    out = mod(squar(out), p)
    return out

def root(a, poly):
    d = mpz(a)
    p = mpz(poly)
    out = mpz(d)
    psize = p.bit_length()
    for i in range(psize-2):
        d = mod(squar(d), p)
    return d

class field:
    def __init__(self, Polynomial=0):        
        self.Polynomial  = mpz(Polynomial)
        
    def mul(self, a, b):
        return mod(mul(a, b), self.Polynomial)
    
    def squar(self, a):
        return mod(squar(a), self.Polynomial)
    
    def mod(self, a):
        return mod(a, self.Polynomial)
    
    def inv(self, a):
        return inv(a, self.Polynomial)
    
    def root(self, a):
        return root(a, self.Polynomial)
    
class nfield:
    def __init__(self, Prime=0):        
        self.Prime  = mpz(Prime)
        
    def mul(self, a, b):
        return gmpy2.f_mod(gmpy2.mul(a, b), self.Prime)
    
    #def squar(self, a):
    #    return gmpy2.f_mod(squar(a), self.Prime)
    
    def mod(self, a):
        return gmpy2.f_mod(a, self.Prime)
    
    def inv(self, a):
        return gmpy2.invert(a, self.Prime)
    
    #def root(self, a):
    #    return root(a, self.Prime)