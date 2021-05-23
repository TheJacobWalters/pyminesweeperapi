import api
import unittest
import redis
import pdb
import pickle
import json

class mytestClass(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()

    def test_default(self):
        result = self.app.get('/').data
        self.assertEqual(result, b'hello world')

class testRedisDB(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()

    def test_mongodb(self):
        result = self.app.get('/mongoHealthCheck').data
        result = json.loads(result)['mongo Health']
        self.assertTrue(result)

    def test_sizeOfBoard(self):
        REDIS = redis.Redis()
        self.app.get("/newGameDefinedOrder")
        for x in range(30):
            for y in range(16):
                self.assertTrue(REDIS.get(f'{x}-{y}'))
                
    def test_HardcodedSizeOfBoard(self):
        REDIS = redis.Redis()
        self.app.get("/newGameDefinedOrder")
        for x in range(30):
            for y in range(16):
                self.assertTrue(REDIS.get(f'{x}-{y}'))
class testClicking(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()
    
    def test_clickOnClear(self):
        self.app.get("/newGameDefinedOrder")
        result = self.app.get("/click/0/0").data
        result = json.loads(result)['Game Over']
        self.assertFalse(result)
    
    def test_clickOnMine(self):
        self.app.get("/newGameDefinedOrder")
        result = self.app.get("/click/0/1").data
        result = json.loads(result)["Game Over"]
        self.assertTrue(result)
    

    