from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Mechanic, db
from .schemas import mechanic_schema, mechanics_schema

mechanics_bp = Blueprint('mechanics', __name__)

@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(mechanic_data)
    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic_data)), 201

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    all_mechanics = db.session.query(Mechanic).all()
    return jsonify(mechanics_schema.dump(all_mechanics)), 200

@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return jsonify(mechanic_schema.dump(mechanic)), 200

@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    try:
        updated_data = mechanic_schema.load(request.json, session=db.session, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in request.json.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"}), 200