import math
import random
import time
import tkinter as tk
import tkinter.filedialog as fd


class Character:
    DIRECTIONS_DICT = {
        'NW': ((-1, -1), -3/4*math.pi),
        'N': ((-1, 0), -1/2*math.pi),
        'NE': ((-1, 1), -1/4*math.pi),
        'E': ((0, -1), math.pi),
        'W': ((0, 1), 0),
        'SW': ((1, -1), 3/4*math.pi),
        'S': ((1, 0), 1/2*math.pi),
        'SE': ((1, 1), 1/4*math.pi)
    }
    
    BLOCKED_CHARS = ['*']
    
    def __init__(self, row, col, game):
        self.row = row
        self.col = col
        self.game = game
    
    @property
    def coordinates(self):
        return self.row, self.col
    
    def validMove(self, newRow, newCol):
        if not -1 < newRow < self.game.rows or not -1 < newCol < self.game.columns:
            return False
        if self.game.grid.grid_slaves(row=newRow, column=newCol)[0]['text'] in self.BLOCKED_CHARS:
            return False
        return True
    
    def move(self, rowDelta, colDelta):
        self.game.grid.grid_slaves(row=self.row, column=self.col)[0]['text'] = '.'
        
        if self.validMove(self.row + rowDelta, self.col + colDelta):
            self.row = self.row + rowDelta
            self.col = self.col + colDelta
            return
        if self.validMove(self.row + rowDelta, self.col):
            self.row = self.row + rowDelta
            return
        if self.validMove(self.row, self.col + colDelta):
            self.col = self.col + colDelta
            return

class Doctor(Character):
    BLOCKED_CHARS = ['*', '#']
    KILL_CHARS = ['A', '#']
    DEATH_CHAR = 'X'
                
    def sonicTeleport(self):
        self.game.grid.grid_slaves(row=self.row, column=self.col)[0]['text'] = '.'
        while True:
            rRow = random.randrange(self.game.rows)
            rCol = random.randrange(self.game.columns)
            if self.game.grid.grid_slaves(row=rRow, column=rCol)[0]['text'] != '.':
                continue
            
            if self.game.easy:
                adjacentSquares = [self.game.grid.grid_slaves(row=rRow + i, column=rCol + j)[0]['text'] 
                                   for j in range(-1, 2) for i in range(-1, 2) 
                                   if self.validMove(rRow + i, rCol + j)]
                if 'A' in adjacentSquares:
                    continue
                
            self.row = rRow
            self.col = rCol
            break
        
class Dalek(Character):
    KILL_CHARS = ['A', '#']
    DEATH_CHAR = '#'
    
    def dalekMove(self):
        docRow, docCol = self.game.doctor.coordinates
        deltaRow, deltaCol = docRow - self.row, docCol - self.col
        
        # So that the dalek can stop if its on top of you. No need to update squares next turn then.
        if deltaRow == 0 and deltaCol == 0:
            return
        
        # Could optimize this by doing lost of checks on DIRECTIONS_DICT with the deltaRow, deltaCol but this is simpler
        # and optimization is not really matter for this program since its so small and simple anyway.
        movementAngle = math.atan2(deltaRow, deltaCol)
        
        # Returns difference between movementangle and the angle each of the keys give
        def compareAngles(a1, a2):
            return math.pi - abs(abs(a1 - a2) - math.pi)
        angleDelta = {v[0]: compareAngles(movementAngle, v[1]) for k, v in self.DIRECTIONS_DICT.items()}
        twoClosest = sorted(angleDelta.items(), key = lambda item: item[1])[:2]
        # Randomly returns one of the two closest depending on weight. Reversed can be used because only choosing between 2
        moveDirection = random.choices([x[0] for x in twoClosest], weights=[x[1] for x in reversed(twoClosest)], k=1)
        
        self.move(*moveDirection[0])

