
import numpy as np
import random
import simpy


n=1
# variables for the method of Batch means.
k=10000
r=100
      
def customer(env, name, counter):
    """Customer arrives, is served and leaves."""
    global wait
    arrive = env.now
    with counter.request() as req:
        yield req 
        wait = env.now - arrive
      
        p=random.uniform(0,1)
        if p<0.75:
            tib =random.expovariate(1)
        else:
            tib =random.expovariate(0.2)
        yield env.timeout(tib)
         
def source(env, ArriRate, counter):
    """Source generates customers randomly"""
    global MeanWaitingTime, sd_mean
    global s
    #d=1
    s=0
    i=1
    y=0
    MeanWaitingTime=0
    V_WaitTime=[]
    V_mean_waiting=[]
    while (s<1000): 
        'Run the single-run simulation for certain number of batches, which depends on how soon the d=S/k^0.5 will get less than the set d . '
        
        t = random.expovariate(ArriRate)
        yield env.timeout(t)
        c = customer(env, 'Customer%02d' % i, counter )
        env.process(c)
        if i>k: # start to collect data when i > warm-up period.
            V_WaitTime.append(wait)
            if i==k+(s+1)*r: #start to calculate the mean in the s-th batch. 
                y=np.mean(V_WaitTime)
                V_mean_waiting.append(y)
                V_WaitTime=[]
                
                if s==0:
                    sd_mean=0
                    #d=1
                else:
                    sd_mean=((1-1/s)*sd_mean**2+(y- MeanWaitingTime)**2/(s+1))**0.5
                    #d=sd_mean/(s+1)**0.5
                MeanWaitingTime=(s*MeanWaitingTime+y)/(s+1)   
                s+=1
        i+=1

# Setup and start the simulation
M=[]
result=[]
for l in range(80,98,2):
    load=float(l)/100
    ArriRate = load*n*0.5
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, ArriRate, counter))
    env.run()
    result=[s,MeanWaitingTime,load]
    np.savetxt('L_n=1_0.'+str(l)+'.txt',result)
    M.append(MeanWaitingTime)
    S.append(s)
np.savetxt('Long_n=1_meanM.txt',M)
np.savetxt('Long_n=1_meanS.txt',S)

