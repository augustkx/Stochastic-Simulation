import matplotlib.pyplot as plt 
import numpy as np
import random
def main():
    'Get data'
    data = np.genfromtxt("eil51.tsp.txt",delimiter=" ",skip_header=6, skip_footer=1)
    data_position = np.genfromtxt("eil51.tsp.txt",delimiter=" ",skip_header=6, skip_footer=1,usecols = (1, 2))
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
  
    show(data_position,initial_tour)
    
    
    'Simulated Annealing Method_ homogenous Markov chain'
    
    c=10#control value/temperature
    rate=0.95#decrease parameter
    tour=initial_tour
    cost=initial_cost
    V_itera=[]
    V_change=[]
    V_cost=[] 
    V_accept=[]
    V_itera1=[]
    V_theory=[]
    itera1=1
    rep=0
    itera=1
    while rep<200:
        rep+=1
        length=0
        accept=0
        
        
        while length <500 :
            'run the Markov chains for length steps at certain temperature '

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
            
            if p>1 or p>random.uniform(0,1):
                cost=change_cost+cost
                tour=new_tour
                accept += 1
                
            V_cost.append(cost)          
            V_itera.append(itera)
            V_change.append(change_cost)
            V_theory.append(426)
            length +=1
            itera+=1
        c=c*rate
        V_accept.append(accept)
        V_itera1.append(itera1)
        itera1 += 1
        
    show(data_position,tour)
    plt.savefig('C51_SA_homo.png')   
    np.savetxt('51_SA.txt',tour)
    np.savetxt('51_SA_cost.txt',[cost])
    np.savetxt('51_SA_accept.txt',V_accept)

    
    'Simulated Annealing Method_ inhomogenous Markov chain'
    V_cost_inhomo=[]
    l=0
    c=1/np.log(2+l)
    tour=initial_tour
    cost=initial_cost
    accept=0
    itera=1
    while l<100000 :
        'run the Markov chains for length steps at certain temperature '

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
            
        if p>1 or p>random.uniform(0,1):
            cost=change_cost+cost
            tour=new_tour
            accept += 1
                
        V_cost_inhomo.append(cost)          
        l +=1
        itera+=1
    show(data_position,tour)
    plt.savefig('C51_inhomo.png')
    print 'inhomo',tour,cost,c,itera
    np.savetxt('51_inhomo.txt',tour)
    np.savetxt('51_inhomo_cost.txt',[cost,accept])
    
    
    'Greedy Method'
    l=0
    tour=initial_tour
    V_cost_g=[]
    cost=initial_cost
    accept=0
    itera=1
    while l<100000 :
        'run the Markov chains for length steps at certain temperature '

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
        
            
        if change_cost<0:
            cost=change_cost+cost
            tour=new_tour
            accept += 1
                
        V_cost_g.append(cost)          
        l +=1
        itera+=1
    show(data_position,tour)
    plt.savefig('C51_G.png')
    
    np.savetxt('51_G.txt',tour)
    np.savetxt('51_G_cost.txt',[cost,accept])
    print 'greedy',tour,cost,itera
    plt.plot( V_itera, V_cost, label='Simulated Annealing Method_ homogenous Markov chain')
    plt.plot( V_itera, V_cost_inhomo, label='Simulated Annealing Method_ inhomogenous Markov chain')
    plt.plot( V_itera, V_cost_g, label='Greedy Method')
    plt.plot( V_itera, V_theory, label='Optimal tour')
    plt.legend(fontsize=9)
    plt.savefig('C51.png',dpi=500)
    plt.clf() 
    plt.plot( V_itera, V_cost, label='Simulated Annealing Method_ homogenous Markov chain')
    plt.plot( V_itera, V_cost_inhomo, label='Simulated Annealing Method_ inhomogenous Markov chain')
    plt.plot( V_itera, V_cost_g, label='Greedy Method')
    plt.plot( V_itera, V_theory, label='Optimal tour')
    plt.legend(fontsize=9)
      
    plt.xlim(0,4000)
    plt.savefig('C51_short.png',dpi=500) 




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
    

