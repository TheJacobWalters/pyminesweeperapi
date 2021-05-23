import json
import random
import pickle
#Create list of where mines will be placed
# these first ones I want to be there then it will be rando
mineLocs = [{'x':1, 'y':0, "ismined": True, "clicked": False},
            {'x':1, 'y':1, "ismined": True, "clicked": False},
            {'x':0, 'y':1, "ismined": True, "clicked": False},
            ]
# make sure there are 99 mines
while(len(mineLocs) < 99):
    x = random.choice(range(30))
    y = random.choice(range(16))

    object = {'x':x,'y':y, "ismined": True, "clicked": False}
    if object not in mineLocs:
        mineLocs.append(object)

assert(len(mineLocs) == 99)

#add the other things
for x in range(30):
    for y in range(16):
        if {'x':x, 'y':y, 'ismined':True, 'clicked':False} not in mineLocs:
            mineLocs.append({'x':x, 'y':y, 'ismined':False, 'clicked':False})

assert(len(mineLocs) == (16 * 30))

with open('./board.json', 'wb') as f:
    for mine in mineLocs:
        pickle.dump(mine, f)

with open('board.json', 'rb') as f:
    try:
        while True:
            print(pickle.load(f))
    except EOFError:
        pass