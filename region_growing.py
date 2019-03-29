# -*- coding:utf-8 -*-
import cv2
import numpy as np
import random

'''
可调参值：起始种子位置和阈值T
'''

# 二维坐标系
class Point(object):
    def __init__(self , x , y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y

# 计算两个点间的欧式距离
def get_dist(seed_location1,seed_location2):
    l1 = im[seed_location1.x , seed_location1.y]
    l2 = im[seed_location2.x , seed_location2.y]
    count = np.sqrt(np.sum(np.square(l1 - l2)))
    print(count)
    return count


if __name__ == '__main__':
    name_list = ['111.png','222.jpg','333.jpg','444.jpg']
    for name in name_list:

        # import Image
        im = cv2.imread(name)
        im_shape = im.shape
        height = im_shape[0]
        width = im_shape[1]
        print('the shape of image :', im_shape)

        # 八邻域图
        connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1), Point(-1, 0)]

        # 标记，判断种子是否已经生长
        img_mark = np.zeros([height , width])

        # 建立空的图像数组,作为待填写，先全黑
        img_new = im.copy()

        for i in range(height):
            for j in range(width):
                img_new[i, j][0] = 0
                img_new[i, j][1] = 0
                img_new[i, j][2] = 0


        seed_list = []
        # 固定种子点
        location = np.where(im==im.max())
        #print(location[0][0],location[1][0])
        for i in range(10):
            seed_list.append(Point(10*i, 10*i))

        T = 7  # 阈值 越大生长的点越多
        marked = 1 # used标记

        while (len(seed_list) > 0):
            # 将已生长的点从一个类的种子点列表中删除
            seed_tmp = seed_list[0]
            seed_list.pop(0)

            img_mark[seed_tmp.x, seed_tmp.y] = marked

            # 遍历8邻域
            for i in range(8):
                tmpX = seed_tmp.x + connects[i].x
                tmpY = seed_tmp.y + connects[i].y

                # 越界
                if (tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= width):
                    continue

                dist = get_dist(seed_tmp, Point(tmpX, tmpY))

                #在种子集合中满足条件的点进行生长
                if (dist < T and img_mark[tmpX, tmpY] == 0):
                    img_new[tmpX, tmpY] = im[tmpX, tmpY]
                    img_mark[tmpX, tmpY] = marked
                    seed_list.append(Point(tmpX, tmpY))


        # 输出图像 esc退出
        new_name = name[:-4] + '_treated.jpg'
        while True:
            cv2.imshow('OUTIMAGE' , img_new)
            c = cv2.waitKey(30) & 0xff
            if c == 27:
                cv2.imwrite(new_name, img_new)
                break