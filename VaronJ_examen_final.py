# Procesamiento de imagenes y visión
# Profesores: Ing. Julián Quiroga S.
# Parcial Final - 24/11/2020
# Realizado por Jelitza Varón Heredia
#
import math
import numpy as np
import cv2
import cv
import os
# import sys

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import collections

# if __name__ == '__main__':

UserPath = 'D:/Python/banderas'  # input('Enter the path of the image: ')

# read the name of image from user
UserNameImg = 'flag1.png'  # input('Enter the name of the image: ')

# Set path of the file
UserPathFile = os.path.join(UserPath, UserNameImg)
UserImage = cv2.imread(UserPathFile)
# cv2.imshow('Image', UserImage)
# cv2.waitKey(0)
UserImage = cv2.cvtColor(UserImage, cv2.COLOR_BGR2RGB)


def recreate_image(centers, labels, rows, cols):
    d = centers.shape[1]
    image_clusters = np.zeros((rows, cols, d))
    label_idx = 0
    for i in range(rows):
        for j in range(cols):
            image_clusters[i][j] = centers[labels[label_idx]]
            label_idx += 1
    return image_clusters


# Def Class
class Banderas:
    # Def construct
    def __init__(self, image):

        self.image = image
        self.labels = None
        self.rows = None
        self.cols = None

    def Colores(self):
        print('A')

        # Número de colores de la imagen utilizando método Kmeans

        n_colors = 3
        img = np.array(self.image, dtype=np.float64) / 255
        rows, cols, ch = img.shape
        self.rows = rows
        self.cols = cols
        assert ch == 3
        image_array = np.reshape(img, (rows * cols, ch))
        image_array_sample = shuffle(image_array, random_state=0)[:10000]
        model = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
        labels = model.predict(image_array)
        centers = model.cluster_centers_
        self.labels = labels

        if 0 in labels:
            colores = 1
            if 1 in labels:
                colores = colores + 1
            if 2 in labels:
                colores = colores + 1
            if 3 in labels:
                colores = colores + 1
        print('La bandera tiene', colores, 'colores')

        if (colores < n_colors):
            n_colors = colores
            model = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
            labels = model.predict(image_array)
            centers = model.cluster_centers_
            self.labels = labels

        # plt.figure(1)
        # plt.clf()
        # plt.axis('off')
        # plt.title('Original image')
        # plt.imshow(img)

        plt.figure(2)
        plt.clf()
        plt.axis('off')
        plt.title('Quantized image ({} colors, method={})'.format(n_colors, 'Kmeans'))
        plt.imshow(recreate_image(centers, labels, rows, cols))
        plt.show()

    def Porcentajes(self):

        print(collections.Counter(self.labels))

        color1 = collections.Counter(self.labels)[0]
        color2 = collections.Counter(self.labels)[0]
        color3 = collections.Counter(self.labels)[0]
        color4 = collections.Counter(self.labels)[0]

        pixeles = self.rows * self.cols

        P_c1 = (100 * color1) / pixeles
        P_c2 = (100 * color2) / pixeles
        P_c3 = (100 * color3) / pixeles
        P_c4 = (100 * color4) / pixeles

        print('El porcentaje del color 1 es', P_c1, '%')
        print('El porcentaje del color 2 es', P_c2, '%')
        print('El porcentaje del color 3 es', P_c3, '%')
        print('El porcentaje del color 4 es', P_c4, '%')

        porcentajes = [P_c1, P_c2, P_c3, P_c4]
        return porcentajes

    def Orientacion(self):
        imagecopy = self.image.copy()
        # src = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #
        # dst = cv2.Canny(src, 50, 200, None, 3)
        #
        # # Copy edges to the images that will display the results in BGR
        # cdst = cv2.cvtColor(dst, cv.COLOR_GRAY2BGR)
        # cdstP = np.copy(cdst)
        #
        # lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)


flag = Banderas(UserImage)
flag.Colores()
porcentajes = flag.Porcentajes()
print(porcentajes)
flag.Orientacion()
