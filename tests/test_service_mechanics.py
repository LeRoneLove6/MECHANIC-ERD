import unittest
from datetime import datetime
from app import create_app
from app.models import db, ServiceMechanics, ServiceTickets, Mechanic, Customer
from app.blueprints.service_mechanics.schemas import servmech_schema, servmechs_schema

class TestServiceMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Create test customer
            self.customer = Customer(
                name="John Doe",
                email="jd@example.com",
                phone="123-4567",
                password="password"
            )
            db.session.add(self.customer)

            # Create test mechanic
            self.mechanic = Mechanic(
                name="Mike Smith",
                email="mike@example.com",
                phone="987-6543",
                salary=50.0
            )
            db.session.add(self.mechanic)
            db.session.commit()

            # Create test service ticket
            self.ticket = ServiceTickets(
                vin="1HGCM82633A004352",
                date_serviced=datetime.utcnow(),
                service_desc="Oil Change",
                customer_id=self.customer.id,
                mechanic_id=self.mechanic.id
            )
            db.session.add(self.ticket)
            db.session.commit()

            # Create initial ServiceMechanics entry
            self.servmech = ServiceMechanics(
                ticket_id=self.ticket.id,
                mechanic_id=self.mechanic.id
            )
            db.session.add(self.servmech)
            db.session.commit()

    # ----------------- Positive Tests -----------------

    def test_create_service_mechanic(self):
        with self.app.app_context():
            ticket = db.session.merge(self.ticket)
            mechanic = db.session.merge(self.mechanic)

            payload = {"ticket_id": ticket.id, "mechanic_id": mechanic.id}
            response = self.client.post('/service-mechanics/', json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['ticket_id'], ticket.id)
            self.assertEqual(response.json['mechanic_id'], mechanic.id)

    def test_get_service_mechanics(self):
        response = self.client.get('/service-mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_service_mechanic_by_ticket_id(self):
        with self.app.app_context():
            servmech = db.session.merge(self.servmech)
            response = self.client.get(f'/service-mechanics/{servmech.ticket_id}')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['ticket_id'], servmech.ticket_id)

    def test_update_service_mechanic(self):
        with self.app.app_context():
            servmech = db.session.merge(self.servmech)
            mechanic = db.session.merge(self.mechanic)

            payload = {"mechanic_id": mechanic.id}
            response = self.client.put(f'/service-mechanics/{servmech.ticket_id}', json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['mechanic_id'], mechanic.id)

    # ----------------- Negative Tests -----------------

    def test_invalid_service_mechanic_creation(self):
        with self.app.app_context():
            ticket = db.session.merge(self.ticket)

            # Missing mechanic_id
            payload = {"ticket_id": ticket.id}
            response = self.client.post('/service-mechanics/', json=payload)

            self.assertEqual(response.status_code, 400)
            self.assertIn("mechanic_id", response.json)  # Check for error message key

    