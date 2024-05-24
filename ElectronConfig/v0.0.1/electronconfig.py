# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:05:49 2024

@author: Josh
"""

import numpy as np

class ElectronConfig:
    
    def __init__(self, Z):
        
        self.Z = Z
        
        with open('electronmap.txt', 'r') as file:
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

if __name__ == '__main__':
    config = ElectronConfig(9)
    print(config.approx_atomic_radius())