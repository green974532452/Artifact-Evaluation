from copy import deepcopy
import pandas as  pd
from generator import genTask
from alpha import alphaComp
from ABalg import abComp
from appr import apprComp

import globalVarBeta as gV
import drawBeta


def comp(taskSet, coreNum,taskNum,beta):
    taskSetTemp = deepcopy(taskSet)
    alp1 = alphaComp(taskSetTemp, coreNum, "alg1")
    gV.d[beta].setdefault('alp1', []).append(alp1)  # 在字典d中加入alp1数据
    # print("alp 1 is ", alp1)
    taskSetTemp = deepcopy(taskSet)
    alp2 = alphaComp(taskSetTemp, coreNum, "alg2")
    gV.d[beta].setdefault('alp2', []).append(alp2)  # 在字典d中加入alp2数据
    # print("alp 2 is ", alp2)
    taskSetTemp = deepcopy(taskSet)
    ab = abComp(taskSetTemp, 0.414, coreNum)
    gV.d[beta].setdefault('ab', []).append(ab)  # 在字典d中加入ab数据
    # print("ab is ", ab)
    taskSetTemp = deepcopy(taskSet)
    appr, lowerB = apprComp(taskSetTemp, coreNum)
    gV.d[beta].setdefault('appr', []).append(appr)  # 在字典d中加入appr数据
    # print("appr is ", appr)
    gV.d[beta].setdefault('lowerB', []).append(lowerB)  # 在字典d中加入lowerB数据
    # print("lowerB is", lowerB)

    gV.db[beta].setdefault('alp1', []).append(alp1 / lowerB)
    gV.db[beta].setdefault('alp2', []).append(alp2 / lowerB)
    if ab<lowerB or alp2<lowerB:
        print("error: alp2<lowerB",alp2,lowerB)
    gV.db[beta].setdefault('ab', []).append(ab / lowerB)
    gV.db[beta].setdefault('appr', []).append(appr / lowerB)


def taskNumRange(benchNum, coreNum, beta):
    for taskNum in range(10, 101, 10):
        bench = genTask(benchNum, taskNum, coreNum, beta)
        '''for i in range(benchNum):
            print("bench",i, "is", bench)'''
        for i in range(benchNum):
            comp(bench[i], coreNum,taskNum,beta)


def coreNumRange(benchNum, taskNum, beta):
    for coreNum in (4, 8, 16, 24, 32, 40, 48, 56, 64):
        bench = genTask(benchNum, taskNum, coreNum, beta)
        '''for i in range(benchNum):
            print("bench",i, "is", bench)'''
        for i in range(benchNum):
            comp(bench[i], coreNum,taskNum,beta)


def betaNumRange(benchNum, taskNum, coreNum):
    for beta in range(1, 11, 1):
        bench = genTask(benchNum, taskNum, coreNum, beta)
        '''for i in range(benchNum):
            print("bench",i, "is", bench)'''
        for i in range(benchNum):
            comp(bench[i], coreNum,taskNum,beta)


# 主模块
def main():
    benchNum = 1  # number of benchmarks
    taskNum = 50  # number of tasks
    beta = 5  # parameter beta
    coreNum = 16  # number of cores
    for index in range(1, 101, 1):
        # taskNumRange(benchNum,coreNum,beta)
        # coreNumRange(benchNum, taskNum, beta)
        betaNumRange(benchNum,taskNum,coreNum)

        writer = pd.ExcelWriter(r'./data/Fig.6(a).xlsx')
        for d2 in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            df = pd.DataFrame(gV.d[d2])

            # df.to_excel(r'G:\abc.xlsx',columns=i+6, index=False)
            df.to_excel(excel_writer=writer, sheet_name='beta ' + str(d2),
                        header=[str(d2) + " alp1", str(d2) + " alp2", str(d2) + " ab", str(d2) + " appr",
                                str(d2) + " lowerB"])
        writer.save()
        writer.close()

    for d1 in [1,2,3,4,5,6,7,8,9,10]:
        for var in ['alp1', 'alp2', 'ab', 'appr']:
            gV.db[d1][var].sort()  # 对字典里数据进行排序db是除以lowerB的数据
            gV.avg[d1][var] = sum(gV.db[d1][var]) / len(gV.db[d1][var])  # 求字典d里面数据的平均值

    arr_a1p1 = []
    arr_a1p2 = []
    arr_ab = []
    arr_appr = []
    arr_avg_alp1 = []
    arr_avg_alp2 = []
    arr_avg_ab = []
    arr_avg_appr = []

    # 将字典的数据存入到数组中
    for index_x in [1,2,3,4,5,6,7,8,9,10]:
        arr_a1p1.append([index_x, gV.db[index_x]['alp1']])
        arr_a1p2.append([index_x, gV.db[index_x]['alp2']])
        arr_ab.append([index_x, gV.db[index_x]['ab']])
        arr_appr.append([index_x, gV.db[index_x]['appr']])
        arr_avg_alp1.append(gV.avg[index_x]['alp1'])
        arr_avg_alp2.append(gV.avg[index_x]['alp2'])
        arr_avg_ab.append(gV.avg[index_x]['ab'])
        arr_avg_appr.append(gV.avg[index_x]['appr'])

        # 存入第100个数据和第900个数据
    for k in [9, 89]:
        gV.arr_a1p1_1_9.append([arr_a1p1[0][1][k], arr_a1p1[1][1][k], arr_a1p1[2][1][k], arr_a1p1[3][1][k],
                                arr_a1p1[4][1][k], arr_a1p1[5][1][k], arr_a1p1[6][1][k], arr_a1p1[7][1][k]
                                   , arr_a1p1[8][1][k], arr_a1p1[9][1][k]])
        gV.arr_a1p2_1_9.append([arr_a1p2[0][1][k], arr_a1p2[1][1][k], arr_a1p2[2][1][k], arr_a1p2[3][1][k],
                                arr_a1p2[4][1][k], arr_a1p2[5][1][k], arr_a1p2[6][1][k], arr_a1p2[7][1][k]
                                   , arr_a1p2[8][1][k], arr_a1p2[9][1][k]])
        gV.arr_ab_1_9.append([arr_ab[0][1][k], arr_ab[1][1][k], arr_ab[2][1][k], arr_ab[3][1][k],
                              arr_ab[4][1][k], arr_ab[5][1][k], arr_ab[6][1][k], arr_ab[7][1][k]
                                 , arr_ab[8][1][k], arr_ab[9][1][k]])
        gV.arr_appr_1_9.append([arr_appr[0][1][k], arr_appr[1][1][k], arr_appr[2][1][k], arr_appr[3][1][k],
                                arr_appr[4][1][k], arr_appr[5][1][k], arr_appr[6][1][k], arr_appr[7][1][k]
                                   , arr_appr[8][1][k], arr_appr[9][1][k]])

    gV.arr_db = [arr_a1p1, arr_a1p2, arr_ab, arr_appr]
    gV.arr_avg = [arr_avg_alp1, arr_avg_alp2, arr_avg_ab, arr_avg_appr]
    # print(gV.arr_avg[0][0])


if __name__ == "__main__":
    main()
    drawBeta.plot()