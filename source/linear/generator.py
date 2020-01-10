import numpy as np
from copy import deepcopy


##########################################################
# Function genTask randomly generate job sets 
# The parameters of the jobs obey the uniform distribution
##########################################################
def genTask(benchNum,taskNum,coreNum,beta):
    z = np.random.uniform(1,100,[benchNum, taskNum])
    a = np.random.uniform(0.5*beta,beta,[benchNum, taskNum]) # a/10 is the ratio of x; 
    x = [[0 for j in range(taskNum)] for i in range(benchNum)] # x is the offloading time; 
    y = [[0 for j in range(taskNum)] for i in range(benchNum)] # y is the computation time
    for i in range(benchNum): # set the x and y: 
        for j in range(taskNum):
            x[i][j]=max((z[i][j]*a[i][j])/10,1)
            y[i][j]=max(z[i][j]*(10-a[i][j])/10,1)
    chi = np.random.uniform(1,coreNum,[benchNum, taskNum])
    x   = np.trunc(x)
    y   = np.trunc(y)
    chi = np.trunc(chi)
    bench = []
    for i in range(benchNum):
        task = [[0 for j  in range(4)] for i in range(taskNum)]
        for j in range(taskNum):
            task[j][0] = x[i][j]   # offloading time
            task[j][1] = y[i][j]   # computation time
            task[j][2] = chi[i][j] # expected cores
            task[j][3] = task[j][1] * task[j][2] # total workload
        taskTemp = deepcopy(task)
        bench.append(taskTemp)
    return bench
