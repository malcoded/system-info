from flask import Flask, jsonify
import platform
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/v1/system_info", methods=["GET"])
def get_system_info():
    system_info = {
        "name": platform.node(),
        "system": platform.system(),
    }
    return jsonify(system_info)


if __name__ == "__main__":
    app.run(debug=True)
