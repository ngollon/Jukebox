import vlc
from os import listdir
from os.path import isfile, join
from natsort import natsorted, ns
from time import time
from event import Event
import RPi.GPIO as GPIO
import threading
from subprocess import call


class Player:
    def __init__ (self, enablePin):
        self.media_player = vlc.MediaPlayer()
        self.media_player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_song_finished, 0)
        self.playlist = []
        self.playlist_index = -1
        self.playlist_thread = threading.Thread(target=self.run_playlist_thread)
        self.playlist_thread.daemon = True
        self.playlist_thread.start()
        self.next_track_event = threading.Event()
        self.time_start_track = time()
        self.enablePin = enablePin
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, GPIO.LOW)

        self.track_changed = Event()
        self.stopped = Event()
        self.volume = 0
        self.set_volume(80)

    def run_playlist_thread(self):
        try:
            while(True):
                self.next_track_event.wait()
                self.next_track_event.clear()
                if len(self.playlist) > self.playlist_index:
                    self.play_track()
                else:
                    GPIO.output(self.enablePin, GPIO.LOW)
                    self.stopped.fire()
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
        print(self.media_player.is_playing())
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()

    def volume_up(self):
        self.set_volume(self.volume + 5)

    def volume_down(self):
        self.set_volume(self.volume - 5)


    def play_album(self, album):
        self.playlist = natsorted([join(album, f) for f in listdir(album) if isfile(join(album, f))], alg=ns.IGNORECASE)
        self.playlist_index = 0
        self.play_track()

    def play_track(self):
        self.media_player.set_mrl(self.playlist[self.playlist_index])
        self.media_player.play()
        GPIO.output(self.enablePin, GPIO.HIGH)
        self.time_start_track = time()
        self.track_changed.fire(self.playlist_index + 1)

    def on_song_finished(self, *args, **kwds):
        self.playlist_index += 1
        self.next_track_event.set()
