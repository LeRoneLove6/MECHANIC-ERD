from flask import Blueprint, request, jsonify
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic


class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)