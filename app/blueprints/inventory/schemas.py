from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from app.models import Inventory, ServiceTickets


# Nested schemas 

class NestedServiceTicketSchema(SQLAlchemySchema):
    class Meta:
        model = ServiceTickets
        load_instance = True

    id = auto_field()
    service_desc = auto_field()
    vin = auto_field()
    date_serviced = auto_field()
    customer_id = auto_field()


class NestedInventorySchema(SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True

    id = auto_field()
    part_name = auto_field()
    price = auto_field()
    quantity = auto_field()



class InventorySchema(SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True

    id = auto_field()
    part_name = auto_field()
    price = auto_field()
    quantity = auto_field()
    # Include related tickets 
    tickets = fields.Nested(NestedServiceTicketSchema, many=True)


class ServiceTicketsSchema(SQLAlchemySchema):
    class Meta:
        model = ServiceTickets
        load_instance = True

    id = auto_field()
    vin = auto_field()
    date_serviced = auto_field()
    service_desc = auto_field()
    customer_id = auto_field()
    # Include related parts 
    parts = fields.Nested(NestedInventorySchema, many=True)



inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)
