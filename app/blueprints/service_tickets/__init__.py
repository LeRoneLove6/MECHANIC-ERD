from flask import Blueprint


service_tickets_bp = Blueprint(
    "service_tickets",  
    __name__,           
    url_prefix="/service_tickets"  
)

from app.blueprints.service_tickets.routes import (
    create_service_ticket,
    get_service_tickets,
    get_service_ticket,
    update_service_ticket,
    delete_service_ticket
)
