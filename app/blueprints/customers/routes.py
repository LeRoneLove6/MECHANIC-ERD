from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import Customer, db
from .schemas import customer_schema, customers_schema

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(customer_data)
    db.session.commit()
    return jsonify(customer_schema.dump(customer_data)), 200


@customers_bp.route('/', methods=['GET'])
def get_customers():
    all_customers = db.session.query(Customer).all()
    return jsonify(customers_schema.dump(all_customers)), 200

@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 400
        
    return jsonify(customer_schema.dump(customer)), 200

@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 400
        
    try:
        updated_data = customer_schema.load(request.json, session=db.session, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in request.json.items():
        setattr(customer, key, value)
    db.session.commit()
    return jsonify(customer_schema.dump(customer)), 200

@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200