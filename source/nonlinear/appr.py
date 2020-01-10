import math


from copy import deepcopy
from ABalg import abComp
import TP



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

def feasi(taskS1,taskS2,d,coreNum):
    taskS0 = []
    S0core = countCore(taskS0,3)
    S2core = countCore(taskS2,4)
    #print("S0+S2",S0core,S2core, coreNum)
    while S0core + S2core > coreNum:
        #print("S0+S2",S0core,S2core, coreNum)
        changed = 0
        for task in taskS1:
            if task[3]>1 and task[5]<=0.75*d:
                taskTem = deepcopy(task)
                changed = changed + 1
                taskTem[3] = taskTem[3] - 1
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
                assignCore = math.ceil(max([1,task[1]*task[2]/(1.5*d)]))      #########################
                nonlinear = TP.twophare(assignCore,task[2])
                taskTem[3] = assignCore                                        ########################
                if taskTem[1]*taskTem[2]/(assignCore*nonlinear) >=d:                       #########################
                    taskS0.append(taskTem)
                else:
                    taskS1.append(taskTem)
                taskS2.pop(taskS2.index(task))
        if changed == 0:
            return False
        S0core = countCore(taskS0,3)
        S2core = countCore(taskS2,4)
    return True


def appr(taskSet,d,coreNum):
    for task in taskSet:
        if 2*task[1]*task[2] <= d/2:
            taskSet.pop(taskSet.index(task))
    for task in taskSet:
        mLGd = math.ceil(max([1,task[1]*task[2]/d]))
        if mLGd > task[2]:
            mLGd = -1
        task.insert(3,mLGd) #m_i^d
        mHarfd =  max([1,4*task[1]*task[2]/d])
        if mHarfd > task[2]:
            mHarfd = -1
        task.insert(4,mHarfd) #m_i^d/2
        task.insert(5,2*task[1]*task[2]/task[3]) #W/m_i^d
    taskS1 = []
    for task in taskSet:
        if task[4] == -1:
            taskS1.append(task)
            taskSet.pop(taskSet.index(task))
    taskSet = sorted(taskSet, key = lambda task:task[5],reverse = True)
    m = 0
    for task in taskSet:
        if m + task[3] > coreNum:
            break
        m = m+task[3]
        taskS1.append(task)
        taskSet.pop(taskSet.index(task))
    return feasi(taskS1,taskSet,d,coreNum)
    #print("task set 1 is ",taskS1)
    #print("task set 2 is ",taskSet)





def apprComp(taskSet,coreNum):
    lowerBappr = 0
    taskSet = sorted(taskSet,key = lambda task:task[0])
    workSum = 0
    ymax = 0
    ymin = 1000
    for task in taskSet:
        workSum = workSum + task[3]
        if ymax < task[1]:
            ymax = task[1]
        if ymin > task[1]:
            ymin = task[1]
    #print("ymax",ymax)
    lowerB = workSum/coreNum
    #print("W/m", lowerB)
    xmin = taskSet[0][0]
    #print("xmin", xmin)
    x = 0
    for task in taskSet:
        x = x + task[0]
    for task in taskSet:
        task[0] = 0
    lb = lowerB
    #print("before", taskSet)
    ub = abComp(taskSet,1,coreNum)
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
    while lb < ub-1:
        d = (lb+ub)/2
        if d>ymax and d >lowerB and appr(taskSet,d,coreNum):
            ub = d
        else:
            lb = d
    # lowerBappr = max([ymax,lowerB,lb]) +xmin
    lowerBappr = max([ymax,lb]) + xmin
    #print("former lower", lowerBappr)
    lowerBappr = max([lowerBappr,x+ymin])
    #print("lower bound, x", lowerBappr,x+ymin)
    #print("app's ratio ", (x+1.5*d)/lowerBappr)
    return x + 1.5*d, lowerBappr