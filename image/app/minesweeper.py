from collections import deque
import random
import platform
import time
import pprint
from datetime import datetime as dt
import logging
logging.basicConfig(level=logging.INFO, filename="/dev/stdout")
from datetime import datetime

SIZE_X = 10
SIZE_Y = 10

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2


class Minesweeper:
    def __init__(self):
        self.time = None
    def __repr__(self):
        pprint.pp(self.tiles)
        return (self.tiles)

    def click(self, x,y):
        tile = self.tiles[x][y]
        tile['state'] = STATE_CLICKED

        if (tile['isMine'] == False) :
            return 'Didnt trip mines'
        else:
            return 'Tripped the mines'

    def flagSpace(self, x, y):
        tile = self.tiles[x][y]
        tile['state'] = STATE_FLAGGED


    def get_public_board(self):
        board = dict({})
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                if y == 0:
                    board[x] = {}
                board[x][y] = self.tiles[x][y]["state"]
        return board    
    
    def get_private_board(self):
        return self.tiles

    def setup(self):
        self.startTime = str(datetime.now())
        logging.info(f'startime at initial {self.startTime}')
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None

        # create buttons
        self.tiles = dict({})
        self.mines = 0
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # currently random amount of mines
                if random.uniform(0.0, 1.0) < 0.1:
                    isMine = True
                    self.mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "mines": 0 # calculated after grid is built
                }

                self.tiles[x][y] = tile

        # loop again to find nearby mines and display number on tile
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc

    def restart(self):
        self.setup()

    def gameOver(self, won):
        '''
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["wrong"])
                if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["mine"])
        '''

        msg = "You Win! Play again?" if won else "You Lose! Play again?"

    def updateTimer(self):
        '''
        logging.info(f"inside updateTime -> self.startTime {self.startTime}")
        then = self.startTime
        then = datetime.strptime(then, "%Y-%m-%d %H:%M:%S.%f") 
        now = datetime.now()
        diff = now - then
        diff = str(diff)
        return diff
        '''
        pass

    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  #top right
            {"x": x-1,  "y": y},    #top middle
            {"x": x-1,  "y": y+1},  #top left
            {"x": x,    "y": y-1},  #left
            {"x": x,    "y": y+1},  #right
            {"x": x+1,  "y": y-1},  #bottom right
            {"x": x+1,  "y": y},    #bottom middle
            {"x": x+1,  "y": y+1},  #bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1
