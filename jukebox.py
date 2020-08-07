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
d.draw_text("Hallo!")

library_path = "/srv/library"

GPIO.setmode(GPIO.BCM)

log("Initializing Player")
p = MpdPlayer(24)

log("Initalizing Libraries")
library = Library(library_path)

def on_tag_discovered(tag):
    # Check if there is a album with this name    
    uris = library.find_tag(tag)
    if any(uris):
        p.play(uris)
    else:
        d.draw_text(tag)    

p.track_changed += lambda number: d.draw_text(str(number))
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
for folder in library.unindexed_folders():
    log(f"New folder {folder} found.")
    d.draw_text(folder)
    tag = tr.wait_for_tag()
    library.add_to_index(tag, folder)
    log(f"New album {folder} assigned to tag {tag}.")    

tr.tag_discovered += on_tag_discovered

log("Initialization done")

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

GPIO.cleanup()