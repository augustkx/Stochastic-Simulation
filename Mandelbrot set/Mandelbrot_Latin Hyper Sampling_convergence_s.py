# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 06:28:07 2015

@author: Administrator
"""


from scipy.stats import uniform
import time
import numpy as np
#from matplotlib import mpl
import matplotlib.pyplot as plt
import random

def main_show():
    'visualization of the Mandelbrot set'
    ms=Mset()  
    ms.show()


def main():
    'Run the Monte Carlo Simulation for certain times, which depends on how soon the d=S/k^0.5 will get less than the set d . '
    array_sample=[]
    array_mean_area=[]
    array_n=[]
    change=[]
    m=0
    
    for sample in range(500,50500,500):

        d=1
        n=0
        mean_area=0
        sd_area=0
        
        while (d>=1E-2 or n<20):
          
            ms=Mset()            
            ms.number_samples=sample        
            ms.mandel_LHS()
            
            if n == 0:
                sd_area = 0
            else:
                sd_area = ((1-1/n)*sd_area**2+(ms.Area_iteration_samples-mean_area)**2/(n+1))**0.5
            mean_area=(ms.Area_iteration_samples+mean_area*n)/(n+1)
            
            if n==0:
                d=1
            else:            
                d=sd_area/(n+1)**0.5
            n += 1
            
            #print n, d, sd_area, mean_area
        print n,sd_area, mean_area
        array_sample.append(sample)
        array_n.append(int(n))
        array_mean_area.append(mean_area)
        change.append(array_mean_area[m]-array_mean_area[m-1])
        m+=1
        #print array_n
    plt.plot(array_sample, array_mean_area)
    plt.ylim(1.45,1.57)
    plt.xlabel('Number of samples')
    plt.ylabel('Area of Mandelbrot set')
    plt.title('Latin hypercube sampling \n Convergence of A_i,s as s increases')
    plt.savefig('Latiin_2.png')
    plt.clf()
    print array_mean_area
    print time.clock()
    """============need to change================================================================================================="""
    np.savetxt('Latin Sampling_s.txt', array_n)
    np.savetxt('Latin Sampling_change_mean_s.txt',change)
    np.savetxt('Latin Sampling_mean_s.txt',array_mean_area)
    
   
    
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
        self.iteration=1000
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
            #print self.s, self.n
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

main()
