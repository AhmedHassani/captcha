import os
import sqlite3

from PIL import Image, ImageDraw, ImageFont
from random import randint, random
from flask import Flask, render_template,redirect, request, url_for,session,flash
app = Flask(__name__)
app.secret_key = "abc"
code = "0"
email =""

def auth(username,password):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    data = cur.execute("SELECT * from students")
    for d in data.fetchall():
        if(d[1]==username and d[2]==password):
            return True
        else:
            return False
def auth_admin(username,password):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    data = cur.execute("SELECT * from admin")
    for d in data.fetchall():
        if(d[0]==username and d[1]==password):
            return True
        else:
            return False
#
def get_degrees(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    data = cur.execute("SELECT * from degrees WHERE id= '"+id+"'")
    data = data.fetchall()[0]
    return  data


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
    global email
    email=username
    cap_code = request.form['cap']
    cap_code = str(cap_code)
    if (auth(username,password)==True) and (cap_code.upper()==code.upper()):
        return redirect(url_for('show'))
    return redirect(url_for('home'))

@app.route('/show', methods=['GET'])
def show():
    data = get_degrees(email)
    return render_template("show.html",data=data)

@app.route('/login-admin', methods=['GET'])
def login_admin():
    img_list = os.listdir("static/captcha")
    index = randint(0, 1000)
    img = img_list[index]
    global code
    code = img
    code=code.replace(".jpg","")
    path = os.path.join("captcha", img)
    return render_template("login_admin.html",data=path)

@app.route('/logina', methods=['POST'])
def admin_auth():
    username = request.form['username']
    password = request.form['password']
    cap_code = request.form['cap']
    cap_code = str(cap_code)
    print(username)
    print(password)
    print(cap_code)
    print(code)
    if (auth_admin(username,password)==True) and (cap_code.upper()==code.upper()):
        return redirect(url_for('dashbord'))
    return redirect(url_for('login_admin'))

@app.route('/dashbord', methods=['GET'])
def dashbord():
    return render_template("index.html")

@app.route('/adds', methods=['POST'])
def add_student():
    conn = sqlite3.connect('db.db')
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    cur = conn.cursor()
    sql = ''' INSERT INTO students(name,email,pass)
                  VALUES(?,?,?) '''
    cur = conn.cursor()
    params = (name, username,password)
    cur.execute(sql,params)
    conn.commit()
    conn.close()
    return redirect(url_for('dashbord'))

@app.route('/addsd', methods=['POST'])
def add_student_d():
    conn = sqlite3.connect('db.db')
    id = request.form['id']
    os = request.form['os']
    security = request.form['security']
    web = request.form['web']
    network = request.form['network']
    robot = request.form['robot']
    ai = request.form['ai']
    image = request.form['image']
    avg = request.form['avg']
    state = request.form['state']
    name = request.form['name']
    branch = request.form['branch']
    stage = "الرابعه"
    cur = conn.cursor()
    sql = ''' INSERT INTO degrees(id,os,security,web,network,robot,ai,image,avg,state,name,branch,stage)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    params = (id,os,security,web,network,robot,ai,image,avg,state,name,branch,stage)
    cur.execute(sql,params)
    conn.commit()
    conn.close()
    return redirect(url_for('dashbord'))



if __name__=="__main__":
    app.run(debug=True)