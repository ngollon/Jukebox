import RPi.GPIO as GPIO
import event

class Button:
    def __init__ (self, channel):
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(channel, GPIO.BOTH, callback=self.on_change, bouncetime=200)
        self.channel = channel
        self.pressed = event.Event()
        self.released = event.Event()

    def on_change(self, channel):
        current = self.is_pressed()
        print (current)
        if current:
            self.pressed.fire()
        else:
            self.released.fire()

    def is_pressed(self):
        return not GPIO.input(self.channel)
