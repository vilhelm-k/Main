import tkinter as tk
import random

class Minesweeper:
    def __init__(self):
        self.root = tk.Tk()
        self.start_menu()
        self.root.mainloop()
    
    def start_menu(self):
        # Clear the frame
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create the start menu
        tk.Label(self.root, text='Number of columns:').pack()
        columns_entry = tk.Entry(self.root, width=5)
        columns_entry.pack()
        tk.Label(self.root, text='Number of rows:').pack()
        rows_entry = tk.Entry(self.root, width=5)
        rows_entry.pack()
        tk.Label(self.root, text='Number of bombs:').pack()
        bombs_entry = tk.Entry(self.root, width=5)
        bombs_entry.pack()
        tk.Button(self.root, text='Start', command=lambda: self.start_game(rows_entry.get(), columns_entry.get(), bombs_entry.get())).pack()

    def start_game(self, rows, columns, bombs):
        # Validate input
        try:
            rows = int(rows)
            columns = int(columns)
            bombs = int(bombs)
            if rows < 1 or columns < 1 or bombs < 1 or bombs > rows * columns - 9:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror('Error', 'Invalid input')
            return

        # Update the game settings
        self.rows = rows
        self.columns = columns
        self.number_of_bombs = bombs

        # Clear the frame and create a new set of buttons
        for widget in self.root.winfo_children():
            widget.destroy()
        grid_frame = tk.Frame(self.root)
        grid_frame.pack()
        self.buttons = [[None for _ in range(columns)] for _ in range(rows)]
        for i in range(rows):
            for j in range(columns):
                button = tk.Button(grid_frame, text='', width=1, height=1)
                button.bind('<Button-1>', lambda _, i=i, j=j: self.reveal(i, j))
                button.bind('<Control-Button-1>', lambda _, i=i, j=j: self.flag(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        # Reset game state
        self.ongoing = True
        self.first_click = True
        self.flagged = set()
        self.revealed = set()
        self.bombs = set()
        self.remaining_tracker_text = tk.StringVar()
        self.remaining_tracker_text.set(f'Remaining flags: {self.number_of_bombs - len(self.flagged)}')
        tk.Label(self.root, textvariable=self.remaining_tracker_text).pack()

    def reveal(self, i, j):
        if (i, j) in self.flagged or (i, j) in self.revealed:
            return
        button = self.buttons[i][j]
        self.revealed.add((i, j))

        if self.first_click:
            self.place_bombs(i, j)
            self.first_click = False

        if (i, j) in self.bombs:
            # You lose!
            self.clicked_bomb(button)
            return

        self.clicked_empty(button, i, j)

        # Check if the player has won
        if len(self.revealed) == self.rows * self.columns - self.number_of_bombs and self.ongoing:
            self.ongoing = False
            self.reveal_all()
            self.game_over('You won!')

    def flag(self, i, j):
        if (i, j) in self.revealed:
            return
        button = self.buttons[i][j]
        if (i, j) in self.flagged:
            # Remove the flag
            button.config(fg='black', text='')
            self.flagged.remove((i, j))
        else:
            # Add a flag
            button.config(fg='red', text='F')
            self.flagged.add((i, j))
        self.remaining_tracker_text.set(f'Remaining flags: {self.number_of_bombs - len(self.flagged)}')

    def place_bombs(self, i, j):
        self.bombs = set()
        # Ensure that the first square clicked and its neighbors don't have any bombs
        illegal_squares = [(x, y) for x in range(i-1, i+2) for y in range(j-1, j+2)]
        while len(self.bombs) < self.number_of_bombs:
            i = random.randint(0, self.rows - 1)
            j = random.randint(0, self.columns - 1)
            if (i, j) not in illegal_squares:
                self.bombs.add((i, j))

    def reveal_all(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.reveal(i, j)
    
    def clicked_bomb(self, button):
        if self.ongoing:
            self.ongoing = False
            self.reveal_all()
            self.game_over('Game over')
        button['text'] = 'X'
        button['highlightbackground'] = 'red'
    
    def clicked_empty(self, button, i, j):
        if self.ongoing:
            button['highlightbackground'] = 'grey'
        # Count the number of bombs in the surrounding squares
        count = 0
        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if (x, y) in self.bombs:
                    count += 1
        if count == 0:
            # If there are no adjacent bombs, reveal all adjacent squares
            self.flood_fill(i, j)
            return
        button['text'] = str(count)
    
    def flood_fill(self, i, j):
        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if x >= 0 and x < self.rows and y >= 0 and y < self.columns:
                    self.reveal(x, y)

    def game_over(self, message):
        # Create a new frame on top of the existing frame and show the game over message as well as a restart and exit button
        game_over_frame = tk.Frame(self.root)
        game_over_frame.pack()
        tk.Label(game_over_frame, text=message).pack()
        tk.Button(game_over_frame, text='Restart', command=self.start_menu).pack()
        tk.Button(game_over_frame, text='Exit', command=self.root.destroy).pack()

# Create the Minesweeper game
Minesweeper()