from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from ImageFont import truetype

# https://luma-oled.readthedocs.io/en/latest/hardware.html#i2c

class Display:
    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)        
        self.device = ssd1306(self.serial)        

    def clear(self):
        with canvas(self.device):
            pass        
            
    def draw_text(self, text, size):
        with canvas(self.device) as draw:
            width = self.device.width
            height = self.device.height
        
            font = truetype('VCR_OSD_MONO_1.001.ttf', size)
            (tw, th) = font.getsize(text)

            draw.text(((width - tw) / 2, (height - th) / 2), text, font=font, fill=255)