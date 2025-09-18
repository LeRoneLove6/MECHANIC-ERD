from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from .schemas import customer_schema, customers_schema, login_schema
from app.extensions import limiter
from app.utils.utils import encode_token, token_required


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")



# LOGIN

@customers_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials["email"]
        password = credentials["password"]
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password:
        token = encode_token(customer.id)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": token
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid email or password"
    }), 400



# CREATE CUSTOMER

@customers_bp.route("/", methods=["POST"])
@limiter.limit("15 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.add(customer_data)
    db.session.commit()

    return jsonify(customer_schema.dump(customer_data)), 201



# GET ALL CUSTOMERS 

@customers_bp.route("/", methods=["GET"])
def get_customers():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = select(Customer)
    customers = db.paginate(query, page=page, per_page=per_page)

    return jsonify({
        "items": customers_schema.dump(customers.items),
        "total": customers.total,
        "page": customers.page,
        "pages": customers.pages
    }), 200



# GET SINGLE CUSTOMER

@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer_schema.dump(customer)), 200



# UPDATE CUSTOMER

@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        updated_data = customer_schema.load(request.json, session=db.session, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in updated_data.__dict__.items():
        if key != "_sa_instance_state":  # skip SQLAlchemy internals
            setattr(customer, key, value)

    db.session.commit()
    return jsonify(customer_schema.dump(customer)), 200

# DELETE CUSTOMER

@customers_bp.route("/<int:id>", methods=["DELETE"])
@limiter.limit("5 per day")
@token_required
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200
