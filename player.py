from os import listdir
from os.path import isfile, join
from natsort import natsorted, ns
from time import time
from event import Event
import RPi.GPIO as GPIO
import threading
import pexpect
from subprocess import call

class Player:
    def __init__ (self, enablePin):
        self.media_player = pexpect.spawn('mpg321 -R player')
        self.playlist = []
        self.playlist_index = -1

        self.monitoring_thread = threading.Thread(target=self.run_monitoring_thread)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

        self.next_track_event = threading.Event()
        self.time_start_track = time()
        self.enablePin = enablePin
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, GPIO.LOW)

        self.track_changed = Event()
        self.stopped = Event()
        self.volume = 0
        self.set_volume(80)

    def run_monitoring_thread(self):
        try:
            while True:
                self.media_player.expect("@P (0|3)", timeout=315360000)
                print("Track Stopped")
                self.on_song_finished()
        except (KeyboardInterrupt, SystemExit):
            pass

    def set_volume(self, new_volume):
        if new_volume > 100:
            new_volume = 100
        if new_volume < 70:
            new_volume = 70
        if new_volume != self.volume:
            self.volume = new_volume
            call(["amixer", "sset", "PCM", "%d%%" % (new_volume)])

    def previous(self):
        if len(self.playlist) == 0:
            return

        if time() - self.time_start_track > 5:
            self.play_track()
        elif self.playlist_index > 0:
            self.playlist_index -= 1
            self.play_track()

    def next(self):
        if self.playlist_index < len(self.playlist) - 1:
            self.playlist_index += 1
            self.play_track()

    def toggle_pause(self):
        self.media_player.sendline("PAUSE")

    def volume_up(self):
        self.set_volume(self.volume + 5)

    def volume_down(self):
        self.set_volume(self.volume - 5)

    def play_album(self, album):
        self.playlist = natsorted([join(album, f) for f in listdir(album) if isfile(join(album, f))], alg=ns.IGNORECASE)
        self.playlist_index = 0
        self.play_track()

    def play_track(self):
        print("Track Started")
        self.media_player.sendline("LOAD %s" % (self.playlist[self.playlist_index]))
        GPIO.output(self.enablePin, GPIO.HIGH)
        self.time_start_track = time()
        self.track_changed.fire(self.playlist_index + 1)

    def on_song_finished(self):
        self.playlist_index += 1
        if len(self.playlist) > self.playlist_index:
            self.play_track()
        else:
            self.stopped.fire()
