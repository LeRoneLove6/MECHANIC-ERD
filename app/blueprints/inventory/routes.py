from flask import Blueprint, request, jsonify
from app.models import db, Inventory, ServiceTickets
from .schemas import InventorySchema

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json()
    if not data or 'part_name' not in data or 'price' not in data:
        return jsonify({'error': 'Missing part_name or price'}), 400

    new_item = Inventory(
        part_name=data['part_name'],
        price=data['price'],
        quantity=data.get('quantity', 0)
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(inventory_schema.dump(new_item)), 201


@inventory_bp.route('/', methods=['GET'])
def get_inventories():
    items = db.session.query(Inventory).all()
    return jsonify(inventories_schema.dump(items)), 200


@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({'error': 'Inventory item not found'}), 404
    return jsonify(inventory_schema.dump(item)), 200


@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({'error': 'Inventory item not found'}), 404

    data = request.get_json()
    item.part_name = data.get('part_name', item.part_name)
    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify(inventory_schema.dump(item)), 200


@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    item = db.session.get(Inventory, id)
    if not item:
        return jsonify({'error': 'Inventory item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Inventory item deleted successfully'}), 200


@inventory_bp.route('/<int:inventory_id>/assign_ticket', methods=['POST'])
def assign_part_to_ticket(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    if not item:
        return jsonify({'error': 'Inventory item not found'}), 404

    ticket_id = request.get_json().get('ticket_id')
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found'}), 404

    if ticket not in item.tickets:
        item.tickets.append(ticket)
        db.session.commit()

    return jsonify(inventory_schema.dump(item)), 200


@inventory_bp.route('/<int:inventory_id>/remove_ticket', methods=['POST'])
def remove_part_from_ticket(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    if not item:
        return jsonify({'error': 'Inventory item not found'}), 404

    ticket_id = request.get_json().get('ticket_id')
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found'}), 404

    if ticket in item.tickets:
        item.tickets.remove(ticket)
        db.session.commit()

    return jsonify(inventory_schema.dump(item)), 200
