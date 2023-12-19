from flask import Flask, jsonify
import platform

app = Flask(__name__)


@app.route("/system_info", methods=["GET"])
def get_system_info():
    system_info = {
        "name": platform.node(),
        "system": platform.system(),
    }
    return jsonify(system_info)


if __name__ == "__main__":
    app.run(debug=True)
