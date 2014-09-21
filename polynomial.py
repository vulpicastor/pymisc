# A toy Polynomial class and related methods
# 
# The MIT License (MIT)
# 
# Copyright (c) 2014 Lizhou Sha
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from future import division, print_function  # For Python 2 compatibility
import numpy as np
import cmath

class Polynomial(object):
    
    def __init__(self, *coeffs):
        """Creates a Polynomial with the coefficients, starting with the constant"""
        self.coeffs = np.Array(coeffs)
        self.order = len(self.coeffs) - 1
    
    def coeff(self, k):
        """-> coefficient of the `k`th order term"""
        return self.coeffs[k]
    
    def val(self, v):
        """-> evaluate P(v)"""
        return sum([c*v**(k) for k, c in enumerate(self.coeffs)])
    
    def roots(self):
        """-> numpy.Array of the roots"""
        if self.order == 0:
            if self.coeffs[0] != 0:
                raise ZeroDivisionError("Wut, 5 == 0 ?")
            else:
                return complex
        elif self.order == 1:
            a, b = self.coeffs
            return -float(b) / a
        elif self.order == 2:
            a, b, c = self.coeffs
            dis = b * b - 4 * a * c
            if dis >= 0:
                disqrt = math.sqrt(dis)
            else:
                disqrt = cmath.sqrt(dis)
            return (-b - disqrt) / 2. / a, (-b + disqrt) / 2. / a
        else:
            raise ArithmeticError("Dunno how to solve :(")
    
    def add(self, other):
        """-> self + other"""
        return sum_poly(self, other)
    
    def mul(self, other):
        """Automatic FOILing"""
        new_order = self.order + other.order
        prod = []
        if self.order >= other.order:
            p, q = self.coeffs, other.coeffs
            min_order, max_order = other.order, self.order
        else:
            p, q = other.coeffs, self.coeffs
            min_order, max_order = self.order, other.order
        for i in xrange(1, min_order+2):
            prod.append( sum( [ a * b for a, b in zip(p, reversed(q[:i])) ] ) )
        for j in xrange(1, max_order+1):
            prod.append( sum( [ a * b for a, b in zip(p[j:], reversed(q)) ] ) )
        return Polynomial(prod)
    
    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.mul(other)

    def __str__(self):
        return 'Polynomial(%r)' % list(self.coeffs)

    def __repr__(self):
        return self.__str__()

def sum_poly(*polys):
    orders = [p.order for p in polys] # all the order of the summands
    max_order = max(orders)
    coeffses = [p.coeffs[:] for p in polys] # make sure the coeffs are copied
    coeffses = [[0]*(max_order-o) + cs for (o, cs) in zip(orders, coeffses)] # padd with zero
    sums = [sum(cs) for cs in zip(*coeffses)]
    return Polynomial(sums)
