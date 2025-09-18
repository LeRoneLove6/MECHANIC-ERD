import unittest
from datetime import datetime
from app import create_app
from app.models import db, Customer
from app.utils.utils import encode_token

class TestCustomer(unittest.TestCase):
    def setUp(self):
        
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

        
        with self.app.app_context():
            self.customer = Customer(
                name="John Doe",
                email="jd@email.com",
                phone="123-4567",
                password="123"
                
            )
            db.session.add(self.customer)
            db.session.commit()
            db.session.refresh(self.customer)  # ensures instance is bound
            # Generate auth token while session is active
            self.token = encode_token(self.customer.id)

       
        self.new_customer_payload = {
            "name": "Alice",
            "email": "alice@email.com",
            "phone": "555-1234",
            "password": "abc"
        }
        self.invalid_customer_payload = {
            "name": "Bob",
            "email": ""  
        }

    

    def test_create_customer(self):
        """Test creating a new customer"""
        response = self.client.post('/customers/', json=self.new_customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Alice")

    def test_valid_login(self):
        """Test customer login with valid credentials"""
        payload = {"email": "jd@email.com", "password": "123"}
        response = self.client.post('/customers/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_update_customer(self):
        """Test token-authenticated customer update"""
        update_payload = {"name": "Peter", "phone": "", "email": "", "password": ""}
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.put(f'/customers/{self.customer.id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Peter")

    def test_delete_customer(self):
        """Test deleting a customer"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.delete(f'/customers/{self.customer.id}', headers=headers)
        self.assertEqual(response.status_code, 401)

    # ----------------- Negative Test -----------------

    def test_invalid_creation(self):
        member_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/customers/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

