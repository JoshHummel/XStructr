# -*- coding: utf-8 -*-
"""
Created on Tue May 14 21:51:36 2024

@author: Josh
"""
import math
import pygame

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

class Vector:
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
        #theta is angle in (x^2-y^2)-z plane (radians)
        #phi is angle in x-y plane (radians)
        try:
            self.phi = math.atan(self.y/self.x)
        except ZeroDivisionError:
            self.phi = math.pi/2
            
        try:        
            self.theta = math.atan(self.z/math.sqrt(self.x**2+self.y**2))
        except ZeroDivisionError:
            self.theta = math.pi/2
        
        if self.x < 0:
            if self.y < 0:
                self.phi = -math.pi + self.phi
            else:
                self.phi = math.pi + self.phi
            
        if self.z < 0:
            if self.y < 0:
                self.theta += math.pi
            else:
                self.theta += math.pi - self.theta
        elif self.y < 0:
            self.theta += (2*math.pi) - self.theta
        
        
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
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def cross(self, other):
        if other.isinstance(Vector):
            x = (self.y * other.z) - (self.z * other.y)
            y = (self.z * other.x) - (self.x * other.z)
            z = (self.x * other.y) - (self.y * other.x)
            
            return Vector(x, y, z)
        
    def __str__(self):
        return f"X: {self.x} Y: {self.y} Z: {self.z}"

class Particle:
    
    def __init__(self, mass, radius, charge, pos, vel, acc):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.charge = charge
        
    def distanceTo(self, other):
        return math.sqrt((self.pos.x - other.pos.x)**2 + 
                         (self.pos.y - other.pos.y)**2 + 
                         (self.pos.z - other.pos.z)**2)
    
    def vectorDist(self, other):
        
        x = self.pos.x - other.pos.x
        y = self.pos.y - other.pos.y
        z = self.pos.z - other.pos.z
        
        return Vector(x, y, z)
        
        
    def isTouching(self, other):
        if self.distanceTo(other) <= (self.radius + other.radius):
            return True
        else:
            return False
        
    def collide():
        #FIXME: add collide function
        pass
        
    def apply_force(self, other):
        #calculate magnitude of force
        force = 8.99 * 10e9 * self.charge * other.charge / (self.distanceTo(other))**2
        
        #get distance vector to other charged particle
        dist = self.vectorDist(other)
        
        fx = force * math.cos(dist.phi)
        fy = force * math.sin(dist.phi)
        fz = force * math.cos(dist.theta)
        fVec = Vector(fx, fy, fz)
        
        self.acc = self.acc + (fVec/self.mass)
        other.acc = other.acc - (fVec/other.mass)
        
    def update(self, dt):
        
        #Currently using Euler's method, error growth is high
        #Next step is to use Verlet Integration
        
        self.vel = self.vel + (self.acc * dt)
        self.pos = self.pos + (self.vel * dt)      
    
    
def main():
    
    particle1 = Particle(1, 20, 0.000004, Vector(0, 0, 0), Vector(0,0,0), Vector(0,0,0))
    particle2 = Particle(0.0001, 20, -0.00001, Vector(0, 300, 0), Vector(0,0,0), Vector(0,0,0))
    particle3 = Particle(0.0001, 20, -0.00001, Vector(-300, -300, 0), Vector(0,0,0), Vector(0,0,0))
    particle4 = Particle(0.0001, 20, -0.00001, Vector(300, -300, 0), Vector(0,0,0), Vector(0,0,0))
    
    particles = [particle1, particle2, particle3, particle4]
    
    pygame.init()
    size = width, height = (1920, 950)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    offx = size[0] / 2
    offy = size[1] / 2
    dt = 0
    
    while running:
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill('white')
        for j in range(len(particles)-1):
            for k in range(j+1, len(particles)):
                particles[j].apply_force(particles[k])
                    
        for j in range(len(particles)):
            particles[j].update(dt)
            pygame.draw.circle(screen, 'blue', 
                        (particles[j].pos.x + offx, offy - particles[j].pos.y),
                        particles[j].radius)
        
        keys = pygame.key.get_pressed()
        #Press 'q' to quit, SPACE to restart
        if keys[pygame.K_q]:
            running = False
        elif keys[pygame.K_SPACE]:
            main()
        
        pygame.display.flip()
        
        dt = clock.tick(360) / 1000
        
    pygame.quit()
    
    
if __name__ == '__main__':
    main()