import numpy
from pylab import *
import copy
import random

'''构造20*20的栅格地图，10表示可通行点，0表示障碍物'''
map_grid = numpy.full((20, 20), int(10))
# map_grid[3, 3:8] = 0
# map_grid[3:10, 7] = 0
# map_grid[10, 3:8] = 0
# map_grid[17, 13:17] = 0
# map_grid[10:17, 13] = 0
map_grid[10, 13:17] = 0


class RRT(object):
    def __init__(self, start, goal, step, constant):
        self.start = start   #起始点
        self.goal = goal     #目标点
        self.step = step     #RRT生长最小单位长度
        self.constant = constant  #较小常数，当目标点与新生成节点距离小于该值，搜索成功
        self.inpoint = numpy.array([[], [], [], [], []])  #点表
        self.best_path_array = numpy.array([[], []])   #路径回溯

    def point_rand(self):
        while True:
            x = random.randint(0, 19)
            y = random.randint(0, 19)
            if map_grid[int(x), int(y)] == 10:
                point_r = numpy.array([x, y])
                break
        return point_r

    def Dis(self, point1, point2):
        L2 = (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
        L = numpy.sqrt(L2)
        return L

    def point_change(self, point1, point2):
        if point1[0] < point2[0]:
            x = 1
        elif point1[0] == point2[0]:
            x = 0
        else:
            x = -1
        if point1[1] < point2[1]:
            y = 1
        elif point1[1] == point2[1]:
            y = 0
        else:
            y = -1
        return x, y

    def point_new(self):
        point_r = self.point_rand()
        for i in range(self.inpoint.shape[1]):
            L = self.Dis((self.inpoint[0, i], self.inpoint[1, i]), point_r)
            self.inpoint[4, i] = L
        self.inpoint = self.inpoint.T[numpy.lexsort(self.inpoint)].T
        min_point = self.inpoint[:, 0]
        x_c, y_c = self.point_change((min_point[0], min_point[1]), point_r)
        x = min_point[0] + x_c * self.step
        y = min_point[1] + y_c * self.step
        if x < 0 or x > 19 or y < 0 or y > 19 or map_grid[int(x), int(y)] == 0:
            return 10
        else:
            n = self.Dis((x, y), self.goal)
            point_n = [x, y, min_point[0], min_point[1], n]
            self.inpoint = numpy.c_[self.inpoint, point_n]
            return n

    def path_back(self):
        best_path = self.goal
        self.best_path_array = numpy.array([[self.goal[0]], [self.goal[1]]])
        j = 0
        while j <= self.inpoint.shape[1]:
            for i in range(self.inpoint.shape[1]):
                if best_path[0] == self.inpoint[0][i] and best_path[1] == self.inpoint[1][i]:
                    x = self.inpoint[2][i]
                    y = self.inpoint[3][i]
                    best_path = [x, y]
                    self.best_path_array = numpy.c_[self.best_path_array, best_path]
                    break  # 如果已经找到，退出本轮循环，减少耗时
                else:
                    continue
            j += 1

    def main(self):
        best = self.start
        init_inpoint = [best[0], best[1], best[0], best[1], 0]
        self.inpoint = numpy.column_stack((self.inpoint, init_inpoint))
        ite = 1
        while ite <= 2000:
            n = self.point_new()
            if n <= self.constant:
                print('第%d次找到目标' % ite)
                break
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


    def draw_path_inpoint(self, a):
        map_closed = copy.deepcopy(map_grid)
        for i in range(a.inpoint.shape[1]):
            x = a.inpoint[:, i]
            map_closed[int(x[0]), int(x[1])] = 3

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
        ax3 = plt.subplot(222)
        ax4 = plt.subplot(223)

        plt.sca(ax1)
        self.draw_init_map()

        plt.sca(ax3)
        self.draw_path_inpoint(a)
        plt.sca(ax4)
        self.draw_direction_point(a)
        plt.savefig('./RRT.jpg')
        plt.show(ax4)


'''输入起始点（5， 4）和终点（14， 14）'''
if __name__ == '__main__':
    a1 = RRT((4, 4), (14, 14), 1, 0)
    a1.main()
    a1.path_back()
    m1 = MAP((4, 4), (14, 14))
    m1.draw_four_axes(a1)

