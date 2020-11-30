import cv2
import numpy as np
import math
import keyboard

class clase_canvas_1():
    def __init__(self):
        # initialize blank canvas
        self.canvas = None
        self.canvas_figure = None
        self.bandera = 0
        self.color = [255, 0, 0]
        self.tam = 7
        # initial position on pen
        self.x1, self.y1 = 0, 0
        self.contador = 0

    def CreateMask(self,Image):
        hsv_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)  # convert from BGR to HSV color range
        # lower_range = np.array([100,100,0],np.uint8)    #HSV lower range
        lower_range = np.array([20, 100, 100], np.uint8)  # HSV lower range
        # upper_range = np.array([140,255,255],np.uint8)  #HSV upper range
        upper_range = np.array([30, 255, 255], np.uint8)  # HSV upper range
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.inRange(hsv_Image, lower_range, upper_range)  # Create binary mask
        # Perform morphological operations to get rid of the noise
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        return mask

    def ContourDetect(self, mask):
        # Find Contours based on the mask created.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def drawLine(self, Image, contours):
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



        if keyboard.is_pressed('b'):
            self.canvas = np.zeros_like(Image)

        elif keyboard.is_pressed('s'):
            cv2.imwrite('AirCanvas.png', self.canvas)
            cv2.close()

        if keyboard.is_pressed('r'):
            self.canvas_figure = self.canvas.copy()
            self.bandera = 1

        elif keyboard.is_pressed('c'):
            self.canvas_figure = self.canvas.copy()
            self.bandera = 2

        elif keyboard.is_pressed('+'):
            self.tam = self.tam + 2

        elif keyboard.is_pressed('-'):
            self.tam = self.tam - 2
            if self.tam <= 7:
                self.tam = 7

        elif keyboard.is_pressed('o') and self.contador == 0:
            self.canvas_figure = self.canvas.copy()
            self.contador = 1

        elif keyboard.is_pressed('p') and self.contador == 1:  # if key 'p' is pressed
            min_error = 1000000000000000
            contorno_menor = []

            image_gray = cv2.cvtColor(self.canvas_figure, cv2.COLOR_BGR2GRAY)
            # Otsu's global threshold
            ret, Ibw_otsu = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours_, hierarchy = cv2.findContours(image_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for idx, cont in enumerate(contours_):
                momentos = cv2.moments(contours_[idx])
                cx = int(momentos['m10'] / momentos['m00'])
                cy = int(momentos['m01'] / momentos['m00'])
                error = math.sqrt(((cx - x2) ** 2) + ((cy - y2) ** 2))
                if error < min_error:
                    contorno_menor = contours_[idx]
                    min_error = error
            cv2.drawContours(self.canvas, [contorno_menor], 0, self.color, -1)
            self.contador = 0

        elif keyboard.is_pressed('f') and self.bandera != 0:

            canvas_subtract = cv2.subtract(self.canvas, self.canvas_figure)
            image_gray = cv2.cvtColor(canvas_subtract, cv2.COLOR_BGR2GRAY)
            # Otsu's global threshold
            ret, Ibw_otsu = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, hierarchy = cv2.findContours(image_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            c = max(contours, key=cv2.contourArea)

            if self.bandera == 1:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(self.canvas_figure, [box], 0, self.color, 2)
            elif self.bandera == 2:
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(self.canvas_figure, center, radius, self.color, 2)
            self.canvas = self.canvas_figure.copy()
            self.bandera = 0

        elif keyboard.is_pressed('f'):
            1;

        elif keyboard.is_pressed('l'):
            self.color = [0, 0, 0]
            self.tam = 15

        elif keyboard.is_pressed('a'):
            self.color = [255, 0, 0]
            self.tam = 7

        elif keyboard.is_pressed('q'):
            self.color = [0, 0, 255]
            self.tam = 7

        elif keyboard.is_pressed('y'):
            self.color = [0, 255, 255]
            self.tam = 7

        elif keyboard.is_pressed('v'):
            self.color = [0, 128, 0]
            self.tam = 7

        elif keyboard.is_pressed('m'):
            self.color = [128, 0, 128]
            self.tam = 7




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
                if self.x1 == 0 and self.y1 == 0:
                    self.x1, self.y1 = x2, y2

                elif abs(x2 - self.x1) > 60 or abs(y2 - self.y1) > 60:
                    self.x1, self.y1 = x2, y2

                else:
                    # Draw the line on the canvas
                    self.canvas = cv2.line(self.canvas, (self.x1, self.y1), (x2, y2), self.color, self.tam)
                # New point becomes the previous point
                self.x1, self.y1 = x2, y2




    def insert_options(self,img):
        img = cv2.rectangle(img, (40, 5), (150, 70), (230, 216, 173), -1)
        cv2.putText(img, "RECTANGLE (r)", (55, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (260, 5), (370, 70), (255, 191, 0), -1)
        cv2.putText(img, "CIRCLE (c)", (288, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (480, 5), (590, 70), (255, 144, 30), -1)
        cv2.putText(img, "FREE (f)", (517, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (700, 5), (810, 70), (225, 105, 65), -1)
        cv2.putText(img, "CLEAR (l)", (731, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (920, 5), (1030, 70), (139, 0, 0), -1)
        cv2.putText(img, "CLEAR ALL (b)", (935, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (1140, 5), (1260, 70), (255, 0, 0), -1)
        cv2.putText(img, "BLUE (a)", (1182, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (1140, 120), (1260, 185), (0, 0, 255), -1)
        cv2.putText(img, "RED (q)", (1182, 158), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (1140, 235), (1260, 300), (0, 255, 255), -1)
        cv2.putText(img, "YELLOW (y)", (1169, 272), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (1140, 350), (1260, 415), (0, 128, 0), -1)
        cv2.putText(img, "GREEN (v)", (1172, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (1140, 465), (1260, 530), (128, 0, 128), -1)
        cv2.putText(img, "PURPLE (m)", (1172, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        img = cv2.rectangle(img, (1140, 580), (1260, 645), (128, 128, 128), -1)
        cv2.putText(img, "EXIT (s)", (1185, 615), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        return img

    def display(self, Image):
        # Merge the canvas and the frame.
        Image = cv2.add(Image, self.canvas)
        cv2.imshow('Image', Image)
        cv2.waitKey(1)