import os
import msvcrt
import threading
import time
import subprocess
import random

# wait waitTime amount of time before move the piece down 1 spot
def wait():
    global coords, waitTime, running, permBoard, pieces, score
    while running:
        if not(pause):
            coords[1] += 1
            coords, pieces[0] = movePiece(permBoard.copy(), coords, pieces[0])
            permBoard, score = checkLine(permBoard, score)
        time.sleep(waitTime)

# startup animation and establishing permBoard
def displayBoard():
    line = "<! . . . . . . . . . .!>".center(90) # all rows places can be placed on
    # bottom of the board
    bottomLineTop = "<!====================!>".center(90)
    bottomLineBottom = '\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/'.center(90)

    # create the board
    board = ["\n"]
    for i in range(20):
        board.append(line)
    board.append(bottomLineTop)
    board.append(bottomLineBottom)

    # display the board animation
    for line in board:
        print(line)
        time.sleep(.025)
    
    # establish all side information
    info = ["".center(30), "Press 'r' to start".center(30), "".center(30), "Controls".center(30), "'w' to rotate left".center(30), "'s' to rotate right ".center(30), "'a' to move left".center(30), "'d' to move right ".center(30), "'space' to hard drop".center(30), "'q' to quit ".center(30)]

    time.sleep(.3)

    # show all side information
    for i, items in enumerate(info):
        try:
            board[i+1] = items + board[i+1][30:]
            with lock:
                os.system("cls")
                print("\n".join(board))
            time.sleep(.025)
        except:
            break
    
    return board

# clears the spot where the next piece is shown
def clearNextMove(board):
    for i in range(4):
        board[i+13] = "".center(30) + board[i+13][30:]
    return board

# show next piece
def nextMovePreview(board):
    clearNextMove(board) # clear the spot where it show the next piece
    # displays the new piece
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

# check if a movement action is allowed
def checkMovement(pieceCoords=list, direction=int, board=list):
    for items in pieceCoords:
        if items[0]-2 < 35 and direction == 0: return False, False # dont move left
        elif (items[0]+2 > 53 and direction == 1): return False, False # dont move right
        elif (items[1]+1 > 20 and direction == 2): return False, False # dont move down
    
        
        if items[1] > 0:
            if board[items[1]][items[0]-2] == "█" and direction == 0: return False, True # dont move left
            elif board[items[1]][items[0]+2] == "█" and direction == 1: return False, True # dont move right
            if board[items[1]+1][items[0]] == "█": return False, True # dont move down
        
    return True, True # moving is allowed

# place a piece onto permBoard
def placePieces(board, coordList):
    global permBoard
    # add coordinate from coordList as squares in permBoard
    for coord in coordList:
        if coord[1] > 0:
            board[coord[1]] = board[coord[1]][:coord[0]] + "██" + board[coord[1]][coord[0]+2:]
    permBoard = board
    return board

# drop the current piece to the bottom
def hardDrop(board, coordList, coords):
    yCount = 0 # how far down the piece should go
    stop = False # loop control
    while not stop:
        # Check if moving down one more step would cause collision
        for item in coordList:
            if item[1] + yCount + 1 >= len(board) or board[item[1] + yCount + 1][item[0]] != " ":
                stop = True
                break
        if not stop:
            yCount += 1
    
    for i in range(4): coordList[i][1] += yCount # update the piece coordinates

    # place the piece down and select a new piece
    piece = [pieces[1], 0]
    pieces[1] = random.randint(0,6)
    coords = [43, 1]
    board = placePieces(board, coordList)
    
    # display the board
    with lock:
        os.system("cls")
        print("\n".join(board))
    return coords, piece