class Game:
    NON_CHARACTER_SQUARES = ['*', '.', '#']
    DALEK_SQUARE = 'A'
    DOCTOR_SQUARE = 'D'
    VALID_INPUTS = NON_CHARACTER_SQUARES + [DALEK_SQUARE, DOCTOR_SQUARE]
    easy = True
    easyRate = 1
    hardRate = 0.5
    paused = False
    tickRate = easyRate # Time between ticks
    WASD_DICT = {
        'w': (-1, 0),
        'a': (0, -1),
        's': (1, 0),
        'd': (0, 1)
    }
    pressedKeys = {
        'w': False,
        'a': False,
        's': False,
        'd': False,
        't': False
    }
        
    def __init__(self, root):
        # Screen initialization
        self.root = root
        self.root.title('DALEK')
        
        # Startscreen
        self.startscreen = tk.Frame(self.root)
        self.startscreen.pack()
        
        tk.Label(self.startscreen, text='   Välkommen till spelet DALEK!   ', font=('Helvetica', 24, 'bold')).pack(pady=(0, 15))
        tk.Label(self.startscreen, text='''Här förklarar jag allting efter 💀''').pack(pady=(0, 15))
        
        difficultyFrame = tk.Frame(self.startscreen)
        self.easyButton = tk.Button(difficultyFrame,
                                    text='Easy',
                                    activeforeground='red',
                                    state=tk.ACTIVE,
                                    command=self.setEasy)
        self.hardButton = tk.Button(difficultyFrame,
                                    text='Hard',
                                    activeforeground='red',
                                    command=self.setHard)
        difficultyFrame.pack(pady=(0, 15))
        self.easyButton.pack(side=tk.LEFT)
        self.hardButton.pack(side=tk.LEFT)
        
        self.filename = tk.StringVar()
        self.filename.set('Du har inte valt någon fil')
        tk.Label(self.startscreen, textvariable=self.filename).pack()
        tk.Button(self.startscreen, text='Välj fil', command=self.selectFile).pack(pady=(0, 15))
        
        self.launchButton = tk.Button(self.startscreen,
                                      text='START',
                                      activeforeground='red',
                                      state=tk.DISABLED,
                                      command=self.play)
        self.launchButton.pack()
        
        # Game metadata
        self.boardInfo = tk.StringVar()
        tk.Label(self.root, textvariable=self.boardInfo).pack()
        
        # Grid frame
        self.grid = tk.Frame(root)
        self.grid.pack(expand=True, side= tk.BOTTOM)
    
    def setEasy(self):
        self.easyButton['state'] = tk.ACTIVE
        self.hardButton['state'] = tk.NORMAL
        self.easy = True
        self.tickRate = self.easyRate
        
    def setHard(self):
        self.easyButton['state'] = tk.NORMAL
        self.hardButton['state'] = tk.ACTIVE
        self.easy = False
        self.tickRate = self.hardRate
        
    def selectFile(self):
            filename = fd.askopenfilename(filetypes=(('text files', 'txt'),))
            if not filename:
                return
            self.filename.set(filename)
            self.initializeBoard()
            
    def initializeBoard(self, restart=False): 
        with open(self.filename.get(), 'r') as file:
            rows = file.read().splitlines()
        self.board = [[*row] for row in rows]
        self.rows = len(self.board)
        self.columns = len(self.board[0])
        
        for widget in self.grid.winfo_children():
            widget.destroy()
        self.doctor = None
        self.daleks = []
        
        errors = []
        # Iterates over the board to check if it is valid and to initialize the characters
        for i, row in enumerate(self.board):
            rowError = False
            if len(row) != self.columns:
                errors += [f'Row {i + 1} is not the same length as the first row. All rows must be equal in length']
                rowError = True
            for j, col in enumerate(row):
                colError = False
                if col not in self.VALID_INPUTS:
                   errors += [f'{col} is not a valid input. Only {self.VALID_INPUTS} are permitted in input file.']
                   colError = True
                   
                if col == self.DOCTOR_SQUARE:
                    if self.doctor:
                        errors += [f'There is more than one doctor. Second one is at {i}, {j} (0 index).']
                        colError = True
                    self.doctor = Doctor(i, j, self)
                    
                if col == self.DALEK_SQUARE:
                    self.daleks.append(Dalek(i, j, self))
                    
                color = '#800e17' if colError else 'red' if rowError else 'black'
                tk.Label(self.grid, text=col, width=1, height=1, bg=color).grid(row=i, column=j)
        if restart:
            return
        if len(errors) == 0:
            self.launchButton['state'] = tk.ACTIVE
            self.boardInfo.set(f'Rows: {self.rows}, Columns: {self.columns}\nDaleks: {len(self.daleks)}')
        else:
            self.boardInfo.set('\n'.join(errors))
    
    def play(self, restart=False):
        self.alive = True
        if not restart:
            self.startscreen.destroy()
        self.root.bind('<space>', self.pause)
        self.root.bind('w', self.keyPress)
        self.root.bind('a', self.keyPress)
        self.root.bind('s', self.keyPress)
        self.root.bind('d', self.keyPress)
        self.root.bind('t', self.keyPress)
        
        self.root.update()
        time.sleep(0.5)
        while self.alive:
            self.boardInfo.set(f'Daleks left: {len(self.daleks)}')
            self.root.update()
            self.updateCharacters()
            time.sleep(self.tickRate)
            self.drawDaleks()
            self.drawDoctor()
            
            if len(self.daleks) == 0: 
                break
            for k, v in self.pressedKeys.items():
                self.pressedKeys[k] = False
            while self.paused:
                time.sleep(1)
        
        if self.alive:
            self.boardInfo.set('You won!')
        else:
            self.boardInfo.set(f'You lost... There was {len(self.daleks)} daleks left')
        self.restartButton = tk.Button(self.root,
                                        text='RESTART',
                                        activeforeground='red',
                                        command=self.restart)
        self.restartButton.pack(side=tk.TOP)
    
    def updateCharacters(self):
        """Updates the positions of the characters for the next turn"""
        if self.pressedKeys['t']:
            self.doctor.sonicTeleport()
        else:
            row, col = 0, 0
            for k, v in self.pressedKeys.items():
                if v: 
                    row += self.WASD_DICT[k][0]
                    col += self.WASD_DICT[k][1]
            self.doctor.move(row, col)
            
        for dalek in self.daleks:
            dalek.dalekMove()
            
    def drawDaleks(self):
        """Places the daleks on the board, killing them on disallowed square."""
        for dalek in self.daleks:
            row, col = dalek.coordinates
            if self.grid.grid_slaves(row=row, column=col)[0]['text'] not in dalek.KILL_CHARS:
                self.grid.grid_slaves(row=row, column=col)[0]['text'] = self.DALEK_SQUARE
            else:
                self.grid.grid_slaves(row=row, column=col)[0]['text'] = dalek.DEATH_CHAR
                self.daleks = [d for d in self.daleks if d.coordinates != (row, col)]
    
    def drawDoctor(self):
        """Places the doctor on the board, killing him if on disallowed square"""
        row, col = self.doctor.coordinates
        if self.grid.grid_slaves(row=row, column=col)[0]['text'] not in self.doctor.KILL_CHARS:
            self.grid.grid_slaves(row=row, column=col)[0]['text'] = self.DOCTOR_SQUARE
        else:
            self.grid.grid_slaves(row=row, column=col)[0]['text'] = self.doctor.DEATH_CHAR
            self.alive = False
    
    def keyPress(self, event):
        self.pressedKeys[event.keysym] = True
        
    def pause(self, event):
        self.paused = not self.paused
        
    def restart(self):
        self.initializeBoard(restart=True)
        self.play(restart=True)
        self.restartButton.destroy()
                 
def main():
    root = tk.Tk()
    new_game = Game(root)
    # new_game.play()
    root.mainloop()
    
if __name__ == '__main__':
    main()