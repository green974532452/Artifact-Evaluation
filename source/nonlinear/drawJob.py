import matplotlib.pyplot as plt
import globalVarJob as gV

n=20
def plot():
    fig = plt.figure()
    fig.subplots_adjust(top=0.99, bottom=0.22, left=0.09, right=0.93, wspace=0.43, hspace=0.5)
    ax = fig.add_subplot(111)
    plt.yticks([1.0,1.3,1.6,1.9,2.2,2.5],size=n)
    plt.xticks([0,10,20,30,40,50,60,70,80,90,100],size=n)
    plt.xlim(6.7,106)
    plt.ylim(1.0,3.2)
    # plt.xlabel(r"$(b)\ non-linear-speadup\ jobs$", size=n)
    plt.xlabel(r"$jobs$",size=n)
    plt.text(20, 0.42, r"$(b)\ nonlinear-speadup\ jobs$", size=n)
    # # plt.text(40,0.7, r'$(b)\ m=16,β=0.5$')
    # plt.text(20, 0.55, r'$(b)\ nonlinear,m=16,β=0.5$', size=n)
    x = [10,20,30,40,50,60,70,80,90,100]

    #条矩形图的位置
    x_alp1=[10,20,30,40,50,60,70,80,90,100]
    x_alp2 = [ 7, 17, 27, 37, 47, 57, 67, 77, 87, 97]
    x_ab = [13,23,33,43,53,63,73,83,93,103]
    x_appr = [7, 17, 27, 37, 47, 57, 67, 77, 87, 97]

    # 生成折线图
    plt.plot(x, gV.arr_avg[0],"+-.",color='g',linewidth=1,label='Impt-I')
    plt.plot(x, gV.arr_avg[1], "+--", color='red',linewidth=1,label='Impt-I*')
    plt.plot(x, gV.arr_avg[2], "+-", color='blue',linewidth=1,label='Impt-II')
    plt.plot(x, gV.arr_avg[3], "+:", color='y',linewidth=1,label='Impt-B')
    # plt.legend(loc='best', ncol=4)
    plt.legend(loc='best', ncol=2, fontsize=n)

    #生成矩形图
    m=2
    for k_1 in [0,1,2,3,4,5,6,7,8,9]:
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
    plt.savefig("./figure/Fig.4(b).png")
    plt.show()