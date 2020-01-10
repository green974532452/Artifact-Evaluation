import math



#alg = "alg1" or "alg2"
def sortTask(taskSet,coreNum, alg):
    maxWork = 0
    totalWork = 0
    secWork = 0
    work = []
    taskSet = sorted(taskSet, key = lambda s: s[3], reverse = True)
    for i in range(len(taskSet)): 
        work.insert(i,taskSet[i][1]*taskSet[i][2])
    totalWork = sum(work) # toal workload
    work      = sorted(work,reverse=True) # find the second largest workload
    maxWork   = work[0]
    if alg == "alg1":
        taskSet = sorted(taskSet,key = lambda task:task[3])        
    if alg == "alg2":
        if len(work)>1:
            secWork = work[1]
        else:
            secWork = work[0]
        taskSetTemp = []
        taskSetTemp.insert(0,taskSet[0])
        taskSet.pop(0)
        for i in range(len(taskSet),0,-1): # from the last to the first
            value = []
            for k in range(len(taskSet)): # find the i-th max task
                task = []
                task = taskSet[k]
                val = task[0] + max([task[1],totalWork*task[3]/(secWork*coreNum)])-totalWork*task[3]/((totalWork -secWork)*coreNum)
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


#modified
def alphaComp(taskSet,coreNum,alg):
    ##print("task set is", taskSet)
    taskSet, alpha = sortTask(taskSet,coreNum,alg)
    ##print("Finally task set is", taskSet)
    ##print("alp is ", alpha)
    cores  = []
    for i in range(coreNum):
        cores.append(0)        
    x = 0
    for task in taskSet:
        x = x+task[0]
        assignCoreNum = max([math.floor(alpha*coreNum),1])
        i = assignCoreNum
        for i in range(assignCoreNum-1,coreNum-1):
            if cores[i] < cores[i+1]:
                #assignCoreNum = i+1 #min([i+1,math.ceil(task[2])])
                ##print("assgin core is ",assignCoreNum)
                break
        assignCoreNum = min([i+1,math.floor(task[2]),coreNum])
        ##print("task exe",task[3]/assignCoreNum, "Assigned cores", assignCoreNum,"x", x)
        for i in range(assignCoreNum):
            cores[i] = max([x,cores[assignCoreNum-1]]) + task[3]/assignCoreNum
        cores = sorted(cores)
        ##print("core", cores)
    ##print("offloading = ",x)
    return cores[len(cores)-1]