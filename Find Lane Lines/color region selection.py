import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

'''导入图片'''
image = mpimg.imread('test.jpg')

'''获取图片大小，复制图片'''
ysize = image.shape[0]
xsize = image.shape[1]
color_select = np.copy(image)
line_image = np.copy(image)
# print('图片高度',  ysize, '图片长度', xsize)

'''选择三原色范围 0-255'''
red_threshold = 200
green_threshold = 200
blue_threshold = 200

rgb_threshold = [red_threshold, green_threshold, blue_threshold]

'''设定选择区域'''
# 三角形，三个顶点坐标
left_bottom = [0, 500]
right_bottom = [1000,660]
apex = [600, 400]

'''根据三个顶点坐标得到边（y = Ax + B）, np.polyfit返回拟合的系数[A, B]'''
fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

'''选择小于该设定值的像素点,将符合条件的设置为True'''
color_threshold = (image[:, :, 0]) < rgb_threshold[0] \
            | (image[:, :, 1] < rgb_threshold[1]) \
            | (image[:, :, 2] < rgb_threshold[2])

'''选择设定区域，三角形内部区域'''
# meshigrid（x，y）的作用是产生一个以向量x为行，向量y为列的矩阵
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
'''注意图片的(0,0)坐标在左上，不是常规的左下'''
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) & \
                    (YY > (XX*fit_right[0] + fit_right[1])) & \
                    (YY < (XX*fit_bottom[0] + fit_bottom[1]))

color_select[color_threshold | ~region_thresholds] = [0, 0, 0]
line_image[~color_threshold & region_thresholds] = [255, 0, 0]

'''显示结果'''
plt.imshow(image)
'''画出选定区域'''
x = [left_bottom[0], right_bottom[0], apex[0], left_bottom[0]]
y = [left_bottom[1], right_bottom[1], apex[1], left_bottom[1]]
plt.plot(x, y, 'b--', lw=4)
plt.imshow(color_select)
plt.show()
plt.imshow(line_image)
plt.show()