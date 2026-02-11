### Create a service

You can name the service whatever you want.

```
$sudo nano /etc/systemd/system/jdc34-cam.service
$sudo systemctl enable jdc34-cam.service
$sudo systemctl daemon-reload
$sudo systemctl restart jdc34-cam.service
```

#### jdc34-cam.service contents

```
[Unit]
Description=Start JDC34 Camera Software
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/home/pi/camera-jdc34/software
User=root
ExecStart=xinit ./openbox
Restart=always

[Install]
WantedBy=multi-user.target
```

Openbox will launch a window which will run main.py which runs OpenCV
