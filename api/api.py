from flask import Flask
import redis
import pickle
import json
import pdb
app = Flask(__name__)

# connect to mongodb
redisConnection = redis.Redis()

@app.route('/')
def index():
    return 'hello world'

@app.route('/mongoHealthCheck')
def mongoTest():
    return {'mongo Health' : redisConnection.ping()}

@app.route('/newGameDefinedOrder')
def newGameDefinedOrder():
    REDIS = redis.Redis()
    with open('board.json', 'rb') as file:
        while True:
            try:
                JSON = pickle.load(file)
                x = JSON['x']
                y = JSON['y']
                REDIS.set(f"{x}-{y}", pickle.dumps(JSON))
                return "success"
            except EOFError:
                break
        return "failure"
'''
@app.route('/newGame')
def newGame():
    REDIS = redis.Redis()
    for x in range(30):
        for y in range(16):
            REDIS.set(f"{x}-{y}", pickle.dumps({'mined':True}))
    return "success"
'''
@app.route("/click/<x>/<y>")
def click(x, y):
    REDIS = redis.Redis()
    result = REDIS.get(f"{x}-{y}")
    result = pickle.loads(result)
    result['clicked'] = True
    pdb.set_trace()
    mined = result['ismined']
    result = pickle.dumps(result)
    REDIS.set(f"{x}-{y}", result)
    if (mined):
        return json.dumps({'Game Over' : True})
    else:
        return json.dumps({'Game Over' : False})