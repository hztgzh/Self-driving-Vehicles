import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

'''导入图片，获得灰白图片'''
image = mpimg.imread('exit-ramp.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

'''为高斯平滑定义一个内核大小,必须为奇数(3, 5, 7...)'''
kernel_size = 3
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

'''为Canny定义参数'''
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

'''显示结果'''
plt.imshow(edges, cmap='Greys_r')
plt.show()