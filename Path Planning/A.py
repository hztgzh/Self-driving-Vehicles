import numpy
from pylab import *
import copy

'''构造20*20的栅格地图，10表示可通行点，0表示障碍物'''
map_grid = numpy.full((20, 20), int(10))
map_grid[3, 3:8] = 0
map_grid[3:10, 7] = 0
map_grid[10, 3:8] = 0
map_grid[17, 13:17] = 0
map_grid[10:17, 13] = 0
map_grid[10, 13:17] = 0


class AStar(object):
    def __init__(self, start, goal):
        self.start = start   #起始点
        self.goal = goal     #目标点
        self.open = numpy.array([[], [], [], [], [], []])  #open表
        self.closed = numpy.array([[], [], [], [], [], []])  #close表
        self.best_path_array = numpy.array([[], []])   #路径回溯

    '''h函数，使用欧式距离作为成本'''
    def h_value(self, son_p):
        h2 = (son_p[0] - self.goal[0]) ** 2 + (son_p[1] - self.goal[1]) ** 2
        h = numpy.sqrt(h2)
        return h

    '''g函数，使用累积欧式距离作为成本'''
    '''注意这里的距离为到起点距离，所以要加上父节点到起点距离'''
    def g_value(self, son_p, father_p):
        g2 = (father_p[0] - son_p[0]) ** 2 + (father_p[1] - son_p[1]) ** 2
        g = numpy.sqrt(g2) + father_p[4]
        return g

    '''f函数,f =  g + h'''
    def f_value(self, son_p, father_p):
        f = self.g_value(son_p, father_p) + self.h_value(son_p)
        return f

    '''描述父节点和子节点的变化，方便路径回溯'''
    def direction(self, father_p, son_p):
        x = son_p[0] - father_p[0]
        y = son_p[1] - father_p[1]
        return x, y

    '''判断拓展点m是否在open表或者closed表中，jud=1表示在表中'''
    def judge_location(self, m, list_co):
        jud = 0
        index = 0
        for i in range(list_co.shape[1]):
            if m[0] == list_co[0, i] and m[1] == list_co[1, i]:
                jud = jud + 1
                index = i
                break
            else:
                jud = jud
        return jud, index

    '''下一节点，从周围8个节点选取'''
    def child_point(self, father_p):
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if i == 0 and j == 0:
                    continue
                m = [father_p[0] + i, father_p[1] + j]
                '''剔除边界外和障碍物的点'''
                if m[0] < 0 or m[0] > 19 or m[1] < 0 or m[1] > 19 or map_grid[int(m[0]), int(m[1])] == 0:
                    continue
                record_g = self.g_value(m, father_p)
                record_f = self.f_value(m, father_p)
                x_direction, y_direction = self.direction(father_p, m)
                para = [m[0], m[1], x_direction, y_direction, record_g, record_f]
                a, index = self.judge_location(m, self.open)
                b, index2 = self.judge_location(m, self.closed)
                '''如果open表中存在，更新值,如果在close表中跳过，如果都不在加入open表'''
                if a == 1:
                    if record_f <= self.open[5][index]:
                        self.open[5][index] = record_f
                        self.open[4][index] = record_g
                        self.open[3][index] = y_direction
                        self.open[2][index] = x_direction
                    continue
                elif b == 1:
                    continue
                else:
                    self.open = numpy.c_[self.open, para]
    '''路径'''
    def path_back(self):
        best_path = self.goal
        self.best_path_array = numpy.array([[self.goal[0]], [self.goal[1]]])
        j = 0
        while j <= self.closed.shape[1]:
            for i in range(self.closed.shape[1]):
                if best_path[0] == self.closed[0][i] and best_path[1] == self.closed[1][i]:
                    x = self.closed[0][i] - self.closed[2][i]
                    y = self.closed[1][i] - self.closed[3][i]
                    best_path = [x, y]
                    self.best_path_array = numpy.c_[self.best_path_array, best_path]
                    break  # 如果已经找到，退出本轮循环，减少耗时
                else:
                    continue
            j += 1

    def main(self):
        best = self.start
        h0 = self.h_value(best)
        init_open = [best[0], best[1], 0, 0, 0, h0]
        self.open = numpy.column_stack((self.open, init_open))
        ite = 1
        while ite <= 1000:
            if self.open.shape[1] == 0:
                print('未找到')
                return
            self.open = self.open.T[numpy.lexsort(self.open)].T
            best = self.open[:, 0]
            print('检验第%s次当前点坐标*******************' % ite)
            print(best)
            self.closed = numpy.c_[self.closed, best]
            if best[0] == self.goal[0] and best[1] == self.goal[1]:  # 如果best是目标点，退出
                print('搜索成功！')
                return
            self.child_point(best)  # 生成子节点并判断数目
            print(self.open)
            self.open = numpy.delete(self.open, 0, axis=1)  # 删除open中最优点
            ite = ite + 1

class MAP(object):

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        map_grid[start] = 7
        map_grid[goal] = 5

    def draw_init_map(self):
        plt.imshow(map_grid, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        xlim(-1, 20)  # 设置x轴范围
        ylim(-1, 20)  # 设置y轴范围
        my_x_ticks = numpy.arange(0, 20, 1)
        my_y_ticks = numpy.arange(0, 20, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)

    def draw_path_open(self, a):
        map_open = copy.deepcopy(map_grid)
        for i in range(a.open.shape[1]):
            x = a.open[:, i]
            map_open[int(x[0]), int(x[1])] = 2
            plt.imshow(map_open, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
            xlim(-1, 20)  # 设置x轴范围
            ylim(-1, 20)  # 设置y轴范围
            my_x_ticks = numpy.arange(0, 20, 1)
            my_y_ticks = numpy.arange(0, 20, 1)
            plt.xticks(my_x_ticks)
            plt.yticks(my_y_ticks)
            plt.grid(True)

    def draw_path_closed(self, a):
        map_closed = copy.deepcopy(map_grid)
        for i in range(a.closed.shape[1]):
            x = a.closed[:, i]
            map_closed[int(x[0]), int(x[1])] = 6

        plt.imshow(map_closed, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        xlim(-1, 20)  # 设置x轴范围
        ylim(-1, 20)  # 设置y轴范围
        my_x_ticks = numpy.arange(0, 20, 1)
        my_y_ticks = numpy.arange(0, 20, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)

    def draw_direction_point(self, a):
        map_direction = copy.deepcopy(map_grid)
        for i in range(a.best_path_array.shape[1]):
            x = a.best_path_array[:, i]
            map_direction[int(x[0]), int(x[1])] = 6
        plt.imshow(map_direction, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        # plt.colorbar()
        xlim(-1, 20)  # 设置x轴范围
        ylim(-1, 20)  # 设置y轴范围
        my_x_ticks = numpy.arange(0, 20, 1)
        my_y_ticks = numpy.arange(0, 20, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)

    def draw_four_axes(self, a):
        plt.figure()
        ax1 = plt.subplot(221)
        ax2 = plt.subplot(222)
        ax3 = plt.subplot(223)
        ax4 = plt.subplot(224)

        plt.sca(ax1)
        self.draw_init_map()
        plt.sca(ax2)
        self.draw_path_open(a)
        plt.sca(ax3)
        self.draw_path_closed(a)
        plt.sca(ax4)
        self.draw_direction_point(a)
        plt.show(ax4)

'''输入起始点（5， 4）和终点（14， 14）'''
if __name__ == '__main__':
    a1 = AStar((5, 4), (14, 14))
    a1.main()
    a1.path_back()
    m1 = MAP((5, 4), (14, 14))
    m1.draw_four_axes(a1)
