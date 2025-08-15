from flask import Blueprint

customers_bp = Blueprint('customers', __name__)

from .routes import (
    create_customer,
    get_customers,  
    get_customer,
    update_customer,
    delete_customer
)

