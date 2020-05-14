# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# SUDOKU SOLVING UI PROJECT
# Solve every sudoku problem with Backtracking Algorithm
# By Dat Huynh
# Written in January, 2020
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

import pygame
import time
pygame.init()


# -------------------------------------------------------------
# GUI
# -------------------------------------------------------------
class Board:
    board = [
    [8, 7, 6, 9, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 6, 0, 0, 0],
    [0, 4, 0, 3, 0, 5, 8, 0, 0],
    [4, 0, 0, 0, 0, 0, 2, 1, 0],
    [0, 9, 0, 5, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 4, 0, 3, 0, 6],
    [0, 2, 9, 0, 0, 0, 0, 0, 8],
    [0, 0, 4, 6, 9, 0, 1, 7, 3],
    [0, 0, 0, 0, 0, 1, 0, 0, 4]
    ]

    def __init__(self, width, height, rows, cols, window):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.window = window
        self.cells = [[Cell(width, height, i, j, self.board[i][j]) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None
        self.solvable = True
        self.update()

    # draw grid lines and numbers of sudoku
    def draw(self):
        unit = self.width / 9
        # grid lines
        for i in range(self.rows + 1):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.window, (0, 0, 0), (0, i*unit), (self.width, i*unit), thick)
            pygame.draw.line(self.window, (0, 0, 0), (i*unit, 0), (i*unit, self.height), thick)

        # cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.window)

    # update the 2D list of values from the list of cells
    def update(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # mark and store the position of the selected cell
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    # clear the temporary value of a cell
    def remove(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)
    
    # return the position (row, column) of a mouse click
    def click(self, position):
        if position[0] < self.width and position[1] < self.height:
            unit = self.width / 9
            x = int(position[0] // unit)
            y = int(position[1] // unit)
            return (y, x)
        return None

    # check and update the model if a new added value is valid
    def place(self, value):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_value(value)
            self.update()

            if is_valid(self.model, (row, col), value):
                return True
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp(0)
                self.update()
                return False

    # set the temporary value of an empty cell
    def try_value(self, value):
        self.cells[self.selected[0]][self.selected[1]].set_temp(value)

    # check if all the cells in sudoku are filled
    def is_completed(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].value == 0:
                    return False
        return True

    # solve the sudoku using Backtracking
    # return True if sudoku has been solved
    # return False if sudoku is unsolvable
    def solve(self):
        if self.model is None:
            return False

        # find an empty cell in sudoku
        empty = get_empty(self.model)
        # no empty cell means it has been solved
        if empty is None:
            return True
        else:
            row, col = empty

        # try all the value to find the valid one
        for i in range(1, 10):
            if is_valid(self.model, empty, i):
                self.model[row][col] = i
                self.cells[row][col].set_value(i)
                self.cells[row][col].draw_new(self.window)
                self.update()
                pygame.display.update()
                pygame.time.delay(50)
                
                # recursively solve the next empty cell
                if self.solve():
                    return True
                self.model[row][col] = 0
                self.cells[row][col].set_value(0)
                self.update()
                self.cells[row][col].draw_new(self.window)
                pygame.display.update()
                pygame.time.delay(50)

        return False     
    

class Cell:
    rows = 9
    cols = 9

    def __init__(self, width, height, row, col, value):
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.value = value
        self.temp = 0
        self.selected = False
        self.unit = width / 9
        self.x = self.unit * col
        self.y = self.unit * row
        self.font = pygame.font.SysFont("comicsansms", 46)

    # draw numbers in sudoku and rectangles highlighting selected cells
    def draw(self, window):
        if self.value != 0:
            text = self.font.render(str(self.value), True, (0, 0, 0))
            window.blit(text, (self.x + (self.unit - text.get_width()) / 2, self.y + (self.unit - text.get_height()) / 2))
        elif self.value == 0 and self.temp != 0:
            text = self.font.render(str(self.temp), True, (128, 128, 128))
            window.blit(text, (self.x + 5, self.y + 5))
        if self.selected:
            pygame.draw.rect(window, (0, 0, 192), (self.x, self.y, self.unit, self.unit), 4)

    def draw_new(self, window, check=True):
        pygame.draw.rect(window, (255, 255, 255), (self.x, self.y, self.unit, self.unit), 0)

        if self.value != 0:
            text = self.font.render(str(self.value), True, (0, 0, 0))
            window.blit(text, (self.x + (self.unit - text.get_width()) / 2, self.y + (self.unit - text.get_height()) / 2))
        if check:
            pygame.draw.rect(window, (0, 192, 0), (self.x, self.y, self.unit, self.unit), 4)
        else:
            pygame.draw.rect(window, (192, 0, 0), (self.x, self.y, self.unit, self.unit), 4)

    def set_value(self, value):
        self.value = value

    def set_temp(self, value) :
        self.temp = value

# -------------------------------------------------------------
# SOLVING FUNCTIONS
# -------------------------------------------------------------
def solve(board):
    if board == None:
        return False

    empty = get_empty(board)
    if empty is None:
        return True
    else:
        row, col = empty

    for i in range(1, 10):
        if is_valid(board, empty, i):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0

    return False


# return the first empty cell
def get_empty(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i, j)

    return None


# check if a number can be placed in a cell
def is_valid(board, cell, no):
    row, col = cell

    # check other numbers in row
    for i in range(len(board)):
        if board[row][i] == no and i != col:
            return False

    # check other numbers in column
    for i in range(len(board)):
        if board[i][col] == no and i != row:
            return False

    # check other numbers in block
    first_row = (row // 3) * 3
    first_col = (col // 3) * 3
    for i in range(first_row, first_row + 3):
        for j in range(first_col, first_col + 3):
            if board[i][j] == no and i != row and j != col:
                return False

    return True


# redraw the window
def refresh_window(window, board, current_time, strikes):
    window.fill((255, 255, 255))
    # time
    font = pygame.font.SysFont("comicsansms", 30)
    text = font.render("Time " + str_time(current_time), True, (64, 64, 64))
    window.blit(text, (window.get_width() - 110, window.get_height() - 40))
    if not board.solvable:
        text = font.render("UNSOLVABLE SUDOKU!", True, (192, 0, 0))
        window.blit(text, (20, window.get_height() - 40))
    elif not board.is_completed():
        # strikes
        text = font.render("X " * strikes, True, (192, 0, 0))
        window.blit(text, (20, window.get_height() - 40))
    else:
        text = font.render("SUDOKU SOLVED!", True, (0, 192, 0))
        window.blit(text, (20, window.get_height() - 40))
    # redraw cells and boards
    board.draw()


# given time in seconds, return string with format 'minute:second'
def str_time(time):
    second = time % 60
    minute = time // 60
    hour = minute // 60
    if second < 10:
        format = str(minute) + ":0" + str(second)
    else:
        format = str(minute) + ":" + str(second)
    return format


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("---------------------")

        for j in range(len(board)):
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            print(str(board[i][j]) + " ", end="")
            if j == 8:
                print("")


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku 2020")
    new_board = Board(540, 540, 9, 9, window)
    key = None
    start = time.time()
    strikes = 0

    run = True
    while run:
        current_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    key = None
                    new_board.remove()

                if event.key == pygame.K_SPACE:
                    new_board.solve()
                    if not new_board.is_completed():
                        new_board.solvable = False
                    key = None

                if event.key == pygame.K_RETURN:
                    row, col = new_board.selected
                    if new_board.cells[row][col].temp != 0:
                        if new_board.place(new_board.cells[row][col].temp):
                            print("Success")
                        else:
                            print("Wrong Number")
                            strikes += 1
                        key = None

                        if new_board.is_completed():
                            print("Congratulation!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = new_board.click(position)
                if clicked:
                    new_board.select(clicked[0], clicked[1])
                    key = None

        if new_board.selected and key != None:
            new_board.try_value(key)

        refresh_window(window, new_board, current_time, strikes)
        pygame.display.update()

main()
pygame.quit()