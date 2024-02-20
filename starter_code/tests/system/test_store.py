import json
from typing import Any

from models.store import StoreModel
from tests.base_test import BaseTest
from models.item import ItemModel


class StoreTest(BaseTest):
    def test_create_store(self) -> None:
        with self.app() as client:
            with self.app_context():
                response: Any = client.post('/store/test')
                
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertEqual({'id': 1, 'name': 'test', 'items': []},
                                 json.loads(response.data))
                
    
    def test_create_duplicated_store(self) -> None:
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response: Any = client.post('/store/test')
                
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {'message': "A store with name 'test' already exists."},
                    json.loads(response.data)
                )
    
    def test_delete_store(self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response: Any = client.delete('/store/test')
                
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(
                    StoreModel.find_by_name('test'),
                    json.loads(response.data)
                )

    def test_find_store(self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response: Any = client.get('/store/test')
                
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {'id': 1, 'name': 'test', 'items': []},
                    json.loads(response.data)
                )

    def test_store_not_found(self) -> None:
        with self.app() as client:
            with self.app_context():
                response: Any = client.get('/store/test')
                
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(
                    {'message': 'Store not found'},
                    json.loads(response.data)
                )
    
    def test_store_found_with_items(self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response: Any = client.get('/store/test')
                
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {'id': 1, 'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]},
                    json.loads(response.data)
                )

    def test_store_list(self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response: Any = client.get('/stores')
                
                self.assertEqual(
                    {'stores': [{'id': 1, 'name': 'test', 'items': []}]},
                    json.loads(response.data)
                )
    
    def test_store_list_with_items(self) -> None:
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response: Any = client.get('/stores')
                
                self.assertEqual(
                    {'stores': [{'name': 'test',
                                 'items': [
                                     {'id': 1, 'name': 'test','price': 19.99}]}]},
                    json.loads(response.data)
                )
