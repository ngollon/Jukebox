import re
from button import Button
from tagreader import TagReader
from mpd_player import MpdPlayer
from display import Display
from library import Library
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
library = Library(library_path)

def on_tag_discovered(tag):
    # Check if there is a album with this name    
    uri = library.find_tag(tag)
    if not uri is None:
        p.play_album(uri)
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

d.clear()

log("Checking for new albums")
for name in library.untagged_albums():
    log(f"New album {name} found.")
    d.draw_text(name, 12)
    tag = tr.wait_for_tag()
    library.index(tag, name)
    log(f"New album {name} assigned to tag {tag}.")    

tr.tag_discovered += on_tag_discovered

log("Initialization done")

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

GPIO.cleanup()
