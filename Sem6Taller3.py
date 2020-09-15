# Procesamiento de imagenes y visión
# Profesores: Ing. Julián Quiroga S e Ing. Nestor Ribero
# Taller 3
# Realizado por Jelitza Varón Heredia
#

import os
import cv2
import math
import numpy as np
import time

path = 'D:/Python/Taller1Procesamiento/img'  # input('Enter the path of the image: ')
image_name = 'lena_gauss_noisy.png'  # input('Enter the name of the image with te extention: ')
path_file = os.path.join(path, image_name)
image = cv2.imread(path_file)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


class filters:

    # Def construct
    def __init__(self, img):
        self.sigma = None
        self.image = img
        self.window = None

    def gauss(self, window, sigma):
        self.window = window
        self.sigma = sigma
        # N = self.window
        start_time = time.time()
        image_gauss_lp = cv2.GaussianBlur(self.image, (self.window, self.window), self.sigma, self.sigma)
        end_time = time.time()
        total_time_gauss = end_time - start_time
        print("excecution time gauss ", total_time_gauss)

        cv2.imshow("image gauss", image_gauss_lp)
        cv2.waitKey(0)

        # noise estimation

        image_noise = abs(self.image - image_gauss_lp)
        cv2.imshow("image noise estimation", image_noise)
        cv2.waitKey(0)
        cv2.imwrite('D:/Python/Taller1Procesamiento/img/lena_s&p_noise_estimation_by_gauss.png', image_noise)

        # sqrt of Mean Squared Error
        err = np.sum((self.image.astype("float") - image_gauss_lp.astype("float")) ** 2)
        err /= float(self.image.shape[0] * self.image.shape[1])
        errsqrt = math.sqrt(err)
        print(" Gauss Sqrt of ECM", errsqrt)

        return image_gauss_lp

    def average(self, window):
        self.window = window
        start_time = time.time()
        image_average = cv2.blur(self.image, (self.window, self.window))
        end_time = time.time()


        total_time_average = end_time - start_time
        print("excecution time average ", total_time_average)
        
        # noise estimation
        image_noise = abs(self.image - image_average)

        cv2.imshow("image noise estimation", image_noise)
        cv2.waitKey(0)
        cv2.imwrite('D:/Python/Taller1Procesamiento/img/lena_s&p_noise_estimation_by_average.png', image_noise)

        # sqrt of Mean Squared Error
        err = np.sum((self.image.astype("float") - image_average.astype("float")) ** 2)
        err /= float(self.image.shape[0] * self.image.shape[1])
        errsqrt = math.sqrt(err)
        print(" Average Sqrt of ECM", errsqrt)
        return image_average

    def bilateral(self):
        start_time = time.time()
        image_bilateral = cv2.bilateralFilter(self.image, 15, 25, 25)
        end_time = time.time()
        total_time_bilateral = end_time - start_time
        print("excecution time bilateral ", total_time_bilateral)

        # noise estimation
        image_noise = abs(self.image - image_bilateral)
        cv2.imshow("image noise estimation", image_noise)
        cv2.waitKey(0)
        cv2.imwrite('D:/Python/Taller1Procesamiento/img/lena_s&p_noise_estimation_by_bilateral.png', image_noise)

        # sqrt of Mean Squared Error
        err = np.sum((self.image.astype("float") - image_bilateral.astype("float")) ** 2)
        err /= float(self.image.shape[0] * self.image.shape[1])
        errsqrt = math.sqrt(err)
        print(" bilateral Sqrt of ECM", errsqrt)

        return image_bilateral

    def non_local_mean(self):
        start_time = time.time()
        image_nlm = cv2.fastNlMeansDenoising(self.image, 5, 15, 25)
        end_time = time.time()
        total_time_nlm = end_time - start_time
        print("excecution time nlm ", total_time_nlm)

        # noise estimation
        image_noise = abs(self.image - image_nlm)
        cv2.imshow("image noise estimation", image_noise)
        cv2.waitKey(0)
        cv2.imwrite('D:/Python/Taller1Procesamiento/img/lena_s&p_noise_estimation_by_nlm.png', image_noise)

        # sqrt of Mean Squared Error
        err = np.sum((self.image.astype("float") - image_nlm.astype("float")) ** 2)
        err /= float(self.image.shape[0] * self.image.shape[1])
        errsqrt = math.sqrt(err)
        print(" nlm Sqrt of ECM", errsqrt)
        return image_nlm


test = filters(image_gray)
image_filtered = test.gauss(7, 1.5)
image_filtered1 = test.average(7)
image_filtered2 = test.bilateral()
image_filtered3 = test.non_local_mean()
