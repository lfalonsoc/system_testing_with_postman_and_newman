from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self) -> None:
        with self.app_context():
            StoreModel("test").save_to_db()
            item: ItemModel = ItemModel('test', 19.99, 1)
            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self) -> None:
        with self.app_context():
            store: StoreModel = StoreModel('test_store')
            item: ItemModel = ItemModel('test', 19.99, 1)
            
            store.save_to_db()
            item.save_to_db()
            
            self.assertEqual(item.store.name, 'test_store')
