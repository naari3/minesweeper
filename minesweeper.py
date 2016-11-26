# -*- coding: utf-8 -*-
import numpy as np
import random

class Minesweeper(object):
    """docstring for Minesweeper."""
    def __init__(self, width, height, bombs):
        self.width, self.height = width, height
        self.bombs = bombs
        self.bomb_board = self.create_bomb_board() # 0: None, 1: Bomb,
        self.round_board = self.create_round_board() # 0-8: bombs,
        self.opened_board = np.zeros([self.height, self.width], dtype=int) # 0: None, 1: Opened, 2: Flag,
    def create_bomb_board(self):
        a = np.zeros([self.height, self.width], dtype=int)
        for i in range(self.bombs):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            while a[y][x]: # if a[y][x] is it, reshuffle
                x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            else:
                a[y][x] = 1
        return a
    def get_round(self, x, y):
        x1, x2 = x-1, x+2
        y1, y2 = y-1, y+2
        if x1 < 0: x1 = 0
        if x2 > self.width: x2 = self.width
        if y1 < 0: y1 = 0
        if y2 > self.height: y2 = self.height
        return (self.bomb_board[y1:y2, x1:x2]==1).sum()
    def create_round_board(self):
        a = np.zeros([self.height, self.width], dtype=int)
        for x in range(self.width):
            for y in range(self.height):
                a[y][x] = int(self.get_round(x, y))
        return a
    def open_square(self, x, y, checked=[]):
        if self.opened_board[y][x] == 1:
            return True
        if self.bomb_board[y][x] == 1:
            return False
        if not (x, y) in checked:
            if self.round_board[y][x] == 0:
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if i == j == 0: continue
                            if x+i < 0 or y+j < 0: continue
                            if x+i >= self.width or y+j >= self.height: continue
                            checked.append((x, y))
                            self.open_square(x+i, y+j, checked)
            self.opened_board[y][x] = 1
        return True
    def swap_flag(self, x, y):
        if self.opened_board[y][x] == 0:
            self.opened_board[y][x] = 2
        elif self.opened_board[y][x] == 2:
            self.opened_board[y][x] = 0
    def clear_check(self):
        opb = self.opened_board.copy()
        opb[np.where(opb==2)] = 0
        if (self.bomb_board==opb).sum() == 0:
            return True
        else:
            return False
    def print_bomb_board(self):
        print('  '+' '.join([str(i+1) for i in range(self.width)]))
        for y in range(self.height):
            print(str(y+1) + ' ' + ' '.join([' ' if self.bomb_board[y][x]==0 else 'B' for x in range(self.width)]))
    def print_board(self, in_game=False):
        print('  '+' '.join([str(i+1) for i in range(self.width)]))
        for y in range(self.height):
            print(str(y+1) + ' ' + ' '.join(['.' if self.opened_board[y][x]==0 else 'v' if self.opened_board[y][x]==2 else str(self.round_board[y][x]) if self.round_board[y][x]!=0 else ' ' for x in range(self.width)]))

if __name__ == '__main__':
    a = Minesweeper(9,9,10)
    while True:
        a.print_board()
        p = input('> ')
        if 'f' in p:
            x, y = [int(i)-1 for i in p.replace('f', '').split()]
            a.swap_flag(x, y)
        else:
            x, y = [int(i)-1 for i in p.split()]
            result = a.open_square(x, y)
            if result == False:
                print('!!!!!!!!!!!!!!!!!!!!!!!!')
                print('!!!!!!!!!!!!!!!!!!!!!!!!')
                print('!!!!!!!!!!BOMB!!!!!!!!!!')
                print('!!!!!!!!!!!!!!!!!!!!!!!!')
                print('!!!!!!!!!!!!!!!!!!!!!!!!')
                break
        if a.clear_check():
            print('CLEAR!!!!!!!!!!!!!!!!!!!')
            break
        print()
    a.print_bomb_board()
