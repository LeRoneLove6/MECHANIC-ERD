import unittest
from app import create_app
from app.models import db, Mechanic

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

           
            self.mechanic = Mechanic(
                name="Mike",
                email="mike@email.com",
                phone="987-6543",
                salary=50.00
            )
            db.session.add(self.mechanic)
            db.session.commit()

        self.client = self.app.test_client()

        self.new_mechanic_payload = {
            "name": "Jane",
            "email": "jane@email.com",
            "phone": "123-4567",
            "salary": 60.0
        }

        self.invalid_mechanic_payload = {
            "email": "no_name@email.com" 
        }

    # Utility function to merge detached instances
    def merge(self, instance):
        with self.app.app_context():
            return db.session.merge(instance)

   

    def test_create_mechanic(self):
        response = self.client.post('/mechanics/', json=self.new_mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane")

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_mechanic_by_id(self):
        mechanic = self.merge(self.mechanic)
        response = self.client.get(f'/mechanics/{mechanic.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mike")

    def test_update_mechanic(self):
        mechanic = self.merge(self.mechanic)
        update_payload = {"salary": 75.0}
        response = self.client.put(f'/mechanics/{mechanic.id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['salary'], 75.0)

    def test_delete_mechanic(self):
        mechanic = self.merge(self.mechanic)
        response = self.client.delete(f'/mechanics/{mechanic.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Mechanic deleted successfully")

    def test_search_mechanics(self):
        mechanic = self.merge(self.mechanic)
        response = self.client.get('/mechanics/search', query_string={"mechanic_name": "Mike"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(m['name'] == "Mike" for m in response.json))

    # ----------------- Negative Tests -----------------

    def test_get_nonexistent_mechanic(self):
        response = self.client.get('/mechanics/9999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Mechanic not found")

   