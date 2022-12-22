import tkinter as tk
import random
import os

# Constants for the game
BOARD_SIZE = 8
NUMBER_OF_SHIPS = 5

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ships = []
        self.hits = 0
        self.misses = 0
        self.game_over = False
        
        # Set up the GUI
        self.create_menu()
        self.create_board()
        
        # Place the ships on the board
        self.place_ships()
        
    def create_menu(self):
        # Create a menu with options to fire at the enemy ships, cheat and peek at the enemy ships, and exit
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        game_menu = tk.Menu(menu)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Fire at enemy ships", command=self.fire_at_ships)
        game_menu.add_command(label="Cheat and peek at enemy ships", command=self.peek_at_ships)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        
    def create_board(self):
        # Create a board with a chessboard-like figure to show the game plan and shot markings
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                button = tk.Button(self.board_frame, text=' ', width=2, command=lambda r=i, c=j: self.fire(r, c))
                button.grid(row=i+1, column=j+1)
                self.buttons[i][j] = button
            
        # Add labels for the rows and columns
        for i in range(BOARD_SIZE):
            label = tk.Label(self.board_frame, text=chr(ord('A')+i))
            label.grid(row=0, column=i+1)
            label = tk.Label(self.board_frame, text=str(i+1))
            label.grid(row=i+1, column=0)
            
    def place_ships(self):
        # Place the ships on the board randomly
        for length in range(NUMBER_OF_SHIPS):
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    x = random.randint(0, BOARD_SIZE - length)
                    y = random.randint(0, BOARD_SIZE - 1)
                    if self.check_space(x, y, length, orientation):
                        self.ships.append((x, y, length, orientation))
                        for i in range(length):
                            self.board[y][x+i] = letter
                        placed = True
                else:
                    x = random.randint(0, BOARD_SIZE - 1)
                    y = random.randint(0, BOARD_SIZE - length)
                    if self.check_space(x, y, length, orientation):
                        self.ships.append((x, y, length, orientation))
                        for i in range(length):
                            self.board[y+i][x] = letter
                        placed = True
                        
    def check_space(self, x, y, length, orientation):
        # Check if there is enough space to place a ship at the given coordinates
        if orientation == 'horizontal':
            if x + length > BOARD_SIZE:
                return False
            for i in range(length):
                if self.board[y][x+i] != ' ':
                    return False
        else:
            if y + length > BOARD_SIZE:
                return False
            for i in range(length):
                if self.board[y+i][x] != ' ':
                    return False
        return True
    
    def check_sunk(self, x, y):
        # Check if a ship at the given coordinates has been sunk
        for ship in self.ships:
            if x >= ship[0] and x < ship[0] + ship[2] and y >= ship[1] and y < ship[1] + ship[2]:
                sunk = True
                if ship[3] == 'horizontal':
                    for i in range(ship[2]):
                        if self.board[y][ship[0]+i] != '#':
                            sunk = False
                            break
                else:
                    for i in range(ship[2]):
                       
                        if self.board[ship[1]+i][x] != '#':
                            sunk = False
                            break
                if sunk:
                    self.mark_sunk(ship[0], ship[1], ship[2], ship[3])
                    self.ships.remove(ship)
                    return True
        return False
    
    def mark_sunk(self, x, y, length, orientation):
        # Mark a sunk ship on the board by surrounding it with 'o's
        coord_to_check = [(x, y) for x in range(x-1, x+length+1) for y in range(y-1, y+2)] if orientation == 'horizontal' else [(x, y) for x in range(x-1, x+2) for y in range(y-1, y+length+1)]
        for x, y in coord_to_check:
            if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE:
                if self.board[y][x] == ' ':
                    self.board[y][x] = 'o'
                
    def fire_at_ships(self):
        # Allow the user to fire shots at the enemy ships
        self.root.unbind("<Button-1>")
        self.root.bind("<Button-1>", self.fire)
        
    def fire(self, event=None, row=None, col=None):
        print(f'fire at {row}, {col}')
        # Fire a shot at the specified coordinates
        if event:
            row, col = self.get_button_row_col(event.widget)
        if self.board[row][col] == ' ':
            self.board[row][col] = 'o'
            self.misses += 1
            print("Miss!")
        elif self.board[row][col] in ['o', '#']:
            print("You already fired at this location.")
        else:
            self.board[row][col] = '#'
            self.hits += 1
            print("Hit!")
            if self.check_sunk(col, row):
                print("You sunk a ship!")
        self.update_board()
        if self.game_over:
            self.root.unbind("<Button-1>")
        self.display_hit_percentage()
        if not self.ships:
            print("You won!")
            self.game_over = True
            self.root.unbind("<Button-1>")
            self.root.bind("<Button-1>", self.fire)
        else:
            self.root.unbind("<Button-1>")
            
    def peek_at_ships(self):
        # Allow the user to peek at the enemy ships
        self.root.unbind("<Button-1>")
        self.root.bind("<Button-1>", self.peek)
        
    def peek(self, event=None, row=None, col=None):
        print(f'fire at {row}, {col}')
        # Show the user where the enemy ships are located
        print(f'Peeking at {chr(ord("A")+row)}{col+1}...')
        if event:
            row, col = self.get_button_row_col(event.widget)
        if self.board[row][col] == ' ':
            self.board[row][col] = 'o'
        elif self.board[row][col] in ['o', '#']:
            print("You already fired at this location.")
        else:
            self.board[row][col] = '#'
        self.update_board()
        self.root.unbind("<Button-1>")
        self.root.bind("<Button-1>", self.unpeek)
        
    def unpeek(self, event=None, row=None, col=None):
        # Hide the enemy ships from view again
        if event:
            row, col = self.get_button_row_col(event.widget)
        if self.board[row][col] == 'o':
            self.board[row][col] = ' '
        elif self.board[row][col] == '#':
            self.board[row][col] = 'X'
        self.update_board()
        self.root.unbind("<Button-1>")
        self.hit_percentages = []
        self.high_scores = []
        if os.path.exists('high_scores.txt'):
            with open('high_scores.txt', 'r') as f:
                for line in f:
                    name, percentage = line.strip().split(',')
                    self.hit_percentages.append(float(percentage))
                    self.high_scores.append((name, percentage))
                    
    def display_hit_percentage(self):
        # Display the player's hit percentage
        if self.hits + self.misses == 0:
            hit_percentage = 0
        else:
            hit_percentage = self.hits / (self.hits + self.misses)
        print(f"Hit percentage: {hit_percentage:.2f}")
        if hit_percentage > 0:
            self.hit_percentages.append(hit_percentage)
            name = input("Enter your name for the high scores: ")
            self.high_scores.append((name, hit_percentage))
            self.high_scores.sort(key=lambda x: x[1], reverse=True)
            if len(self.high_scores) > 10:
                self.high_scores = self.high_scores[:10]
            with open('high_scores.txt', 'w') as f:
                for name, percentage in self.high_scores:
                    f.write(f"{name},{percentage}\n")
        
root = tk.Tk()
root.title("Battleship")
game = BattleshipGame(root)
root.mainloop()

# write a function which takes the event as an argument and prints the row and column of the button that was clicked
def print_row_col(event):
    print(event.widget.grid_info()['row'], event.widget.grid_info()['column'])