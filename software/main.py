#!/usr/bin/env -S python

import cv2
import io
import logging
import numpy as np
import time
import os
from buttons.buttons import Buttons
from camera.camera import Camera
from PIL import Image
from oled.OLED_Module_Code.RaspberryPi.python.example.OLED_0in91_test import small_OLED

# control the small OLED
oled = small_OLED()
oled.draw_text("JDC34 camera")
time.sleep(2)
oled.draw_text("Pelicam")

# optional but helpful since print logs disappear in openbox/systemd
logging.basicConfig(
  filename='/home/pi/pelicam/src/camera/pelicam.log',
  level=logging.INFO
)

# initialize camera so it can start creating frame buffers for live preview
camera = Camera()
camera.start_streaming()

# prep splash logo screen
img_path = "/home/pi/pelicam/src/camera/logo.png"
boot_scene = cv2.imread(img_path)

show_previous_photo = False
previous_photo = None
list_coordinates = []

def get_previous_photo(photo_path):
  if not photo_path:
    return

  img = cv2.imread(photo_path)
  return cv2.resize(img, (640, 480))

def get_filename_from_click(x, y):
  for coord in list_coordinates:
    coords = coord["coords"]

    if x > coords[0] and x < coords[0] + 600:
      if y + 40 > coords[1] and y < coords[1] + 40:
        return coord["file"]

# capture mouse-click coordinate
def on_mouse(event, x, y, flags, param):
  global previous_photo, show_previous_photo

  if event == cv2.EVENT_LBUTTONDOWN:
    if has_pictures and not show_previous_photo:
      filepath = get_filename_from_click(x, y)

      if filepath:
        show_previous_photo = True
        previous_photo = get_previous_photo(filepath)

# setup GUI
# black bg
img = np.zeros((480, 640, 3), dtype=np.uint8)
window_name = "Pelicam"
window_width = 640
window_height = 480
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback(window_name, on_mouse)
cv2.imshow(window_name, boot_scene)

# show this img while taking a picture
taking_picture_img = img = np.ones((480, 640, 3), dtype=np.uint8) * 255
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(taking_picture_img, 'Taking picture...', (220, 280), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

# https://stackoverflow.com/a/49517948/2710227
def buf_to_pil_img(buf):
  img = np.array(Image.open(io.BytesIO(buf)))
  return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

camera_active = False
taking_picture = False
has_pictures = False
files_img = None

# this is poorly done, I'll improve this, the coordinate is off/click on the wrong thing
def get_pictures_img():
  global list_coordinates
  file_names_img = np.ones((480, 640, 3), dtype=np.uint8) * 255
  font = cv2.FONT_HERSHEY_SIMPLEX
  cv2.putText(file_names_img, 'Photos', (40, 40), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
  base_dir = '/home/pi/pelicam/src/camera/captured_media/'
  pics = os.listdir(base_dir)
  sort = []

  for pic in pics:
    sort.append(pic.replace('.jpg', ''))

  sort.sort()
  sort.reverse()
  x_offset = 40
  y_offset = 100
  counter = 1

  for pic in sort:
    if pic == ".gitkeep":
      continue

    cv2.putText(file_names_img, pic + '.jpg', (x_offset, y_offset), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    list_coordinates.append({
      "coords": [x_offset, y_offset],
      "file": base_dir + pic + '.jpg'  
    })
  
    y_offset += 50
    counter += 1

    if counter > 7:
      break

  return file_names_img

def button_pressed(button):
  global camera_active, taking_picture, has_pictures, files_img, show_previous_photo

  if button == "SHUTTER":
    if not camera_active:
      camera_active = True
      time.sleep(0.1) # add delay to prevent early photo
    else:
      taking_picture = True
      camera.take_picture()
      taking_picture = False
      has_pictures = True
      files_img = get_pictures_img()

  if button == "BACK":
    show_previous_photo = False
    camera_active = False

# listen to button presses
buttons = Buttons(button_pressed)
buttons.start()

# render menu
while True:
  try:
    if show_previous_photo:
      cv2.imshow(window_name, previous_photo)
    elif camera_active:
      if taking_picture:
        cv2.imshow(window_name, taking_picture_img)
      else:
        cv2.imshow(window_name, buf_to_pil_img(camera.output.frame))
    elif has_pictures:
     cv2.imshow(window_name, files_img)
    else:
      cv2.imshow(window_name, boot_scene)

    cv2.waitKey(17)
  except KeyboardInterrupt:
    break

cv2.destroyAllWindows()
