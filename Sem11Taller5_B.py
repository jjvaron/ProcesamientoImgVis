# Procesamiento de imagenes y visión
# Profesores: Ing. Julián Quiroga S. e Ing. Nestor Ribero
# Taller 5
# Realizado por Jelitza Varón Heredia y Andrea Elneser Tejeda
#
import cv2
from camera_model import *
import json
import os
import sys

path = sys.argv[1]  # 'D:/Documentos_Hp/Desktop/tablero'
# sys.argv[2] = CamaraPhone_A.json
# sys.argv[3] = CamaraPhone_B.json
json_file = os.path.join(path, sys.argv[2])  # sys.argv[2] para cámara A t sys.argv[3] para cámara B

with open(json_file) as fp:
    data_json = json.load(fp)

# intrinsics parameters
fx = 1000
fy = 1000
width = 900  # 1280
height = 900
cx = width / 2
cy = height / 2

# K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1.0]])
# h = 1  # 0.3
# d = 3
# R = set_rotation(0, 0, 0)
# t = np.array([0, -d, h])  # distancia en eje y

# # imagen con datos del archivo 'CamaraPhone_A.json'
K = data_json['K']
h = int(data_json['h'])
d = int(data_json['d'])
t = np.array([0, -d, h])
pan = int(data_json['pan'])
tilt = int(data_json['tilt'])
R = set_rotation(tilt, pan, 0)

# # imagen con datos del archivo 'CamaraPhone_B.json'
# #
# K = data_json['K']
# h = int(data_json['h'])
# d = int(data_json['d'])
# t = np.array([0, -d, h])
# pan = int(data_json['pan'])
# tilt = int(data_json['tilt'])
# # R = set_rotation(tilt, pan, 0)
#
print('Matriz K para cámara de PC', K)
print(d)
print(h)
print(tilt)
print(pan)

# create camera
camera = projective_camera(K, width, height, R, t)

square_3D = np.array([[1, 1, 0], [1, -1, 0], [-1, -1, 0], [-1, 1, 0]])
square_3D_2 = np.array([[1, 1, 2], [1, -1, 2], [-1, -1, 2], [-1, 1, 2]])


square_2D = projective_camera_project(square_3D, camera)
square_2D_2 = projective_camera_project(square_3D_2, camera)

image_projective = 255 * np.ones(shape=[camera.height, camera.width, 3], dtype=np.uint8)

# 1st square
cv2.line(image_projective, (square_2D[0][0], square_2D[0][1]), (square_2D[1][0], square_2D[1][1]), (200, 1, 1), 2)
cv2.line(image_projective, (square_2D[1][0], square_2D[1][1]), (square_2D[2][0], square_2D[2][1]), (200, 1, 1), 2)
cv2.line(image_projective, (square_2D[2][0], square_2D[2][1]), (square_2D[3][0], square_2D[3][1]), (200, 1, 1), 2)
cv2.line(image_projective, (square_2D[3][0], square_2D[3][1]), (square_2D[0][0], square_2D[0][1]), (200, 1, 1), 2)

# 2nd square
cv2.line(image_projective, (square_2D_2[0][0], square_2D_2[0][1]), (square_2D_2[1][0], square_2D_2[1][1]), (200, 1, 1),
         2)
cv2.line(image_projective, (square_2D_2[1][0], square_2D_2[1][1]), (square_2D_2[2][0], square_2D_2[2][1]), (200, 1, 1),
         2)
cv2.line(image_projective, (square_2D_2[2][0], square_2D_2[2][1]), (square_2D_2[3][0], square_2D_2[3][1]), (200, 1, 1),
         2)
cv2.line(image_projective, (square_2D_2[3][0], square_2D_2[3][1]), (square_2D_2[0][0], square_2D_2[0][1]), (200, 1, 1),
         2)

# lines between squares
cv2.line(image_projective, (square_2D_2[0][0], square_2D_2[0][1]), (square_2D[0][0], square_2D[0][1]), (200, 1, 1), 2)
cv2.line(image_projective, (square_2D_2[1][0], square_2D_2[1][1]), (square_2D[1][0], square_2D[1][1]), (200, 1, 1), 2)
cv2.line(image_projective, (square_2D_2[2][0], square_2D_2[2][1]), (square_2D[2][0], square_2D[2][1]), (200, 1, 1), 2)
cv2.line(image_projective, (square_2D_2[3][0], square_2D_2[3][1]), (square_2D[3][0], square_2D[3][1]), (200, 1, 1), 2)

cv2.imshow("Image", image_projective)
# cv2.imwrite('D:/Documentos_Hp/Desktop/tablero/cubo_Phone_A.png', image_projective)

cv2.waitKey(0)
