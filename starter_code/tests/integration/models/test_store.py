from typing import Any

from starter_code.models.store import StoreModel
from starter_code.models.item import ItemModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_intems_empty(self) -> None:
        store: StoreModel = StoreModel('test')
        
        self.assertListEqual(store.items.all(),
                             [],
                             "The store's items length was not 0 even though no items were added.")

    def test_crud(self) -> None:
        with self.app_context():
            store: StoreModel = StoreModel('test')        
            self.assertIsNone(StoreModel.find_by_name('test'))
            
            store.save_to_db()        
            self.assertIsNotNone(StoreModel.find_by_name('test'))
            
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test'))
    
    def test_store_relationship(self) -> None:
        with self.app_context():
            store: StoreModel = StoreModel('test')
            item: ItemModel = ItemModel('test_item', 19.99, 1)
            
            store.save_to_db()
            item.save_to_db()
            
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')
    
    def test_store_json(self) -> None:
        store = StoreModel('test')
        
        expected:dict[str, str | Any] = {
            'id': None,
            "name": 'test',
            "items": []
        }
        
        self.assertDictEqual(store.json(), expected)
    
    def test_store_json_with_item(self) -> None:
        with self.app_context():
            store: StoreModel = StoreModel('test')
            item: ItemModel = ItemModel('test_item', 19.99, 1)
            
            store.save_to_db()
            item.save_to_db()
        
            expected: dict[str, str | Any] = {
                'id': None,
                "name": 'test',
                "items": [{"name": "test_item", "price": 19.99}]
            }
            
            self.assertDictEqual(store.json(), expected)
