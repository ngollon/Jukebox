import re
from button import Button
from tagreader import TagReader
from mpg321_player import Mpg321Player
from display import Display
from os import listdir
from os.path import isdir, join
from library import FileLibrary, UriLibrary
import RPi.GPIO as GPIO
from log import log


# Initialize display first to write Hello
log("Initializing Display")
d = Display()
d.draw_text("Hallo!", 32)

library_path = "/srv/library"

GPIO.setmode(GPIO.BCM)

log("Initializing Player")
p = MpdPlayer(24)

log("Initalizing Libraries")
libraries = [
    FileLibrary(library_path),
    UriLibrary(library_path)
]

def on_tag_discovered(tag):
    # Check if there is a album with this name
    uris = [ u for u in  [ l.find_tag(tag) for l in libraries ] if not u is None ]
    if any(uris):
        p.play_album(next(iter(uris)))        
    else:
        d.draw_text(tag, 12)

p.track_changed += lambda number: d.draw_text(str(number), 40)
p.stopped += lambda: d.clear()

# We have a few buttons
log("Initializing Buttons")
button_prev = Button(17, callback=p.previous)
button_next = Button(27, callback=p.next)
button_pause = Button(18, callback=p.toggle_pause)
button_volup = Button(23, callback=p.volume_up)
button_voldown = Button(22, callback=p.volume_down)

log("Initializing Tag Reader")
tr = TagReader('tty:AMA0:pn532')
tr.tag_discovered += on_tag_discovered

d.clear()
log("Initialization done")

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

GPIO.cleanup()
