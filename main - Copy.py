import os
import msvcrt
import threading
import time
import subprocess
import random

def getChar():
    global key
    global running
    global inputs
    while running:
        key = str(msvcrt.getch())
        #print(key)
        if "q" in key: running = False
        elif "w" in key: inputs[0] = 1
        elif "s" in key: inputs[0] = 2
        elif "a" in key: inputs[1] = 1
        elif "d" in key: inputs[1] = 2
        elif " " in key: inputs[2] = 1
        time.sleep(.05)

def displayBoard():
    line = "<! . . . . . . . . . .!>".center(90)
    bottomLineTop = "<!====================!>".center(90)
    bottomLineBottom = '\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/'.center(90)

    board = ["\n"]
    for i in range(20):
        board.append(line)
    board.append(bottomLineTop)
    board.append(bottomLineBottom)

    for line in board:
        print(line)
        time.sleep(.025)
    
    info = ["".center(30), "Press 'r' to start".center(30), "".center(30), "Controls".center(30), "'w' to rotate left".center(30), "'s' to rotate right ".center(30), "'a' to move left".center(30), "'d' to move right ".center(30), "'space' to hard drop".center(30), "'q' to quit ".center(30)]

    time.sleep(.3)

    for i, items in enumerate(info):
        try:
            board[i+1] = items + board[i+1][30:]
            os.system("cls")
            print("\n".join(board))
            time.sleep(.025)
        except:
            break
    
    return board

def clearNextMove(board):
    for i in range(4):
        board[i+13] = "".center(30) + board[i+13][30:]
    return board

def nextMovePreview(board):
    clearNextMove(board)
    if pieces[1] == 0:
        for i in range(4):
            board[i+13] = "██".center(30) + board[i+13][30:]
    elif pieces[1] == 1:
        for i in range(2):
            board[i+14] = "████".center(30) + board[i+14][30:]
    elif pieces[1] == 2:
        board[14] = "██  ".center(30) + board[14][30:]
        board[15] = "██  ".center(30) + board[15][30:]
        board[16] = "████".center(30) + board[16][30:]
    elif pieces[1] == 3:
        board[14] = "  ██".center(30) + board[14][30:]
        board[15] = "  ██".center(30) + board[15][30:]
        board[16] = "████".center(30) + board[16][30:]
    elif pieces[1] == 4:
        board[14] = "  ████".center(30) + board[14][30:]
        board[15] = "████  ".center(30) + board[15][30:]
    elif pieces[1] == 5:
        board[14] = "████   ".center(30) + board[14][30:]
        board[15] = "   ████  ".center(30) + board[15][30:]
    elif pieces[1] == 6:
        board[14] = "██████".center(30) + board[14][30:]
        board[15] = "  ██  ".center(30) + board[15][30:]
    
    return board

def checkMovement(pieceCoords=list, direction=int):
    for items in pieceCoords:
        if items[0]-2 < 35 and direction == 0:
            print("False - left")
            return False # move left
        elif items[0]+2 > 53 and direction == 1: 
            print("false - right")
            return False # move right
    #print("True")
    return True


