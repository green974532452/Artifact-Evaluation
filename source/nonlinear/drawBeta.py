import matplotlib.pyplot as plt
import globalVarBeta as gV
n=20
def plot():
    fig = plt.figure()
    fig.subplots_adjust(top=0.99, bottom=0.22, left=0.09, right=0.93, wspace=0.43, hspace=0.5)
    ax = fig.add_subplot(111)
    plt.yticks([1.0,1.3,1.6,1.9,2.2,2.5],size=n)
    plt.xticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],size=n)
    plt.xlim(0.069,1.03)
    plt.ylim(1.0,3.2)
    # plt.xlabel(r"$(b)\ non-linear-speadup\ β$", size=n)
    plt.xlabel(r"$β$",size=n)
    plt.text(0.2, 0.42, r"$(b)\ nonlinear-speadup\ jobs$", size=n)
    # # plt.text(0.41,0.7, r'$(b)\ n=50,m=16$')
    # plt.text(0.2, 0.55, r'$(b)\ nonlinear,n=50,m=16$', size=n)
    x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

    #条矩形图的位置
    x_alp1=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    x_alp2 = [0.07,0.17,0.27,0.37,0.47,0.57,0.67,0.77,0.87,0.97]
    x_ab = [0.13,0.23,0.33,0.43,0.53,0.63,0.73,0.83,0.93,1.03]
    x_appr = [0.07,0.17,0.27,0.37,0.47,0.57,0.67,0.77,0.87,0.97]

    # 生成折线图
    plt.plot(x, gV.arr_avg[0],"+-.",color='g',linewidth=1,label='Impt-I')
    plt.plot(x, gV.arr_avg[1], "+--", color='red',linewidth=1,label='Impt-I*')
    plt.plot(x, gV.arr_avg[2], "+-", color='blue',linewidth=1,label='Impt-II')
    plt.plot(x, gV.arr_avg[3], "+:", color='y',linewidth=1,label='Impt-B')
    # plt.legend(loc='best', ncol=4)
    plt.legend(loc='best', ncol=2, fontsize=n)

    #生成矩形图
    m=0.02
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
    plt.savefig("./figure/Fig.6(b).png")
    plt.show()