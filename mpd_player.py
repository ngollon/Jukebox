from time import time, sleep
from event import Event
import RPi.GPIO as GPIO
import threading
from musicpd import MPDClient
from log import log

class MpdPlayer:
    def __init__ (self, enablePin):
        self.enablePin = enablePin
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, GPIO.LOW)

        self.client = MPDClient()
        self.client.connect('localhost', 6600)

        self.monitoring_thread = threading.Thread(target=self.run_monitoring_thread)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

        self.playerstate = 'stop'
        self.current_track = ""
        self.track_changed = Event()
        self.stopped = Event()
        self.volume = -1
        self.set_volume(10)        

    def run_monitoring_thread(self):
        try:         
            while True:
                status = self.client.status()
                if status['state'] == 'stop' and self.playerstate != 'stop':
                    self.current_track = -1
                    log("Player: Playback stopped")
                    GPIO.output(self.enablePin, GPIO.LOW)
                    self.stopped.fire()
                    
                
                if status['state'] == 'play':                    
                    track = str(int(status['song']) + 1)
                    
                    if self.current_track != track:
                        log(f"Player: Track changed to {track}")
                        GPIO.output(self.enablePin, GPIO.HIGH)
                        self.track_changed.fire(track)
                    self.current_track = track                

                self.playerstate = status['state']

                sleep(0.2)
        except (KeyboardInterrupt, SystemExit):
            pass

    def set_volume(self, new_volume):
        if new_volume > 100:
            new_volume = 100
        if new_volume < 0:
            new_volume = 0
        if new_volume != self.volume:
            self.volume = new_volume
            log(f"Player: Setting volume to {self.volume}")
            self.client.setvol(self.volume)

    def previous(self):
        log(f"Player: Go to previous track")
        self.client.previous()

    def next(self):
        log(f"Player: Go to next track")
        self.client.next()

    def toggle_pause(self):
        log(f"Player: Pause toggled")
        self.client.pause()

    def volume_up(self):
        self.set_volume(self.volume + 5)

    def volume_down(self):
        self.set_volume(self.volume - 5)

    def play(self, uris):        
        self.client.clear()
        for uri in uris:
            uri = uri.strip()
            log(f"Player: Adding {uri} to playlist")
            self.client.add(uri)
        log("Player: Starting playback")
        self.client.play()
        