def movePiece(board, coords, piece):
    global inputs

    # piece rotation
    # rotate left
    if inputs[0] == 1: 
        if piece[0] == 2 or piece[0] == 3 or piece[0] == 6:
            if piece[1] == 0: piece[1] = 3
            else: piece[1] -= 1
        elif piece[0] == 0 or piece[0] == 4 or piece[0] == 5:
            if piece[1] == 0: piece[1] = 1
            else: piece[1] = 0
    #rotate right
    elif inputs[0] == 2:
        if piece[0] == 2 or piece[0] == 3 or piece[0] == 6:
            if piece[1] == 3: piece[1] = 0
            else: piece[1] += 1
        elif piece[0] == 0 or piece[0] == 4 or piece[0] == 5:
            if piece[1] == 0: piece[1] = 1
            else: piece[1] = 0
    
    if inputs[2] == 1:
        pass
        # hard drop code here

    coordList = []
    for items in tetromino[piece[0]][piece[1]]:
        #print(items, coords)
        coordList.append([items[0] + coords[0], items[1] + coords[1]])
    
    if checkMovement(coordList, 0) == False:
        x = []
        for i in range(4): x.append(coordList[i][0])
        difference = min(x)
        for i in range(4): coordList[i][0] = coordList[i][0] + (35-difference)
    elif checkMovement(coordList, 1) == False:
        x = []
        for i in range(4): x.append(coordList[i][0])
        difference = max(x)
        for i in range(4): coordList[i][0] = coordList[i][0] - (difference-53)

    # movement
    if checkMovement(coordList, 0) and inputs[1] == 1:
        for i in range(4): coordList[i][0] -= 2
        coords[0] -= 2
    elif checkMovement(coordList, 1) and inputs[1] == 2:
        for i in range(4): coordList[i][0] += 2
        coords[0] += 2
    inputs = [0, 0, 0]

    for coord in coordList:
        if coord[1] > 0:
            board[coord[1]] = board[coord[1]][:coord[0]] + "██" + board[coord[1]][coord[0]+2:]
    coords[1] += 1

    if coords[1] == 21:
        piece = [random.randint(0,6), 0]
        coords = [43, 1]

    return board, coords, piece

if __name__ == "__main__":
    os.system("cls")
    subprocess.run("mode con: cols=90 lines=30", shell=True)
    time.sleep(1)
    os.system('color 2')
    
    #█
    tetromino = [(((0,0), (0,-1), (0,-2), (0,-3)), ((-2,0), (0,0), (2,0), (4,0))), # I
                 (((0,0), (0,-1), (2,0), (2,-1)),), # O
                 (((0,0), (2,0), (0,-1), (0,-2)), ((-2,0), (-2,-1), (0,-1), (2,-1)), ((0,-1), (2,-1), (2,0), (2,1)), ((-2,0), (0,0), (2,0), (2,-1))), # L
                 (((0,0), (2,0), (2,-1), (2,-2)), ((-2,-1), (-2,0), (0,0), (2,0)), ((0,-1), (-2,-1), (-2,0), (-2,1)), ((-2,-1), (0,-1), (2,-1), (2,0))), # J
                 (((-2,0), (0,0), (0,-1), (2,-1)), ((0,0), (0,-1), (2,0), (2,1))), # S
                 (((-2,-1), (0,-1), (0,0), (2,0)), ((0,0), (0,1), (2,0), (2,-1))), # Z
                 (((0,0), (0,1), (2,0), (-2,0)), ((0,0), (-2,0), (0,-1), (0,1)), ((0,0), (0,-1), (-2,0), (2,0)), ((0,0), (2,0), (0,-1), (0,1)))] # T

    inputs = [0, 0, 0] # rotation, movement, drop
    running = True
    keyInp = threading.Thread(target=getChar)
    keyInp.start()
    key = ""
    permBoard = displayBoard()
    #board = permBoard.copy()

    while True:
        if "r" in key:
            key = ""
            break
        time.sleep(.01)
    
    # 0=I, 1=O, 2=L, 3=J, 4=s, 5=z, 6=T
    # 0=upright, 1=90*, 2=180*, 3=270*
    pieces = [[random.randint(0,6), 0], random.randint(0,6)]
    coords = [43, 1]
    waitTime = .2
    timeSave = time.gmtime()[5]
    
    while True:
        if not(running):
            break

        board = nextMovePreview(permBoard.copy())
        pieces[0][0] = 2

        #if time.gmtime()[5] > timeSave:
            #timeSave = time.gmtime()[5] 
            #timeSave = 1000
        board, coords, pieces[0] = movePiece(board, coords, pieces[0])

        
        
        time.sleep(waitTime)
        os.system("cls")
        print("\n".join(board))

