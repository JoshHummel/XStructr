# -*- coding: utf-8 -*-
"""
Created on Tue May 14 21:51:36 2024

@author: Josh
"""

import pygame
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
            
            self.x = r * np.cos(phi)
            self.y = r * np.sin(phi)
            self.z = r * np.sin(theta)
        else:
            self.x = x
            self.y = y
            self.z = z
        
            #theta is angle in (x^2-y^2)-z plane (radians)
            #phi is angle in x-y plane (radians)
            try:
                self.phi = np.arctan(self.y/self.x)
            except ZeroDivisionError:
                self.phi = np.pi/2
            
            try:        
                self.theta = np.arctan(self.z/np.sqrt(self.x**2+self.y**2))
            except ZeroDivisionError:
                self.theta = np.pi/2
        
            if self.x < 0:
                if self.y < 0:
                    self.phi = -np.pi + self.phi
                else:
                    self.phi = np.pi + self.phi
            
            if self.z < 0:
                if self.y < 0:
                    self.theta += np.pi
                else:
                    self.theta = np.pi - self.theta
            elif self.y < 0:
                self.theta = (2*np.pi) - self.theta
        
        
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        
        return Vector(x, y, z)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        
        return Vector(x, y, z)
    
    def __mul__(self, other):
        if type(other) is Vector:
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
            
        elif type(other) is int or type(other) is float:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        else:
            return None
            
        return Vector(x, y, z)    
        
    def __truediv__(self, other):
        if type(other) is Vector:
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
            
        elif type(other) is int or type(other) is float:
            x = self.x / other
            y = self.y / other
            z = self.z / other
        else:
            return None
            
        return Vector(x, y, z)
    
    def __eq__(self, other):
        if type(other) is Vector:
            if self.x == other.x and self.y == other.y and self.z == other.z:
                return True
            else:
                return False
        else:
            return False
        
    def magnitude(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def cross(self, other):
        if other.isinstance(Vector):
            x = (self.y * other.z) - (self.z * other.y)
            y = (self.z * other.x) - (self.x * other.z)
            z = (self.x * other.y) - (self.y * other.x)
            
            return Vector(x, y, z)
        
    def __str__(self):
        return f"{self.x},{self.y},{self.z}"


class Particle:
    
    particles = []
    
    def __init__(self, mass, radius, charge, pos, vel, acc):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.charge = charge
        self.net_force = Vector(0,0,0)
        Particle.particles.append(self)
        
    def distanceTo(self, other):
        return np.sqrt((self.pos.x - other.pos.x)**2 + 
                         (self.pos.y - other.pos.y)**2 + 
                         (self.pos.z - other.pos.z)**2)
    
    def vectorDist(self, other):
        
        x = self.pos.x - other.pos.x
        y = self.pos.y - other.pos.y
        z = self.pos.z - other.pos.z
        
        return Vector(x, y, z)    
    
    
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