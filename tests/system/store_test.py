from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client: 
            with self.app_context():
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'items': []})


    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                self.assertIsNotNone(StoreModel.find_by_name('test'))

                resp = client.post('/store/test')
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data),
                                    {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.delete('/store/test')
                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(resp.data),
                                    {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test')
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/store/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name':'test',
                                                            'items': [{
                                                                'name': 'test',
                                                                'price': 19.99}]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.get('/stores')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {
                    'stores': [{'name': 'test', 'items': []}]
                })


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/stores')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {
                    'stores': [{'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]
                })

                