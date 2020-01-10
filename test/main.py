from copy import deepcopy
import pandas as  pd
import numpy as np
import time
from generator import genTask
from alpha import alphaComp
from ABalg import abComp
from appr import apprComp
import globalVar as gV


def comp(taskSet,coreNum):
    taskSetTemp = deepcopy(taskSet)
    alp1 = alphaComp(taskSetTemp, coreNum, "alg1")
    # print("alp 1 is ", alp1)
    taskSetTemp = deepcopy(taskSet)
    alp2 = alphaComp(taskSetTemp, coreNum, "alg2")
    # print("alp 2 is ", alp2)
    taskSetTemp = deepcopy(taskSet)
    ab   = abComp(taskSetTemp,0.414,coreNum)
    # print("ab is ", ab)
    taskSetTemp = deepcopy(taskSet)
    appr, lowerB = apprComp(taskSetTemp,coreNum)
    # print("appr is ", appr)
    # print("lowerB is", lowerB)
    gV.alp1.append(alp1 / lowerB)
    gV.alp2.append(alp2 / lowerB)
    gV.ab.append(ab / lowerB)
    gV.appr.append(appr / lowerB)



def taskNumRange(benchNum,coreNum,beta):
    for taskNum in range(10,101,10):
        bench = genTask(benchNum,taskNum,coreNum,beta)
        '''for i in range(benchNum):
            print("bench",i, "is", bench)'''
        for i in range(benchNum):
            comp(bench[i],coreNum)


def coreNumRange(benchNum,taskNum,beta):
    # for coreNum in (4,8,16,24,32,40,48,56,64):
    coreNum=gV.randoms
    bench = genTask(benchNum,taskNum,coreNum,beta)
    '''for i in range(benchNum):
        print("bench",i, "is", bench)'''
    for i in range(benchNum):
        comp(bench[i],coreNum)


def betaNumRange(benchNum,taskNum,coreNum):
    for beta in range(1,11,1):
        bench = genTask(benchNum,taskNum,coreNum,beta)
        '''for i in range(benchNum):
            print("bench",i, "is", bench)'''
        for i in range(benchNum):
            comp(bench[i],coreNum)


        
       



# 主模块
def main():
    benchNum = 1 # number of benchmarks
    taskNum  = np.random.randint(10, 100)   # number of tasks
    beta     = np.random.randint(1, 10)    # parameter beta
    # coreNum  = np.random.randint(4, 64)   # number of cores
    start = time.time()
    data=[]
    gV.randoms = np.random.randint(4, 64)
    for index in range(1,101,1):
        # taskNumRange(benchNum,coreNum,beta)
        coreNumRange(benchNum,taskNum,beta)
        # betaNumRange(benchNum,taskNum,coreNum)
    End = time.time()
    times=End-start
    data.append("Run: 100 tests in: "+str(round(times, 2))+" seconds")
    data.append( "Impt-I " + "Success: " + str(len(gV.alp1)))
    data.append("Impt-I " + "Errors: " + str((100 - len(gV.alp1))))
    data.append("Impt-I* " + "Success: " + str(len(gV.alp2)))
    data.append("Impt-I* " + "Errors: " + str((100 - len(gV.alp2))))
    data.append("Impt-II " + "Success: " + str(len(gV.ab)))
    data.append("Impt-II "+ "Errors: " + str((100 - len(gV.ab))))
    data.append("Impt-B " + "Success: " + str(len(gV.appr)))
    data.append("Impt-B " + "Errors: " + str((100 - len(gV.appr))))
    return data
def writefile(data):
    path='./data/test log.txt'
    with open(path,"w")as f:
        for d in data:
            f.write(d)
            f.write("\n")

if __name__ == "__main__":
    data = main()
    writefile(data)

