# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:21:34 2024

@author: Josh
"""

import numpy as np
import math
from atomic_physics import Vector
from atomic_physics import Particle
from atomic_physics import Atom
import pygame
import time
import sys

def get_potential_function(self, other, dr):
    
    '''
    Calculates potential function between two particles
    params:
        self, other: Atom/Particle objects
        
    returns:
        V: numpy array containing values of potential function
           at varying radii
    
    '''
    
    r = self.distanceTo(other)
    
    r_x = np.linspace(r-dr, r+dr, 3)
    #steps = int((10**int(np.log10(r)))/dr)
    
    radius = (self.radius + other.radius)/2
    #sigma = radius * np.e ** (-(1/6)*np.log(2))
    sigma = radius * 0.8908987181403393
    epsilon = 10e-23
    
    V = (4*epsilon/(r_x**2))*((sigma/r_x)**12
                          - (sigma/r_x)**6)
    
    V = np.insert(V, [0], 0.0, axis=0)
    
    return V
    
def calc_force_from_potential(self, other, V, dr):
    
    '''
    Calculates force vector from potential function
    params:
        self, other: Atom/Particle objects
        V: potential function
        dr: delta r, some small constant to derive V by
        
    returns:
        fvec: force Vector applied to self
    '''
    
    #print(int((self.distanceTo(other) - dr)/dr))
    #print(int(self.distanceTo(other)/dr))
    
    F = np.gradient(V)
    
    r = self.distanceTo(other)
    
    rvec = self.vectorDist(other)
    
    fx = F[1] * np.cos(rvec.phi)
    fy = F[1] * np.sin(rvec.phi)
    fz = F[1] * np.cos(rvec.theta)
    fvec = Vector(fx, fy, fz)

    return fvec



def calc_forces(particles, dr, dt, t):
    #pre-calculate forces, positions and save to file
    
    with open('config.txt', 'w') as file:
        
        for time in range(1, int((t/dt)+1)):

            file.write(f'{time*dt},')
            
            line = ''
            for i in particles:
                netf = Vector(0,0,0)
                line += f'{i.pos},'
                for j in particles:
                    if i is j:
                        continue
                    
                    potential = get_potential_function(i, j, dr)
                    
                    netf = netf + calc_force_from_potential(i, j, potential, dr)
                    
                i.net_force = netf
                
            for k in particles:
                new_acc = k.net_force / k.mass
                new_vel = k.vel + (k.acc + new_acc)*dt*0.5
                new_pos = k.pos + (k.vel + new_vel)*dt*0.5
                
                k.acc = new_acc
                k.vel = new_vel
                k.pos = new_pos
                
            file.write(f'{line[:-1]}\n')
            sys.stdout.write(f'\rCalculating: {(100*time/(t/dt)):.2f}%')
            sys.stdout.flush()
    
                
def main():
    
    particle1 = Atom(1, 113*10e-12, 11, 23, Vector(-5*10e-10, 0, 0))
    particle2 = Atom(-1, 181*10e-12, 9, 18, Vector(5*10e-10, 0, 0))
    #particle3 = Particle(0.0001, 34, -0.0001, Vector(-300, -15, 0), Vector(50,0,0), Vector(0,0,0))
    #particle4 = Particle(0.0001, 34, -0.0001, Vector(300, 15, 0), Vector(-50,0,0), Vector(0,0,0))

    particles = [particle1, particle2]

    t = 0
    
    while True:
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill('white')
        try:
            row = data[t, 1:]
        except:
            main()
        c = 0
        for particle in particles:
            x = row[3*c]
            y = row[1+3*c]
            z = row[2+3*c]
            position = Vector(x, y, z)
            pygame.draw.circle(screen, 'blue', 
            (position.x*10e9 + offx, offy - position.y*10e9),
            particle.radius*10e9)
            c += 1
        time.sleep(dt)
        keys = pygame.key.get_pressed()
        #Press 'q' to quit, SPACE to restart
        if keys[pygame.K_q]:
            quitting=True
            break
        elif keys[pygame.K_SPACE]:
            main()
        
        pygame.display.flip()
        t += 1
        
    if quitting:
        pygame.quit()
    else:
        main()
    
particle1 = Atom(1, 113*10e-12, 11, 23, Vector(-5*10e-10, 0, 0))
particle2 = Atom(-1, 181*10e-12, 9, 18, Vector(5*10e-10, 0, 0))
#particle3 = Particle(0.0001, 34, -0.0001, Vector(-300, -15, 0), Vector(50,0,0), Vector(0,0,0))
#particle4 = Particle(0.0001, 34, -0.0001, Vector(300, 15, 0), Vector(-50,0,0), Vector(0,0,0))

particles = [particle1, particle2]
calc_forces(particles, 10e-15, 0.0001, 5)

pygame.init()
size = width, height = (1920, 950)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
offx = width / 2
offy = height / 2

data = np.genfromtxt('config.txt', delimiter=',')

dt = 0.0001

main()
            
