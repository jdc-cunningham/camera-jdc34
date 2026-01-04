#!/usr/bin/env -S python

import cv2
import numpy as np
import logging

img = np.zeros((480, 640, 3), dtype=np.uint8) 
img.fill(155) # to white

window_name = "Resizable Window"
width = 640
height = 480
font = cv2.FONT_HERSHEY_SIMPLEX

logging.basicConfig(
  filename='/home/pi/app.log',  # Name of the log file
  level=logging.INFO,   # The minimum level of messages to log (INFO and above)
  format='%(asctime)s:%(levelname)s:%(message)s' # Format of each log message
)

logging.info("start")

def on_mouse(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONDOWN:
    logging.info(f'click {x}, {y}')

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback(window_name, on_mouse)
cv2.imshow(window_name, img)

while True:
  try:
    cv2.imshow(window_name, img)
    cv2.waitKey(33)
  except KeyboardInterrupt:
    break

cv2.destroyAllWindows()
