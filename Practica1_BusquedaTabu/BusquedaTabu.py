import numpy as np
import pandas as pd
import random as rn
import copy

def greedy(N, costs):
    x_0 = [0] #Siempre se inicia en la ciudad 0
    while(len(x_0)<N): #Se cicla hasta que se hayan pasado todas las ciudades
        temp = copy.copy(costs[x_0[-1]]) #Variable temporal de ayuda
        temp[x_0] = np.max(costs[x_0[-1]])+1 #Se pone el costo máximo+1 a aquellas ciudades que ya se visitaron para que no se escojan
        x_0.append(np.argmin(temp)) #Se agrega el índice de la ciudad a la que es más barato moverse
    return x_0

def f(x,costs): #Función de costo de una solución
    r = 0
    a = x+[0]
    for i in range(len(a)-1):
        r += costs[a[i],a[i+1]]
    return r

def Neighbour(x,T,N,costs): #Generación del vecindario
    c = rn.choice(range(1,N)) #Se escoge una ciudad aleatoria a mover
    temp = copy.copy(x) #Variable temporal de ayuda
    vecindario = [] #Se inicializa el vecindario
    
    while(c in T[:,0]): #Se escoge una ciudad aleatoria hasta que esta no esté en la lista tabú y que no sea 0, ya que siempre se va a empezar en la ciudad 0
        c = rn.choice(range(1,N))
    temp.remove(c)
    
    for i in range(1,N):
        vecindario.append(temp[:i]+[c]+temp[i:])
    vecindario.remove(x)
    T = np.append(T,[[c,N/2]],axis=0)
    return vecindario, T

def BusquedaTabu(I_max,N,costs):
    x_0 = greedy(N,costs)
    x_best = x_0
    f_best = f(x_0,costs)
    k = 0
    x = x_0
    T = np.array([])
    T = T.reshape((0,2))
    while(k < I_max):
        N_star, T = Neighbour(x,T,N,costs)
        N_star_costs = np.array([f(i,costs) for i in N_star])
        x = N_star[np.argmin(N_star_costs)]
        f_x = f(x,costs)
        if f_x < f_best:
            x_best = x
            f_best = f_x
        k += 1
        T[:,1] -= 1
        i = 0
        while i < len(T):
            if T[i,1]==0:
                T = np.delete(T,i,axis=0)
                i -= 1
            i+=1
    return x_best, f_best


def ejecutar(name,M):
    with open(f"{name}.txt") as f:
        lines = f.readlines() #Lee el input
        N = int(lines[0])
        I_max = int(lines[1])
        cost = []
        for i in range(N-1):
            cost.append(list(map(int,lines[2+i].split(" "))))

    costs = np.zeros((N,N)) #Se inicializa tabla de costes
    for i in range(N-1): #Se crea la tabla de costes
        costs[i,i+1:] = cost[i]
        costs[i+1:,i] = cost[i]
    
    soluciones = []
    costes = np.array([])

    for i in range(9):
        x_best, f_best = BusquedaTabu(I_max,N,costs)
        soluciones.append(x_best)
        costes = np.append(costes,f_best)
    
    return soluciones, costes

if __name__ == __main__:
    
    name = input("Nombre del archivo txt con la entrada (sin la extención): ")
    M = int(input("Número de veces a ejecutar BT: "))
    
    soluciones, costes = ejecutar(name,M)
    
    print("Mejor solución encontrada: ", soluciones[np.argmin(costes)], "con coste: ", min(costes))
    print("Peor solución encontrada: ", soluciones[np.argmax(costes)], "con coste: ", max(costes))
    print("Solución 'mediana': ", soluciones[np.argsort(costes)[M//2]], "con coste: ", costes[np.argsort(costes)[M//2]])
    print("Media: ", np.mean(costes))
    print("Desviación estandar: ", np.std(costes))