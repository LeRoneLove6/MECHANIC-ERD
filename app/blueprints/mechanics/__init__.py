from flask import Blueprint

mechanics_bp = Blueprint('mechanics', __name__)

from .routes import (
    create_mechanic,
    get_mechanics, 
    get_mechanic,
    update_mechanic,
    delete_mechanic
)
