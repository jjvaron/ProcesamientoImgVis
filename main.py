# Procesamiento de imagenes y visión - Profesor: Ing. Julián Quiroga S
# Taller 1
# Realizado por Jelitza Varón Heredia

import cv2
import os

# import numpy as np


# read path of image from user
UserPath = input('Enter the path of the image: ')  # 'D:/Python/Taller1Procesamiento'
# read the name of image from user
UserNameImg = input('Enter the name of the image with te extention: ')  # 'lena.png'
# Set path of the file
UserPathFile = os.path.join(UserPath, UserNameImg)


# Def Class
class colorImage:
    # Def construct
    def __init__(self):
        # read the image
        self.img = cv2.imread(UserPathFile)
        # display image
        cv2.imshow('Image', self.img)
        print('A continuación usted va a visualizar la imagen', UserNameImg)
        print('Presione una tecla para cerrar la imagen ')
        cv2.waitKey(0)
        # distroy image window
        cv2.destroyAllWindows()

    def displayProperties(self):
        # read the image
        self.img = cv2.imread(UserPathFile)
        # set image dimensions
        Dimensions = self.img.shape

        Height = self.img.shape[0]
        Width = self.img.shape[1]
        Channels = self.img.shape[2]
        # print image dimensions
        print('Image Dimension   : ', Dimensions)
        print('Image Height      : ', Height)
        print('Image Width       : ', Width)
        print('Num of Channel    : ', Channels)
        # return 'end of displayProperties'

    def makeGray(self):
        # read the image
        self.img = cv2.imread(UserPathFile, 0)  # ( ImgCV, cv2.IMREAD_GRAYSCALE)
        # display image
        cv2.imshow('Image gray scale', self.img)
        cv2.waitKey(0)
        print('A continuación usted va a visualizar la imagen', UserNameImg)
        print('Presione una tecla para cerrar la imagen ')
        # distroy image window
        cv2.destroyAllWindows()
        # return 'end of makeGray'

    def colorizeRGB(self, Channel):
        # read the image
        self.img = cv2.imread(UserPathFile)  # self.ImgCV = cv2.cvtColor(ImgCV, cv2.COLOR_BGR2RGB)
        # make a copy for each channel
        redChannel = self.img.copy()
        greenChannel = self.img.copy()
        blueChannel = self.img.copy()
        # set green and blue channels to 0
        redChannel[:, :, 0] = 0
        redChannel[:, :, 1] = 0
        # set blue and red channels to 0
        greenChannel[:, :, 0] = 0
        greenChannel[:, :, 2] = 0
        # set green and red channels to 0
        blueChannel[:, :, 1] = 0
        blueChannel[:, :, 2] = 0

        # display image acording to the channel selected by the user
        if Channel == 'Red':
            cv2.imshow('Image ColorizeRGB', redChannel)
        if Channel == 'Green':
            cv2.imshow('Image ColorizeRGB', greenChannel)
        if Channel == 'Blue':
            cv2.imshow('Image ColorizeRGB', blueChannel)

        cv2.waitKey(0)
        # distroy image window
        cv2.destroyAllWindows()
        #return 'end of colorizeRGB'

    def makeHue(self):
        # convert space of color from BGR to HVS
        self.img = cv2.imread(UserPathFile, cv2.COLOR_BGR2HSV)
        # set th S and V layer to 255
        self.img[:, :, 1] = 255
        self.img[:, :, 2] = 255

        # convert space of color from HVS to RGB
        backtoRGB = cv2.cvtColor(self.img, cv2.COLOR_HSV2RGB)
        # display image
        cv2.imshow("HSV to RGB with Hue", backtoRGB)
        cv2.waitKey(0)
        # distroy image window
        cv2.destroyAllWindows()


# test
# Prueba1 is an object of colorImage class
Prueba1 = colorImage()
# display image in gray scale
Prueba1.makeGray()
# display image properties
Prueba1.displayProperties()
# display image with one chanel (R, G or B)
Prueba1.colorizeRGB('Red')
# display image with Hue
Prueba1.makeHue()
