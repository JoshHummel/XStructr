# -*- coding: utf-8 -*-
"""
Created on Tue May 14 21:51:36 2024

@author: Josh
"""

import numpy as np

ELECTRON_MASS = 9.1093837015e-31
ELECTRON_CHARGE = -1.602176634e-19
CLASSICAL_ELECTRON_RADIUS = 2.8179403262e-15
PLANCK_CONSTANT = 6.62607015e-34
SPEED_OF_LIGHT = 299792458
BOHR_RADIUS = 5.29177210903e-11
NEUTRON_MASS = 1.67492749804e-27
NEUTRON_RADIUS = 8.0e-16
PROTON_MASS = 1.67262192369e-27
PROTON_CHARGE = 1.602176634e-19
PROTON_RADIUS = 8.414e-16
BOLTZMANN_CONST = 1.380649e-23

class Vector:
    
    def __init__(self, x=None, y=None, z=None, r=None, phi=None, theta=None):
        
        
        
        if x is None and y is None and z is None:
            self.phi = phi
            self.theta = theta
            
            self.v = np.array([r * np.cos(phi), r * np.sin(phi), r * np.sin(theta)])
        else:
            self.v = np.array([x, y, z])
        
            #theta is angle in (x^2-y^2)-z plane (radians)
            #phi is angle in x-y plane (radians)
            if (self.v[0] == 0):
                self.phi = np.pi/2
            else:
                self.phi = np.arctan(self.v[1]/self.v[0])
                
            if (self.v[0] == 0 and self.v[1] == 0):
                self.theta = np.pi/2
            else:
                self.theta = np.arctan(self.v[2]/(np.sqrt(self.v[0]**2+self.v[1]**2)))
        
            if self.v[0] < 0:
                if self.v[1] < 0:
                    self.phi = -np.pi + self.phi
                else:
                    self.phi = np.pi + self.phi
            
            if self.v[2] < 0:
                if self.v[1] < 0:
                    self.theta += np.pi
                else:
                    self.theta = np.pi - self.theta
            elif self.v[1] < 0:
                self.theta = (2*np.pi) - self.theta
                
    def get_vec(self):
        return self.v
        
        
    def __add__(self, other):
        x = self.v[0] + other.v[0]
        y = self.v[1] + other.v[1]
        z = self.v[2] + other.v[2]
        
        return Vector(x, y, z)
    
    def __sub__(self, other):
        x = self.v[0] - other.v[0]
        y = self.v[1] - other.v[1]
        z = self.v[2] - other.v[2]
        
        return Vector(x, y, z)
    
    def __mul__(self, other):
        if type(other) is Vector:
            x = self.v[0] * other.v[0]
            y = self.v[1] * other.v[1]
            z = self.v[2] * other.v[2]
            
        elif type(other) is int or type(other) is float:
            x = self.v[0] * other
            y = self.v[1] * other
            z = self.v[2] * other
        else:
            return None
            
        return Vector(x, y, z)    
        
    def __truediv__(self, other):
        if type(other) is Vector:
            x = self.v[0] / other.v[0]
            y = self.v[1] / other.v[1]
            z = self.v[2] / other.v[2]
            
        elif type(other) is int or type(other) is float:
            x = self.v[0] / other
            y = self.v[1] / other
            z = self.v[2] / other
        else:
            return None
            
        return Vector(x, y, z)
    
    def __eq__(self, other):
        if type(other) is Vector:
            if self.v[0] == other.v[0] and self.v[1] == other.v[1] and self.v[2] == other.v[2]:
                return True
            else:
                return False
        else:
            return False
        
    def magnitude(self):
        return np.linalg.norm(self.get_vec())
    
    def cross(self, other):
        if other.isinstance(Vector):
            c = np.cross(self.get_vec(), other.get_vec())
            
            return Vector(c[0], c[1], c[2])
        
    def __str__(self):
        return f"{self.v[0]}, {self.v[1]}, {self.v[2]}"


class Particle:
    
    particles = []
    
    def __init__(self, mass, radius, charge, pos=Vector(0,0,0), vel=Vector(0,0,0), acc=Vector(0,0,0)):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.charge = charge
        self.net_force = Vector(0,0,0)
        Particle.particles.append(self)
        
    def distanceTo(self, other):
        return (self.pos - other.pos).magnitude()
    
    def vectorDist(self, other):        
        return self.pos - other.pos
    
    
class Atom(Particle):
    
    atoms = []
    
    def __init__(self, charge, radius, Z=1, istnum=1, pos=Vector(0,0,0), vel=Vector(0,0,0), acc=Vector(0,0,0)):
        
        mass = ((Z * PROTON_MASS) + ((istnum - Z) * NEUTRON_MASS)
                + ((Z - charge) * ELECTRON_MASS))
        
        #FIXME: calculate radius of atom based on bonds
        #radius = 1.23 * 10e-10
        
        Particle.__init__(self, mass, radius, charge*ELECTRON_CHARGE, pos, vel, acc)
        self.Z = Z
        self.istnum = istnum
        
        Atom.atoms.append(self)
        Particle.particles.append(self)
        
    
if __name__ == '__main__':
    pass