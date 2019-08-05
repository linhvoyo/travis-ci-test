from models.store import StoreModel
from tests.unit.base_test_unit import UnitBaseTest

class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test', 
                        "The name of the store after creation does not equal 'test'")