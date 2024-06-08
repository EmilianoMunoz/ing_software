from flask import jsonify, Blueprint, request
from app.services.cabin import CabinService
from app.models.response_message import ResponseBuilder
from app.mapping import ResponseSchema, CabinSchema
import socket
import random

cabin = Blueprint('cabin', __name__)
cabin_schema = CabinSchema()
response_schema = ResponseSchema()

@cabin.route('/', methods=['GET'])
def index():
    # Get the IP of localhost from flask
    myip = socket.gethostbyname(socket.gethostname())
    resp = jsonify({"microservicio": myip, "status": "ok"})
    resp.status_code = random.choice([200, 404])
    return resp

@cabin.route('/compensation', methods=['GET'])
def compensation():
    myip = request.remote_addr
    resp = jsonify({"microservicio": myip, "status": "ok"})
    resp.status_code = 200
    return resp

@cabin.route('/add', methods=['POST'])
def post_cabin():
    try:
        service = CabinService()
        cabin = cabin_schema.load(request.json)
        created_cabin = service.create(cabin)
        response = {"cabin": cabin_schema.dump(created_cabin)}
        return jsonify(response), 201
    except Exception as e:
        error_message = f"Error al agregar usuario: {str(e)}"
        return jsonify({"error": error_message}), 400

@cabin.route('/<int:id>', methods=['GET'])
def find(id):
    service = CabinService()
    raffle = service.find_by_id(id)

    if raffle:
        response_builder = ResponseBuilder()
        response_builder.add_message("Usuario encontrado").add_status_code(100).add_data(cabin_schema.dump(raffle))
        return jsonify(response_schema.dump(response_builder.build()))
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@cabin.route('/all', methods=['GET'])
def find_all():
    service = CabinService()
    response_builder = ResponseBuilder()
    cabins = service.find_all()
    cabins_json = [cabin_schema.dump(cabin) for cabin in cabins]
    response_builder.add_message("Usuarios encontrados").add_status_code(100).add_data({'cabins': cabins_json})
    return jsonify(response_schema.dump(response_builder.build()))

@cabin.route('/update/<int:cabin_id>', methods=['PUT'])
def update_cabin(cabin_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Datos de usuario no proporcionados"}), 400

        service = CabinService()
        updated_cabin = service.update(cabin_id, data)

        if updated_cabin:
            response_builder = ResponseBuilder()
            response_builder.add_message("Usuario actualizado con éxito").add_status_code(200).add_data(cabin_schema.dump(updated_cabin))
            return jsonify(response_schema.dump(response_builder.build()))

        return jsonify({"error": "El usuario no se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cabin.route('/delete/<int:cabin_id>', methods=['DELETE'])
def delete_cabin(cabin_id):
    try:
        service = CabinService()
        deleted = service.delete(cabin_id)

        if deleted:
            return jsonify({"message": "Usuario eliminado con éxito", "status_code": 200}), 200

        return jsonify({"error": "Usuario no encontrado", "status_code": 404}), 404
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500
