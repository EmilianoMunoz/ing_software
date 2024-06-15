from flask import jsonify, Blueprint, request
from app.services.cabin import CabinService
from app.models.response_message import ResponseBuilder
from app.mapping import ResponseSchema, CabinSchema
import socket
import random
import logging 

cabin = Blueprint('cabin', __name__)
cabin_schema = CabinSchema()
response_schema = ResponseSchema()

@cabin.route('/', methods=['GET'])
def index():
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
        error_message = f"Error al agregar cabaña: {str(e)}"
        return jsonify({"error": error_message}), 400

@cabin.route('/<int:id>', methods=['GET'])
def find(id):
    service = CabinService()
    cabin = service.find_by_id(id)

    if cabin:
        response_builder = ResponseBuilder()
        response_builder.add_message("Cabaña encontrada").add_status_code(100).add_data(cabin_schema.dump(cabin))
        return jsonify(response_schema.dump(response_builder.build()))
    else:
        return jsonify({"error": "Cabaña no encontrada"}), 404

@cabin.route('/all', methods=['GET'])
def find_all():
    logging.debug("Received GET request for all cabins")
    try:
        service = CabinService()
        response_builder = ResponseBuilder()
        logging.debug("CabinService instantiated")
        
        cabins = service.find_all()
        logging.debug(f"Cabins found: {cabins}")

        if not cabins:
            logging.error("No cabins found")
            response_builder.add_message("No se encontraron cabañas").add_status_code(404).add_data({})
            return jsonify(response_schema.dump(response_builder.build())), 404

        cabins_json = [cabin_schema.dump(cabin) for cabin in cabins]
        logging.debug(f"Cabins JSON: {cabins_json}")

        response_builder.add_message("Cabañas encontradas").add_status_code(200).add_data({'cabins': cabins_json})
        logging.debug("Message, status code, and data added to response builder")

        response = response_builder.build()
        logging.debug(f"Response built: {response}")

        return jsonify(response_schema.dump(response)), 200
    except Exception as e:
        logging.error(f"Error in find_all: {str(e)}")
        return jsonify({"error": f"Error general: {str(e)}"}), 500

@cabin.route('/update/<int:cabin_id>', methods=['PUT'])
def update_cabin(cabin_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Datos de cabaña no proporcionados"}), 400

        service = CabinService()
        updated_cabin = service.update(cabin_id, data)

        if updated_cabin:
            response_builder = ResponseBuilder()
            response_builder.add_message("Cabaña actualizada con éxito").add_status_code(200).add_data(cabin_schema.dump(updated_cabin))
            return jsonify(response_schema.dump(response_builder.build()))

        return jsonify({"error": "La cabaña no se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cabin.route('/delete/<int:cabin_id>', methods=['DELETE'])
def delete_cabin(cabin_id):
    try:
        service = CabinService()
        deleted = service.delete(cabin_id)

        if deleted:
            return jsonify({"message": "Cabaña eliminada con éxito", "status_code": 200}), 200

        return jsonify({"error": "Cabaña no encontrada", "status_code": 404}), 404
    except Exception as e:
        return jsonify({"error": str(e), "status_code": 500}), 500
