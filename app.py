from flask import Flask, send_from_directory, request, jsonify
import socket
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")

# ===== 配置区：未来接真云台时在这里改 =====
GIMBAL_HOST = os.environ.get("GIMBAL_HOST", "192.168.1.100")  # 云台 IP
GIMBAL_PORT = int(os.environ.get("GIMBAL_PORT", "9000"))      # 控制端口
USE_SOCKET = False  # 测试阶段 False；真机到手改成 True
# ==========================================================

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


def send_to_gimbal(command: str, value: str | None = None) -> None:
    """
    :param command: MOVE / ZOOM / MODE ...
    :param value: LEFT / RIGHT / UP / DOWN / IN / OUT ...
    """
    msg = f"{command}:{value}" if value else command
    print(f"[DEBUG] send command to gimbal: {msg}")

    # 调试阶段不发送，未来 USE_SOCKET=True 即可发送
    if not USE_SOCKET:
        return

    # ===== 接入真实云台：TCP socket 示例 =====
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((GIMBAL_HOST, GIMBAL_PORT))
        s.send(msg.encode("utf-8"))
        s.close()
    except Exception as e:
        print(f"[ERROR] failed to send to gimbal: {e}")
    # ========================================================


@app.route("/api/control", methods=["POST"])
def api_control():
    """
    POST JSON:
    {
      "action": "move" / "zoom",
      "direction": "LEFT" / "RIGHT" / "UP" / "DOWN" / "IN" / "OUT"
    }
    """
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    direction = data.get("direction")

    if action not in {"move", "zoom"}:
        return jsonify({"status": "error", "msg": "invalid action"}), 400

    if direction is None:
        return jsonify({"status": "error", "msg": "direction required"}), 400

    if action == "move":
        send_to_gimbal("MOVE", direction)
    elif action == "zoom":
        send_to_gimbal("ZOOM", direction)

    return jsonify({"status": "ok", "action": action, "direction": direction})


@app.route("/api/ping")
def api_ping():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
