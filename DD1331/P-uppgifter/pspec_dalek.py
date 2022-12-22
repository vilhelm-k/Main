class Character:
    row: int
    col: int
    def __init__(self, row: int, col: int) -> None:
        # Creates a new character at location (row, col)
        pass
        
    def coordinates(self) -> tuple:
        # Returns (self.row, self.col)
        pass
    
    def moveExecute(self, newRow: int, newCol: int, game) -> bool:
        # Checks if move is possible and executes it by changing the position of self
        pass
    
    def moveInitial(self, key: int, game) -> None:
        # Initializes the move by setting current square in self to '.'
        # Calls moveExecute, first in main direction. If diagonal, it also tries to move straight
        pass

class Doctor(Character):
    BLOCKED_CHARS = ['*', '#']
    KILL_CHARS = ['A', '#']
    
    def doctorMove(self, game) -> None:
        # Prompts user to select move direction or to use sonicTeleport
        pass
                
    def sonicTeleport(self, game, easy: bool) -> None:
        # Randomly selects a valid square to move.
        # If difficulty is easy it also checks so there are no daleks within immediate proximity, hence guaranteeing survival.
        pass
        
class Dalek(Character):
    BLOCKED_CHARS = ['*']
    KILL_CHARS = ['A', '#']
    
    def dalekMove(self, game) -> None:
        # Checks where the doctor is and determines generates a direction to move in.
        # Use of math.atan2 combined with random.choices to randomly select weighted move direction if move delta is 
        # inbetween possible move directions depending on how close they are to delta to doctor
        pass
        
class Board(list):
    def __str__(self):
        # 2D-list with different print 
        pass

class Game:
    VALID_INPUTS = ['D', 'A', '*', '.', '#']
    board: Board
    doctor: Doctor
    daleks: list #List of daleks
    difficulty: str
    
    def __init__(self, filename: str = None) -> None:
        # Either preselected file or it prompts user to input something
        # Sets board to be equal to 2D-array taken from the inputfile
        # Goes through file, checking if it is valid, and returns where it is invalid if not.
        # When it runs into 'A' or 'D' it creates a Doctor or Dalek character in self.doctor or in self.dalek list.
        # Asks for difficulty
        pass
        
    def play(self) -> None:
        # Runs a while loop
        # Runs self.doctor.doctorMove(), then loops through self.daleks and has them all move also
        # Runs through daleks, placing 'A' at each of their coordinates. If they're new square is in KILL_CHARS
        # it places a # and removes all daleks with this coordinate
        # Places the doctor. If this square is in KILL_CHARS its game over
        # Checks if there are 0 daleks left and if so ends game
        # Loop repeats
        pass
                 
def main():
    new_game = Game()
    new_game.play()
    
if __name__ == '__main__':
    main()