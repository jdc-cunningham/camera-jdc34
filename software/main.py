# testing pieces of hardware

import time
from imu import IMU
from buttons import Buttons

imu = IMU()
imu.start()

buttons = Buttons()
buttons.start()

while True:
  # print (imu.accel)
  time.sleep(0.1)



