# 2048.py
# CLI version of the 2048 game in python.
#
# - wasd for controls
# - Does not support windows
from random import randint
import tty, sys

def print_inline(s):
    print(s, end='')
def print_new_line():
    print('')

def count_zeroes():
    return sum([sum([1 for c in r if c == 0]) for r in x])

def max_value():
    return max([max(r) for r in x])

def print_board():
    for i in range(0,4):
        for j in range(0,4):
            print_inline('{:5d}'.format(x[i][j])),
        print_new_line()
    print_new_line()

def add_number():
    pos = randint(0, count_zeroes() - 1)
    for i in range(0,4):
        for j in range(0,4):
            if (x[i][j] == 0):
                if (pos == 0): x[i][j] = 2
                pos -= 1;

def gravity():
    changed = False
    for i in range(0,4):
        for j in range(0,4):
            k = i
            while (k < 4 and x[k][j] == 0): k+=1
            if (k != i and k < 4):
                x[i][j], x[k][j] = x[k][j], 0
                changed = True
    return changed

def sum_up():
    changed = False
    for i in range(0,3):
        for j in range(0,4):
            if (x[i][j] != 0 and x[i][j] == x[i+1][j]):
                x[i][j] = 2*x[i][j]
                x[i+1][j] = 0
                changed = True
    return changed

def process_move(c):
    moves = "wasd" # up, left, down, right
    for i in range(len(moves)):
        if moves[i] == c:
            rotate(i)
            changed = any([gravity(), sum_up(), gravity()])
            rotate(4-i)
            return changed
    print ("invalid move")
    return False

def rotate(n): # rotate 90 degrees n times
    for i in range(0,n):
        y = [row[:] for row in x] # clone x
        for i in range(0,4):
            for j in range(0,4):
                x[i][3-j] = y[j][i]

# Initialize board.
x = [[0 for c in range(4)] for r in range(4)]

def getc():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

add_number()
while True:
    print_board()
    move = getc()
    if (move == 'q'):
        print_inline ("Exiting...\n")
        break
    moved = process_move(move)
    if moved: add_number()
    if (max_value() >= 2048):
        print_inline ("You win\n")
        break
    if (count_zeroes() == 0):
        print_inline ("You lost\n")
        break
