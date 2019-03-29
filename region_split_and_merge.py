

# Definition for a QuadTree node.
import cv2
import numpy as np

class Point(object):
    def __init__(self , x , y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Node:
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight, location):
        self.mean_val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.location = location


class Solution:
    def __init__(self, image, total_mean, total_max, total_min):
        self.image = image
        self.total_mean = total_mean
        self.total_max = total_max
        self.total_min = total_min

    def construct(self, picture, location):

        root = Node(None, False, None, None, None, None, location)

        if picture.shape[0] == 1:
            root.isLeaf = True
            root.mean_val = picture.mean()
            self.color(location, root.mean_val)

        elif self.stop_split(picture):  # 判断是否继续分割
            root.isLeaf = True
            root.mean_val = picture.mean()
            self.color(location, root.mean_val)

        else:  # 继续分割
            height = picture.shape[0]
            width = picture.shape[1]
            halfheight = height // 2
            halfwidth = width // 2# 使用 // 表示整除
            root.isLeaf = False # 如果网格中有值不相等，这个节点就不是叶子节点
            #print(height, width, halfheight, halfwidth)

            # 自回归
            # base为子图基准量
            base_start_x = location[0].x
            base_start_y = location[0].y
            base_end_x = location[1].x
            base_end_y = location[1].y

            root.topLeft = self.construct(picture[:halfheight, :halfwidth], [Point(base_start_x, base_start_y), Point(base_start_x + halfheight, base_start_y + halfwidth)])
            root.topRight = self.construct(picture[:halfheight, halfwidth:], [Point(base_start_x, base_start_y + halfwidth), Point(base_start_x + halfheight, base_end_y)])
            root.bottomLeft = self.construct(picture[halfheight:, :halfwidth], [Point(base_start_x + halfheight, base_start_y), Point(base_end_x, base_start_y + halfwidth)])
            root.bottomRight = self.construct(picture[halfheight:, halfwidth:], [Point(base_start_x + halfheight, base_start_y + halfwidth), Point(base_end_x, base_end_y)])
        return root

    def stop_split(self, iim):
        if iim.max() - iim.min() <= 10:
            return True
        else: return False

    def color(self, location, mean_val):
        first_point = location[0]
        second_point = location[1]
        print(first_point.x, first_point.y, ' to ', second_point.x, second_point.y)
        if mean_val <= self.total_mean:
            for i in range(first_point.x, second_point.x):
                for j in range(first_point.y, second_point.y):
                    self.image[i][j] = self.total_max
        else:
            for i in range(first_point.x, second_point.x):
                for j in range(first_point.y, second_point.y):
                    self.image[i][j] = self.total_min

if __name__ == '__main__':
    name_list = ['111.png', '222.jpg', '333.jpg', '444.jpg']
    for name in name_list:

        # import Image
        im = cv2.imread(name, 0)
        im_shape = im.shape
        height = im_shape[0]
        width = im_shape[1]
        print('the shape of image :', im_shape)
        new_name = name[:-4] + '_treated.jpg'

        init_locate = [Point(0, 0), Point(height, width)] # 对角线两点定位矩形
        # zpd为无意义变量
        zpd = Solution(im, im.mean(), im.max(), im.min())

        zpd.construct(im, init_locate)

        while True:
            cv2.imshow('OUTIMAGE' , zpd.image)
            c = cv2.waitKey(30) & 0xff
            if c == 27:
                cv2.imwrite(new_name, zpd.image)
                break
