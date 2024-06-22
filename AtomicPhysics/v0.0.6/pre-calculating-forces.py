# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:21:34 2024

@author: Josh
"""

import numpy as np
from atomic_physics import Vector
from atomic_physics import Particle
from atomic_physics import Atom
import pygame
import time
import sys
import os

def get_potential(self, other):
    
    '''
    Calculates potential function between two particles
    params:
        self, other: Atom/Particle objects
        
    returns:
        V: numpy array containing values of potential function
           at varying radii
    
    '''
    
    r = self.distanceTo(other)
    
    radius = (self.radius + other.radius)/2
    #sigma = radius * np.e ** (-(1/6)*np.log(2))
    sigma = radius * 0.8908987181403393
    epsilon = 10e-45
    
    V = (4*epsilon/(r**2))*((sigma/r)**12
                          - (sigma/r)**6)
    
    rvec = self.vectorDist(other)
    Vx = V * np.cos(rvec.phi)
    Vy = V * np.sin(rvec.phi)
    Vz = V * np.cos(rvec.theta)
    
    return Vector(Vx, Vy, Vz)



def calc_forces(particles, dt, t):
    #pre-calculate forces, positions and save to file
    
    precision = int(np.log10(dt))
    
    with open('config.txt', 'w') as file:
        
        for time in range(1, int((t/dt)+1)):

            file.write(f'{round(time*dt, precision)},')
            
            line = ''
            for i in particles:
                netV = Vector(0,0,0)
                line += f'{i.pos},'
                for j in particles:
                    if i is j:
                        continue
                    
                    potential = get_potential(i, j)
                    
                    netV = netV + potential
                    
                i.netf = netV
                
            for k in particles:
                
                new_vel = k.netf / k.mass
                new_pos = k.pos + (k.vel + new_vel)*dt*0.5
                
                k.vel = new_vel
                k.pos = new_pos
                
            file.write(f'{line[:-1]}\n')
            sys.stdout.write(f'\rCalculating: {(100*time/(t/dt)):.2f}%')
            sys.stdout.flush()
        sys.stdout.write('\n')
    
                
def main(dt):
    
    '''
    particle1 = Atom(1, 113*10e-12, 11, 23, Vector(-5*10e-10, 0, 0))
    particle2 = Atom(-1, 181*10e-12, 9, 18, Vector(5*10e-10, 0, 0))
    #particle3 = Atom(1, 113*10e-12, 11, 23, Vector(0, -5*10e-10, 0))
    #particle4 = Atom(-1, 181*10e-12, 9, 18, Vector(0, 5*10e-10, 0))

    particles = [particle1, particle2]
    '''
    init_time = time.perf_counter()
    
    quitting = False
    
    while not quitting:
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill('white')
        
        t = int((time.perf_counter() - init_time)/dt)
        
        text = font.render(f'{(t*dt):.04f} s', False, (0,0,0))
        screen.blit(text, (0,0))
        
        try:
            row = data[t, 1:]
        except:
            main(dt)
        
        for c, particle in enumerate(particles):
            x = row[3*c]
            y = row[1 + (3*c)]
            z = row[2 + (3*c)]
            position = Vector(x, y, z)
            pygame.draw.circle(screen, 'blue', 
            (position.x*10e9 + offx, offy - position.y*10e9),
            particle.radius*10e9)
            
        pygame.display.flip()
        
        keys = pygame.key.get_pressed()
        #Press 'q' to quit, SPACE to restart
        if keys[pygame.K_q]:
            quitting=True
            break
        elif keys[pygame.K_SPACE]:
            main(dt)
        
    if quitting:
        pygame.quit()
    else:
        main(dt)
    
particle1 = Atom(1, 138e-12, 19, 39)
particle2 = Atom(-1, 181e-12, 17, 35)
#particle3 = Atom(1, 160, 11, 15, Vector(0, 300, 0))
#particle4 = Atom(-1, 120, 20, 40, Vector(0, -300, 0))

particles = [particle1, particle2]
start = time.perf_counter()
# Usage: ./calculate.exe <dt> <time> <# of particles>
#os.system("./calculate.exe")
elapsed = time.perf_counter() - start
mins, sec = divmod(elapsed, 60)
hr, mon = divmod(mins, 60)
print(f'\nCompleted in {int(hr)}:{int(mins)}:{sec}.')

pygame.init()
size = width, height = (1920, 950)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
offx = width / 2
offy = height / 2
font = pygame.font.Font('freesansbold.ttf', 24)

data = np.genfromtxt('data.txt', delimiter=',')

dt = 0.0001

main(dt)
            
