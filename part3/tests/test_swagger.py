import unittest

from app import create_app


class SwaggerDocsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_swagger_ui_is_available(self):
        response = self.client.get('/docs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HBnB API', response.data)

    def test_swagger_spec_is_available(self):
        response = self.client.get('/swagger.json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'api', response.data)


if __name__ == '__main__':
    unittest.main()
