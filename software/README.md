### Minimal software

Very basic camera software that features these abilities:

* button interfacing
* show live camera passthrough
* take a picture
* view the picture through list on touchscreen
* display text on OLED

#### Prerequisite

There is quite a bit of initial setup process on this [page](./fresh-os-install-steps.md).

I need to do that thoroughly/not in a rush.

After that you can do the following:

- Make a virtual env

In this software folder run `$python -m venv .jdc34-cam` then activate it

After that, run `$pip install -r requirements.txt`

- openbox

Do `$chmod +x` on openbox

- launch the window

`$sudo xinit ./openbox`

- running the menu on boot

I used systemd to do this. You can see this [page](./systemd.md) on setting up a systemd file.

#### Pelicam

[Pelicam](https://github.com/jdc-cunningham/pelicam) is the full-featured software intended to drive different camera modules, display types and small or full-sized Raspberry Pis.
