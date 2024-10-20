# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:21:34 2024

@author: Josh
"""

import numpy as np
from classes import Vector
from classes import Particle
from classes import Atom
import pygame
import time
import sys
import os
import subprocess
import random

def write_config(particles):
    with open("config.txt", "w") as file:
        for p in particles:
            s = f"{p.mass}, {p.radius}, {p.charge}, "
            s += f"{p.pos}, "
            s += f"{p.vel}, "
            s += f"{p.acc}\n"
            file.write(s)
            
def gen_particles(n):
    parts = []
    
    for i in range(n):
        Z = random.randrange(1,38)
        pos = Vector(random.randrange(-30,31)*pow(10,-10), random.randrange(-30,31)*pow(10,-10), 0)
        parts.append(Atom(0, random.randrange(25, 261)*pow(10,-12), Z, Z*2, pos, Vector(0,0,0), Vector(0,0,0)))
    
    return parts
        
def main_phys(dt, length, cdt, scale, numparts):
    random.seed(None)
    
    #directory for testing
    os.chdir('C:/Users/Josh/Documents/GitHub/XStructr/Release 1')
    
    particles = gen_particles(numparts)
    
    write_config(particles)
    start = time.perf_counter()
    
    # Usage: ./calculate.exe <dt> <time> <# of particles>
    subprocess.call(f"./calculate.exe {cdt} {length} {numparts}")
    
    elapsed = time.perf_counter() - start
    mins, sec = divmod(elapsed, 60)
    hr, mon = divmod(mins, 60)
    print(f'\nCompleted in {int(hr)}:{int(mins)}:{sec:.3f}.')
    
    data = np.genfromtxt('data.txt', delimiter=',')

    pygame.init()
    size = width, height = (1920, 950)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    offx = width / 2
    offy = height / 2
    font = pygame.font.Font('freesansbold.ttf', 24)

    init_time = time.perf_counter()
    
    quitting = False
    
    while not quitting:
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill('white')
        
        t = int((time.perf_counter() - init_time)/(10**dt))
        
        text = font.render(f'{(t*(10**(10+cdt))):.04f} ns', False, (0,0,0))
        screen.blit(text, (0,0))
        
        try:  # TODO: fix so no errors are thrown
            row = data[t, :]
        except:
            init_time = time.perf_counter()
        
        for c, particle in enumerate(particles):
            x = row[3*c]
            y = row[1 + (3*c)]
            z = row[2 + (3*c)]
            position = Vector(x, y, z)
            pygame.draw.circle(screen, 'blue', 
                (position.get_vec()[0]*(10**(scale)) + offx, offy - position.get_vec()[1]*(10**(scale))),
                particle.radius*10**(scale))
            
        pygame.display.flip()
        
        keys = pygame.key.get_pressed()
        #Press 'q' to quit, SPACE to restart
        if keys[pygame.K_q]:
            quitting=True
            break
        elif keys[pygame.K_SPACE]:
            init_time = time.perf_counter()
        
    if quitting:
        pygame.quit()
    else:
        init_time = time.perf_counter()
        

if __name__ == "__main__":
    
    pass