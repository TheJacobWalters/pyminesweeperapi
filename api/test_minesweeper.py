import api
import unittest
import pdb
import json


class Tester(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        response = response.data
        response = json.loads(response)['success']
        self.assertTrue(response)
    
    def test_healthcheck(self):
        response = self.app.get('/healthcheck')
        response = response.data
        response = json.loads(response)['success']
        self.assertTrue(response)

    def test_newGame(self):
        response = self.app.get('/newGame')
        response = response.data
        response = json.loads(response)['success']
        self.assertTrue(response)
    
    # only Dev
    def test_click_unmined(self):
        self.app.get('/newGame')
        response = self.app.get('/click/0/0')
        response = response.data
        response = json.loads(response)['GameOver']
        self.assertFalse(response)
    
    # only Dev
    def test_click_mined(self):
        self.app.get('/newGame')
        response = self.app.get('/click/0/1')
        response = response.data
        response = json.loads(response)['GameOver']
        self.assertTrue(response)

    def test_mark(self):
        self.app.get('/newGame')
        response = self.app.get('/mark/0/1')
        response = response.data
        response = json.loads(response)['IsMarked']
        self.assertTrue(response)

        response = self.app.get('/markedMines')
        response = response.data
        response = json.loads(response)['markedMines']
        self.assertEqual(response, '1' )
    
    def test_hints(self):
        self.app.get('/newGame')
        response = self.app.get('/click/0/0')
        response = response.data
        response = json.loads(response)['hint']
        self.assertEqual(response, 3)

