from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from app.models import Customer


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


# For login only
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

login_schema = LoginSchema()
