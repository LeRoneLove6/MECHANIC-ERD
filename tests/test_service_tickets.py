import unittest
from datetime import datetime
from app import create_app
from app.models import db, ServiceTickets, Customer, Mechanic
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            
            self.customer = Customer(
                name="John Doe",
                email="jd@example.com",
                phone="123-4567",
                password="password"
            )
            db.session.add(self.customer)

            
            self.mechanic = Mechanic(
                name="Mike Smith",
                email="mike@example.com",
                phone="987-6543",
                salary=50.0
            )
            db.session.add(self.mechanic)
            db.session.commit()

           
            self.ticket = ServiceTickets(
                vin="1HGCM82633A004352",
                date_serviced=datetime.utcnow(),
                service_desc="Oil Change",
                customer_id=self.customer.id,
                mechanic_id=self.mechanic.id
            )
            db.session.add(self.ticket)
            db.session.commit()

  

    def test_create_service_ticket(self):
        with self.app.app_context():
            customer = db.session.merge(self.customer)
            mechanic = db.session.merge(self.mechanic)

            payload = {
                "vin": "2HGCM82633A004353",
                "date_serviced": datetime.utcnow().isoformat(),
                "service_desc": "Brake Replacement",
                "customer_id": customer.id,
                "mechanic_id": mechanic.id
            }
            response = self.client.post('/service-tickets/', json=payload)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['vin'], "2HGCM82633A004353")
            self.assertEqual(response.json['customer_id'], customer.id)
            self.assertEqual(response.json['mechanic_id'], mechanic.id)

    def test_get_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_service_ticket_by_id(self):
        with self.app.app_context():
            ticket = db.session.merge(self.ticket)
            response = self.client.get(f'/service-tickets/{ticket.id}')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], ticket.id)

    def test_update_service_ticket(self):
        with self.app.app_context():
            ticket = db.session.merge(self.ticket)
            mechanic = db.session.merge(self.mechanic)

            payload = {"service_desc": "Updated Service", "mechanic_id": mechanic.id}
            response = self.client.put(f'/service-tickets/{ticket.id}', json=payload)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['service_desc'], "Updated Service")
            self.assertEqual(response.json['mechanic_id'], mechanic.id)

    def test_delete_service_ticket(self):
        with self.app.app_context():
            ticket = db.session.merge(self.ticket)
            response = self.client.delete(f'/service-tickets/{ticket.id}')

            self.assertEqual(response.status_code, 200)
            self.assertIn("deleted successfully", response.json['message'].lower())

    # ----------------- Negative Tests -----------------

    def test_invalid_service_ticket_creation(self):
        # Missing required fields
        payload = {"vin": "12345"}
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

   