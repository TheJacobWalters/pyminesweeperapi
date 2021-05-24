from flask import Flask
import json
import redis
import pdb
import pickle

app = Flask(__name__)

def getNeighbors(x,y):
    x = int(x)
    y = int(y)

    def func (input):
        if input[0] < 0:
            return False
        if input[0] > 29:
            return False
        if input[1] < 0:
            return False
        if input[1] > 15:
            return False
        else:
            return True

    neighbors = []
    neighbors.append((x-1, y-1))
    neighbors.append((x, y-1))
    neighbors.append((x+1, y-1))
    neighbors.append((x-1, y))
    neighbors.append((x+1, y))
    neighbors.append((x-1, y+1))
    neighbors.append((x, y+1))
    neighbors.append((x+1, y+1))
    
    neighbors = list(filter(func, neighbors))

    return neighbors

def getHint(x,y):
    REDIS = redis.Redis()
    hint = 0
    neighbors = getNeighbors(x,y)
    for neighbor in neighbors:
        result = REDIS.get(f'{neighbor[0]}-{neighbor[1]}')
        result = pickle.loads(result)
        if result['ismined']:
            hint += 1

    return hint
    # call get neighbors and then check those against whats in the db

@app.route('/')
def index():
    return json.dumps({'success': True})

@app.route('/healthcheck')
def healthcheck():
    REDIS = redis.Redis()
    result = REDIS.ping()
    return json.dumps({'success':result})

@app.route('/newGame')
def newGame():
    REDIS = redis.Redis()
    REDIS.set('markedMines', 0)
    with open('board.json', 'rb') as f:
        while True:
            try:
                current = pickle.load(f)
                x = current['x']
                y = current['y']
                REDIS.set(f'{x}-{y}', pickle.dumps(current))
            except EOFError:
                break
    
    return json.dumps({'success': True})

# this needs to be changed to return a hint
@app.route('/click/<x>/<y>')
def click(x,y):
    REDIS = redis.Redis()
    result = REDIS.get(f'{x}-{y}')
    result = pickle.loads(result)
    result['clicked'] = True
    if result['ismined'] :
        result['GameOver'] = True
    else:
        result['GameOver'] = False
    result['hint'] = getHint(x,y)
    insertion = pickle.dumps(result)
    REDIS.set(f'{x}-{y}',insertion)
    return json.dumps(result)

@app.route('/mark/<x>/<y>')
def mark(x,y):
    REDIS = redis.Redis()
    result = REDIS.get(f'{x}-{y}')
    result = pickle.loads(result)
    result['IsMarked'] = True
    REDIS.incr('markedMines')
    insertion = pickle.dumps(result)
    REDIS.set(f'{x}-{y}', insertion)
    return json.dumps(result)

@app.route('/markedMines')
def getMarkeMines():
    REDIS = redis.Redis()
    result = REDIS.get('markedMines')
    result = result.decode()
    return json.dumps({'markedMines':result})

if __name__ == "__main__":
    #getHint(0,0)
    #getNeighbors(0,0)
    app.run()