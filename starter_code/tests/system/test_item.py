import json
from typing import Any, Dict

from starter_code.models.store import StoreModel
from starter_code.models.user import UserModel
from starter_code.models.item import ItemModel
from starter_code.tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self) -> None:
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_resp: Any = client.post(
                    '/auth',
                    data=json.dumps(
                        {'username': 'test', 'password': '1234'}
                    ),
                    headers={'Content-Type': 'application/json'}
                )
                auth_token: Any = json.loads(auth_resp.data)['access_token']
                self.access_token: Any = f'JWT {auth_token}'
                
    def test_get_item_no_auth (self) -> None:
        with self.app() as client:
            with self.app_context():
                response: Any = client.get('(/item/test)')
                self.assertEqual(response.status_code, 404)
    
    def test_get_item_no_found (self) -> None:
        with self.app() as client:
            with self.app_context():
                resp: Any = client.get(
                    '/item/test',
                    headers={"Authorization": self.access_token}
                )
                self.assertEqual(resp.status_code, 404)
    
    def test_get_item (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp: Any = client.get(
                    '/item/test',
                    headers={"Authorization": self.access_token}
                )
                self.assertEqual(resp.status_code, 200)
    
    def test_delete_item (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                
                resp: Any = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    {'message': 'Item deleted'},
                    json.loads(resp.data)
                )
    
    def test_create_item (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                
                resp: Any = client.post(
                    '/item/test',
                    data={'price': 17.99, 'store_id': 1}
                )
                
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(
                    {'name': 'test', 'price': 17.99},
                    json.loads(resp.data)
                )

    def test_create_duplicate_item (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                
                resp: Any = client.post(
                    '/item/test',
                    data={'price': 17.99, 'store_id': 1}
                )
                
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(
                    {'message': "An item with name 'test' already exists."},
                    json.loads(resp.data)
                )
    
    def test_put_item (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                
                resp: Any = client.put(
                    '/item/test',
                    data={'price': 17.99, 'store_id': 1}
                )

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(
                    {'name': 'test', 'price': 17.99},
                    json.loads(resp.data)
                )

    def test_put_update_item (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                
                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)
                
                resp: Any = client.put(
                    '/item/test',
                    data={'price': 17.99, 'store_id': 1}
                )
                
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(
                    {'name': 'test', 'price': 17.99},
                    json.loads(resp.data)
                )

    def test_item_list (self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                
                resp: Any = client.get('/items')
                
                self.assertDictEqual(
                    {'items': [{'name': 'test', 'price': 5.99}]},
                    json.loads(resp.data)
                )
