from time import time
from event import Event
import RPi.GPIO as GPIO
import threading
import musicpd

class MpdPlayer:
    def __init__ (self, enablePin):
        self.enablePin = enablePin
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.output(self.enablePin, GPIO.LOW)

        self.client = musicpd.MPDClient()
        self.client.connect()

        self.monitoring_thread = threading.Thread(target=self.run_monitoring_thread)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

        self.track_changed = Event()
        self.stopped = Event()
        self.volume = 0
        self.set_volume(80)        

    def run_monitoring_thread(self):
        try:         
            while True:
                print(self.client.cmd('idle'))     
                # Fire stopped and track_changed!           
        except (KeyboardInterrupt, SystemExit):
            pass

    def set_volume(self, new_volume):
        if new_volume > 100:
            new_volume = 100
        if new_volume < 70:
            new_volume = 70
        if new_volume != self.volume:
            self.volume = new_volume
            self.client.cmd('volume', self.volume)

    def previous(self):
        self.client.cmd('previous')

    def next(self):
        self.client.cmd('next')

    def toggle_pause(self):
        self.client.cmd('pause')

    def volume_up(self):
        self.set_volume(self.volume + 5)

    def volume_down(self):
        self.set_volume(self.volume - 5)

    def play_album(self, album):
        self.client.cmd('clear')
        self.client.cmd('add', album)
        self.client.cmd('play')        
