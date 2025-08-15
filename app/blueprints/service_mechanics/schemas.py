from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import ServiceMechanics

class ServiceMechanicsSchema(SQLAlchemyAutoSchema):
    ticket_id = fields.Int(required=True)
    mechanic_id = fields.Int(required=True)

    class Meta:
        model = ServiceMechanics
        load_instance = True


servmech_schema = ServiceMechanicsSchema()
servmechs_schema = ServiceMechanicsSchema(many=True)