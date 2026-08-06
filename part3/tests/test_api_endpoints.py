import unittest

from app import create_app
from app.services import facade


class ApiEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # POST /api/v1/users/ is admin-only, so tests bootstrap an admin
        # directly through the facade (bypassing the API) and log in.
        facade.create_user({
            'first_name': 'Admin',
            'last_name': 'Istrator',
            'email': 'admin@example.com',
            'password': 'adminpass',
            'is_admin': True
        })
        login = self.client.post('/api/v1/auth/login', json={
            'email': 'admin@example.com',
            'password': 'adminpass'
        })
        token = login.get_json()['access_token']
        self.admin_headers = {'Authorization': f'Bearer {token}'}

    def test_create_user_requires_authentication(self):
        payload = {
            'first_name': 'Ghaida',
            'last_name': 'alsabti',
            'email': 'alsabtighaida@gmail.com',
            'password': 'supersecret'
        }
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_create_user_with_valid_payload(self):
        payload = {
            'first_name': 'Ghaida',
            'last_name': 'alsabti',
            'email': 'alsabtighaida@gmail.com',
            'password': 'supersecret'
        }
        response = self.client.post('/api/v1/users/', json=payload, headers=self.admin_headers)
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertIn('id', body)
        self.assertNotIn('password', body)

    def test_create_user_with_invalid_email_returns_400(self):
        payload = {
            'first_name': 'Ghaida',
            'last_name': 'alsabti',
            'email': 'bad-email',
            'password': 'supersecret'
        }
        response = self.client.post('/api/v1/users/', json=payload, headers=self.admin_headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(response.get_json()['error'], 'Invalid email address')

    def test_amenities_endpoint_is_available(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_places_endpoint_is_available(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_reviews_endpoint_is_available(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
