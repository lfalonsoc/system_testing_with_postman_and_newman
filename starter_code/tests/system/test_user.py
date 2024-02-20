import json
from typing import Any

from starter_code.models.user import UserModel
from base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self) -> None:
        with self.app() as client:
            with self.app_context():
                response : Any = client.post (
                    '/register',
                    data={'username': 'test', 'password': '1234'}
                )
                
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User create successfully.'},
                                     json.loads(response.data))
    
    def test_registerand_login(self) -> None:
        with self.app() as client:
            with self.app_context():
                client.post (
                    '/register',
                    data={'username': 'test', 'password': '1234'}
                )
                auth_response : Any = client.post (
                    '/auth',
                    data=json.dumps({'username': 'test', 'password': '1234'}),
                    headers={'Content-Type': 'application/json'}
                )
                
                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_ducplicate_user(self) -> None:
        with self.app() as client:
            with self.app_context():
                client.post (
                    '/register',
                    data={'username': 'test', 'password': '1234'}
                )
                response : Any = client.post (
                    '/register',
                    data={'username': 'test', 'password': '1234'}
                )
                
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {'message': 'A user with that username already exists.'},
                    json.loads(response.data)
                )
