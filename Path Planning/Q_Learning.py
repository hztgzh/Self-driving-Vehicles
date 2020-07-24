import numpy as np
from pylab import *
import copy

map_grid = np.full((20, 20), 10)
map_grid[4, 4] = 0
map_grid[14, 14] = 7

Q = np.zeros((20, 20), dtype=float, order='C')
Q[14, 14] = 100 #终点
Q[4, 4] = -1 #起始点

for episode in range(300):
    Q_old = copy.deepcopy(Q)
    for i in range(Q.shape[1]):
        for j in range(Q.shape[1]):
            a1 = min(j + 1, 19)
            a2 = min(i + 1, 19)
            a3 = max(j -1, 0)
            a4 = max(i - 1, 0)
            if  Q[i, j] == 100:
                pass
            else:
                Q[i, j] = Q[i, j] + 0.9 * (-1 + max(Q_old[i, a1],Q_old[a2, j],Q_old[i, a3],Q_old[a4, j]) - Q_old[i, j])

best_path = [4, 4]
best_path_array = np.array([[best_path[0]], [best_path[1]]])

for i in range(500):
    if Q[best_path[0], best_path[1]] != 100:
        x = best_path[0]
        y = best_path[1]
        a1 = min(best_path[1] + 1, 19)
        a2 = min(best_path[0] + 1, 19)
        a3 = max(best_path[1] - 1, 0)
        a4 = max(best_path[0] - 1, 0)
        Qmax = Q[best_path[0], best_path[1]]
        if Q[best_path[0], a1] > Qmax:
            Qmax = Q[best_path[0], a1]
            x = best_path[0]
            y = a1

        if Q[a2, best_path[1]] > Qmax:
            Qmax = Q[a2, best_path[1]]
            x = a2
            y = best_path[1]

        if Q[best_path[0], a3] > Qmax:
            Qmax = Q[best_path[0], a3]
            x = best_path[0]
            y = a3

        if Q[a4, best_path[1]] > Qmax:
            Qmax = Q[a4, best_path[1]]
            x = a4
            y = best_path[1]

        best_path = [x, y]
        best_path_array = np.c_[best_path_array, best_path]
    else:
        break


map_direction = copy.deepcopy(map_grid)
for i in range(best_path_array.shape[1]):
    x = best_path_array[:, i]
    map_direction[int(x[0]), int(x[1])] = 6
    map_direction[4, 4] = 0
    map_direction[14, 14] = 0
plt.imshow(map_direction, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
# plt.colorbar()
xlim(-1, 20)  # 设置x轴范围
ylim(-1, 20)  # 设置y轴范围
my_x_ticks = np.arange(0, 20, 1)
my_y_ticks = np.arange(0, 20, 1)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.show()

