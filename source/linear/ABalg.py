import math
import numpy as np

########################################################
# Function sortAB sort the jobs in taskSet by their workload, and parition the jobs into two sets as shown in Alg.3
# taskSet: target job set
# alp: rho in the paper
# coreNum: the number of cores
########################################################
def sortAB(taskSet,alp,coreNum):
    taskSet = sorted(taskSet, key = lambda task:task[2])
    taskSA = []
    taskSB = []
    for task in taskSet:
        if task[2] > alp*coreNum:
            taskSA.append(task)
        else:
            taskSB.append(task)
    taskSA1 = []
    taskSA2 = []
    for task in taskSA:
        if task[0]<=task[1]:
            taskSA1.append(task)
        else:
            taskSA2.append(task)
    taskSA1 = sorted(taskSA1,key = lambda task:task[0])
    taskSA2 = sorted(taskSA2,key = lambda task:task[1],reverse=True)
    taskSA1.extend(taskSA2)
    if len(taskSB) == 0:
        return taskSA1
    taskSB = sorted(taskSB,key=lambda task:task[1],reverse = True)
    m = 0
    highest = taskSB[0][1]
    for task in taskSB:
        '''if highest <= 0:
            #print("KKKKKKKKKKKKKKKKKKKKKK",highest)
            #print(taskSet)'''
        #if highest<=0 or len(task)<=3:
            ##print(task)
            #return None
        assignCoreNum = max([1,math.ceil(task[3]/highest)])
        if m + assignCoreNum > coreNum:
            m = task[2]
            highest = task[1]
            ##print("SSSSSSSSSSSSSSSSSSSSSSSSS",highest)
            task.insert(4,task[1]) #new execution time
            task.insert(5,task[2]) #new cores
            task.insert(6,highest) #highest in the pack
        else:
            m = m + assignCoreNum
            task.insert(4,max(1,math.ceil(task[3]/assignCoreNum))) #new execution time
            task.insert(5,assignCoreNum) #new cores
            task.insert(6,highest) #highest in the pack
    x = 0
    left = 0
    for i in range(len(taskSB)-1):
        if taskSB[i][6] == taskSB[i+1][6]:
            x = x + taskSB[i+1][6]
        else:
            for j in range(left,i+1):
                task = taskSB[j]
                task.insert(7,x) #total offloading time of a pack
            x=0
            left = i+1
    for i in range(left,len(taskSB)):
        task = taskSB[i]
        task.insert(7,x)
    taskSB1 = []
    taskSB2 = []
    for task in taskSB:
        if task[7] <= task[6]:
            taskSB1.append(task)
        else:
            taskSB2.append(task)
    taskSB1 = sorted(taskSB1,key = lambda task:task[7])
    taskSB2 = sorted(taskSB2,key = lambda task:task[6],reverse=True)
    taskSB1.extend(taskSB2)
    for task in taskSB1:
        extT = task[4]
        expCore = task[5]
        task.insert(1,extT) #new execution time
        task.insert(2,expCore) #new core number
    taskSA1.extend(taskSB1)  
    for task in taskSA1:
        for i in range(len(task)-3):
            task.pop()
    for i in range(1,len(taskSA1)):
        task = taskSA1[i]
        task[0] = task[0] + taskSA1[i-1][0]
    #print(taskSA1)
    return taskSA1


########################################################
# Function abComp compute the makespan by using Impl-II
# taskSet: target job set
# alp: rho in the paper
# coreNum: the number of cores
########################################################
def abComp(taskSet,alp,coreNum):
    taskSet = sortAB(taskSet,alp,coreNum) # sort the taskSet and implemnt the partitioning 
    if taskSet==None:
        #print(taskSet)
        return None
    total = 0
    for task in taskSet: # total workload
        total = total + task[1]*task[2]
    #print("lower bound is ", total/coreNum)
    cores = np.zeros(coreNum)
    while len(taskSet)>0:
        cores = sorted(cores)
        #print("cores is ",cores)
        for task in taskSet:
            firstK = math.floor(min([task[2],coreNum-1])) # assign proper nubmer of cores to job
            if cores[firstK]<=task[0]: # if the core's finishing time is less than the offloading time
                task[0] = task[0]
            else:
                task[0] = cores[firstK]
        taskSet = sorted(taskSet,key = lambda task:task[0])
        task = taskSet[0]
        #print("task's start time",task[0],task[1],task[3])
        for i in range(0,math.ceil(task[2])):
            cores[i] = task[0] + task[1] # update core's finishing time
            #print("cores start time:", cores[i])
        taskSet.pop(0)
    return max(cores)
