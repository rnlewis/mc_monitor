from flask import Flask, render_template, jsonify
import threading
from monitor.rcon_monitor import RconMonitor

app = Flask(__name__)

monitor = RconMonitor()
threading.Thread(target=monitor.background_loop,
                 kwargs={"interval": 15}, daemon=True).start()


@app.route("/")
def dashboard():
    return render_template("dashboard.html",
                           data=monitor.snapshot.to_dict(),
                           status=monitor.status.to_dict())


@app.route("/players")
def players():
    return jsonify(monitor.status.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
