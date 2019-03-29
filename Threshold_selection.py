import cv2
import numpy as np

# 二维坐标系
class Point(object):
    def __init__(self , x , y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y

if __name__ == '__main__':
    name_list = ['111.png','222.jpg','333.jpg','444.jpg']
    # 八邻域图
    connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1),
                Point(-1, 0)]

    for name in name_list:

        threshold_list = []

        img = cv2.imread(name, 0)
        height = img.shape[0]
        width = img.shape[1]

        img_ = img.copy()
        edges = cv2.Canny(img_, 125, 250)  # canny边缘检测

        for i in range(height):
            for j in range(width):
                for k in range(8):
                    if edges[i][j] == 0:
                        continue

                    tmpX = i + connects[k].x
                    tmpY = j + connects[k].y

                    # 越界
                    if (tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= width):
                        continue

                    else:threshold_list.append(img[tmpX][tmpY])

        threshold = np.mean(threshold_list)
        print(threshold)
        _, img_treated = cv2.threshold(img, int(threshold), 255, cv2.THRESH_BINARY)

        new_name = name[:-4] + '_treated.jpg'




        while True:

            #cv2.ShowImage("Image", image)

            cv2.imshow("hw3", img_treated)

            c = cv2.waitKey(30) & 0xff
            if c == 27:
                cv2.imwrite(new_name, img_treated)
                break
