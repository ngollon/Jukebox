import RPi.GPIO as GPIO
import event
import threading
from time import sleep
from log import log

class Button:
    DEBOUNCE_TIME = 0.1

    def __init__ (self, channel, callback = None):
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.on_change)
        self.channel = channel
        self.pressed = event.Event()
        self.released = event.Event()

        if callback != None:
            self.pressed += callback

        self.pressed += lambda: log(f"Button {self.channel} pressed.")
        self.released += lambda: log(f"Button {self.channel} released.")

        self.edge_event = threading.Event()
        self.monitoring_thread = threading.Thread(target=self.run_monitoring_thread)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        self.state = not GPIO.input(channel)

    def run_monitoring_thread(self):
        try:
            while True:
                self.edge_event.wait()
                self.state = not self.state # On any edge, something will change
                self.raise_event()
                sleep(self.DEBOUNCE_TIME)

                new_stable_state = not GPIO.input(self.channel)
                if self.state != new_stable_state:
                    self.state = new_stable_state
                    self.raise_event()
                self.edge_event.clear()
        except KeyboardInterrupt:
            pass

    def raise_event(self):
        if self.state:
            self.pressed.fire()
        else:
            self.released.fire()

    def on_change(self, channel):
        self.edge_event.set()

    def is_pressed(self):
        return self.state
