# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:05:49 2024

@author: Josh
"""

import numpy as np
import pygame

from atomic_physics import Vector
from atomic_physics import Particle
from atomic_physics import Atom

class ElectronConfig:
    
    def __init__(self, Z):
        
        self.Z = Z
        
        with open("electronmap.txt", "r") as file:
            data = np.genfromtxt(file, delimiter=',', dtype=int)       
        
        s = np.zeros((9, 2))
        p = np.zeros((9, 6))
        d = np.zeros((9, 10))
        f = np.zeros((9, 14))
        
        for k in range(4):
            i = np.where((data[:Z, 1] == k))
            if k == 0:
                s[data[i, 0], data[i, 2]] = 1
            elif k == 1:
                p[data[i, 0], data[i, 2]] = 1
            elif k == 2:
                d[data[i, 0], data[i, 2]] = 1
            elif k == 3:
                f[data[i, 0], data[i, 2]] = 1
                    
        self.s = np.array([np.count_nonzero(s[i]) for i in range(0, 9)])
        self.p = np.array([np.count_nonzero(p[i]) for i in range(0, 9)])
        self.d = np.array([np.count_nonzero(d[i]) for i in range(0, 9)])
        self.f = np.array([np.count_nonzero(f[i]) for i in range(0, 9)])
        
        
    def get_highest_orbital(self):
        for i in range(7,0,-1):
            if self.f[i] > 0:
                return (i, 3)
            elif self.d[i] > 0:
                return (i, 2)
            elif self.p[i] > 0:
                return (i, 1)
            elif self.s[i] > 0:
                return (i, 0)
            
    def approx_atomic_radius(self): #returns atomic radius in picometers
        with open('atomic_radii.txt', 'r') as file:
            radii = np.genfromtxt(file, delimiter=',', skip_header=1)
        
        return radii[self.Z - 1]
    
        
    def __str__(self):
        string = ''
        for i in range(1,9):
            count = self.s[i]
            if count != 0:
                string += f'{i}s{count}/'
            if i > 2:
                count = self.f[i-2]
                if count != 0:
                    string += f'{i-2}f{count}/'
            count = self.d[i-1]
            if count != 0:
                string += f'{i-1}d{count}/'
            count = self.p[i]
            if count != 0:
                string += f'{i}p{count}/'

        return string[0:-1]


class Orbital:
    
    def __init__(self, Z, n, l, m, e, pos=Vector(0,0,0)):
        self.n_quant_num = n
        self.l_quant_num = l
        self.m_quant_num = m
        self.num_electrons = e
        self.atom_num = Z
        self.pos = pos
        

    def get_wave_func(self, abs_pos=Vector(0,0,0)): #FIXME: return wave function value at a point in R3
        ao = 77e-10 #FIXME: placeholder value
        rel_pos = abs_pos - self.pos
        r = rel_pos.magnitude()
        phi = rel_pos.phi
        theta = rel_pos.theta
        
        if (rel_pos.magnitude() == 0.0):
            return 0
        
        if (self.n_quant_num == 1 and self.l_quant_num == 0): # wave function of 1s orbital
            rho = (2*self.atom_num)/(self.n_quant_num*ao)
            return (1/(2*np.sqrt(2)))*((self.atom_num/ao)**(3/2))*np.exp((-1*rho*r)/2)*(np.sqrt(1/(4*np.pi)))
        elif (self.n_quant_num == 2 and self.l_quant_num == 0):
            rho = (2*self.atom_num)/(self.n_quant_num*ao)
            return (1/(2*np.sqrt(2)))*((self.atom_num/ao)**(3/2))*(2-(rho*r))*np.exp((-1*rho*r)/2)*(np.sqrt(1/(4*np.pi)))
        elif (self.n_quant_num == 2 and self.l_quant_num == 1):
            rho = (2*self.atom_num)/(self.n_quant_num*ao)
            if (self.m_quant_num == -1):
                return (1/(2*np.sqrt(6)))*((self.atom_num/ao)**(3/2))*(rho*r)*np.exp((-1*rho*r)/2)*(np.sqrt(3/(4*np.pi)))*(np.cos(theta))
            elif (self.m_quant_num == 0):
                return (1/(2*np.sqrt(6)))*((self.atom_num/ao)**(3/2))*(rho*r)*np.exp((-1*rho*r)/2)*(np.sqrt(3/(4*np.pi)))*(np.sin(theta)*np.cos(phi))
            elif (self.m_quant_num == 1):
                return (1/(2*np.sqrt(6)))*((self.atom_num/ao)**(3/2))*(rho*r)*np.exp((-1*rho*r)/2)*(np.sqrt(3/(4*np.pi)))*(np.sin(theta)*np.sin(phi))
            else:
                return 0
        elif (self.n_quant_num == 3 and self.l_quant_num == 0):
            rho = (2*self.atom_num)/(self.n_quant_num*ao)
            return (1/(9*np.sqrt(3)))*((self.atom_num/ao)**(3/2))*(6-(6*rho*r)+(rho*r)**2)*np.exp((-1*rho*r)/2)*(np.sqrt(1/(4*np.pi)))
        elif (self.n_quant_num == 3 and self.l_quant_num == 1):
            rho = (2*self.atom_num)/(self.n_quant_num*ao)
            if (self.m_quant_num == -1):
                return (1/(9*np.sqrt(6)))*((self.atom_num/ao)**(3/2))*(4-(rho*r))*(rho*r)*np.exp((-1*rho*r)/2)*(np.sqrt(3/(4*np.pi)))*(np.cos(theta))
            elif (self.m_quant_num == 0):
                return (1/(9*np.sqrt(6)))*((self.atom_num/ao)**(3/2))*(4-(rho*r))*(rho*r)*np.exp((-1*rho*r)/2)*(np.sqrt(3/(4*np.pi)))*(np.sin(theta)*np.cos(phi))
            elif (self.m_quant_num == 1):
                return (1/(9*np.sqrt(6)))*((self.atom_num/ao)**(3/2))*(4-(rho*r))*(rho*r)*np.exp((-1*rho*r)/2)*(np.sqrt(3/(4*np.pi)))*(np.sin(theta)*np.sin(phi))
            else:
                return 0
    
    def get_e_prob(self): #FIXME: evaluated probability density function over volume and return value
        pass



if __name__ == '__main__':
    #config = ElectronConfig(9)
    
    pygame.init()
    size = width, height = (1920, 950)
    screen = pygame.display.set_mode(size)
    image = pygame.Surface(size, pygame.SRCALPHA)
    clock = pygame.time.Clock()
    offx = int(width / 2)
    offy = int(height / 2)
    
    screen.fill('white')
    
    one_s = Orbital(6, 3, 1, 0, 4)
    
    clock = pygame.time.Clock()
    
    for x in range(-200, 200):
        for y in range(-200, 200):
            prob = (one_s.get_wave_func(Vector(x*10e-10,y*10e-10,30e-10)))**2
            try:
                color = pygame.Color(255, 0, 0, int((np.log(prob)))+115)
            except:
                print(int((np.log(prob))))
            image.set_at((x + offx, offy - y), color)
            
    screen.blit(image, (0,0))
    pygame.display.update()

    while True:
        clock.tick(30)
        keys = pygame.key.get_pressed()
        #Press 'q' to quit, SPACE to restart
        if keys[pygame.K_q]:
            pygame.quit()
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                break