from clase_canvas_1 import *
import cv2
import numpy as np

if __name__ == '__main__':
    # 0 means primary camera .
    Camera = cv2.VideoCapture(0)
    Camera.set(3, 1280)
    Camera.set(4, 720)
    # initialize blank canvas
    lienzo = clase_canvas_1()

    while True:
        # read new frame
        ret , Image = Camera.read()
        # flip horizontally
        Image = cv2.flip(Image, 1)

        if lienzo.canvas is None:
            lienzo.canvas = np.zeros_like(Image)  # initialize a black canvas

        mask = lienzo.CreateMask(Image)  # create mask
        contours = lienzo.ContourDetect(mask)  #detect Contours
        lienzo.drawLine(Image, contours) #Draw line

        Image = lienzo.insert_options(Image)
        lienzo.display(Image)
