# Procesamiento de imagenes y visión
# Profesores: Ing. Julián Quiroga S. e Ing. Nestor Ribero
# Taller 5
# Realizado por Jelitza Varón Heredia y Andrea Elneser Tejeda
#


import numpy as np
import cv2
import glob
import os
import json

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((11 * 8, 3), np.float32)
objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# path = 'D:/Python/tablero'
path = 'D:/Documentos_Hp/Desktop/tablero'
path_file = os.path.join(path, 'tablero*.PNG')

images = glob.glob(path_file)

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (11, 8), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (11, 8), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(250)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print(mtx)
print(dist)

file_name = 'CamaraPC_B.json'
json_file = os.path.join(path, file_name)

data = {
    'K': mtx.tolist(),
    'distortion': dist.tolist(),
    'd': 3,
    'h': 2,
    'tilt': 30,
    'pan': 0
}

# file_name = 'CamaraPC_A.json'
# data = {
#     'K': mtx.tolist(),
#     'distortion': dist.tolist(),
#     'd': 2,
#     'h': 1,
#     'tilt': 0,
#     'pan': 5
# }

with open(json_file, 'w') as fp:
    json.dump(data, fp, sort_keys=True, indent=1, ensure_ascii=False)

# with open(json_file) as fp:
#     json_data = json.load(fp)
# # print(json_data)
