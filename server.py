from flask import Flask, jsonify
import platform
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/v1/system_info", methods=["GET"])
def get_system_info():
    # Obtenemos el nombre del dispositivo
    device_name = platform.node()

    # Obtenemos el tipo de procesador
    processor = platform.processor()

    # Obtenemos la cantidad de memoria RAM
    ram = platform.ram()

    # Obtenemos el ID del dispositivo
    product_id = platform.product()

    # Obtenemos el tipo de sistema operativo
    system = platform.system()

    # Obtenemos el ID del lápiz y la entrada táctil
    pen_and_touch_input = platform._get_sys_info()["input"]["pen_and_touch_input"]

    # Imprimimos la información obtenida
    system_info = {device_name, processor, ram, product_id, system, pen_and_touch_input}
    return jsonify(system_info)


if __name__ == "__main__":
    app.run(debug=True)
