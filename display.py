import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

class Display:
    def __init__(self):
        self.diplay =  Adafruit_SSD1306.SSD1306_128_64(rst=24)
        self.diplay.begin()

        self.diplay.clear()
        self.diplay.display()

    def clear(self):
        self.diplay.clear()
        self.diplay.display()

    def print_track_number(self, number):
        self.draw_text(str(number), 40)

    def print_tag(self, tag):
        self.draw_text(tag, 12)

    def draw_text(self, text, size):
        width = self.diplay.width
        height = self.diplay.height
        image = Image.new('1', (width, height))

        font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', size)

        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        (tw, th) = font.getsize(text)

        draw.text(((width - tw) / 2, (height - th) / 2), text, font=font, fill=255)

        self.diplay.image(image)
        self.diplay.display()
