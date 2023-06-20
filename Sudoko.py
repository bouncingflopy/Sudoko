import pygame as pg
import math

board = [
[9, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0, 7],
[5, 0, 0, 0, 0, 3, 0, 0, 4],
[0, 0, 7, 0, 0, 0, 2, 0, 0],
[0, 0, 3, 6, 0, 8, 0, 0, 0],
[0, 0, 0, 4, 0, 0, 6, 1, 0],
[0, 8, 5, 0, 4, 0, 0, 0, 0],
[0, 0, 0, 3, 2, 0, 0, 6, 0],
[0, 4, 0, 0, 1, 0, 0, 9, 0]]

print("edit? (y/n)")
if (input() == "y"):
    board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
squares = []

pg.init()
fps = 30
width = 720
height = 720
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Sudoko Solver")
screen.fill((84, 94, 110))

class Square:
    def __init__(self, value, row, col, locked):
        self.value = value
        self.row = row
        self.col = col
        self.x = row * 80
        self.y = col * 80
        self.locked = locked
        if locked:
            self.color = (159, 176, 201)
        else:
            self.color = (202, 213, 230)

    def Draw(self):
        pg.draw.rect(screen, self.color, pg.Rect(self.x+5, self.y+5, 70, 70))
        font = pg.font.SysFont("comicsans", 40)
        if self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            screen.blit(text, (self.x+40-text.get_width()/2, self.y+40-text.get_height()/2))

    def Set(self, value):
        if not self.locked:
            self.value = value

def Setup():
    for x in range(9):
        sq = []
        for y in range(9):
            if board[y][x] == 0:
                sq.append(Square(board[y][x], x, y, False))
            else:
                sq.append(Square(board[y][x], x, y, True))
            sq[y].Draw()
        squares.append(sq)

    pg.draw.line(screen, (222, 79, 69), (240, 0), (240, 720), 3)
    pg.draw.line(screen, (222, 79, 69), (480, 0), (480, 720), 3)
    pg.draw.line(screen, (222, 79, 69), (0, 240), (720, 240), 3)
    pg.draw.line(screen, (222, 79, 69), (0, 480), (720, 480), 3)

def Redraw():
    for row in squares:
        for square in row:
            square.Draw()

def valid(selected, number, ret):
    valid = True

    if number == 0:
        squares[selected[1]][selected[0]].Set(number)
        return None

    for s in squares[selected[1]]:
        if s.value == number:
            valid = False
    for s in range(9):
        if squares[s][selected[0]].value == number:
            valid = False
    sx = math.floor(selected[0]/3)
    sy = math.floor(selected[1]/3)
    for sa in range(3):
        for sb in range(3):
            if squares[sy*3+sa][sx*3+sb].value == number:
                valid = False

    if valid:
        if ret:
            squares[selected[1]][selected[0]].Set(number)
        return True
    else:
        return False

def count(current):
    output = 0

    for i in range(1, 9):
        output += valid(current, i, False)

    return output

def minCount():
    output = 10
    s = None

    for r in squares:
        for square in r:
            if square.value == 0:
                if count([square.col, square.row]) < output:
                    output = count([square.col, square.row])
                    s = square

    return [s.col, s.row]

def Change(current, amount):
    if amount == 0:
        while squares[current[1]][current[0]].locked:
            current[0] = (current[0] + 1) % 9
            if current[0] == 0:
                current[1] = (current[1] + 1) % 9
                if current[1] == 0:
                    return current
    elif amount == 1:
        current[0] = (current[0] + 1) % 9
        if current[0] == 0:
            current[1] = (current[1] + 1) % 9
            if current[1] == 0:
                return 0
        while squares[current[1]][current[0]].locked:
            current[0] = (current[0] + 1) % 9
            if current[0] == 0:
                current[1] = (current[1] + 1) % 9
                if current[1] == 0:
                    return 0
    elif amount == -1:
        current[0] = (current[0] - 1) % 9
        if current[0] == 8:
            current[1] = (current[1] - 1) % 9
            if current[1] == 8:
                return 0
        while squares[current[1]][current[0]].locked:
            current[0] = (current[0] - 1) % 9
            if current[0] == 8:
                current[1] = (current[1] - 1) % 9
                if current[1] == 8:
                    return 0
    return current

def solved():
    for l in squares:
        for s in l:
            if s.value == 0:
                return False
    return True

def Solve():
    current = minCount()
    value = 1
    current = Change(current, 0)
    if current == 0:
        return 1
    selected = squares[current[1]][current[0]]
    selected.color = (127, 0, 0)
    past = []
    while True:
        if valid(current, value, True):
            selected.color = (202, 213, 230)
            selected.Set(value)
            if solved():
                return 1
            past.append(current)
            current = minCount()
            if current == 0:
                return 1
            value = 1
            selected = squares[current[1]][current[0]]
            selected.color = (127, 0, 0)
        else:
            if value < 9:
                value += 1
            else:
                if len(past) > 0:
                    current = past[-1]
                    del past[-1]
                else:
                    current = minCount()
                selected.color = (202, 213, 230)
                if current == 0:
                    return 1
                selected.Set(0)
                selected = squares[current[1]][current[0]]
                selected.color = (127, 0, 0)
                value = selected.value

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return 0
                if event.key == pg.K_SPACE:
                    return 1

        Redraw()
        pg.display.update()
    return 0

def main():
    Setup()
    selected = None
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return None
                if selected != None:
                    if event.key == pg.K_1:
                        valid(selected, 1, True)
                    if event.key == pg.K_2:
                        valid(selected, 2, True)
                    if event.key == pg.K_3:
                        valid(selected, 3, True)
                    if event.key == pg.K_4:
                        valid(selected, 4, True)
                    if event.key == pg.K_5:
                        valid(selected, 5, True)
                    if event.key == pg.K_6:
                        valid(selected, 6, True)
                    if event.key == pg.K_7:
                        valid(selected, 7, True)
                    if event.key == pg.K_8:
                        valid(selected, 8, True)
                    if event.key == pg.K_9:
                        valid(selected, 9, True)
                    if event.key == pg.K_0:
                        valid(selected, 0, True)
                    if event.key == pg.K_SPACE:
                        st = Solve()
                        if st == 0:
                            return None
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                for x in range(9):
                    for y in range(9):
                        if squares[y][x].x+5 < pos[0] < squares[y][x].x+75 and squares[y][x].y+5 < pos[1] < squares[y][x].y+75:
                            selected = (x, y)

        Redraw()
        pg.display.update()

main()
pg.quit()
