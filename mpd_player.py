from os import listdir
from os.path import isfile, join
from natsort import natsorted, ns
from time import time
from event import Event
import RPi.GPIO as GPIO
import threading
import pexpect
from subprocess import call

class MpdPlayer:
    def __init__ (self, enablePin):
        self.enablePin = enablePin
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, GPIO.LOW)

        self.track_changed = Event()
        self.stopped = Event()
        self.volume = 0
        self.set_volume(80)
        # Poll MPD to fire stopped and track_changed

    def run_monitoring_thread(self):
        try:         
            pass
        except (KeyboardInterrupt, SystemExit):
            pass

    def set_volume(self, new_volume):
        if new_volume > 100:
            new_volume = 100
        if new_volume < 70:
            new_volume = 70
        if new_volume != self.volume:
            self.volume = new_volume
            # // Calcualte new volume and set to mpd

    def previous(self):
        # Send to MPD

    def next(self):
        # Send to MPD

    def toggle_pause(self):
        # Send to MPD

    def volume_up(self):
        self.set_volume(self.volume + 5)

    def volume_down(self):
        self.set_volume(self.volume - 5)

    def play_album(self, album):
        # Send to MPD
