import random
from random import shuffle
import copy
import tkinter as tk


class Sudoku_GUI:
    def __init__(self, master, game):
        self.game = game
        self.master = master
        self.master.title('SUDOKU')
        self.master.geometry('760x860')
        self.master.config(bg='gray20')
        self.master.resizable(False, False)

        self.MARGIN = 20
        self.SIDE = 80
        self.WIDTH = self.HEIGHT = self.MARGIN * 2 + self.SIDE * 9

        self.row, self.col = -1, -1

        self.make_top_row()

        self.canvas = tk.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg='gray20', highlightthickness=0)
        self.canvas.pack(fill='both', side=tk.TOP)

        self.make_bottom_row()

        self.draw_grid()
        self.draw_puzzle()

        self.done = False

        self.canvas.bind('<Button-1>', self.box_click)
        self.canvas.bind('<Key>', self.key_press)

    def make_top_row(self):
        self.top_row = tk.Canvas(self.master, width=self.WIDTH, height=40)
        self.choice = tk.StringVar(self.top_row)
        self.choice.set('EASY')
        self.menu = tk.OptionMenu(self.top_row, self.choice, *self.game.levels.keys(), command=self.change_level)
        self.top_row.config(bg='gray20', highlightthickness=0)
        self.menu.pack(pady=(self.MARGIN, 0))
        self.top_row.pack(side=tk.TOP)

    def make_bottom_row(self):
        self.bottom_row = tk.Canvas(self.master, width=self.WIDTH, height=40)
        self.clear_btn = tk.Button(self.bottom_row, text='CLEAR', width=20, command=self.clear_answers)
        self.new_btn = tk.Button(self.bottom_row, text='NEW', width=20, command=self.new_game)
        self.solve_btn = tk.Button(self.bottom_row, text='SOLVE', width=20, command=self.solve_game)
        self.clear_btn.pack(side=tk.LEFT)
        self.solve_btn.pack(side=tk.LEFT)
        self.new_btn.pack(side=tk.LEFT)
        self.bottom_row.pack(side=tk.TOP)

    def get_level(self):
        self.pick = self.choice.get()

    def change_level(self, event):
        self.get_level()
        self.canvas.delete('winner')
        self.canvas.delete('cursor')
        self.game.__init__(self.pick)
        self.draw_puzzle()

    def block_coordinates(self):
        x0 = self.MARGIN
        y0 = self.MARGIN
        x1 = self.MARGIN + self.SIDE * 3
        y1 = self.MARGIN + self.SIDE * 3
        self.draw_blocks(x0, y0, x1, y1)

        x0 = self.MARGIN
        y0 = self.MARGIN + self.SIDE * 6
        x1 = self.MARGIN + self.SIDE * 3
        y1 = self.MARGIN + self.SIDE * 9
        self.draw_blocks(x0, y0, x1, y1)

        x0 = self.MARGIN + self.SIDE * 3
        y0 = self.MARGIN + self.SIDE * 3
        x1 = self.MARGIN + self.SIDE * 6
        y1 = self.MARGIN + self.SIDE * 6
        self.draw_blocks(x0, y0, x1, y1)

        x0 = self.MARGIN + self.SIDE * 6
        y0 = self.MARGIN
        x1 = self.MARGIN + self.SIDE * 9
        y1 = self.MARGIN + self.SIDE * 3
        self.draw_blocks(x0, y0, x1, y1)

        x0 = self.MARGIN + self.SIDE * 6
        y0 = self.MARGIN + self.SIDE * 6
        x1 = self.MARGIN + self.SIDE * 9
        y1 = self.MARGIN + self.SIDE * 9
        self.draw_blocks(x0, y0, x1, y1)

    def draw_blocks(self, x0, y0, x1, y1):
        color = 'gray30'
        self.canvas.create_rectangle(x0, y0, x1, y1, tags='block', fill=color, outline=color)
        x = y = self.MARGIN + 4 * self.SIDE + self.SIDE / 2

    def draw_grid(self):
        self.block_coordinates()
        for i in range(10):
            if i % 3 == 0:
                color = 'turquoise3'
            else:
                color = 'light gray'

            x0 = self.MARGIN + i * self.SIDE
            y0 = self.MARGIN
            x1 = self.MARGIN + i * self.SIDE
            y1 = self.HEIGHT - self.MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=2)

            x0 = self.MARGIN
            y0 = self.MARGIN + i * self.SIDE
            x1 = self.WIDTH - self.MARGIN
            y1 = self.MARGIN + i * self.SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=2)

    def draw_puzzle(self):
        self.canvas.delete('numbers')
        for i in range(9):
            for j in range(9):
                answer = self.game.grid[i][j]
                if answer != 0:
                    x = self.MARGIN + j * self.SIDE + self.SIDE / 2
                    y = self.MARGIN + i * self.SIDE + self.SIDE / 2
                    original = self.game.start[i][j]
                    if answer == original:
                        color = 'white'
                    else:
                        color = 'orange'
                    self.canvas.create_text(x, y, font=('Arial', 20, 'bold'), text=answer, tags='numbers', fill=color)

    def draw_cursor(self):
        self.canvas.delete('cursor')
        if self.row >= 0 and self.col >= 0:
            x0 = self.MARGIN + self.col * self.SIDE + 1
            y0 = self.MARGIN + self.row * self.SIDE + 1
            x1 = self.MARGIN + (self.col + 1) * self.SIDE - 2
            y1 = self.MARGIN + (self.row + 1) * self.SIDE - 2
            self.canvas.create_rectangle(x0, y0, x1, y1, outline='orange', width=3, tags='cursor')

    def box_click(self, event):
        if self.done:
            return
        x, y = event.x, event.y
        # CHECK IF CLICK IS IN A BOX
        if (self.MARGIN < x < self.WIDTH - self.MARGIN and self.MARGIN < y < self.HEIGHT - self.MARGIN):
            self.canvas.focus_set()

            # GET ROW AND COL FROM X, Y COORDINATES
            row, col = (y - self.MARGIN) / self.SIDE, (x - self.MARGIN) / self.SIDE
            row = int(row)
            col = int(col)
            # DESELECT AN ALREADY SELECTED BOX
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.start[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.draw_cursor()

    def key_press(self, event):
        if self.done:
            return
        # CHECK IF KEY IS A DIGIT BETWEEN 1-9
        if self.row >= 0 and self.col >= 0 and event.char in "01234567890":
            # SET GRID TO KEY VALUE
            self.game.grid[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.draw_puzzle()
            self.draw_cursor()
            if self.game.grid == self.game.solved:
                self.done = True
                self.draw_win()

    def draw_win(self):
        x0 = self.MARGIN + self.SIDE * 2
        y0 = self.MARGIN + self.SIDE * 3
        x1 = self.MARGIN + self.SIDE * 7
        y1 = self.MARGIN + self.SIDE * 6
        self.canvas.create_rectangle(x0, y0, x1, y1, tags='winner', fill='turquoise3', outline='turquoise3')
        x = y = self.MARGIN + 4 * self.SIDE + self.SIDE / 2
        self.canvas.create_text(x, y, text='YOU WIN!', tags='winner', fill='white', font=('Arial', 32, 'bold'))
        self.clear_btn['state'] = 'disabled'
        self.solve_btn['state'] = 'disabled'

    def clear_answers(self):
        self.canvas.delete('winner')
        self.canvas.delete('cursor')
        self.game.grid = copy.deepcopy(self.game.start)
        self.done = False
        self.draw_puzzle()

    def new_game(self):
        self.canvas.delete('winner')
        self.canvas.delete('cursor')
        self.get_level()
        self.game.__init__(self.pick)
        self.done = False
        self.draw_puzzle()
        self.clear_btn['state'] = 'normal'
        self.solve_btn['state'] = 'normal'

    def solve_game(self):
        self.canvas.delete('cursor')
        self.game.grid = copy.deepcopy(self.game.solved)
        self.done = True
        self.draw_puzzle()
        self.clear_btn['state'] = 'disabled'
        self.solve_btn['state'] = 'disabled'


class Sudoku_Generator:
    def __init__(self, choice='EASY'):
        self.counter = 0
        self.choice = choice
        # BASED ON NUMBER OF BOXES FILLED IN
        self.levels = {'VERY EASY': [51, 53], 'EASY': [37, 50], 'MEDIUM': [32, 36], 'HARD': [27, 31], 'VERY HARD': [20, 26]}
        self.limit = random.randint(self.levels[self.choice][0], self.levels[self.choice][1])
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.generate_puzzle()

    def generate_puzzle(self):
        self.generate_solution(self.grid)
        self.solved = copy.deepcopy(self.grid)

        self.remove_from_grid()
        self.start = copy.deepcopy(self.grid)

    def test_sudoku(self, grid):
        # TEST EACH BOX TO CHECK IF VALID PUZZLE
        for row in range(9):
            for col in range(9):
                num = grid[row][col]

                # REMOVE NUMBER FROM GRID TO CHECK IF VALID
                grid[row][col] = 0
                if not self.valid_location(grid, row, col, num):
                    return False
                else:
                    # PUT NUM BACK IN GRID
                    grid[row][col] = num
        return True

    def num_in_row(self, grid, row, num):
        if num in grid[row]:
            return True
        return False

    def num_in_col(self, grid, col, num):
        for i in range(9):
            if grid[i][col] == num:
                return True
        return False

    def num_in_block(self, grid, row, col, num):
        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3
        for i in range(sub_row, (sub_row + 3)):
            for j in range(sub_col, (sub_col + 3)):
                if grid[i][j] == num:
                    return True
        return False

    def valid_location(self, grid, row, col, num):
        if self.num_in_row(grid, row, num):
            return False
        elif self.num_in_col(grid, col, num):
            return False
        elif self.num_in_block(grid, row, col, num):
            return False
        return True

    def find_empty_square(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return

    def solve_puzzle(self, grid):
        for i in range(0, 81):
            row = i // 9
            col = i % 9

            # NEXT EMPTY BOX
            if grid[row][col] == 0:
                for num in range(1, 10):
                    # CHECK IF NUMBER NOT YET USED IN ROW/COL/BLOCK
                    if self.valid_location(grid, row, col, num):
                        grid[row][col] = num
                        if not self.find_empty_square(grid):
                            self.counter += 1
                            break
                        else:
                            if self.solve_puzzle(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def generate_solution(self, grid):
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # NEXT EMPTY BOX
            if grid[row][col] == 0:
                shuffle(num_list)
                for num in num_list:
                    if self.valid_location(grid, row, col, num):
                        grid[row][col] = num
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                # IF GRID FULL
                                return True
                break
        grid[row][col] = 0
        return False

    def get_non_empty_squares(self, grid):
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

    def remove_from_grid(self):
        # GET ALL NON-EMPTY BOXES
        non_empty_squares = self.get_non_empty_squares(self.grid)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3

        # LIMIT BASED ON DIFFICULTY
        while rounds > 0 and non_empty_squares_count >= self.limit:
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1

            # SAVE REMOVED VALUE
            removed_square = self.grid[row][col]
            self.grid[row][col] = 0

            # SOLVE A COPY
            grid_copy = copy.deepcopy(self.grid)

            self.counter = 0
            self.solve_puzzle(grid_copy)

            # IF MORE THAN ONE SOLUTION, PUT LAST REMOVED VALUE BACK
            if self.counter != 1:
                self.grid[row][col] = removed_square
                non_empty_squares_count += 1
                rounds -= 1
        return


if __name__ == '__main__':
    game = Sudoku_Generator()
    app = tk.Tk()
    gui = Sudoku_GUI(app, game)
    app.mainloop()
