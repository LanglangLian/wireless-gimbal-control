from flask import Flask, send_from_directory
import socket

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


def send_to_gimbal(cmd):
    print("sending to", cmd)


@app.route("/left")
def left():
    send_to_gimbal("LEFT")
    return "ok"


@app.route("/right")
def right():
    send_to_gimbal("RIGHT")


@app.route("/up")
def up():
    send_to_gimbal("UP")
    return "ok"


@app.route("/down")
def down():
    send_to_gimbal("DOWN")
    return "ok"


@app.route("/zoom_in")
def zoom_in():
    send_to_gimbal("ZOOM_IN")
    return "ok"


@app.route("/zoom_out")
def zoom_out():
    send_to_gimbal("ZOOM_OUT")
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
