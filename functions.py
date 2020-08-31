# Function file

import cv2
import os


# Function that returns the user's image
def askUserImg():
    UserPath = input('Enter the path of the image: ')
    # read the name of image from user
    UserNameImg = input('Enter the name of the image with the extension (png, jpg, etc): ')
    # Set path of the file
    UserPathFile = os.path.join(UserPath, UserNameImg)
    imgRead = cv2.imread(UserPathFile)

    return imgRead


# funtion that clasifies the user's image
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
