import vlc
import re
from button import Button
from tagreader import TagReader
from player import Player
from display import Display
from os import listdir
from os.path import isdir, join
import RPi.GPIO as GPIO

# Initialize display first to write Hello
d = Display()
d.draw_text("Hallo!", 32)

library_path = "/srv/library"

GPIO.setmode(GPIO.BCM)

p = Player(24)

def on_tag_discovered(tag):
     # Check if there is a album with this name
     try:
         selected_album = (join(library_path, f) for f
                           in listdir(library_path)
                           if isdir(join(library_path, f))
                               and bool(re.search(tag + "$", f, re.I))).next()
         p.play_album(selected_album)
     except StopIteration:
         d.print_tag(tag)

p.track_changed += lambda number: d.print_track_number(number)
p.stopped += lambda: d.clear()

# We have a few buttons
button_prev = Button(17, callback=p.previous)
button_next = Button(27, callback=p.next)
button_pause = Button(18, callback=p.toggle_pause)
button_volup = Button(23, callback=p.volume_up)
button_voldown = Button(22, callback=p.volume_down)

tr = TagReader('tty:AMA0:pn532')
tr.tag_discovered += on_tag_discovered

d.clear()

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

GPIO.cleanup()