# move the current piece
def movePiece(board, coords, piece):
    global inputs # inputs shows what movements need to be made
    nextMovePreview(board) # shows the preview of the next piece

    '''piece rotation'''
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

    # get the coordinates of each 'tile' the current piece is on
    coordList = []
    for items in tetromino[piece[0]][piece[1]]:
        coordList.append([items[0] + coords[0], items[1] + coords[1]])
    
    # moves pieces back onto the board if they rotate out
    if not any(checkMovement(coordList, 0, board)):
        x = []
        for i in range(4): x.append(coordList[i][0])
        difference = min(x)
        for i in range(4): coordList[i][0] = coordList[i][0] + (35-difference)
    elif not any(checkMovement(coordList, 1, board)):
        x = []
        for i in range(4): x.append(coordList[i][0])
        difference = max(x)
        for i in range(4): coordList[i][0] = coordList[i][0] - (difference-53)

    '''movment'''
    # move left
    if not(False in(checkMovement(coordList, 0, board))) and inputs[1] == 1:
        for i in range(4): coordList[i][0] -= 2
        coords[0] -= 2
    # move right
    elif not(False in(checkMovement(coordList, 1, board))) and inputs[1] == 2:
        for i in range(4): coordList[i][0] += 2
        coords[0] += 2

    '''hard drop'''
    if inputs[2] == 1:
        inputs = [0, 0, 0]
        return hardDrop(board, coordList, coords)
    
    inputs = [0, 0, 0] # reset user inputs

    # place a piece down if it hits the bottom or another piece; move to next piece
    if False in checkMovement(coordList, 2, board):
        global pieces
        piece = [pieces[1], 0]
        pieces[1] = random.randint(0,6)
        #print(piece)
        coords = [43, 1]
        board = placePieces(board, coordList)
        with lock:
            os.system("cls")
            print("\n".join(board))
        return coords, piece

    # add the current piece onto the board
    for coord in coordList:
        if coord[1] > 0:
            board[coord[1]] = board[coord[1]][:coord[0]] + "██" + board[coord[1]][coord[0]+2:]

    # update the board display when the lock is open
    with lock:
        os.system("cls")
        print("\n".join(board))

    return coords, piece

# add the score to the board
def updateScore(board, score):
    board[2] = board[2][:-30] + "Score:".center(30)
    board[3] = board[3][:-30] + str(score).center(30)
    return board

# return True if a line needs to be cleared
def isLineFull(line):
    for item in line:
        if item != "█" : return False
    return True

# gets the info show on the sides of the board
def getSideInfo(board):
    info = []
    for line in board:
        if len(line) == 90: info.append([line[:30], line[-30:]])
    return info

'''
re-align controls and score on the board
this is needed because when you delete the full line all side info moves down
this moves all side info back up
'''
def fixSideInfo(board, info):
    for i in range(len(board)-1):
        board[i+1] = info[i][0] + board[i+1][30:60] + info[i][1]
    return board

# check if a line should be  cleared
def checkLine(board, score):
    global lineCounter
    linesCleared = 0 # how many lines were cleared
    for i in range(len(board)-1): # iterate through each line on the board
        if isLineFull(board[i+1][35:55]): # True if line should be cleared
            linesCleared += 1
            info = getSideInfo(board) # get controls and score on the side
            del board[i+1] # delete full line
            board.insert(1, "<! . . . . . . . . . .!>".center(90)) # insert new line at the top of the board
            board = fixSideInfo(board, info) # add info back onto board in the right spot

    # change score depending on lines cleared
    if linesCleared == 1: score += 40
    elif linesCleared == 2: score += 100
    elif linesCleared == 3: score += 300
    elif linesCleared == 4: score += 1200

    lineCounter += linesCleared # add to the amount of lines scored on current level
    # if more than 10 lines have been clear, go to next level/speed up
    if lineCounter >= 10:
        global waitTime
        waitTime /= 2
        lineCounter = 0

    board = updateScore(board, score) # update the board to show the new score

    return board, score

# check if game over
def checkGameEnd(board, coords):
    if board[1][43] == "█" and coords[1] >- 2: # if piece spawn location is blocked
        global running
        running = False

