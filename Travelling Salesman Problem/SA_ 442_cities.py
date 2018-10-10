import matplotlib.pyplot as plt 
import numpy as np
import random
def main():
    'Get data'
    data = np.genfromtxt("pcb442.tsp.txt",skip_header=6, skip_footer=1)
    data_position = np.genfromtxt("pcb442.tsp.txt",skip_header=6, skip_footer=1,usecols = (1, 2))
    N_City=len(data)
    
    distance=np.zeros((N_City,N_City))
    for i in range(0,N_City):
        for j in range(0,N_City):
            distance[i][j]= ( (data[i][1]-data[j][1])**2  +  (data[i][2]-data[j][2])**2 )**0.5

    
    #Set the initial cost:in the order of 1,2,3,...N.
    initial_cost=0
    initial_tour=[]
    for i in range(0,N_City):
        initial_tour.append(data[i][0])
    initial_tour.append(1)    
    for i in range(0,N_City):
        initial_cost=initial_cost+distance[initial_tour[i]-1][initial_tour[i+1]-1]
  
    print 'c', initial_cost
    show(data_position,initial_tour)
    
    
    'Simulated Annealing Method_ homogenous Markov chain'
    
    c=1000#control value/temperature    
    rate=0.999#decrease parameter
    tour=initial_tour
    cost=initial_cost
    V_itera=[]
    V_change=[]
    V_cost=[] 
    V_accept=[]
    V_rep=[]
    V_theory=[]

    rep=0 # the number of simulation
    itera=1 #the whole number of Markov chains
    
    stop=0
    while stop<1000:# Stoping condition: the accepted tours in an Markov chain simulation is zero for 100 number of Markov chains.
        rep+=1
        length=0
        accept=0
        
        while length <1000 : 
            'run the Markov chains for length steps at each temperature '

            s=random.randint(1,len(tour)-2)
            k=random.randint(1,len(tour)-2)            
            while (k==s or k==s+1 or k==s-1):
                k=random.randint(1,len(tour)-2) 
            if s>k:
                a=s
                s=k
                k=a
            new_tour=move_state(tour,s,k)
            change_cost=distance[new_tour[s-1]-1][new_tour[s]-1]+distance[new_tour[k]-1][new_tour[k+1]-1]-distance[new_tour[s-1]-1][new_tour[k]-1] -distance[new_tour[s]-1][new_tour[k+1]-1]
            p=np.exp(-change_cost/c)
            
            if p>1 or p>random.uniform(0,1):# Metropolis
                cost=change_cost+cost
                tour=new_tour
                accept += 1
            
            V_cost.append(cost)          
            V_itera.append(itera)
            V_change.append(change_cost)
            V_theory.append(50778)
            length +=1
            itera+=1
        
        if accept==0:# Stoping condition marking
            stop+=1

        
        c=c*rate
        V_accept.append(accept)
        V_rep.append(rep)# to compare how quickly it convergrnve to an local minimum.

        print accept
    
    show(data_position,tour)
    plt.savefig('442_SA_homo.png')   
    print 'rep',rep,'HO',tour,cost,c,itera
    
    #plt.plot( V_itera1, V_accept, label='Number of accepted generated tours')
    #plt.title('The decrease of accepted generated tours each Markov chain')
    #plt.legend(fontsize=9)
    plt.plot( V_itera, V_cost, label='Simulated Annealing Method_ homogenous Markov chain')
    plt.plot( V_itera, V_theory, label='Optimal tour')
    plt.legend(fontsize=9)

    plt.savefig('SA_442_6000.png', dpi=400) 
    plt.clf() 
    plt.plot( V_itera, V_cost, label='Simulated Annealing Method_ homogenous Markov chain')
    plt.plot( V_itera, V_theory, label='Optimal tour')
    plt.legend(fontsize=9)

    plt.xlim(0,10000)
    plt.savefig('SA_c_6000_short.png', dpi=400) 
    np.savetxt('442_G.txt',tour)
    np.savetxt('442_G_cost.txt',[cost])
    np.savetxt('442_G_accept.txt',V_accept)
    
    
def move_state(tour,s,k):
    'the next state of Markov chains.'
        
    j=0
    n_tour=np.zeros((len(tour)))
    for i in range(s,k+1):
        n_tour[i]=tour[k-j]
        j+=1
    for i in range(0,s):
        n_tour[i]=tour[i]
    for i in range(k+1,len(tour)):
        n_tour[i]=tour[i]
    
    return n_tour
def show(data_position,tour):        
    Pt = [data_position[tour[i]-1] for i in range(len(tour))]
    Pt = np.array(Pt)
    plt.plot(Pt[:,0], Pt[:,1], '-o')
    plt.show()
        

main()
    

