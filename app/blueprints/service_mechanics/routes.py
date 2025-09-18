from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import ServiceMechanics, db
from .schemas import servmech_schema, servmechs_schema

service_mechanics_bp = Blueprint('service_mechanics', __name__)

@service_mechanics_bp.route('/', methods=['POST'])
def create_service_mechanic():
    try:
        servmech_data = servmech_schema.load(request.json, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(servmech_data)
    db.session.commit()
    return jsonify(servmech_schema.dump(servmech_data)), 200

@service_mechanics_bp.route('/', methods=['GET'])
def get_service_mechanics():
    all_servmechs = db.session.query(ServiceMechanics).all()
    return jsonify(servmechs_schema.dump(all_servmechs)), 200

@service_mechanics_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_mechanic(ticket_id):
    servmech = db.session.get(ServiceMechanics, ticket_id)
    if not servmech:
        return jsonify({"error": "ServiceMechanic not found"}), 400
    return jsonify(servmech_schema.dump(servmech)), 200

@service_mechanics_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_mechanic(ticket_id):
    servmech = db.session.get(ServiceMechanics, ticket_id)
    if not servmech:
        return jsonify({"error": "ServiceMechanic not found"}), 400
    try:
        updated_data = servmech_schema.load(request.json, session=db.session, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in request.json.items():
        setattr(servmech, key, value)
    db.session.commit()
    return jsonify(servmech_schema.dump(servmech)), 200

