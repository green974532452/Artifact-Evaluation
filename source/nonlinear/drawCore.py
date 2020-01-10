import matplotlib.pyplot as plt
import globalVarCore as gV

n=20
def plot():
    fig = plt.figure()
    fig.subplots_adjust(top=0.99, bottom=0.22, left=0.09, right=0.93, wspace=0.43, hspace=0.5)
    ax = fig.add_subplot(111)
    plt.yticks([1.0,1.3,1.6,1.9,2.2,2.5],size=n)  #y轴坐标
    # plt.xticks([0,4,8,16,24,32,40,48,56,64],size=n)
    plt.xticks([0, 4, 8, 16, 24, 32, 40, 48, 56, 64], size=n)
    # plt.xlim(0,67)
    plt.xlim(2.4, 67)
    # plt.ylim(1.0,3.0)
    plt.ylim(1.0, 3.2)
    # plt.xlabel(r"$cores$")
    plt.xlabel(r"$processors$",size=n)
    # plt.xlabel(r"$(b)\ nonlinear-speadup\ processors$", size=n)
    plt.text(11, 0.45, r"$(b)\ nonlinear-speadup\ jobs$",size=n)
    # plt.text(30, 0.7, r'$(b)\ nonlinear$')
    x = [4, 8, 16, 24, 32, 40, 48, 56, 64]

    #条矩形图的位置
    # x_alp1=[4,8,16,24,32,40,48,56,64]
    # x_alp2 = [3, 7, 15, 23, 31, 39, 47, 55, 63]
    # x_ab = [5, 9, 17, 25, 33, 41, 49, 57, 65]
    # x_appr = [3, 7, 15, 23, 31, 39, 47, 55, 63]
    x_alp1 = [4, 8, 16, 24, 32, 40, 48, 56, 64]
    x_alp2 = [2.5, 6.5, 14.5, 22.5, 30.5, 38.5, 46.5, 54.5, 62.5]
    x_ab = [5.5, 9.5, 17.5, 25.5, 33.5, 41.5, 49.5, 57.5, 65.5]
    x_appr = [2.5, 6.5, 14.5, 22.5, 30.5, 38.5, 46.5, 54.5, 62.5]

    # 生成折线图
    plt.plot(x, gV.arr_avg[0],"+-.",color='g',linewidth=1,label='Impt-I')
    plt.plot(x, gV.arr_avg[1], "+--", color='red',linewidth=1,label='Impt-I*')
    plt.plot(x, gV.arr_avg[2], "+-", color='blue',linewidth=1,label='Impt-II')
    plt.plot(x, gV.arr_avg[3], "+:", color='y',linewidth=1,label='Impt-B')
    # plt.legend(loc='best', ncol=4)
    plt.legend(loc='best', ncol=2, fontsize=n)

    #生成矩形图
    m=1.2
    for k_1 in [0,1,2,3,4,5,6,7,8]:
        rect_alp1 = plt.Rectangle((x_alp1[k_1], gV.arr_a1p1_1_9[0][k_1]), m,
                                  gV.arr_a1p1_1_9[1][k_1] - gV.arr_a1p1_1_9[0][k_1],edgecolor="g",fill=False)
        rect_alp2 = plt.Rectangle((x_alp2[k_1], gV.arr_a1p2_1_9[0][k_1]), m,
                                  gV.arr_a1p2_1_9[1][k_1] - gV.arr_a1p2_1_9[0][k_1],edgecolor="red",fill=False)
        rect_ab = plt.Rectangle((x_ab[k_1], gV.arr_ab_1_9[0][k_1]), m,
                                  gV.arr_ab_1_9[1][k_1] - gV.arr_ab_1_9[0][k_1],edgecolor="blue",fill=False)
        rect_appr = plt.Rectangle((x_appr[k_1], gV.arr_appr_1_9[0][k_1]), m,
                                  gV.arr_appr_1_9[1][k_1] - gV.arr_appr_1_9[0][k_1],edgecolor="y",fill=False)
        ax.add_patch(rect_alp1)
        ax.add_patch(rect_alp2)
        ax.add_patch(rect_ab)
        ax.add_patch(rect_appr)
    plt.savefig("./figure/Fig.5(b).png")
    plt.show()