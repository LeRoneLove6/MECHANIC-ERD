from sqlalchemy import select
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTickets, Mechanic, ServiceMechanics, Inventory, db
from .schemas import service_ticket_schema, service_tickets_schema

service_tickets_bp = Blueprint('service-tickets', __name__, url_prefix='/service-tickets')




# CREATE a service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(ticket_data)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket_data)), 201

# GET all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = db.session.query(ServiceTickets).all()
    return jsonify(service_tickets_schema.dump(tickets)), 200

# GET a single service ticket by ID
@service_tickets_bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    ticket = db.session.get(ServiceTickets, id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return jsonify(service_ticket_schema.dump(ticket)), 200

# UPDATE a service ticket
@service_tickets_bp.route('/<int:id>', methods=['PUT'])
def update_service_ticket(id):
    ticket = db.session.get(ServiceTickets, id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    try:
        updated_data = service_ticket_schema.load(request.json, session=db.session, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in request.json.items():
        setattr(ticket, key, value)

    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200

# DELETE a service ticket
@service_tickets_bp.route('/<int:id>', methods=['DELETE'])
def delete_service_ticket(id):
    ticket = db.session.get(ServiceTickets, id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"}), 200


# SEARCH service tickets by mechanic
@service_tickets_bp.route('/search', methods=['GET'])
def search_tickets_by_mechanic():
    mechanic_name = request.args.get('mechanic')
    if not mechanic_name:
        return jsonify({"error": "Please provide a mechanic name"}), 400

    query = (
        select(ServiceTickets)
        .join(ServiceMechanics, ServiceTickets.id == ServiceMechanics.ticket_id)
        .join(Mechanic, Mechanic.id == ServiceMechanics.mechanic_id)
        .where(Mechanic.name.ilike(f"%{mechanic_name}%"))
    )

    tickets = db.session.execute(query).scalars().all()
    return jsonify(service_tickets_schema.dump(tickets)), 200


# -----------------------------
# Many-to-Many Relationship Endpoints
# -----------------------------

# Assign a part to this service ticket
@service_tickets_bp.route('/<int:ticket_id>/add_part', methods=['POST'])
def add_part_to_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    part_id = request.json.get('inventory_id')
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Inventory part not found"}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200

# Remove a part from this service ticket
@service_tickets_bp.route('/<int:ticket_id>/remove_part', methods=['DELETE'])
def remove_part_from_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    part_id = request.json.get('inventory_id')
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Inventory part not found"}), 404

    if part in ticket.parts:
        ticket.parts.remove(part)
        db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# Assign a mechanic to this service ticket
@service_tickets_bp.route('/<int:ticket_id>/add_mechanic', methods=['POST'])
def add_mechanic_to_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    mechanic_id = request.json.get('mechanic_id')
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    exists = db.session.query(ServiceMechanics).filter_by(
        ticket_id=ticket.id, mechanic_id=mechanic.id
    ).first()

    if not exists:
        link = ServiceMechanics(ticket_id=ticket.id, mechanic_id=mechanic.id)
        db.session.add(link)
        db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 200

# Remove a mechanic from this service ticket
@service_tickets_bp.route('/<int:ticket_id>/remove_mechanic', methods=['POST'])
def remove_mechanic_from_ticket(ticket_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    mechanic_id = request.json.get('mechanic_id')
    link = db.session.query(ServiceMechanics).filter_by(
        ticket_id=ticket.id, mechanic_id=mechanic_id
    ).first()

    if link:
        db.session.delete(link)
        db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 200
