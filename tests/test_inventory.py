import unittest
from datetime import datetime, timezone
from app import create_app
from app.models import db, Inventory, ServiceTickets, Customer, Mechanic

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            
            self.customer = Customer(
                name="John Doe",
                email="jd@email.com",
                phone="123-4567",
                password="123"
            )
            db.session.add(self.customer)

            
            self.mechanic = Mechanic(
                name="Mike",
                email="mike@email.com",
                phone="987-6543",
                salary=50.00
            )
            db.session.add(self.mechanic)
            db.session.commit()

            
            self.ticket = ServiceTickets(
                vin="1HGCM82633A004352",
                date_serviced=datetime.now(timezone.utc),
                service_desc="Brake replacement",
                customer_id=self.customer.id,
                mechanic_id=self.mechanic.id
            )
            db.session.add(self.ticket)
            db.session.commit()

           
            self.inventory = Inventory(
                part_name="Brake Pad",
                quantity=10,
                price=50.0
            )
            db.session.add(self.inventory)
            db.session.commit()

            # Refresh all instances to bind them to the session
            db.session.refresh(self.customer)
            db.session.refresh(self.mechanic)
            db.session.refresh(self.ticket)
            db.session.refresh(self.inventory)

        self.client = self.app.test_client()

        self.new_inventory_payload = {
            "part_name": "Oil Filter",
            "quantity": 5,
            "price": 15.0
        }
        self.invalid_inventory_payload = {
            "quantity": 5  
        }

   

    def test_create_inventory(self):
        response = self.client.post('/inventory/', json=self.new_inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], "Oil Filter")

    def test_get_inventories(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_inventory_by_id(self):
        with self.app.app_context():
            inventory = db.session.merge(self.inventory)
            response = self.client.get(f'/inventory/{inventory.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['part_name'], "Brake Pad")

    def test_update_inventory(self):
        with self.app.app_context():
            inventory = db.session.merge(self.inventory)
            update_payload = {"quantity": 20, "price": 55.0}
            response = self.client.put(f'/inventory/{inventory.id}', json=update_payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['quantity'], 20)
            self.assertEqual(response.json['price'], 55.0)

    def test_delete_inventory(self):
        with self.app.app_context():
            inventory = db.session.merge(self.inventory)
            response = self.client.delete(f'/inventory/{inventory.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], "Inventory item deleted successfully")

    def test_assign_part_to_ticket(self):
        with self.app.app_context():
            inventory = db.session.merge(self.inventory)
            ticket = db.session.merge(self.ticket)

            
            if ticket not in inventory.tickets:
                inventory.tickets.append(ticket)
                db.session.commit()

            payload = {"ticket_id": ticket.id}
            response = self.client.post(f'/inventory/{inventory.id}/assign_ticket', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn(ticket.id, [t['id'] for t in response.json.get('tickets', [])])

    def test_remove_part_from_ticket(self):
        with self.app.app_context():
            inventory = db.session.merge(self.inventory)
            ticket = db.session.merge(self.ticket)

           
            if ticket not in inventory.tickets:
                inventory.tickets.append(ticket)
                db.session.commit()

            payload = {"ticket_id": ticket.id}
            response = self.client.post(f'/inventory/{inventory.id}/remove_ticket', json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(ticket.id, [t['id'] for t in response.json.get('tickets', [])])

    # ----------------- Negative Tests -----------------

    def test_invalid_inventory_creation(self):
        response = self.client.post('/inventory/', json=self.invalid_inventory_payload)
        self.assertEqual(response.status_code, 400)
