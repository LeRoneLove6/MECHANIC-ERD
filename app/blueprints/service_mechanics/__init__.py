from flask import Blueprint

service_mechanics_bp = Blueprint('service_mechanics', __name__)

from .routes import (
    create_service_mechanic,
    get_service_mechanics,
    get_service_mechanic,
    update_service_mechanic,
)
