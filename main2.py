import cv2
import numpy as np
import os
import keyboard

def CreateMask(Image):
    hsv_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)  # convert from BGR to HSV color range
    lower_range = np.array([100, 100, 0], np.uint8)  # HSV lower range
    upper_range = np.array([140, 255, 255], np.uint8)  # HSV upper range
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.inRange(hsv_Image, lower_range, upper_range)  # Create binary mask
    # Perform morphological operations to get rid of the noise
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    return mask


def ContourDetect(mask):
    # Find Contours based on the mask created.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def drawLine(Image, contours, canvas, x1, y1):
    # if contour area is not none and is greater than noiseth draw the line
    noiseth = 2000
    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noiseth:
        c = max(contours, key=cv2.contourArea)

        # x2, y2, w, h = cv2.boundingRect(c)
        # # Draw that bounding box
        # cv2.rectangle(Image, (x2, y2), (x2 + w, y2 + h), (0, 25, 255), 2)

        M = cv2.moments(c)
        x2, y2 = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # cv2.circle(Image, (int(x), int(y)), int(radius), (0, 255, 255), 2)

        # this will we true only for the first time marker is detected
        if x1 == 0 and y1 == 0:
            x1, y1 = x2, y2
        else:
            # Draw the line on the canvas
            canvas = cv2.line(canvas, (x1, y1), (x2, y2), [255, 255, 255], 2)
        # New point becomes the previous point
        x1, y1 = x2, y2
    else:
        # If there were no contours detected then make x1,y1 = 0 (reset)
        x1, y1 = 0, 0
    return Image, canvas, x1, y1


def display(Image, canvas):
    # Merge the canvas and the frame.
    Image = cv2.add(Image, canvas)
    cv2.imshow('Image', Image)
    cv2.waitKey(1)


def Aproxpoll(canvas,canvas_):
    resta = cv2.subtract(canvas, canvas_)
    image_gray = cv2.cvtColor(resta, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.erode(mask, kernel, iterations=2)
    contours = ContourDetect(mask)

    for i in contours:
        epsilon = 0.04 * cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, epsilon, closed=True)

        canvas = np.zeros_like(Image)
        canvas = cv2.polylines(canvas, [approx], True, (0, 255, 255), 2)

        canvas_ = cv2.add(canvas_, canvas)
        canvas = canvas_.copy()
    return canvas, canvas_


if __name__ == '__main__':
    # 0 means primary camera .
    Camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    Camera.set(3, 1280)
    Camera.set(4, 720)
    # initialize blank canvas
    canvas = None
    # initial position on pen
    x1, y1 = 0, 0
    while True:
        # read new frame
        ret, Image = Camera.read()
        # flip horizontally
        Image = cv2.flip(Image, 1)

        if canvas is None:
            canvas = np.zeros_like(Image)  # initialize a black canvas
            canvas_ = canvas.copy()

        mask = CreateMask(Image)  # create mask
        contours = ContourDetect(mask)  # detect Contours
        Image, canvas, x1, y1 = drawLine(Image, contours, canvas, x1, y1)  # Draw line
        display(Image, canvas)




        #cv2.drawContours(Image, contours, -1, (0, 255, 255), 1)

        if keyboard.is_pressed('p'):  # if key 'q' is pressed
            canvas, canvas_ = Aproxpoll(canvas, canvas_)

        if keyboard.is_pressed('c'):  # if key 'q' is pressed
            canvas = np.zeros_like(Image)
            canvas_ = canvas.copy()




