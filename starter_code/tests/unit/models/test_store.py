from starter_code.models.store import StoreModel
from starter_code.tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self) -> None:
        store = StoreModel('test')
        
        self.assertEqual(store.name,
                         'test',
                         "The name of the store after creation does not equal the constuctor argument")
        