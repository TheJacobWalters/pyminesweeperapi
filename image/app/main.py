from fastapi import FastAPI
import minesweeper
import logging
logging.basicConfig(level=logging.INFO, filename="/dev/stdout")
app = FastAPI()
ms = None
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/newgame")
def hello():
    global ms
    ms = minesweeper.Minesweeper()
    ms.setup()
    return ms.get_public_board()
    
@app.get('/getpublicboard')
def getpublicboard():
    global ms
    if ms is None:
        ms = minesweeper.Minesweeper()
        ms.setup()
    return ms.get_public_board()

@app.get('/getprivateboard')
def getprivateboard():
    global ms
    if ms is None:
        ms = minesweeper.Minesweeper()
        ms.setup()
    return ms.get_private_board()

@app.get("/click/{x_id}/{y_id}")
def click(x_id: int, y_id: int):

    global ms
    #ms = minesweeper.Minesweeper()
    #ms.setup()

    #logging.info(f"clicking {x_id} {y_id}")
    res = ms.click(x_id, y_id)
    res = { "message": res ,
            #"time" : ms.updateTimer(),
            "board" : ms.get_public_board()
        }
    return res