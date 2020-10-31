import cv2
import numpy as np
import os


if __name__ == '__main__':
    Low_lim = np.array([100,100,0],np.uint8)
    Up_lim = np.array([140,255,255],np.uint8)
    Kernel = np.ones((7, 7), np.uint8)

    Camera = cv2.VideoCapture(0)
    #ret = True
    while (True):
        _, Image = Camera.read()
        Image = cv2.flip(Image, 1)
        Image_hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)

        Mask = cv2.inRange(Image_hsv, Low_lim, Up_lim)
        Mask = cv2.erode(Mask, Kernel, iterations=2)
        Mask = cv2.dilate(Mask, Kernel, iterations=2)

        Mix = cv2.bitwise_and(Image, Image, mask=Mask)
        contours, _ = cv2.findContours(Mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for idx, i in enumerate(contours):
            color = (0, 255, 255)
            cv2.drawContours(Image, contours, idx, color, 1)

        #_, Ibw_otsu = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow("Image", Image)
        cv2.waitKey(1)


    # path = r'C:\Users\juanp\Downloads\St.png'
    # Image = cv2.imread(path)
    # Image_gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    # #Image = cv2.bitwise_not(Image)
    # _, Image_T = cv2.threshold(Image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # contours, _ = cv2.findContours(Image_T, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #
    # for idx, i in enumerate(contours):
    #     color = (100, 255, 255)
    #     cv2.drawContours(Image_T, contours, 0, color, 100)
    #
    # cv2.imshow("Image", Image_T)
    # cv2.waitKey(0)