#! /usr/bin/env python
#
# Methods and classes to generate terrain.
#


import random

exp = 2.718281828459045

def generate_coefficients(hills):
    
    # Generate coeffs for plane
    a = random.uniform(-1.0,1.0)
    b = random.uniform(-1.0,1.0)
    c = random.uniform(1.0,5.0)
    d = random.uniform(0.0,3.0)
    
    final = {'plane':{'a':a,'b':b,'c':c,'d':d},'hills':[]}
    
    # Generate coeffs for hills
    for i in range(hills):
        a = random.uniform(0.0, 5.0)
        x0 = random.uniform(-1.0, 1.0)
        y0 = random.uniform(-1.0, 1.0)
        sig_x = random.uniform(0.2, 0.5)
        sig_y = random.uniform(0.2, 0.5)
        final['hills'].append({'a':a,'x0':x0,'y0':y0,'sig_x':sig_x,'sig_y':sig_y})
    
    return final

class Terrain:
    def __init__(self,hills):
        self.hills = hills
        self.coeffs = generate_coefficients(hills)
    
    def eval(self,x,y):
        a = self.coeffs['plane']['a']
        b = self.coeffs['plane']['b']
        c = self.coeffs['plane']['c']
        d = self.coeffs['plane']['d']
        # evaluate plane
        final = -(1/c)*(d + a*x + b*y)
        
        # evaluate hills
        for hill in self.coeffs['hills']:
            a = hill['a']
            x0 = hill['x0']
            y0 = hill['y0']
            sig_x = hill['sig_x']
            sig_y = hill['sig_y']
            
            final += a*exp**(-(((x - x0)**2.0)/(2.0*sig_x**2.0) + ((y - y0)**2.0)/(2.0*sig_y**2.0)))
        
        return final
            
    
    def gradient(self,x,y):
        final = {'dx':0.0,'dy':0.0}
        
        # determine gradient for plane
        a = self.coeffs['plane']['a']
        b = self.coeffs['plane']['b']
        c = self.coeffs['plane']['c']
        final['dx'] += -a/c
        final['dy'] += -b/c
        
        # determine gradient for hills
        for hill in self.coeffs['hills']:
            a = hill['a']
            x0 = hill['x0']
            y0 = hill['y0']
            sig_x = hill['sig_x']
            sig_y = hill['sig_y']
            
            final['dx'] += (a*exp**(-(x0 - x)**2.0/(2.0*sig_x**2.0) - (y0 - y)**2.0/(2.0*sig_y**2.0))*(x0 - x))/sig_x**2.0
            final['dy'] += (a*exp**(-(x0 - x)**2.0/(2.0*sig_x**2.0) - (y0 - y)**2.0/(2.0*sig_y**2.0))*(y0 - y))/sig_y**2.0
            
        return final
    
    
    
    
    
