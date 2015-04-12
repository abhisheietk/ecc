
import gmpy2
from gmpy2 import mpz
#import sys
#sys.path.append('../ecc')
import field
import numpy as np

class point:
    def __init__(self, x, y):
        self.x  = mpz(x)
        self.y  = mpz(y)
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def dump(self):
        print hex(self.x), hex(self.y)


    
class curve:
    def __init__(self, A=0, B=0, Polynomial=0, Generator=0, Order = 0):
        self.A  = mpz(A)
        self.B  = mpz(B)
        self.Polynomial  = mpz(Polynomial)
        self.Generator  = Generator
        width = self.Generator.bit_length()
        width += 8 - ((width % 8) or 8)
        c = self.Generator >> (width-8)
        if c == 4:
            self.Gx = (self.Generator ^ (c << (width-8))) >> ((width-8)/2)
            self.Gy = (self.Generator ^ (c << (width-8)) ^ (self.Gx << ((width-8)/2)))
        self.Field = field.field(self.Polynomial)

        self.Order  = mpz(Order)
        self.G = point(self.Gx, self.Gy)
        if self.isNotPoint(self.G):
            print 'generator not good'
        
            
        
    def get_A(self):
        return self.A        
        
    def get_B(self):
        return self.B
        
    def get_Polynomial(self):
        return self.Polynomial
    
    def get_G(self):
        return self.G
            
    def get_Order(self):
        return self.Order
    
    def isNotPoint(self, p):
        Field = self.Field
        x1 = p.get_x()
        y1 = p.get_y()
        Field = self.Field
        y2 = Field.squar(y1)
        x2 = Field.squar(x1)
        xy = Field.mul(x1, y1)
        x2xpa = Field.mul(x2, (x1 ^ self.A))
        return y2 ^ xy ^ x2xpa ^ self.B
        
    def double(self, p):
        Field = self.Field
        px = p.get_x()
        py = p.get_y()
        
        M = Field.mul(py, Field.inv(px)) ^ px
        
        rx = Field.squar(M) ^ M ^ self.A        
        ry = Field.mul((px ^ rx), M) ^ rx ^ py
        return point(rx, ry)
    
    def add(self, p, q):
        Field = self.Field
        if p == q:
            print 'doubled'
            return self.double(p)
        else:
            px = p.get_x()
            py = p.get_y()
            qx = q.get_x()
            qy = q.get_y()

            M = Field.mul((py ^ qy), Field.inv(px ^ qx))
            rx = Field.squar(M) ^ M ^ px ^ qx ^ self.A
            ry = Field.mul((px ^ rx), M) ^ rx ^ py
            return point(rx, ry)
        
    def scalerMul(self, p, d):
        Field = self.Field
        d = mpz(d)
        roundp = p
        start = 0
        for i in range(d.bit_length()):            
            if d.bit_test(i):
                if start:
                    out = self.add(out, roundp)
                else:
                    out = roundp
                start = 1
            roundp = self.double(roundp)
        return out