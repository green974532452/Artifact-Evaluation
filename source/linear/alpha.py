import math


###############################################
# Function sortTask sort the jobs in taskSet, and calculate the alpha factor
# alg = alg1 means Impl-I
# alg = alg2 means Impl-I*
# taskSet: target job set
# coreNum: the number of cores
###############################################
def sortTask(taskSet,coreNum, alg):
    maxWork = 0   # maximum workload
    totalWork = 0 # total workload
    secWork = 0   # the second largest workload
    work = []     # the workload of each job
    taskSet = sorted(taskSet, key = lambda s: s[3], reverse = True) # sort the jobs by their workloads
    for i in range(len(taskSet)): # calculate the workload for each job
        work.insert(i,taskSet[i][1]*taskSet[i][2])
    totalWork = sum(work) # toal workload
    work      = sorted(work,reverse=True) # sort the jobs aiming to find the second largest workload and implement Impl-I*
    maxWork   = work[0]
    if alg == "alg1":
        taskSet = sorted(taskSet,key = lambda task:task[3]) # sort the jobs aiming to find the largest workload       
    if alg == "alg2":
        if len(work)>1:
            secWork = work[1] # find the second largest workload
        else:
            secWork = work[0] # find the largest workload
        taskSetTemp = [] # store the jobs that have been sorted
        taskSetTemp.insert(0,taskSet[0])
        taskSet.pop(0)
        for i in range(len(taskSet),0,-1): # from the last to the first
            value = []
            for k in range(len(taskSet)): # find the i-th max task
                task = []
                task = taskSet[k]
                val = task[0] + max([task[1],totalWork*task[3]/(secWork*coreNum)])-totalWork*task[3]/((totalWork -secWork)*coreNum) # calculate the parameters at Line 4 of Alg. 2
                ##print("val is ", val)
                value.insert(i, val)
            minIndex = 0
            maxOff = 0
            for j in range(len(value)):
                if value[j] == min(value) and maxOff < taskSet[j][0]:
                    maxOff = taskSet[j][0]
                    minIndex = j
            task = []
            for k in range(4):
                task.insert(k,taskSet[minIndex][k])
            taskSetTemp.insert(i,task)
            taskSet.pop(minIndex)
        taskSet = taskSetTemp
    if alg == "alg1":
        alpha = maxWork/totalWork
    if alg == "alg2":
        alpha = secWork/totalWork
    ##print("finally = ",taskSet)
    ##print("lower bound = ", totalWork/coreNum)
    lowerB = totalWork/coreNum
    return taskSet, alpha    


###############################################
# Function alphaComp compute the makespan by using Impl-I and Impl-I*
# alg = alg1 means Impl-I
# alg = alg2 means Impl-I*
# taskSet: target job set
# coreNum: the number of cores
###############################################
def alphaComp(taskSet,coreNum,alg):
    ##print("task set is", taskSet)
    taskSet, alpha = sortTask(taskSet,coreNum,alg) # sort the jobs and calculate the alpha factor
    ##print("Finally task set is", taskSet)
    ##print("alp is ", alpha)
    cores  = []
    for i in range(coreNum):
        cores.append(0)        
    x = 0 # store the offloading time
    for task in taskSet: # offload and schedule each job 
        x = x+task[0] # the currrent offloading time
        assignCoreNum = max([math.floor(alpha*coreNum),1]) # calculate the number cores assigned to the interested job 
        i = assignCoreNum
        for i in range(assignCoreNum-1,coreNum-1): # find the proper cores
            if cores[i] < cores[i+1]:
                #assignCoreNum = i+1 #min([i+1,math.ceil(task[2])])
                ##print("assgin core is ",assignCoreNum)
                break
        assignCoreNum = min([i+1,math.floor(task[2]),coreNum]) # assign the proper cores to the job
        ##print("task exe",task[3]/assignCoreNum, "Assigned cores", assignCoreNum,"x", x)
        for i in range(assignCoreNum): # calculate the finishing time of each core
            cores[i] = max([x,cores[assignCoreNum-1]]) + task[3]/assignCoreNum
        cores = sorted(cores)
        ##print("core", cores)
    ##print("offloading = ",x)
    return cores[len(cores)-1]