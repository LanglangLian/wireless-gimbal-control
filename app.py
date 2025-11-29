from flask import Flask, send_from_directory
import socket

app = Flask(__name__)

# 显示网页
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

def send_to_gimbal(cmd):
    print("[DEBUG] 控制命令:", cmd)


@app.route("/left")
def left():
    send_to_gimbal("LEFT")
    return "ok"

@app.route("/right")
def right():
    send_to_gimbal("RIGHT")
    return "ok"

@app.route("/up")
def up():
    send_to_gimbal("UP")
    return "ok"

@app.route("/down")
def down():
    send_to_gimbal("DOWN")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
