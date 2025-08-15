from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Customer




class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)        