from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Customer, ServiceTickets, db
from .schemas import service_ticket_schema, service_tickets_schema



service_tickets_bp = Blueprint('service_tickets', __name__)

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(service_ticket_data)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(service_ticket_data)), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    all_service_tickets = db.session.query(ServiceTickets).all()
    return jsonify(service_tickets_schema.dump(all_service_tickets)), 200

@service_tickets_bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    service_ticket = db.session.get(ServiceTickets, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return jsonify(service_ticket_schema.dump(service_ticket)), 200

@service_tickets_bp.route('/<int:id>', methods=['PUT'])
def update_service_ticket(id):
    service_ticket = db.session.get(ServiceTickets, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    try:
        updated_data = service_ticket_schema.load(request.json, session=db.session, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in request.json.items():
        setattr(service_ticket, key, value)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(service_ticket)), 200

@service_tickets_bp.route('/<int:id>', methods=['DELETE'])
def delete_service_ticket(id):
    customer = db.session.get(Customer, id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"}), 200