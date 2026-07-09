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

def warp_surface(surf,p_list,div=200):

    p0 = p_list[0] #botl 1
    p1 = p_list[1] #topl 0
    p3 = p_list[2] #botr 2
    p2 = p_list[3] #topr 3 

    temp_surf = pygame.Surface(surf.get_size(),pygame.SRCALPHA)
    temp_surf.fill((0,0,0,0))
    w, h = temp_surf.get_size()
    tile_w = w / div
    tile_h = h / div

    for y in range(div):
        v0 = y / div
        v1 = (y + 1) / div

        left0  = p0.lerp(p3, v0)
        right0 = p1.lerp(p2, v0)
        left1  = p0.lerp(p3, v1)
        right1 = p1.lerp(p2, v1)

        for x in range(div):
            u0 = x / div
            u1 = (x + 1) / div

            pA = left0.lerp(right0, u0)
            pB = left0.lerp(right0, u1)
            pC = left1.lerp(right1, u1)
            pD = left1.lerp(right1, u0)
            tile = surf.subsurface(
                pygame.Rect(x * tile_w, y * tile_h, tile_w, tile_h)
            )
            center = (pA + pB + pC + pD) / 4
            temp_surf.blit(tile, center)
    return temp_surf


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
    back_image = pygame.image.load("assets/back.png")
    back_image = pygame.transform.scale(back_image, big_screen.get_size())
    sm_back_image = pygame.transform.scale(back_image, screen.get_size())
    while game_running:
        big_screen.blit(back_image,(0,0))
        
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
                elif event.key -- pygame.K_r:
                    p_list = []
                    big_screen.fill((0,0,0))
                    big_screen.blit(back_image,(0,0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                if len(p_list) < 4:
                    p_list.append(pygame.Vector2(mouse_coord))
                    
        if len(p_list) == 4:
            last_drop,game_running,piece,board,landed_pieces,score,next_piece = gc.game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces,score,next_piece)
            score = int(score)
            rend_back(screen)
            render_board(screen,board,piece)

            rot_surf =  warp_surface(pygame.transform.scale_by(screen,3),p_list)
            big_screen.blit(back_image,(0,0))
            big_screen.blit(rot_surf,(0,0))
        pygame.display.flip()

        dt = clock.tick(60) / 1000
    pygame.quit()
    return score

print(start_game())
