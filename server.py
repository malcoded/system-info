from flask import Flask, jsonify, request
import platform
from flask_cors import CORS
from geopy.geocoders import Nominatim
import netifaces
import socket


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_client_device_name(client_ip):
    try:
        client_name, _, _ = socket.gethostbyaddr(client_ip)
        return client_name
    except socket.herror:
        return "Not available"


def get_mac_addresses():
    mac_addresses = {}

    for interface in netifaces.interfaces():
        try:
            mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
            mac_addresses[interface] = mac
        except (ValueError, IndexError, KeyError):
            mac_addresses[interface] = "Not available"

    return mac_addresses


def obtener_ubicacion(latitud, longitud):
    geolocalizador = Nominatim(user_agent="mi_aplicacion")
    ubicacion = geolocalizador.reverse((latitud, longitud))

    return ubicacion.address if ubicacion else "Ubicación no encontrada"


def get_client_ip():
    # Intenta obtener la dirección IP desde el encabezado X-Forwarded-For
    # Si no está presente, utiliza request.remote_addr
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def get_client_ip_f():
    # Intenta obtener la dirección IP desde los encabezados X-Real-IP o X-Forwarded-For
    # Si no están presentes, utiliza request.remote_addr
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

        # Obtenemos el ID del lápiz y la entrada táctil
        # pen_and_touch_input = platform._get_sys_info()["input"]["pen_and_touch_input"]
        ip_address = get_client_ip()
        device_name_ip_f = get_client_ip_f()
        user_agent = request.user_agent.string
        location = obtener_ubicacion(latitud, longitud)
        mac_addresses = get_mac_addresses()
        ipxd = request.remote_addr
        device_name_ip = get_client_device_name(ipxd)
        # Imprimimos la información obtenida
        system_info = {
            "device_name_server": device_name,
            "processor_server": processor,
            "system_server": system,
            "ip_address": ip_address,
            "device_name_ip_f": device_name_ip_f,
            "user_agent": user_agent,
            "location": location,
            "mac_addresses": mac_addresses,
            "device_name_ip": device_name_ip,
            "ipxd": ipxd,
        }
        return jsonify(system_info)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
