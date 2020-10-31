import cv2
import numpy as np
import os
import copy


def CreateMask(Image):
    hsv_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV) #convert from BGR to HSV color range
    #lower_range = np.array([100,100,0],np.uint8)    #HSV lower range
    lower_range = np.array([20, 100, 100], np.uint8)  # HSV lower range
    #upper_range = np.array([140,255,255],np.uint8)  #HSV upper range
    upper_range = np.array([30, 255, 255], np.uint8)  # HSV upper range
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.inRange(hsv_Image, lower_range, upper_range) #Create binary mask
    # Perform morphological operations to get rid of the noise
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 2)
    return mask

def ContourDetect(mask):
    # Find Contours based on the mask created.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def drawLine(Image, contours,canvas,x1,y1, canvas_figure, bandera, color, tam):
    # if contour area is not none and is greater than noiseth draw the line
    noiseth = 2000
    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noiseth:
        c = max(contours, key=cv2.contourArea)

        # x2, y2, w, h = cv2.boundingRect(c)
        # # Draw that bounding box
        # cv2.rectangle(Image, (x2, y2), (x2 + w, y2 + h), (0, 25, 255), 2)

        M = cv2.moments(c)
        x2 , y2 = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #cv2.circle(Image, (int(x), int(y)), int(radius), (0, 255, 255), 2)


        if x2 < 180 and x2 > 40 and y2 > 1 and y < 80:
            canvas_figure = canvas.copy()
            bandera = 1

        elif x2 < 340 and x2 > 200 and y2 > 1 and y < 80:
            canvas_figure = canvas.copy()
            bandera = 2

        elif x2 < 500 and x2 > 360 and y2 > 1 and y < 80 and bandera != 0:
            canvas_subtract = np.zeros_like(canvas)
            rows, cols, dim = canvas.shape
            for k in range(dim):
                for i in range(rows):
                    for j in range(cols):
                        if canvas[i, j, k] != canvas_figure[i, j, k]:
                            canvas_subtract[i, j, k] = canvas[i, j, k]

            image_gray = cv2.cvtColor(canvas_subtract, cv2.COLOR_BGR2GRAY)
            # Otsu's global threshold
            ret, Ibw_otsu = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, hierarchy = cv2.findContours(image_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            for idx, cont in enumerate(contours):
                if bandera == 1:
                    x, y, width, height = cv2.boundingRect(contours[idx])
                    cv2.rectangle(canvas_figure, (x, y), (x + width, y + height), color, 2)
                else:
                    (x, y), radius = cv2.minEnclosingCircle(contours[idx])
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv2.circle(canvas_figure, center, radius, color, 2)

            canvas = canvas_figure.copy()
            bandera = 0



        elif x2 < 500 and x2 > 360 and y2 > 1 and y2 < 80:
            1;

        elif x2 < 820 and x2 > 680 and y2 > 1 and y2 < 80:
            canvas = np.zeros_like(Image)

        elif x2 < 660 and x2 > 520 and y2 > 1 and y2 < 80:
            color = [0, 0, 0]
            tam = 12

        elif x2 < 1270 and x2 > 1130 and y2 > 1 and y2 < 80:
            color = [255, 0, 0]
            tam = 4

        elif x2 < 1270 and x2 > 1130 and y2 > 111 and y2 < 190:
            color = [0, 0, 255]
            tam = 4

        elif x2 < 1270 and x2 > 1130 and y2 > 221 and y2 < 300:
            color = [0, 255, 255]
            tam = 4

        elif x2 < 1270 and x2 > 1130 and y2 > 221 and y2 < 300:
            color = [0, 255, 255]
            tam = 4

        elif x2 < 1270 and x2 > 1130 and y2 > 331 and y2 < 410:
            color = [0, 128, 0]
            tam = 4

        elif x2 < 1270 and x2 > 1130 and y2 > 441 and y2 < 520:
            color = [128, 128, 128]
            tam = 4

        elif x2 < 1270 and x2 > 1130 and y2 > 551 and y2 < 630:
            color = [128, 0, 128]
            tam = 4

        else:

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

                elif abs(x2-x1) > 60 or abs(y2-y1) > 60:
                    x1, y1 = x2, y2

                else:
                    # Draw the line on the canvas
                    canvas = cv2.line(canvas, (x1, y1), (x2, y2), color, tam)
                # New point becomes the previous point
                x1, y1 = x2, y2
    return Image, canvas,x1,y1, canvas_figure, bandera, color, tam

def display(Image,canvas):
    # Merge the canvas and the frame.
    Image = cv2.add(Image,canvas)
    cv2.imshow('Image',Image)
    cv2.waitKey(1)

def insert_options(img):
    img = cv2.rectangle(img, (40, 1), (180, 80), (250, 230, 230), -1)
    cv2.putText(img, "RECTANGLE", (72, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (200, 1), (340, 80), (216, 191, 216), -1)
    cv2.putText(img, "CIRCLE", (245, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (360, 1), (500, 80), (221, 160, 221), -1)
    cv2.putText(img, "FREE", (405, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (520, 1), (660, 80), (238, 130, 238), -1)
    cv2.putText(img, "CLEAR", (565, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (680, 1), (820, 80), (214, 112, 218), -1)
    cv2.putText(img, "CLEAR ALL", (715, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (1130, 1), (1270, 80), (255, 0, 0), -1)
    cv2.putText(img, "BLUE", (1182, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (1130, 111), (1270, 190), (0, 0, 255), -1)
    cv2.putText(img, "RED", (1182, 158), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (1130, 221), (1270, 300), (0, 255, 255), -1)
    cv2.putText(img, "YELLOW", (1172, 268), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (1130, 331), (1270, 410), (0, 128, 0), -1)
    cv2.putText(img, "GREEN", (1172, 378), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (1130, 441), (1270, 520), (128, 128, 128), -1)
    cv2.putText(img, "GRAY", (1172, 488), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    img = cv2.rectangle(img, (1130, 551), (1270, 630), (128, 0, 128), -1)
    cv2.putText(img, "PURPLE", (1172, 598), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    return img


if __name__ == '__main__':
    #0 means primary camera .
    Camera = cv2.VideoCapture(0)
    Camera.set(3, 1280)
    Camera.set(4, 720)
    #initialize blank canvas
    canvas = None
    canvas_figure = None
    bandera = 0
    color = [255, 0, 0]
    tam = 4
    #initial position on pen
    x1,y1=0,0
    while True:
        # read new frame
        ret , Image = Camera.read()
        # flip horizontally
        Image = cv2.flip(Image, 1)

        if canvas is None:
            canvas = np.zeros_like(Image)  # initialize a black canvas

        mask = CreateMask(Image)  # create mask
        contours = ContourDetect(mask)  #detect Contours
        Image, canvas, x1, y1, canvas_figure, bandera, color, tam = drawLine(Image, contours,canvas,x1,y1, canvas_figure, bandera, color, tam) #Draw line

        Image = insert_options(Image)
        display(Image,canvas)

        
