import vlc
import re
from button import Button
from tagreader import TagReader
from player import Player
from display import Display
from os import listdir
from os.path import isdir, join
import RPi.GPIO as GPIO

library_path = "/srv/library"

GPIO.setmode(GPIO.BCM)

p = Player()
d = Display()

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

d.draw_text("Test", 40)

tr = TagReader('tty:AMA0:pn532')
tr.tag_discovered += on_tag_discovered

wait = input("PRESS ENTER TO CONTINUE.")

GPIO.cleanup()
