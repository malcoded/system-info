from flask import Flask, jsonify, request
import platform
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_client_ip():
    # Intenta obtener la dirección IP desde el encabezado X-Forwarded-For
    # Si no está presente, utiliza request.remote_addr
    return request.headers.get("X-Forwarded-For", request.remote_addr)


@app.route("/api/v1/system_info", methods=["GET"])
def get_system_info():
    # Obtenemos el nombre del dispositivo
    device_name = platform.node()

    # Obtenemos el tipo de procesador
    processor = platform.processor()

    # Obtenemos la cantidad de memoria RAM
    # ram = platform.ram()

    # Obtenemos el ID del dispositivo
    # product_id = platform.product()

    # Obtenemos el tipo de sistema operativo
    system = platform.system()

    # Obtenemos el ID del lápiz y la entrada táctil
    # pen_and_touch_input = platform._get_sys_info()["input"]["pen_and_touch_input"]
    ip_address = ip_address = get_client_ip()
    user_agent = request.user_agent.string
    # Imprimimos la información obtenida
    system_info = {
        "device_name": device_name,
        "processor": processor,
        "system": system,
        "ip_address": ip_address,
        "user_agent": user_agent,
    }
    return jsonify(system_info)


if __name__ == "__main__":
    app.run(debug=True)
