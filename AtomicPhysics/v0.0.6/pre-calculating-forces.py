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
import subprocess
import random

def write_config(particles):
    with open("config.txt", "w") as file:
        for p in particles:
            s = f"{p.mass}, {p.radius}, {p.charge}, "
            s += f"{p.pos.x}, {p.pos.y}, {p.pos.z}, "
            s += f"{p.vel.x}, {p.vel.y}, {p.vel.z}, "
            s += f"{p.acc.x}, {p.acc.y}, {p.acc.z}\n"
            file.write(s)
            
        
def main(dt, length, cdt, scale):

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
        
        text = font.render(f'{(t*cdt*10e9):.04f} ns', False, (0,0,0))
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
                (position.x*scale + offx, offy - position.y*scale),
                particle.radius*scale)
            
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
    
    particle1 = Atom(-1, 99e-12, 17, 35, Vector(-2e-9, 0, 0))
    particle2 = Atom(1, 154e-12, 11, 23, Vector(2e-9, 0, 0))
    #particle1 = Atom(0, 188e-12, 18, 40, Vector(-2e-9, 0, 0))
    #particle2 = Atom(0, 188e-12, 18, 40, Vector(2e-9, 0, 0))
    #particle3 = Atom(1, 160, 11, 15, Vector(0, 300, 0))
    #particle4 = Atom(-1, 120, 20, 40, Vector(0, -300, 0))
    
    calc_dt = 1e-16
    calc_len = 1e-11
    sim_dt = 1e-4
    scale = 1e11

    particles = [particle1, particle2]
    write_config(particles)
    start = time.perf_counter()
    
    # Usage: ./calculate.exe <dt> <time> <# of particles>
    subprocess.check_call(f"./calculate.exe {calc_dt} {calc_len} {len(particles)}")
    
    elapsed = time.perf_counter() - start
    mins, sec = divmod(elapsed, 60)
    hr, mon = divmod(mins, 60)
    print(f'\nCompleted in {int(hr)}:{int(mins)}:{sec:.3f}.')
    
    data = np.genfromtxt('data.txt', delimiter=',');

    pygame.init()
    size = width, height = (1920, 950)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    offx = width / 2
    offy = height / 2
    font = pygame.font.Font('freesansbold.ttf', 24)

    main(sim_dt, calc_len, calc_dt, scale)