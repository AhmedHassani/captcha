import os

from PIL import Image, ImageDraw, ImageFont
from random import randint, random
from flask import Flask, render_template,redirect, request, url_for,session,flash
app = Flask(__name__)
app.secret_key = "abc"
code = "0"
def get_random_color():
    return randint(120, 200), randint(120, 200), randint(120, 200)

def get_random_code():
    codes = [[chr(i) for i in range(48, 58)], [chr(i) for i in range(65, 91)], [chr(i) for i in range(97, 123)]]
    codes = codes[randint(0, 2)]
    return codes[randint(0, len(codes) - 1)]

def generate_captcha(width=140, height=60, length=4):
    img = Image.new("RGB", (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/font.ttf", size=36)
    text = ""
    for i in range(length):
        c = get_random_code()
        text += c
        rand_len = randint(-5, 5)
        draw.text((width * 0.2 * (i + 1) + rand_len, height * 0.2 + rand_len), c,font=font,fill=get_random_color())
    for i in range(3):
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    for i in range(16):
        draw.point((randint(0, width), randint(0, height)), fill=get_random_color())
        img.save("static/captcha/" + text + ".jpg")
    return text + ".jpg"

@app.route('/get_captcha', methods=['GET'])
def get_captcha():
    img_list = os.listdir("static/captcha")
    index = randint(0, 1000)
    img = img_list[index]
    return os.path.join("static/captcha", img)

@app.route('/', methods=['GET'])
def home():
    img_list = os.listdir("static/captcha")
    index = randint(0, 1000)
    img = img_list[index]
    global code
    code = img
    code=code.replace(".jpg","")
    path = os.path.join("captcha", img)
    return render_template("login_sudent.html",data=path)
@app.route('/logins', methods=['POST'])
def login_student():
    username = request.form['username']
    password = request.form['password']
    cap_code = request.form['cap']
    cap_code = str(cap_code)
    print(username)
    print(password)
    print(cap_code.upper(),code.upper())
    return redirect(url_for('show'))
@app.route('/show', methods=['GET'])
def show():
    return render_template("show.html")
if __name__=="__main__":
    app.run(debug=True)