# http://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server.py

import io
import time
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition

base_path = "/home/pi/pelicam/src/camera/captured_media/"

class StreamingOutput(io.BufferedIOBase):
  def __init__(self):
    self.frame = None
    self.condition = Condition()

  def write(self, buf):
    with self.condition: 
      self.frame = buf
      self.condition.notify_all()

class Camera:
  def __init__(self):
    self.picam2 = Picamera2()
    self.output = None

    self.photo_config = self.picam2.create_still_configuration(
      main={"size": self.picam2.sensor_resolution, "format":"RGB888"}
    )

    self.video_config = self.picam2.create_video_configuration(
      main={"size": (640, 480), "format":"RGB888"},
    )

  def change_mode(self, mode):
    if mode == "full":
      self.picam2.switch_mode(self.photo_config)
    else:
      self.picam2.switch_mode(self.video_config)

  def take_picture(self):
    img_path = base_path + str(time.time()).split(".")[0] + ".jpg"
    self.change_mode("full")
    self.picam2.capture_file(img_path)
    self.change_mode("stream")

  def start_streaming(self):
    self.picam2.configure(self.video_config)
    self.output = StreamingOutput()
    self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))
