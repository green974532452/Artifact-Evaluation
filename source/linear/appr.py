import math


from copy import deepcopy
from ABalg import abComp



########################################################
# Function countCore counts the cores used to execute the jobs in taskS0
# taskS0: the target job sets
# k: task[k] stores the number of cores need by the job
########################################################
def countCore(taskS0,k):
    totalCore = 0
    if len(taskS0) == 0:
        totalCore = 0
    else:
        for task in taskS0:
            if k==4 and task[k] <=1:
                continue
            totalCore = totalCore + task[k]
    return totalCore



########################################################
# Function feasi checks whether is a feasible schedule with makespan 1.5*d
# taskS1: jobs can be executed within d/2
# taskS2: taskS1 is taskSet - taskS1
# coreNum: the number of cores
########################################################
def feasi(taskS1,taskS2,d,coreNum):
    taskS0 = []
    S0core = countCore(taskS0,3)
    S2core = countCore(taskS2,4)
    #print("S0+S2",S0core,S2core, coreNum)
    while S0core + S2core > coreNum: # the condition is false if there is a feasible assignement
        #print("S0+S2",S0core,S2core, coreNum)
        changed = 0
        for task in taskS1:
            if task[3]>1 and task[5]<=0.75*d: # the job need more than one core, and if it is executed within 0.75*d
                taskTem = deepcopy(task)
                changed = changed + 1
                taskTem[3] = taskTem[3] - 1 # use less core to execute this job
                taskS0.append(taskTem)
                taskS1.pop(taskS1.index(task))
            elif task[3] == 1:
                index = taskS1.index(task)
                length = len(taskS1)
                for i in range(length):
                    #print("OOOOOOOOOOOOOOOOOOOOOOOOOO ",i, index+1,len(taskS1))
                    task1 = taskS1[i]
                    if task1[3] == 1 and i != index:
                        taskTem = deepcopy(task)
                        taskTem1 = deepcopy(task1)
                        changed = changed + 1
                        taskTem[3]  = 0.5
                        taskTem1[3] = 0.5
                        taskS0.append(taskTem)
                        taskS0.append(taskTem1)
                        taskS1.pop(taskS1.index(task))
                        taskS1.pop(taskS1.index(task1))
                        break
        for task in taskS2:
            idleCore = coreNum-countCore(taskS0,3) - countCore(taskS1,3)
            if idleCore>0 and task[1]*task[2]/idleCore < 1.5 *d :
                taskTem = deepcopy(task)
                changed = changed + 1
                assignCore = math.ceil(max([1,task[1]*task[2]/(1.5*d),]))
                taskTem[3] = assignCore
                if taskTem[1]*taskTem[2]/assignCore >=d:
                    taskS0.append(taskTem)
                else:
                    taskS1.append(taskTem)
                taskS2.pop(taskS2.index(task))
        if changed == 0:
            return False
        S0core = countCore(taskS0,3)
        S2core = countCore(taskS2,4)
    return True

########################################################
# Functioin appr check whether is a feasible schedule with makespan 1.5*d
# taskSet: the target job set
# coreNum: the number of cores
########################################################
def appr(taskSet,d,coreNum):
    for task in taskSet: # remove job J from taskSet if workload of J is no more than d/2
        if task[1]*task[2] <= d/2:
            taskSet.pop(taskSet.index(task))
    for task in taskSet: # calculate the core number that should be assigned to each job
        mLGd = math.ceil(max([1,task[1]*task[2]/d]))
        if mLGd > task[2]:
            mLGd = -1
        task.insert(3,mLGd) #m_i^d
        mHarfd =  max([1,2*task[1]*task[2]/d])
        if mHarfd > task[2]:
            mHarfd = -1
        task.insert(4,mHarfd) #m_i^d/2
        task.insert(5,task[1]*task[2]/task[3]) #W/m_i^d
    taskS1 = []
    for task in taskSet: # remove job J if it cannot be execution within d/2
        if task[4] == -1:
            taskS1.append(task)
            taskSet.pop(taskSet.index(task))
    taskSet = sorted(taskSet, key = lambda task:task[5],reverse = True)
    m = 0
    for task in taskSet:
        if m + task[3] > coreNum:
            break
        m = m+task[3]
        taskS1.append(task) # the job can be executed within d/2
        taskSet.pop(taskSet.index(task))
    return feasi(taskS1,taskSet,d,coreNum)
    #print("task set 1 is ",taskS1)
    #print("task set 2 is ",taskSet)



########################################################
# Functioin apprComp compute the makespan by using Impt-B
# taskSet: the target job set
# coreNum: the number of cores
########################################################
def apprComp(taskSet,coreNum):
    lowerBappr = 0 # the lower bound of the makespan
    taskSet = sorted(taskSet,key = lambda task:task[0]) # sort task set by the offloading time
    workSum = 0 # summation of the workload
    ymax = 0    # maximum execution time among the jobs in taskSet
    ymin = 1000 # minimum execution time among the jobs in taskSet
    for task in taskSet: # solve the total workload workSum, the maximum execution time ymax, and the minimum execution time
        workSum = workSum + task[3]
        if ymax < task[1]:
            ymax = task[1]
        if ymin > task[1]:
            ymin = task[1]
    #print("ymax",ymax)
    lowerB = workSum/coreNum # solve the lower bound of the makespan
    #print("W/m", lowerB)
    xmin = taskSet[0][0] # the minimum offloading time
    #print("xmin", xmin)
    x = 0
    for task in taskSet: # solve the total offloading time
        x = x + task[0]
    for task in taskSet:
        task[0] = 0
    lb = lowerB   # lb is used as the lower bound for the makespan in Impl-B
    #print("before", taskSet)
    ub = abComp(taskSet,1,coreNum) # ub is used as the upper bound for the makespan in Impt-B, which can be calculated by Impl-II
    if ub==None:
        #print(taskSet)
        return None
    #print("after",taskSet)
    ymax = 0
    for task in taskSet:
        if task[1] > ymax:
            ymax = task[1]    
    d = ub
    #print("ub = d", d)
    while lb < ub-1: # implment Impl-B as the binary searching
        d = (lb+ub)/2
        if d>ymax and d >lowerB and appr(taskSet,d,coreNum): # appr check whether there is a feasible schedule with response time 1.5*d, where 1.5 is the approximation factor. 
            ub = d
        else:
            lb = d
    # lowerBappr = max([ymax,lowerB,lb]) +xmin
    lowerBappr = max([ymax,lb]) + xmin
    #print("former lower", lowerBappr)
    lowerBappr = max([lowerBappr,x+ymin])
    #print("lower bound, x", lowerBappr,x+ymin)
    #print("app's ratio ", (x+1.5*d)/lowerBappr)
    return x + 1.5*d, lowerBappr # return the makespan (the sum of total offloading time and the responses time for scheduling the jobs), and the lower bound for the makespan.