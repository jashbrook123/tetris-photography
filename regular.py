import numpy as np
import random
import time
import pygame
import game_class as gc

def get_coords(x, y,w,h):
    newx = x*w + 25
    newy = y*h + 25
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
    
def display_store(screen,held_piece,text_font):
    txt = text_font.render("Hold: ",True, (255,0,0))
    screen.blit(txt,(190,150))
    if held_piece == None: return
    piece_matrix = held_piece.matrix
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
    screen.blit(temp_surf,(190,150))

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
    screen = pygame.Surface((350, 450))
    big_screen = pygame.display.set_mode((700, 900))
    pygame.display.set_caption("Tetris")
    pygame.display.set_icon(pygame.image.load("assets/title.jpg"))
    clock = pygame.time.Clock()
    db_time = 250  # ms
    past_click = 250
    game_tick = 1

    game_running = True

    board = gc.Board()
    piece_type = random.choice(list(gc.tetrominoes.keys()))
    piece = getattr(gc, "Piece")(piece_type)
    next_piece_type = random.choice(list(gc.tetrominoes.keys()))
    next_piece = getattr(gc, "Piece")(next_piece_type)
    held_piece = None   

    last_drop = time.time()
    drop_speed = 0.25 #smaller = harder 
    landed_pieces = []
    score = 0
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
                elif event.key == pygame.K_SPACE:
                    if held_piece == None:
                        held_piece = piece
                        held_piece.x = 3
                        held_piece.y = 0
                        
                        piece = next_piece
                        next_piece_type = random.choice(list(gc.tetrominoes.keys()))
                        next_piece = getattr(gc, "Piece")(next_piece_type)
                    else:
                        piece,held_piece = held_piece,piece
                        piece.x = 3
                        piece.y = 0
                elif event.key == pygame.K_ESCAPE:
                    game_tick = 1- game_tick


        if game_tick == 1:
            last_drop,game_running,piece,board,landed_pieces,score,next_piece = gc.game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces,score,next_piece)
        score = int(score)
        rend_num(screen,score,text_font)
        display_next(screen,next_piece,text_font)
        display_store(screen,held_piece,text_font)
        render_board(screen,board,piece)

        big_screen.blit(pygame.transform.scale_by(screen,2),(0,0))
        pygame.display.flip()

        dt = clock.tick(60) / 1000
    pygame.quit()
    return score


start_game()