if __name__ == "__main__":
    '''setting up the console'''
    os.system("cls") # clear console
    subprocess.run("mode con: cols=90 lines=30", shell=True) # resize console
    time.sleep(1)
    os.system('color 2') # text color green

    '''initilizing variables'''
    # tuple with every piece and every rotation
    tetromino = [(((0,0), (0,-1), (0,-2), (0,-3)), ((-2,0), (0,0), (2,0), (4,0))), # I
                 (((0,0), (0,-1), (2,0), (2,-1)),), # O
                 (((0,0), (2,0), (0,-1), (0,-2)), ((-2,0), (-2,-1), (0,-1), (2,-1)), ((0,-1), (2,-1), (2,0), (2,1)), ((-2,0), (0,0), (2,0), (2,-1))), # L
                 (((0,0), (2,0), (2,-1), (2,-2)), ((-2,-1), (-2,0), (0,0), (2,0)), ((0,-1), (-2,-1), (-2,0), (-2,1)), ((-2,-1), (0,-1), (2,-1), (2,0))), # J
                 (((-2,0), (0,0), (0,-1), (2,-1)), ((0,0), (0,-1), (2,0), (2,1))), # S
                 (((-2,-1), (0,-1), (0,0), (2,0)), ((0,0), (0,1), (2,0), (2,-1))), # Z
                 (((0,0), (0,1), (2,0), (-2,0)), ((0,0), (-2,0), (0,-1), (0,1)), ((0,0), (0,-1), (-2,0), (2,0)), ((0,0), (2,0), (0,-1), (0,1)))] # T
    # 0=I, 1=O, 2=L, 3=J, 4=s, 5=z, 6=T
    # 0=upright, 1=90*, 2=180*, 3=270*
    pieces = [[random.randint(0,6), 0], random.randint(0,6)] # current piece and next piece
    coords = [43, 1] # base location of where the piece is
    inputs = [0, 0, 0] # keyboard inputs; [rotation, movement, drop]
    running = True # is game running; used for closing thread safely
    pause = False
    quit = False
    waitTime = .4 # how quickly pieces drop
    score = 0 # current score
    lineCounter = 0 # counts how many lines have been scored
    key = "" # str to save button presses
    permBoard = displayBoard()

    # waiting for game to begin by pressing 'r'
    while True:
        key = str(msvcrt.getch()) # get keyboard press
        # if r is pressed, break loop
        if "r" in key:
            key = ""
            break
        # if q is pressed, close the code
        elif "q" in key:
            os._exit(1)
        time.sleep(.05)
    
    lock = threading.Lock() # initilize screen update lock
    waitThread = threading.Thread(target=wait) # initilize thread of dropping pieces
    waitThread.start() # start thread
    # game loop
    while running:
        # get keyboard input
        if msvcrt.kbhit():
            key = str(msvcrt.getch())
        
        # keyboard functionality
        if "q" in key: # quit
            running = False
            quit = True
        elif "w" in key: inputs[0] = 1 # rotate left
        elif "s" in key: inputs[0] = 2 # rotate right
        elif "a" in key: inputs[1] = 1 # move left
        elif "d" in key: inputs[1] = 2 # move right
        elif " " in key: inputs[2] = 1 # hard drop
        elif "e" in key: # pause game
            pause = True
            while True: # wait until 'e' is pressed again, then unpause
                time.sleep(.01)
                key = str(msvcrt.getch())
                if "e" in key:
                    pause = False
                    break
        
        coords, pieces[0] = movePiece(permBoard.copy(), coords, pieces[0]) # move piece and update board
        checkGameEnd(permBoard, coords) # check if game over
        key = "" # reset key

        time.sleep(.1)
    
    if quit: os._exit(1) # close the program if 'q' was pressed

    # clear screen and display final score
    time.sleep(.75)
    os.system("cls")
    print("\n\n\n\n\n\n")
    print("|     You died with a final score of:     |".center(90))
    print(f"|{str(score).center(41)}|".center(90))

    input()