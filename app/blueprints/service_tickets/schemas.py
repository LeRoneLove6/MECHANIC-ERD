from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import ServiceTickets
from marshmallow import fields

class ServiceTicketsSchema(SQLAlchemyAutoSchema):
    customer_id = fields.Int(required=True)  # explicitly add it

    class Meta:
        model = ServiceTickets
        load_instance = True

service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)
