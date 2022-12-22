from __future__ import annotations
import math
import random
import tkinter as tk
import tkinter.filedialog as fd

class Game:
    '''Class containing the game'''
    DALEK_CHAR = 'A'
    DOCTOR_CHAR = 'D'
    WALL_CHAR = '*'
    TRASH_CHAR = '#'
    FLOOR_CHAR = '.'
    DEAD_CHAR = 'X'
    VALID_INPUTS = [WALL_CHAR, TRASH_CHAR, FLOOR_CHAR, DALEK_CHAR, DOCTOR_CHAR]
    EASY_RATE = 400 #ms
    HARD_RATE = 200 #ms
    WASD_DICT = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
        
    def __init__(self, root: tk.Tk) -> None:
        # Variable initialization
        self.tickRate = self.EASY_RATE # Time between ticks
        self.easy = True
        
        # Screen initialization
        self.root = root
        self.root.title('DALEK')
        
        # STARTSCREEN #
        self.startscreen = tk.Frame(self.root)
        self.startscreen.pack()
        
        # Startscreen text
        tk.Label(self.startscreen, text='Welcome to DALEK!', font=('Helvetica', 24, 'bold')).pack()
        tk.Label(self.startscreen, 
                 justify=tk.LEFT,
                 text='The goal of the game is for you, the Doctor, to survive until all daleks are destroyed.'
                       '\nMove with WASD. You can also teleport with your sonic screwdriver which you activate with T.'
                       '\nBe careful! If your difficulty is Hard you can teleport to your death. '

                       '\n\nYou die if the daleks reach you, but if multiple daleks collide they become trash.'
                       '\nIf new daleks walk on trash they are also destroyed.'

                       '\n\nYou can pause with SPACE'

                       '\n\nFirst you need to import a valid text file to use as the course.'
                       '\nIt needs equal length rows and can only contain the characters:'
                       f'\n{self.DOCTOR_CHAR} - doctor'
                       f'\n{self.DALEK_CHAR} - dalek'
                       f'\n{self.FLOOR_CHAR} - floor'
                       f'\n{self.WALL_CHAR} - wall'
                       f'\n{self.TRASH_CHAR} - trash'.strip()).pack(padx=(30, 30))
        
        # Difficulty buttons startscreen
        difficultyFrame = tk.Frame(self.startscreen)
        self.easyButton = tk.Button(difficultyFrame, text='Easy', activeforeground='red', command=self.setEasy, state=tk.ACTIVE)
        self.hardButton = tk.Button(difficultyFrame, text='Hard', activeforeground='red', command=self.setHard)
        difficultyFrame.pack(pady=(0, 15))
        self.easyButton.pack(side=tk.LEFT)
        self.hardButton.pack(side=tk.LEFT)
        
        # Select file button
        self.filename = tk.StringVar()
        self.filename.set('No file selected')
        tk.Label(self.startscreen, textvariable=self.filename).pack()
        tk.Button(self.startscreen, text='Choose file', command=self.selectFile).pack(pady=(0, 15))
        
        # Launch button
        self.launchButton = tk.Button(self.startscreen, text='START', activeforeground='red', state=tk.DISABLED, command=self.play)
        self.launchButton.pack()
        
        # Game metadata
        self.gridInfo = tk.StringVar()
        tk.Label(self.root, textvariable=self.gridInfo).pack()
        
        #Pause text
        self.pauseText = tk.StringVar()
        tk.Label(self.root, textvariable=self.pauseText).pack(side=tk.BOTTOM)
        
        # Grid frame
        self.grid = tk.Frame(self.root)
        self.grid.pack(expand=True, side=tk.BOTTOM)
    
    def setEasy(self) -> None:
        '''Sets difficulty'''
        self.easyButton['state'] = tk.ACTIVE
        self.hardButton['state'] = tk.NORMAL
        self.easy = True
        self.tickRate = self.EASY_RATE
        
    def setHard(self) -> None:
        '''Sets difficulty'''
        self.easyButton['state'] = tk.NORMAL
        self.hardButton['state'] = tk.ACTIVE
        self.easy = False
        self.tickRate = self.HARD_RATE
        
    def selectFile(self) -> None:
        '''Selects file to be used for the game and runs the initialize grid function to create the grid.
        Then updates self.launchButton and self.gridInfo.'''
        filename = fd.askopenfilename(filetypes=(('text files', 'txt'),))
        if not filename:
            return
        self.filename.set(filename)
        with open(self.filename.get(), 'r') as file:
            rows = file.read().splitlines()
        
        # Creates 2d-list which is used to init grid and saved for restart.
        self.board = [[*row] for row in rows]
        self.rows = len(self.board)
        self.columns = len(self.board[0])
        
        self.initializeGrid()
        
        # Displays errors / metadata and enables / disables startbutton
        if self.errors:
            self.gridInfo.set(self.errors)
            self.launchButton['state'] = tk.DISABLED
        else:
            self.launchButton['state'] = tk.ACTIVE
            self.gridInfo.set(f'Rows: {self.rows}, Columns: {self.columns}\nDaleks: {len(self.daleks)}')
            
    def initializeGrid(self) -> None:
        '''Creates the grid, initializes characters and checks for errors by iterating over input file'''
        # Removes existing widgets
        for widget in self.grid.winfo_children():
            widget.destroy()
        self.doctor = None
        self.daleks = []
        
        # Errors
        self.errors = ''
        invalidRows = []
        invalidChars = []
        numberOfDoctors = 0
        
        # Iterates over the board to generate grid. Appends errors and changes label color if error is found.
        for i, row in enumerate(self.board):
            rowError = False
            if len(row) != self.columns:
                invalidRows += [i + 1]
                rowError = True
                
            for j, col in enumerate(row):
                colError = False
                if col not in self.VALID_INPUTS:
                   invalidChars += [col]
                   colError = True
                   
                if col == self.DOCTOR_CHAR:
                    numberOfDoctors += 1
                    if numberOfDoctors > 1:
                        colError = True
                    self.doctor = self.Doctor(i, j, self)
                    
                if col == self.DALEK_CHAR:
                    self.daleks.append(self.Dalek(i, j, self))
                    
                color = '#800e17' if colError else 'red' if rowError else 'black'
                tk.Label(self.grid, text=col, width=1, height=1, bg=color).grid(row=i, column=j)
        
        # Builds self.error
        if invalidRows: self.errors += (f'The following rows are not the same length as row 1: {invalidRows}\n')
        if invalidChars: self.errors += (f'The following disallowed characters are present in file: {invalidChars}\n')
        if numberOfDoctors != 1: self.errors += (f'Wrong number of doctors. Should be 1 but there are {numberOfDoctors}\n')
    
    def play(self) -> None:
        '''Begins the game for the first time by setting up variables, activating binds and calling the 'tick' function'''
        self.startscreen.destroy()
        
        self.alive = True
        self.paused = False
        self.pressedKeys = {'w': False, 'a': False, 's': False, 'd': False}
        self.teleport = False
        self.doctorTick = False
        self.keyHeld = None
        
        self.root.bind('w', self.keyPress)
        self.root.bind('a', self.keyPress)
        self.root.bind('s', self.keyPress)
        self.root.bind('d', self.keyPress)
        self.root.bind('<KeyRelease-w>', self.keyReleaseRepeat)
        self.root.bind('<KeyRelease-a>', self.keyReleaseRepeat)
        self.root.bind('<KeyRelease-s>', self.keyReleaseRepeat)
        self.root.bind('<KeyRelease-d>', self.keyReleaseRepeat)
        self.root.bind('t', self.triggerTeleport)
        self.root.bind('<space>', self.pause)
        
        self.tick()

    def restart(self) -> None:
        '''Restarts the game'''
        self.initializeGrid()
        self.restartFrame.destroy()
        self.alive = True
        self.teleport = False
        
        self.tick()
    
    def gameOver(self) -> None:
        '''Runs after game is over, either after win or loss'''
        if self.alive:
            self.gridInfo.set('You won!')
        else:
            self.gridInfo.set(f'You lost... There was {len(self.daleks)} dalek left')
        
        # Restart frame
        self.easy = True
        self.tickRate = self.EASY_RATE
        self.restartFrame = tk.Frame(self.root)
        self.easyButton = tk.Button(self.restartFrame, text='Easy', activeforeground='red', command=self.setEasy, state=tk.ACTIVE)
        self.hardButton = tk.Button(self.restartFrame, text='Hard', activeforeground='red', command=self.setHard)
        self.restartFrame.pack()
        self.easyButton.pack(side=tk.LEFT)
        self.hardButton.pack(side=tk.LEFT)
        tk.Button(self.restartFrame, text='RESTART', activeforeground='red', command=self.restart).pack()
    
    def tick(self) -> None:
        '''Main function for the realtime aspect of the game. 
        Alternates between doctor and dalek turn.
        Calls itself after delay'''
        if self.paused:
            self.root.after(self.tickRate, self.tick)
            return
    
        if self.doctorTick:
            self.doctorUpdate()
        else:
            self.updateDaleks()
            self.drawDaleks()
            self.gridInfo.set(f'Daleks left: {len(self.daleks)}')
        
        # Doctor drawn every turn since it checks if doctor lives. Cheap so inefficiency doesn't matter
        self.drawDoctor()
        
        if not self.alive or len(self.daleks) == 0:
            self.gameOver()
        else:
            self.doctorTick = not self.doctorTick
            self.root.after(self.tickRate, self.tick)
    
    def doctorUpdate(self) -> None:
        '''Updates position of the doctor'''
        if self.teleport:
            self.doctor.sonicTeleport()
            self.teleport = False
        else:
            netMove = [sum(temp) for temp in zip(*[self.WASD_DICT[k] for k, v in self.pressedKeys.items() if v])]
            self.doctor.move(*(netMove if netMove else (0, 0)))
            
    def drawDoctor(self) -> None:
        '''Draws the doctor to the grid and kills if on its KILL_CHARS'''
        row, col = self.doctor.coordinates
        if self.grid.grid_slaves(row=row, column=col)[0]['text'] not in self.doctor.KILL_CHARS:
            self.grid.grid_slaves(row=row, column=col)[0]['text'] = self.DOCTOR_CHAR
        else:
            self.grid.grid_slaves(row=row, column=col)[0]['text'] = self.doctor.DEATH_CHAR
            self.alive = False
    
    def updateDaleks(self) -> None:
        '''Updates positions of all daleks'''
        for dalek in self.daleks:
            dalek.dalekMove()
    
    def drawDaleks(self) -> None:
        '''Draws the daleks to the grid, delting if on its KILL_CHARS'''
        for dalek in self.daleks:
            row, col = dalek.coordinates
            if self.grid.grid_slaves(row=row, column=col)[0]['text'] not in dalek.KILL_CHARS:
                self.grid.grid_slaves(row=row, column=col)[0]['text'] = self.DALEK_CHAR
            else:
                self.grid.grid_slaves(row=row, column=col)[0]['text'] = dalek.DEATH_CHAR
                self.daleks = [d for d in self.daleks if d.coordinates != (row, col)]
        
    def keyPress(self, event: tk.Event) -> None:
        '''Runs on keypress and repeatedly when held on certain systems'''
        if self.keyHeld:
            self.root.after_cancel(self.keyHeld)
            self.keyHeld = None
        else:
            self.pressedKeys[event.keysym] = True
    
    def keyReleaseRepeat(self, event: tk.Event) -> None:
        '''Runs on keyrelease trigger, incorrectly on some systems. 
        To ensure correct logic, keyPress delays the actual keyRelease function until key'''
        self.keyHeld = self.root.after_idle(self.keyRelease, event)
        
    def keyRelease(self, event: tk.Event) -> None:
        '''Executes after the user releases key'''
        self.keyHeld = None
        self.pressedKeys[event.keysym] = False
    
    def pause(self, event: tk.Event) -> None:
        '''Pauses the game'''
        if self.paused:
            self.pauseText.set('')
        else:
            self.pauseText.set('PAUSED')
        self.paused = not self.paused
    
    def triggerTeleport(self, event: tk.Event) -> None:
        '''Ensures user teleports next turn.'''
        self.teleport = True

    class Character:
        '''Base class for characters in the game'''
        DIRECTIONS = [
            ((-1, -1), -3/4*math.pi),
            ((-1, 0), -1/2*math.pi),
            ((-1, 1), -1/4*math.pi),
            ((0, -1), math.pi),
            ((0, 1), 0),
            ((1, -1), 3/4*math.pi),
            ((1, 0), 1/2*math.pi),
            ((1, 1), 1/4*math.pi)
        ]
        
        def __init__(self, row: int, col: int, game: Game) -> None:
            self.row = row
            self.col = col
            self.game = game
        
        @property
        def coordinates(self) -> tuple:
            return self.row, self.col
        
        def validMove(self, newRow: int, newCol: int) -> bool:
            '''Checks if move is valid'''
            if not -1 < newRow < self.game.rows or not -1 < newCol < self.game.columns:
                return False
            if self.game.grid.grid_slaves(row=newRow, column=newCol)[0]['text'] in self.BLOCKED_CHARS:
                return False
            return True
        
        def move(self, rowDelta: int, colDelta: int) -> None:
            '''Moves character to new square'''
            self.game.grid.grid_slaves(row=self.row, column=self.col)[0]['text'] = self.game.FLOOR_CHAR
            
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
        '''Player character'''
        def __init__(self, row: int, col: int, game: Game) -> None:
            super().__init__(row, col, game)
            self.BLOCKED_CHARS = [game.WALL_CHAR, game.TRASH_CHAR]
            self.KILL_CHARS = [game.DALEK_CHAR, game.TRASH_CHAR]
            self.DEATH_CHAR = game.DEAD_CHAR
                    
        def sonicTeleport(self) -> None:
            '''Teleports doctor character'''
            self.game.grid.grid_slaves(row=self.row, column=self.col)[0]['text'] = self.game.FLOOR_CHAR
            while True:
                rRow = random.randrange(self.game.rows)
                rCol = random.randrange(self.game.columns)
                if self.game.grid.grid_slaves(row=rRow, column=rCol)[0]['text'] != self.game.FLOOR_CHAR:
                    continue
                # If easy it checks so dalek is in square adjacent to destination
                if self.game.easy:
                    adjacentSquares = [self.game.grid.grid_slaves(row=rRow + i, column=rCol + j)[0]['text'] 
                                       for j in range(-1, 2) for i in range(-1, 2) 
                                       if self.validMove(rRow + i, rCol + j)]
                    if self.game.DALEK_CHAR in adjacentSquares:
                        continue
    
                self.row = rRow
                self.col = rCol
                break
            
    class Dalek(Character):
        '''Enemy character'''
        def __init__(self, row: int, col: int, game: Game) -> None:
            super().__init__(row, col, game)
            self.BLOCKED_CHARS = [game.WALL_CHAR]
            self.KILL_CHARS = [game.DALEK_CHAR, game.TRASH_CHAR]
            self.DEATH_CHAR = game.TRASH_CHAR
        
        def dalekMove(self) -> None:
            '''Works out what direction the dalek should move towards follow the doctor'''
            docRow, docCol = self.game.doctor.coordinates
            deltaRow, deltaCol = docRow - self.row, docCol - self.col
            
            if deltaRow == 0 and deltaCol == 0:
                return
            
            idealAngle = math.atan2(deltaRow, deltaCol)
            def compareAngles(a1, a2):
                return math.pi - abs(abs(a1 - a2) - math.pi)
            
            # Creates list like DIRECTIONS but with angle between move direction and idealAngle at index 1
            angleDeltas = [(direction[0], compareAngles(idealAngle, direction[1])) for direction in self.DIRECTIONS]
            # Gets the two closest angles via sorting
            twoClosest = sorted(angleDeltas, key = lambda x: x[1])[:2]
            # Randomly selects one based on weight. reversed used since we want compliment of delta.
            moveDirection = random.choices([x[0] for x in twoClosest], weights=[x[1] for x in reversed(twoClosest)], k=1)
            
            self.move(*moveDirection[0])
        

def main() -> None:
    root = tk.Tk()
    Game(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()