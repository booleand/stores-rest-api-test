from tests.base_test import BaseTest
from models.store import StoreModel
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                check_store_response = client.get('/store/storename')
                self.assertEqual(check_store_response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                      json.loads(check_store_response.data.decode('utf-8')))

                create_store_response = client.post('/store/storename')
                self.assertEqual(create_store_response.status_code, 201)

                get_store_response = client.get('/store/storename')
                self.assertEqual(get_store_response.status_code, 200)
                self.assertEqual(json.loads(get_store_response.data.decode('utf-8'))['name'],
                                 'storename')

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                create_store_response = client.post('/store/storename')
                self.assertEqual(create_store_response.status_code, 201)

                delete_store_response = client.delete('/store/storename')
                self.assertEqual(delete_store_response.status_code, 200)
                self.assertEqual(json.loads(delete_store_response.data.decode('utf-8')),
                                 {'message': 'Store deleted'})

                check_store_response = client.get('/store/storename')
                self.assertEqual(check_store_response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                      json.loads(check_store_response.data.decode('utf-8')))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                check_store_response = client.get('/store/storename')
                self.assertEqual(check_store_response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                      json.loads(check_store_response.data.decode('utf-8')))

                create_store_response = client.post('/store/storename')
                self.assertEqual(create_store_response.status_code, 201)

                get_store_response = client.get('/store/storename')
                self.assertEqual(get_store_response.status_code, 200)
                self.assertEqual(json.loads(get_store_response.data.decode('utf-8'))['name'],
                                 'storename')

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                check_store_response = client.get('/store/storename')
                self.assertEqual(check_store_response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(check_store_response.data.decode('utf-8')))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                store_response = client.post('/store/storename')
                self.assertEqual(len(json.loads(store_response.data.decode('utf-8'))['items']), 0)
                client.post('/item/testitem', data={'price': 1.99, 'store_id': 1})

                store_response = client.get('/store/storename')
                self.assertEqual(len(json.loads(store_response.data.decode('utf-8'))['items']), 1)
                self.assertDictEqual(json.loads(store_response.data.decode('utf-8')),
                                     {
                                         'name': 'storename',
                                         'items': [
                                             {
                                             'name': 'testitem',
                                             'price': 1.99,
                                             }]
                                         }
                                      )



    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                stores_response = client.get('/stores')
                self.assertEqual(stores_response.status_code, 200)
                self.assertEqual(len(json.loads(stores_response.data.decode('utf-8'))['stores']), 0)

                create_store_response = client.post('/store/storename')

                stores_response = client.get('/stores')
                self.assertEqual(len(json.loads(stores_response.data.decode('utf-8'))['stores']), 1)
                self.assertDictEqual(json.loads(stores_response.data.decode('utf-8')),
                                     {
                                         'stores':
                                             [
                                                 {
                                                     'name': 'storename',
                                                     'items': []

                                                 }
                                             ]
                                     })


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                stores_response = client.get('/stores')
                self.assertEqual(stores_response.status_code, 200)
                self.assertEqual(len(json.loads(stores_response.data.decode('utf-8'))['stores']), 0)

                create_store_response = client.post('/store/storename')
                client.post('/item/testitem', data={'price': 1.99, 'store_id': 1})



                stores_response = client.get('/stores')
                self.assertEqual(len(json.loads(stores_response.data.decode('utf-8'))['stores']), 1)
                self.assertDictEqual(json.loads(stores_response.data.decode('utf-8')),
                                     {
                                         'stores':
                                             [
                                                 {
                                                     'name': 'storename',
                                                     'items': [
                                                         {
                                                             'name': 'testitem',
                                                             'price': 1.99
                                                         }
                                                     ]

                                                 }
                                             ]
                                     })