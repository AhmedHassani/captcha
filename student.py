from random import randint
from tkinter import Image

from PIL.ImageDraw import ImageDraw


def get_random_code():
    codes = [[chr(i) for i in range(48, 58)], [chr(i) for i in range(65, 91)], [chr(i) for i in range(97, 123)]]
    codes = codes[randint(0, 2)]
    return codes[randint(0, len(codes) - 1)]

def generate_captcha(width=140, height=60, length=4):
    img = Image.new("RGB", (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    #font = ImageFont.truetype("static/font/font.ttf", size=36)
    text = ""
    for i in range(length):
        c = get_random_code()
        text += c
        rand_len = randint(-5, 5)
        #draw.text((width * 0.2 * (i + 1) + rand_len, height * 0.2 + rand_len), c,font=font,fill=get_random_color())
    for i in range(3):
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)
    for i in range(16):
        img.save("static/captcha/" + text + ".jpg")
    return text + ".jpg"