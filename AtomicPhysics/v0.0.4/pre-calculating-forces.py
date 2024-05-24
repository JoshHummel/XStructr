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

def calc_forces(particles, dt, t):
    #pre-calculate forces, positions and save to file
    
    epsilon = 10e-45
    entropy = 0.9
    
    with open('config.txt', 'w') as file:
        
        for time in range(1, int((t/dt)+1)):

            file.write(f'{time*dt},')

            for i in range(len(particles)):
                netf = Vector(0,0,0)
                for j in range(len(particles)):
                    if i == j:
                        continue
                    radius = (particles[i].radius + particles[j].radius)
                    #sigma = radius * np.e ** (-(1/6)*np.log(2))
                    #sigma = radius * 0.8908987181
                    sigma = 3.653*10e-10
                    
                    #Lennard-Jones potential force
                    force = (24*epsilon/(particles[i].distanceTo(particles[j])**2))*(2*(sigma/particles[i].distanceTo(particles[j]))**11
                                          - (sigma/particles[i].distanceTo(particles[j]))**5)
                    
                    if particles[i].distanceTo(particles[j]) > sigma:
                        force += 8.99 * 10e9 * (particles[i].charge * particles[j].charge 
                                        / ((particles[i].distanceTo(particles[j]))**2))
                    
                    #get distance vector to other charged particle
                    dist = particles[i].vectorDist(particles[j])
                    fx = force * math.cos(dist.phi)
                    fy = force * math.sin(dist.phi)
                    fz = force * math.cos(dist.theta)
                    netf = (netf + Vector(fx, fy, fz)) * entropy
                    
                particles[i].net_force = netf
                
            line = ''
            
            for i in particles:
                
                new_acc = i.net_force / i.mass
                new_vel = i.vel + (i.acc + new_acc)*dt*0.5
                new_pos = i.pos + (i.vel + new_vel)*dt*0.5
                
                i.acc = new_acc
                i.vel = new_vel
                i.pos = new_pos
                
                line += f'{new_pos},'
                
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
            (position.x*10e10 + offx, offy - position.y*10e10),
            particle.radius*10e10)
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
#calc_forces(particles, 0.00001, 2)

pygame.init()
size = width, height = (1920, 950)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
offx = size[0] / 2
offy = size[1] / 2

data = np.genfromtxt('config.txt', delimiter=',')

dt = 0.0001

main()
            
