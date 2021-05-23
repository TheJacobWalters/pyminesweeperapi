import pickle

with open('board.json', 'wb') as f:
    pickle.dump({'x':'1', 'func': str}, f)
    pickle.dump({'x':'2', 'func': open}, f)

with open('board.json', 'rb') as f:
    while True:
        try:
            x = pickle.load(f)
            print(x)
        except EOFError:
            break

# remember pickle.load() will get one pickled object from the file