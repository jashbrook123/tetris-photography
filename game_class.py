import numpy as np
import random
import time
import pygame
points_dist = {"1":100,
              "2":250,
              "3":500,
              "4":1000}
tetrominoes = {
    "I": [
        [1, 1, 1, 1]
    ],
    "O": [
        [2, 2],
        [2, 2]
    ],
    "T": [
        [0, 3, 0],
        [3, 3, 3]
    ],
    "S": [
        [0, 4, 4],
        [4, 4, 0]
    ],
    "Z": [
        [5, 5, 0],
        [0, 5, 5]
    ],
    "J": [
        [6, 0, 0],
        [6, 6, 6]
    ],
    "L": [
        [0, 0, 7],
        [7, 7, 7]
    ]
}

def rotate_matrix(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

def collision(board,piece,newx,newy,matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] != 0:
                boardx = newx + col
                boardy = newy + row

                # edge cases
                if boardx < 0: return True
                if boardx >= board.width: return True
                if boardy >= board.height: return True
                
                # check for other pieces
                if boardy >= 0 and (board.grid)[boardy][boardx] !=0: return True 
    return False

def merge_piece(board,piece):
    net_copy = np.copy(board.grid)
    for row in range(len(piece.matrix)):
        for col in range(len(piece.matrix[row])):
            if piece.matrix[row][col] != 0:
                boardx = piece.x + col
                boardy = piece.y + row
                (net_copy)[boardy][boardx] = piece.matrix[row][col]
    return net_copy

def clear_lines(board):
    temp_grid = []
    cleared = 0
    for row in board.grid:
        if 0 not in row:
            cleared += 1
        else:temp_grid.append(row)

    for rows in range(cleared):
        temp_grid.insert(0,[0]*board.width)  
    board.grid = temp_grid
    return cleared

def get_input():
    if msvcrt.kbhit(): return msvcrt.getch()
    return None



class Board:
    def __init__(self):
        self.grid = np.zeros((20, 10), dtype=int)
        self.width = 10
        self.height = 20

class Piece:
    def __init__(self, shape):
        self.image_list = []
        self.matrix = [row[:] for row in tetrominoes[shape]]
        self.x = 3
        self.y = 0

    def rotate(self,board):
        rotated = rotate_matrix(self.matrix)
        if not collision(board,self,self.x,self.y,rotated):
            self.matrix = rotated

def game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces,score,next_piece):

    if time.time() - last_drop > drop_speed:
        last_drop = time.time()

        if not collision(board, piece, piece.x, piece.y + 1, piece.matrix):
            piece.y += 1
        else: 
            board.grid = merge_piece(board, piece)
            cleared_lines = clear_lines(board)
            piece = next_piece
            piece_type = random.choice(list(tetrominoes.keys()))
            next_piece = globals()["Piece"](piece_type)
            
            if collision(board, piece, piece.x, piece.y, piece.matrix):
                game_running = False
            if cleared_lines != 0:
                gained_points = points_dist[str(cleared_lines)]
                score += gained_points/drop_speed
                drop_speed -= gained_points/100000
    return last_drop,game_running,piece,board,landed_pieces,score,next_piece

def left(board,piece):
    if not collision(board, piece, piece.x - 1, piece.y, piece.matrix):
        piece.x -= 1
    return piece

def right(board,piece):
    if not collision(board, piece, piece.x + 1, piece.y, piece.matrix):
        piece.x += 1
    return piece

def soft_drop(board,piece):
    if not collision(board, piece, piece.x, piece.y + 1, piece.matrix):
        piece.y += 1
    return piece

def slam(board,piece):
    while not collision(board, piece, piece.x, piece.y + 1, piece.matrix):
        piece.y += 1
    return piece

def rotate_move(board,piece):
    piece.rotate(board)
    return piece
