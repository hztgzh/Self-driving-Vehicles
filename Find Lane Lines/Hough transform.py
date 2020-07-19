import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

'''边缘检测图片'''
image = mpimg.imread('exit-ramp.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

'''寻找车道线'''
mask = np.zeros_like(edges)
ignore_mask_color = 255

imshape = image.shape
vertices = np.array([[(0,imshape[0]),(450, 290), (490, 290), (imshape[1],imshape[0])]], dtype=np.int32)
cv2.fillPoly(mask, vertices, ignore_mask_color)
masked_edges = cv2.bitwise_and(edges, mask)

'''定义霍夫变换参数,创建一个与绘制的图像相同大小的空白'''
rho = 1  # 距离分辨率
theta = np.pi/180  # 角分辨率
threshold = 1     # 最小投票数
min_line_length = 5  # 组成一条直线的最小像素数
max_line_gap = 1    # 可连接的线段之间的最大间隙（以像素为单位）
line_image = np.copy(image)*0   # 创建一个空白图像

lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

'''在空白图像上绘制线，并将该直线合并到原图像'''
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

color_edges = np.dstack((edges, edges, edges))

lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)
plt.imshow(lines_edges)
plt.show()