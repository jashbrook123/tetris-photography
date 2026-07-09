import numpy as np
import random
import time
import pygame
import game_class as gc

def get_coords(x, y,w,h):
    newx = x*w
    newy = y*h
    return (newx,newy)

def render_board(screen,board,piece):
    new_board = gc.merge_piece(board,piece)
    for y in range(19,-1,-1):
        for x in range(0,10):
            if new_board[y][x] != 0:
                shape_num = new_board[y][x]
                image = pygame.transform.scale_by(pygame.image.load(f"assets/{shape_num}.png"),1)
                coords = get_coords(x,y,image.get_width(),image.get_height())
                screen.blit(image,coords)
    
def display_next(screen,next_piece,text_font):
    txt = text_font.render("Next: ",True, (255,0,0))
    screen.blit(txt,(190,50))
    piece_matrix = next_piece.matrix
    temp_surf = pygame.Surface((100,400))
    for y in range(len(piece_matrix)-1,-1,-1):
        for x in range(0,len(piece_matrix[y])):
            if piece_matrix[y][x] != 0:
                shape_num = piece_matrix[y][x]
                image = pygame.transform.scale_by(pygame.image.load(f"assets/{shape_num}.png"),1)
                coords = get_coords(x,y,image.get_width(),image.get_height())
                temp_surf.blit(image,(coords[0],coords[1]-25))
    temp_surf = temp_surf.convert_alpha()
    temp_surf.set_colorkey((0,0,0))
    screen.blit(temp_surf,(190,50))
    
def rend_num(screen,score,text_font): #draws numbers onto each face
     txt = text_font.render(f"Score: {score}",True, (255,0,0))
     screen.blit(txt,(200,0))

def rend_back(screen):
    alpha = 50 # low = more invisible
    for x in range(10):
        for y in range(20):
            image = pygame.transform.scale_by(pygame.image.load(f"assets/back_tile.png"),1)
            image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            coords = get_coords(x,y,image.get_width(),image.get_height())
            screen.blit(image,coords)


def start_game():
    pygame.init()
    text_font = pygame.font.SysFont("Arial",15)
    screen = pygame.Surface((160, 320))
    big_screen = pygame.display.set_mode((480,960))
    clock = pygame.time.Clock()
    dt = 0
    db_time = 250  # ms
    past_click = 250

    game_running = True

    board = gc.Board()
    piece_type = random.choice(list(gc.tetrominoes.keys()))
    piece = getattr(gc, "Piece")(piece_type)
    next_piece_type = random.choice(list(gc.tetrominoes.keys()))
    next_piece = getattr(gc, "Piece")(next_piece_type)

    last_drop = time.time()
    drop_speed = 0.25 #smaller = harder 
    landed_pieces = []
    score = 0

    p_list = []

    while game_running:
        screen.fill((255,255,255))
        rend_back(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_w or event.key == pygame.K_UP: piece = gc.rotate_move(board,piece)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT: piece = gc.left(board,piece)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: piece = gc.right(board,piece)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:   
                    now = pygame.time.get_ticks()
                    if now - past_click <= db_time: piece = gc.slam(board,piece)
                    else: piece = gc.soft_drop(board,piece)
                    past_click = now
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        last_drop,game_running,piece,board,landed_pieces,score,next_piece = gc.game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces,score,next_piece)
        score = int(score)
        rend_num(screen,score,text_font)
        display_next(screen,next_piece,text_font)
        render_board(screen,board,piece)
        big_screen.blit(pygame.transform.scale_by(screen,3),(0,0))
    
        pygame.display.flip()

        dt = clock.tick(60) / 1000
    pygame.quit()
    return score

print(start_game())
