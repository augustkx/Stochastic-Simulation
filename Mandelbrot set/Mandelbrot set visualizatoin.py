# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 20:19:45 2015

@author: Administrator
"""

from scipy.stats import uniform
#import time
#import numpy as np
#from matplotlib import mpl
import matplotlib.pyplot as plt
import random

def main_show():
    'visualization of the Mandelbrot set'
    ms=Mset()  
    ms.show()

    
    
# the function to calculate teh magnitude of the complex number to see if it surpasses 2 in the i iterations.   
def iterate_mandelbrot(c,i):
    z=0
    for h in range(0,i):
        z = z*z + c
        if abs(z) > 2:
            break
    if abs(z) > 2:
        return h
    else:
        return 'None'

# (Especially used for visualization)the function to calculate the magnitude of the complex number to see if it surpasses 2 in the i iterations.
def iterate_mandelbrot_show(c,i):
    z=0
    for h in range(0,i):
        z = z*z + c
        if abs(z) > 2:
            break
    return h
# the function to generate Latin Hypercube Sampling
def latin_hypercube_sampling(s,low,up):
     segSize = 1/float(s)
     vector_sample=[]
     for i in range(int(s)):
         segMin = float(i) * segSize
         point = segMin + (uniform.rvs(0,1) * segSize)
         pointValue = (point * (up - low)) +low
         vector_sample.append(pointValue)
     random.shuffle(vector_sample)
     return vector_sample




class Mset():

    def __init__(self):
        self.iteration=100
        self.number_samples=1E4
        
    def mandel(self):
        ' Pure random sampling is implemented to draw the samples on the complex plane'
        self.s=0
        for i in range(int(self.number_samples)):
            self.sample = complex(uniform.rvs(-2, 3), uniform.rvs(-1.5, 3 ))
            self.n = iterate_mandelbrot(self.sample,self.iteration) 
            if self.n =='None':            
                self.s += 1
        self.Area_iteration_samples=float(self.s)/float(self.number_samples)*9    
    
    def mandel_LHS(self):
        ' Latin Hypercube sampling is implemented to draw the samples on the complex plane'
        self.s=0
        self.vector_real=latin_hypercube_sampling(self.number_samples,-2,1)
        self.vector_imaginary=latin_hypercube_sampling(self.number_samples,-1.5,1.5)
        for i in range(int(self.number_samples)):            
            self.sample = complex(self.vector_real[i], self.vector_imaginary[i])
            
            self.n = iterate_mandelbrot(self.sample,self.iteration) 
            if self.n =='None':            
                self.s += 1
        self.Area_iteration_samples=float(self.s)/float(self.number_samples)*9    

    def show(self):
        'on the complex plane, draw the Mandelbrot set area in the region lined out by x=-2,1 and y=+-1.5 .'
        self.size=1000
        self.matrix_grid=[]
        for i in range(self.size):
            self.grid=[]
            for j in range(self.size):
                j
                self.sample = complex(-2+j*3/float(self.size), -1.5+i*3/float(self.size))
                self.n = iterate_mandelbrot_show(self.sample,self.iteration)
                self.grid.append(self.n)
            self.matrix_grid.append(self.grid)
        print self.q, self.s, self.Area_iteration_samples
        plt.imshow(self.matrix_grid)
        plt.colorbar(shrink=.92)
        plt.xticks(())
        plt.yticks(())
        plt.show()

main_show()
