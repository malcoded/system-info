from flask import Flask, jsonify, request
import platform
from flask_cors import CORS
from geopy.geocoders import Nominatim
import socket
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# Configura la aplicación Flask para trabajar detrás de un proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)


def get_client_device_name(client_ip):
    try:
        client_name, _, _ = socket.gethostbyaddr(client_ip)
        return client_name
    except socket.herror:
        return "Not available"


def get_mac_address():
    # Crea un paquete ARP para solicitar la dirección MAC de la IP especificada

    return "Not available"


def obtener_ubicacion(latitud, longitud):
    geolocalizador = Nominatim(user_agent="mi_aplicacion")
    ubicacion = geolocalizador.reverse((latitud, longitud))

    return ubicacion.address if ubicacion else "Ubicación no encontrada"


def get_client_ip():
    # Intenta obtener la dirección IP desde el encabezado X-Forwarded-For
    # Si no está presente, utiliza request.remote_addr
    return request.headers.get("X-Real-IP") or request.headers.get(
        "X-Forwarded-For", request.remote_addr
    )


@app.route("/api/v1/system_info", methods=["POST"])
def get_system_info():
    try:
        data = request.json
        latitud = data["latitud"]
        longitud = data["longitud"]
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

        # Obtener el origen de la solicitud
        origin = request.headers.get("Origin")

        # Obtenemos el ID del lápiz y la entrada táctil
        # pen_and_touch_input = platform._get_sys_info()["input"]["pen_and_touch_input"]
        ip_address = get_client_ip()
        user_agent = request.user_agent.string
        location = obtener_ubicacion(latitud, longitud)
        mac_addresses = get_mac_address()
        device_name_ip = get_client_device_name(ip_address)
        # Imprimimos la información obtenida
        system_info = {
            "device_name_server": device_name,
            "processor_server": processor,
            "system_server": system,
            "mac_addresses": mac_addresses,
            "device_name_ip": device_name_ip,
            "origin": origin,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "location": location,
        }
        return jsonify(system_info)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
