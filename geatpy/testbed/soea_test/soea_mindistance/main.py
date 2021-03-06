# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea  # import geatpy
import matplotlib.pyplot as plt
from MyProblem import MyProblem  # 导入自定义问题接口

if __name__ == '__main__':
    """================================实例化问题对象============================"""
    problem = MyProblem()  # 生成问题对象
    """==================================种群设置==============================="""
    Encoding = 'RI'  # 编码方式，采用排列编码
    NIND = 50  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """================================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 200  # 最大进化代数
    myAlgorithm.mutOper.Pm = 0.5  # 变异概率
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """===========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    population.save()  # 把最后一代种群的信息保存到文件中
    """===============================输出结果及绘图============================"""
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1])  # 记录最优种群个体是在哪一代
    best_ObjV = np.min(obj_trace[:, 1])
    print('最小代价为：%s' % (best_ObjV))
    print('最优的决策变量值为：')
    for i in range(var_trace.shape[1]):
        print(var_trace[best_gen, i])

    # print('最佳路线为：')
    # best_journey = np.hstack([0, var_trace[best_gen, :], 0])
    # for i in range(len(best_journey)):
    #     print(chr(int(best_journey[i]) + 65), end = ' ')

    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))

    # 绘图
    xy = var_trace[best_gen]
    problem.places = np.vstack((problem.places, xy))
    size = np.ones_like(problem.places[:, 0]) * 100
    size[9] = 200
    color = ['k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'r']
    plt.scatter(problem.places[:, 0].T, problem.places[:, 1].T, s=size, c=color)
    problem.places = np.delete(problem.places, 9, axis=0)
    # plt.text(0, 0, "Total cost of time and energy=%.5f" % best_ObjV, fontdict={'size': 20, 'color': 'red'})
    plt.text(0, 0, "The best position of UAV=(%.3f,%.3f)" % (var_trace[best_gen, 0],var_trace[best_gen, 1]), fontdict={'size': 20, 'color': 'red'})

    plt.xlim((0, 10))
    plt.ylim((0, 10))
    plt.grid(True)
    plt.xlabel('x坐标')
    plt.ylabel('y坐标')
    plt.show()
    plt.savefig('roadmap.svg', dpi=600, bbox_inches='tight')
