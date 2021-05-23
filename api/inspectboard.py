import pickle
import pdb

with open('board.json', 'rb') as f:
    while True:
        x = pickle.load(f)
        print(x)