import sys
from cv2 import cv2
import numpy as np

img_path = r'C:\AK\Photos\Temp\ak_zen.jpg'
img = cv2.imread(img_path)
if '-i' in sys.argv:
    cv2.imshow('book', img)
    cv2.waitKey(0)

print(f'Height: {img.shape[0]}')
print(f'Width: {img.shape[1]}')
print(f'Channels: {img.shape[2]}')

(b, g, r) = img[0, 0]
print(b, g, r)

hsv_min = np.array((2, 28, 65), np.uint8)
hsv_max = np.array((26, 238, 255), np.uint8)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
thesholds = cv2.inRange(img_hsv, hsv_min, hsv_max)
contours, hierarchy = cv2.findContours(thesholds.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(contours)
cv2.drawContours(img, contours, -1, (255, 0, 0), 3, cv2.LINE_AA, hierarchy, 1)
cv2.imshow('with contours', img)
cv2.waitKey()
cv2.destrotAllWindows()
