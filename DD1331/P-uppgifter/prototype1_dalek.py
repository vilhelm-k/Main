# DALEK

import math
import random


class Character:
    DIRECTIONS_DICT = {
        1: ((-1, -1), -3/4*math.pi),
        2: ((-1, 0), -1/2*math.pi),
        3: ((-1, 1), -1/4*math.pi),
        4: ((0, -1), math.pi),
        5: ((0, 1), 0),
        6: ((1, -1), 3/4*math.pi),
        7: ((1, 0), 1/2*math.pi),
        8: ((1, 1), 1/4*math.pi)
    }
    
    BLOCKED_CHARS = ['*']
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    @property
    def coordinates(self):
        return self.row, self.col
    
    def validMove(self, newRow, newCol, game):
        if not -1 < newRow < game.rows or not -1 < newCol < game.columns:
            return False
        if game.board[newRow][newCol] in self.BLOCKED_CHARS:
            return False
        return True
    
    def move(self, key, game):
        game.board[self.row][self.col] = '.'
        rowDelta, colDelta = self.DIRECTIONS_DICT[key][0]
        
        if self.validMove(self.row + rowDelta, self.col + colDelta, game):
            self.row = self.row + rowDelta
            self.col = self.col + colDelta
            return
        if self.validMove(self.row + rowDelta, self.col, game):
            self.row = self.row + rowDelta
            return
        if self.validMove(self.row, self.col + colDelta, game):
            self.col = self.col + colDelta
            return

class Doctor(Character):
    BLOCKED_CHARS = ['*', '#']
    KILL_CHARS = ['A', '#']
    
    def doctorMove(self, game):
        while True:
            print(game.board)
            print('\nD represents the doctor in the diagram and the numbers your possible movements. Press 0 to use sonic screwdriver and teleport randomly')
            print('1 2 3\n4 D 5\n6 7 8')
            direction = input('What direction do you want to move? Enter 10 to exit: ')
            try:
                direction = int(direction)
            except:
                pass
            if direction == 10:
                quit()
            if direction in self.DIRECTIONS_DICT:
                self.move(direction, game)
                break
            if direction == 0:
                self.sonicTeleport(game, game.difficulty == 'easy')
                break
                
    def sonicTeleport(self, game, easy):
        while True:
            rRow = random.randrange(game.rows)
            rCol = random.randrange(game.columns)
            if game.board[rRow][rCol] != '.':
                continue
            
            if easy:
                adjacentSquares = [game.board[rRow + i][rCol + j] for j in range(-1, 2) for i in range(-1, 2) 
                                   if -1 < rRow + i < game.rows and -1 < rCol + j < game.columns]
                if 'A' in adjacentSquares:
                    continue
            game.board[self.row][self.col] = '.'
            self.row = rRow
            self.col = rCol
            break
        
class Dalek(Character):
    KILL_CHARS = ['A', '#']
    
    def dalekMove(self, game):
        docRow, docCol = game.doctor.coordinates
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
        angleDelta = {k: compareAngles(movementAngle, v[1]) for k, v in self.DIRECTIONS_DICT.items()}
        twoClosest = sorted(angleDelta.items(), key = lambda item: item[1])[:2]
        # Randomly returns one of the two closest depending on weight. Reversed can be used because only choosing between 2
        directionKey = random.choices([x[0] for x in twoClosest], weights=[x[1] for x in reversed(twoClosest)], k=1)
    
        self.move(directionKey[0], game)
        
class Board(list):
    def __str__(self):
        return "\n".join(" ".join(row) for row in self)

class Game:
    VALID_INPUTS = ['D', 'A', '*', '.', '#']
    board: Board
    doctor: Doctor = None
    daleks = []
    difficulty: str
    
    def __init__(self, filename = None):
        # You can either start a game by providing file or else it asks for input.
        # This way you can create courses and levels or allow the user to choose the game, if you would want.
        if filename != None:
            print('Opening file...')
        while True:
            try:
                with open(filename, "r") as file:
                    rows = file.read().splitlines()
                self.board = Board([[*row] for row in rows])
            except:
                filename = input('Input a valid file name to read the course from. Enter STOP to exit.\nFilename: ')
                if filename == 'STOP':
                    quit()
            else:
                break
        
        self.rows = len(self.board)
        self.columns = len(self.board[0])
        
        for i, row in enumerate(self.board):
            if len(row) != self.columns:
                quit(f'Row {i} (0 indexed) is not the same length as the first row. All rows must be equal in length')
            for j, col in enumerate(row):
                # Quickly skips if non character
                if col == '.' or col == '*' or col == '#':
                    continue
                # Error handling
                if col not in self.VALID_INPUTS:
                    quit(f'{col} is not a valid input. Only {self.VALID_INPUTS} are permitted in input file. Error at: Row {i}, Col {j}) (0 index).')
                # Try to add doctor
                if col == 'D':
                    if self.doctor:
                        quit(f'There is more than one doctor. Second one is at {i}, {j} (0 index).')
                    self.doctor = Doctor(i, j)
                # Add dalek
                else:
                    self.daleks.append(Dalek(i, j))
        while True:
            print('Success! Choose difficulty. With Easy you can never die when teleporting but with hard you run the risk.')
            difficulty = input('Easy or Hard? ').lower()
            if difficulty == 'easy' or difficulty == 'hard':
                self.difficulty = difficulty
                return
        
    def play(self):
        # Make smaller functions for updates to make more readable
        while True: 
            # Update characters
            self.doctor.doctorMove(self)
            for dalek in self.daleks:
                dalek.dalekMove(self)
            
            # Draw characters
            for dalek in self.daleks:
                row, col = dalek.coordinates
                if self.board[row][col] not in dalek.KILL_CHARS:
                    self.board[row][col] = 'A'
                else:
                    self.board[row][col] = '#'
                    self.daleks = [d for d in self.daleks if d.coordinates != (row, col)]
            
            docRow, docCol = self.doctor.coordinates
            if self.board[docRow][docCol] not in self.doctor.KILL_CHARS:
                self.board[docRow][docCol] = 'D'
            else:
                self.board[docRow][docCol] = 'X'
                print(self.board)
                quit('Game over')
            
            if len(self.daleks) == 0:
                print(self.board)
                quit('Congratulations! You won :D')
                 
def main():
    new_game = Game('P-uppgifter/readfile.txt')
    new_game.play()
    
if __name__ == '__main__':
    main()