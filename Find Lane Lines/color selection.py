import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

'''导入图片'''
image = mpimg.imread('test.jpg')

'''获取图片大小，复制图片'''
ysize = image.shape[0]
xsize = image.shape[1]
color_select = np.copy(image)
print('图片高度',  ysize, '图片长度', xsize)

'''选择三原色范围 0-255'''
red_threshold = 200
green_threshold = 200
blue_threshold = 200

rgb_threshold = [red_threshold, green_threshold, blue_threshold]

'''将小于该设定值的像素点设置成黑色'''
threshold = (image[:, :, 0]) < rgb_threshold[0] \
            | (image[:, :, 1] < rgb_threshold[1]) \
            | (image[:, :, 2] < rgb_threshold[2])
color_select[threshold] = [0, 0, 0]

'''显示结果'''
plt.imshow(color_select)
plt.show()
'''保存结果'''
# mpimg.imsave("test-after.png", color_select)