from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from app.models import ServiceTickets, Inventory



class NestedInventorySchema(SQLAlchemySchema):
   
    class Meta:
        model = Inventory
        load_instance = True

    id = auto_field()
    part_name = auto_field()
    price = auto_field()


class NestedServiceTicketSchema(SQLAlchemySchema):
  
    class Meta:
        model = ServiceTickets
        load_instance = True

    id = auto_field()
    service_desc = auto_field()




class ServiceTicketsSchema(SQLAlchemySchema):
    class Meta:
        model = ServiceTickets
        load_instance = True

    id = auto_field()
    vin = auto_field()
    date_serviced = auto_field()
    service_desc = auto_field()
    customer_id = auto_field()
    mechanic_id = auto_field()

    # Use NestedInventorySchema here to avoid recursion conflicts
    parts = fields.Nested(NestedInventorySchema, many=True)


class InventorySchema(SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True

    id = auto_field()
    part_name = auto_field()
    price = auto_field()

    # Use NestedServiceTicketSchema to avoid recursion conflicts
    tickets = fields.Nested(NestedServiceTicketSchema, many=True)




service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
