#!/usr/bin/env -S python

import cv2
import numpy as np

img = np.zeros((480, 640, 3), dtype=np.uint8) 
img.fill(155) # to white

window_name = "Resizable Window"
width = 640
height = 480


cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.imshow(window_name, img)


cv2.waitKey(0)
cv2.destroyAllWindows()
