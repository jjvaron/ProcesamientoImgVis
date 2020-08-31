# Procesamiento de imagenes y visión
# Profesores: Ing. Julián Quiroga S e Ing. Nestor Ribero
# Taller 2
# Realizado por Jelitza Varón Heredia


import numpy as np
import cv2
import random
import math
import os


# im = np.zeros((512, 512, 3), np.uint8)
#
#
# pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
# pts = pts.reshape((-1,1,2))
# cv2.polylines(im,[pts],True,(0,255,255))
# cv2.imshow("test", im)
# cv2.waitKey(0)

def askUserImg():
    UserPath = 'D:/Python/Taller1Procesamiento'  # input('Enter the path of the image: ')
    # read the name of image from user
    UserNameImg = 'test.png'  # input('Enter the name of the image with te extention: ')
    # Set path of the file
    UserPathFile = os.path.join(UserPath, UserNameImg)
    imgRead = cv2.imread(UserPathFile)

    return imgRead


def identifyShape(idx):
    # for idx in contours:
    approxContours = cv2.approxPolyDP(idx, 0.01 * cv2.arcLength(idx, True), True)
    # cv2.drawContours(imageDraw, [approxContours], 0, (0), 2)
    if len(approxContours) == 3:
        shapeIdentify = "Triangle"

    elif len(approxContours) == 4:
        (x, y, w, h) = cv2.boundingRect(approxContours)
        ar = w / float(h)
        # A square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shapeIdentify = "square" if 0.95 <= ar <= 1.05 else "rectangle"

    elif len(approxContours) == 5:
        shapeIdentify = "pentagon"

    elif len(approxContours) == 6:
        shapeIdentify = "hexagon"

    elif len(approxContours) == 8:
        shapeIdentify = "octagon"

    elif len(approxContours) == 10:
        shapeIdentify = "star"

    else:
        shapeIdentify = "circle"
    return shapeIdentify


userImg = askUserImg()
# cv2.imshow("test", userImg)
# cv2.waitKey(0)

randNum = random.randint(0, 4)


# Def Class
class imageShape:
    # Def construct
    def __init__(self, width, height, shapeType):  # ,identifyImg
        self.shape = None  # shape generated
        self.width = width
        self.height = height
        self.shapeType = shapeType

    def generateShape(self):
        # generate canvas (black image)

        self.shapeType = 1  #randNum
        img = np.zeros((self.height, self.width, 3), np.uint8)  # [cols, rows] [height, width]
        # display canvas
        # cv2.imshow("test", img)
        # cv2.waitKey(0)

        minValue = np.amin([self.width, self.height])

        if self.shapeType == 0:
            # Triangle
            a = int(minValue / 2)  # side of triangle
            c = (math.sqrt(math.pow(a, 2) + math.pow((a / 2), 2)) / 2)  # height/2  of triangle

            x1 = (self.width / 2)
            y1 = ((self.height / 2) - c)

            # y = mx + b
            # m = y1 / x1
            # b = y1 - (m * x1)
            #
            # y2 = y1 + c
            # x2 = ((y2 - b) / m)
            #
            # x3 = x2 + a
            # y3 = y2

            x2 = x1 + (a / 2)  # (self.width / 2) + c# (self.width / 2) + (a / 2)
            y2 = (self.height / 2) + c  # (self.height / 2) + c

            x3 = x2 - a  # (self.width / 2) - (a / 2)
            y3 = y2  # (self.height / 2) + c

            # d = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

            vertices = np.array([[x1, y1], [x2, y2], [x3, y3]], np.int32)
            # vertices = vertices.reshape((3, 1, 2))
            self.Shape = cv2.polylines(img, [vertices], True, (255, 255, 0), 2)
            cv2.fillPoly(img, [vertices], (255, 255, 0))

            # cv2.imwrite('D:/Python/Taller1Procesamiento/test.jpg', randomShape)

            # vertices2 = np.array([[self.width/2, 0], [self.width/2, self.height],[0,self.height/2],[self.width,
            # self.height/2]], np.int32) cv2.polylines(img, [vertices2], False, (0, 255, 0), 2)

        if self.shapeType == 1:
            # Square
            a = int(minValue / 2)  # side of square
            d = math.sqrt(math.pow(a, 2) + math.pow(a, 2))  # diagonal of square

            x1 = (self.width / 2)
            y1 = ((self.height / 2) - (d / 2))

            x2 = (self.width / 2) + (d / 2)
            y2 = (self.height / 2)

            x3 = (self.width / 2)
            y3 = (self.height / 2) + (d / 2)

            x4 = (self.width / 2) - (d / 2)
            y4 = (self.height / 2)

            vertices = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)

            self.Shape = cv2.polylines(img, [vertices], True, (255, 255, 0), 2)
            shape = cv2.polylines(img, [vertices], True, (255, 255, 0), 2)
            cv2.fillPoly(img, [vertices], (255, 255, 0))

            # cv2.imwrite('D:/Python/Taller1Procesamiento/square.png', shape)

        if self.shapeType == 2:
            # Rectangle
            x1 = int(self.width / 4)
            y1 = int(self.height / 4)

            x2 = int((self.width * 3) / 4)
            y2 = int((self.height * 3) / 4)

            self.Shape = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), -1)

        if self.shapeType == 3:
            # Circle
            r = int(minValue / 4)

            x1 = int(self.width / 2)
            y1 = int(self.height / 2)

            self.Shape = cv2.circle(img, (x1, y1), r, (255, 255, 0), -1)
        if self.shapeType == 4:
            # display canvas
            self.Shape = img

        return self.shape

    def showShape(self):
        # display random shape for 5 seconds

        cv2.imshow("random shape", self.generateShape())
        cv2.waitKey(0)

    def getShape(self):
        global shapeName

        if self.shapeType == 0:
            shapeName = 'Triangle'

        if self.shapeType == 1:
            shapeName = 'Square'

        if self.shapeType == 2:
            shapeName = 'Rectangle'

        if self.shapeType == 3:
            shapeName = 'Circle'

        if self.shapeType == 4:
            shapeName = 'None'
        return shapeName

    def whatShape(self, imageUser):
        # shape detection using contours
        shapeIdentify = ""
        # cv2.imshow("test inside", imageUser)
        # cv2.waitKey(0)

        # image preparation
        imageGray = cv2.cvtColor(imageUser, cv2.COLOR_BGR2GRAY)
        ret, ImageBW = cv2.threshold(imageGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.imshow("test BW", ImageBW)
        # cv2.waitKey(0)

        # floodfill
        height, width = imageUser.shape[:2]
        mask = np.zeros((height + 2, width + 2), np.uint8)
        imageFloodfill = ImageBW.copy()
        cv2.floodFill(imageFloodfill, mask, (0, 0), 255)
        imageFloodfillInv = cv2.bitwise_not(imageFloodfill)
        # cv2.imshow("test floodfill Inv", imageFloodfillInv)
        # cv2.waitKey(0)

        # image mask
        imageFindshape = cv2.bitwise_or(ImageBW, imageFloodfillInv)
        # cv2.imshow("test mask", imageFindshape)
        # cv2.waitKey(0)

        # countours
        # imageDraw = imageUser.copy()
        contours, hierarchy = cv2.findContours(imageFindshape, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contours:
            shapeIdentify = identifyShape(cont)

        return shapeIdentify


# saveImg = self.getShape()
# D:/Python/Taller1Procesamiento/img
# cv2.imwrite('data/dst/lena_opencv_red.jpg', saveImg)

test = imageShape(512, 412, randNum)
test.generateShape()
test.showShape()
print(test.getShape())
#print(test.whatShape(userImg))
