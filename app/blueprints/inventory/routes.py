from flask import Blueprint, request, jsonify
from app.models import db, Inventory, ServiceTickets
from .schemas import InventorySchema

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json()
    new_item = Inventory(
        part_name=data['part_name'],
        price=data['price']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(inventory_schema.dump(new_item)), 201


@inventory_bp.route('/', methods=['GET'])
def get_inventories():
    items = Inventory.query.all()
    return jsonify(inventories_schema.dump(items))

@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory(id):
    item = Inventory.query.get_or_404(id)
    return jsonify(inventory_schema.dump(item))

# UPDATE an inventory item
@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    item = Inventory.query.get_or_404(id)
    data = request.get_json()
    item.part_name = data.get('part_name', item.part_name)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify(inventory_schema.dump(item))

# DELETE an inventory item
@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Inventory item deleted successfully'})



# Assign a part to a service ticket
@inventory_bp.route('/<int:inventory_id>/assign_ticket', methods=['POST'])
def assign_part_to_ticket(inventory_id):
    item = Inventory.query.get_or_404(inventory_id)
    ticket_id = request.get_json().get('ticket_id')
    ticket = ServiceTickets.query.get_or_404(ticket_id)
    
    if ticket not in item.tickets:
        item.tickets.append(ticket)
        db.session.commit()
    return jsonify(inventory_schema.dump(item))

# Remove a part from a service ticket
@inventory_bp.route('/<int:inventory_id>/remove_ticket', methods=['POST'])
def remove_part_from_ticket(inventory_id):
    item = Inventory.query.get_or_404(inventory_id)
    ticket_id = request.get_json().get('ticket_id')
    ticket = ServiceTickets.query.get_or_404(ticket_id)
    
    if ticket in item.tickets:
        item.tickets.remove(ticket)
        db.session.commit()
    return jsonify(inventory_schema.dump(item))
