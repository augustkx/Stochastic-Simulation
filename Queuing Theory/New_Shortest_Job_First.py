import numpy as np
import random
import simpy

n=1 # the numner of servers
CapServer=1.0 #the processor capacity 
# variables for the method of Batch means.
k=10000
r=100
      
def customer(env, name, counter, CapServer,i):
    """Customer arrives, is served and leaves."""
    global V_WaitTime,MeanWaitingTime,sd_mean,s,d
    arrive = env.now
    tib = random.expovariate(CapServer)
    with counter.request(priority=tib) as req:
        yield req 
        wait = env.now - arrive
        yield env.timeout(tib)
        V_WaitTime.append(wait) 
        if i==k+(s+1)*r: #start to calculate the mean in the s-th batch. 
            y=np.mean(V_WaitTime)
            V_mean_waiting.append(y)
            V_WaitTime=[]
               
            if s==0:
                sd_mean=0
                d=1
            else:
                sd_mean=((1-1/s)*sd_mean**2+(y- MeanWaitingTime)**2/(s+1))**0.5
                d=sd_mean/(s+1)**0.5
            
            MeanWaitingTime=(s*MeanWaitingTime+y)/(s+1)   
            s+=1
            print (d)

def source(env, ArriRate, counter):
    """Source generates customers randomly"""
    global MeanWaitingTime,V_mean_waiting,V_WaitTime,sd_mean,i,y,s,d

    d=1
    s=0
    i=1
    y=0
    MeanWaitingTime=0
    sd_mean=0
    V_WaitTime=[]    
    V_mean_waiting=[]
    while  (d>0.4 or s<100): 
        'Run the single-run simulation for certain number of batches, which depends on how soon the d=S/k^0.5 will get less than the set d . '
        c = customer(env, 'Customer%02d' % i, counter, CapServer,i)
        env.process(c)
        t = random.expovariate(ArriRate)
        yield env.timeout(t)
        i+=1




result=[]
M=[]
S=[]
T_W=[]
for l in range(90,91):
    load=float(l)/100
    ArriRate = load*n*CapServer
    TheorymeanWaitingTime=load/(CapServer*(1-load))
    env = simpy.Environment()
    counter = simpy.PriorityResource(env, capacity=n)
    env.process(source(env, ArriRate, counter))
    env.run()
    result=[s,TheorymeanWaitingTime,MeanWaitingTime,load]

    "print 'load:', load , 'Theory meanWaitingTime %7.4f'%( TheorymeanWaitingTime),'simulate waiting time', MeanWaitingTime"
    np.savetxt('n=2_0.'+str(l)+'.txt',result)
    M.append(MeanWaitingTime)
    S.append(s)
#np.savetxt('n=2_meanM.txt',M)
#np.savetxt('n=2_meanS.txt',S)