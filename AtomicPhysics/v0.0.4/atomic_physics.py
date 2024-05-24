# -*- coding: utf-8 -*-
"""
Created on Tue May 14 21:51:36 2024

@author: Josh
"""
import math
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
            
            self.x = r * math.cos(phi)
            self.y = r * math.sin(phi)
            self.z = r * math.sin(theta)
        else:
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
        return math.sqrt((self.pos.x - other.pos.x)**2 + 
                         (self.pos.y - other.pos.y)**2 + 
                         (self.pos.z - other.pos.z)**2)
    
    def vectorDist(self, other):
        
        x = self.pos.x - other.pos.x
        y = self.pos.y - other.pos.y
        z = self.pos.z - other.pos.z
        
        return Vector(x, y, z)
    
    def collide(self, other, dt):
        #FIXME: fix collide function
        
        if self.distanceTo(other) <= (self.radius + other.radius):
            epsilon = 997
            sigma = (self.radius + other.radius)/2
            force = (24*epsilon/(self.distanceTo(other)**2))*(2*(sigma/self.distanceTo(other)**12))
            #get distance vector to other charged particle
            dist = self.vectorDist(other)
            fx = force * math.cos(dist.phi)
            fy = force * math.sin(dist.phi)
            fz = force * math.cos(dist.theta)
            restore_force = Vector(fx, fy, fz)
            return restore_force
        else:
            return Vector(0,0,0)
        
        
def update(particles, surface, offx, offy, dt):
    
    #Currently using Euler's method, error growth is high
    #Next step is to use Verlet Integration
    for i in particles:
        new_pos = i.pos + i.vel * dt + i.acc*0.5*dt*dt
        new_acc = i.net_force / i.mass
        new_vel = i.vel + (i.acc + new_acc)*0.5*dt
         
        i.pos = new_pos
        i.vel = new_vel
        i.acc = new_acc
        
        pygame.draw.circle(surface, 'blue', 
                    (i.pos.x*10e9 + offx, offy - i.pos.y*10e9),
                    i.radius*10e9)

        
def calc_forces(particles, dt):
    #calculate magnitude of force
    #use LJ Potential in future
    
    epsilon = 10e-10
    
    
    for i in range(len(particles)):
        netf = Vector(0,0,0)
        for j in range(len(particles)):
            if i == j:
                continue
            radius = (particles[i].radius + particles[j].radius)/2
            sigma = radius * np.e ** (-(1/6)*np.log(2))
            
            
            #add Lennard-Jones potential force
            
            force = (24*epsilon/(particles[i].distanceTo(particles[j])**2))*(2*(sigma/particles[i].distanceTo(particles[j]))**11
                                  - (sigma/particles[i].distanceTo(particles[j]))**5)
    
            
            #print(particles[i].vel)
            
            #add Coulomb force            
            '''if particles[i].distanceTo(particles[j]) > 2*sigma:
                force += 8.99 * 10e9 * (particles[i].charge * particles[j].charge 
                                / ((particles[i].distanceTo(particles[j]))**2))'''
                   
            print(force/particles[i].mass)
    
            #get distance vector to other charged particle
            dist = particles[i].vectorDist(particles[j])
            fx = force * math.cos(dist.phi)
            fy = force * math.sin(dist.phi)
            fz = force * math.cos(dist.theta)
            netf = netf + Vector(fx, fy, fz)
            #print(particles[i].distanceTo(particles[j]))
            
        
        particles[i].net_force = netf
    
    
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
        

    
def main():
    
    particle1 = Atom(1, 113*10e-12, 11, 23, Vector(-2*10e-10, 0, 0))
    particle2 = Atom(-1, 181*10e-12, 9, 18, Vector(2*10e-10, 0, 0))
    #particle3 = Particle(0.0001, 34, -0.0001, Vector(-300, -15, 0), Vector(50,0,0), Vector(0,0,0))
    #particle4 = Particle(0.0001, 34, -0.0001, Vector(300, 15, 0), Vector(-50,0,0), Vector(0,0,0))
    
    particles = [particle1, particle2]
    
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
        calc_forces(particles, dt)
        update(particles, screen, offx, offy, dt)
        
        keys = pygame.key.get_pressed()
        #Press 'q' to quit, SPACE to restart
        if keys[pygame.K_q]:
            running = False
        elif keys[pygame.K_SPACE]:
            main()
        
        pygame.display.flip()
        
        dt = clock.tick(60) / 1000
        
    pygame.quit()
    
    
if __name__ == '__main__':
    main()