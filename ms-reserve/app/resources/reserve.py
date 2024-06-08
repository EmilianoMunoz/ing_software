from flask import jsonify, Blueprint, request
from app.services.reserve import ReserveService
from app.models.response_message import ResponseBuilder
from app.mapping import ResponseSchema, ReserveSchema
import socket
import random

reserve = Blueprint('reserve', __name__)
reserve_schema = ReserveSchema()
response_schema = ResponseSchema()

@reserve.route('/', methods=['GET'])
def index():
    # Get the IP of localhost from flask
    myip = socket.gethostbyname(socket.gethostname())
    resp = jsonify({"microservicio": myip, "status": "ok"})
    resp.status_code = random.choice([200, 404])
    return resp

@reserve.route('/compensation', methods=['GET'])
def compensation():
    myip = request.remote_addr
    resp = jsonify({"microservicio": myip, "status": "ok"})
    resp.status_code = 200
    return resp

@reserve.route('/add', methods=['POST'])
def post_reserve():
    try:
        service = ReserveService()
        reserve = reserve_schema.load(request.json)
        created_reserve = service.create(reserve)
        response = {"reserve": reserve_schema.dump(created_reserve)}
        return jsonify(response), 201
    except Exception as e:
        error_message = f"Error al agregar usuario: {str(e)}"
        return jsonify({"error": error_message}), 400

@reserve.route('/<int:id>', methods=['GET'])
def find(id):
    service = ReserveService()
    raffle = service.find_by_id(id)

    if raffle:
        response_builder = ResponseBuilder()
        response_builder.add_message("Usuario encontrado").add_status_code(100).add_data(reserve_schema.dump(raffle))
        return jsonify(response_schema.dump(response_builder.build()))
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@reserve.route('/all', methods=['GET'])
def find_all():
    service = ReserveService()
    response_builder = ResponseBuilder()
    reserves = service.find_all()
    reserves_json = [reserve_schema.dump(reserve) for reserve in reserves]
    response_builder.add_message("Usuarios encontrados").add_status_code(100).add_data({'reserves': reserves_json})
    return jsonify(response_schema.dump(response_builder.build()))

@reserve.route('/update/<int:reserve_id>', methods=['PUT'])
def update_reserve(reserve_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Datos de usuario no proporcionados"}), 400

        service = ReserveService()
        updated_reserve = service.update(reserve_id, data)

        if updated_reserve:
            response_builder = ResponseBuilder()
            response_builder.add_message("Usuario actualizado con éxito").add_status_code(200).add_data(reserve_schema.dump(updated_reserve))
            return jsonify(response_schema.dump(response_builder.build()))

        return jsonify({"error": "El usuario no se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reserve.route('/delete/<int:reserve_id>', methods=['DELETE'])
def delete_reserve(reserve_id):
    try:
        service = ReserveService()
        deleted = service.delete(reserve_id)

        if deleted:
            return jsonify({"message": "Usuario eliminado con éxito", "status_code": 200}), 200

        return jsonify({"error": "Usuario no encontrado", "status_code": 404}), 404
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500