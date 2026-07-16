import unittest

from app import create_app


class ApiEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_with_valid_payload(self):
        payload = {
            'first_name': 'Ghaida',
            'last_name': 'alsabti',
            'email': 'alsabtighaida@gmail.com'
        }
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('first_name', response.get_json())
        self.assertEqual(response.get_json()['first_name'], 'Ghaida')

    def test_create_user_with_invalid_email_returns_400(self):
        payload = {
            'first_name': 'Ghaida',
            'last_name': 'alsabti',
            'email': 'bad-email'
        }
        response = self.client.post('/api/v1/users/', json=payload)
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
