from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel
from resources.item import Item

from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                data=json.dumps({'username': 'test', 'password': '1234'}),
                                headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT ' + auth_token

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 19.99})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.99, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('test'))
                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertIsNone(ItemModel.find_by_name('test'))
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/item/test', data={'price': 19.99, 'store_id':1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 19.99})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.post('/item/test', data={'price': 19.99, 'store_id':1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data), {'message': "An item with name 'test' already exists."})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                resp = client.put('/item/test', data={'price': 19.99, 'store_id':1})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 19.99})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                client.post('/item/test', data={'price': 19.99, 'store_id':1})
                resp = client.put('/item/test', data={'price': 17.99, 'store_id':1})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 17.99})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'items': [{'name': 'test', 'price': 19.99}]})
