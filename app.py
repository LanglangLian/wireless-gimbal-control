from flask import Flask, send_from_directory
import socket

app = Flask(__name__)

GIMBAL_IP = "192.168.144.108"      # 云台 IP
GIMBAL_PORT = 2338                 # 云台 UDP 控制端口
LOCAL_PORT = 2337                  # 发送端口（


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", LOCAL_PORT))  # 绑定源端口


def send_to_gimbal(cmd: str):
    print(f"[DEBUG] 发送控制命令到云台: {cmd}")
    sock.sendto(cmd.encode(), (GIMBAL_IP, GIMBAL_PORT))

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

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
    print("Web 控制服务已启动：http://127.0.0.1:8000")
    app.run(host="0.0.0.0", port=8000)

