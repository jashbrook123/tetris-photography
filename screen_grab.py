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
    bigW = screen.get_width()/10
    bigH = screen.get_height()/20
    if bigH < 1: bigH = 1
    if bigW < 1: bigW = 1
    for y in range(19,-1,-1):
        for x in range(0,10):
            if new_board[y][x] != 0:
                shape_num = new_board[y][x]
                image = pygame.transform.scale(pygame.image.load(f"assets/{shape_num}.png"),(bigW,bigH))
                coords = get_coords(x,y,image.get_width(),image.get_height())
                screen.blit(image,coords)    

def rend_back(screen):
    alpha = 50 # low = more invisible
    bigW = screen.get_width()/10
    bigH = screen.get_height()/20
    if bigH < 1: bigH = 1
    if bigW < 1: bigW = 1
    for x in range(10):
        for y in range(20):
            image = pygame.transform.scale(pygame.image.load(f"assets/back_tile.png"),(bigW,bigH))
            image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            coords = get_coords(x,y,image.get_width(),image.get_height())
            screen.blit(image,coords)

def warp_surface(surf,p_list,size,div=100):

    p0 = p_list[0] #topl
    p1 = p_list[1] #topr
    p3 = p_list[2] #botl
    p2 = p_list[3] #botr

    temp_surf = pygame.Surface(size,pygame.SRCALPHA)
    temp_surf.fill((0,0,0,0))
    w, h = surf.get_size()
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

def resize_screen(main_screen, display):
    width = main_screen.get_width()
    height = main_screen.get_height()
    resized_display = pygame.transform.scale(display, (width,height))
    return resized_display

def get_mini_coords(mouse_coord,main_screen,display):
    x,y = mouse_coord.x, mouse_coord.y
    mw,mh = display.get_width(),display.get_height() #miniwidth
    bw,bh = main_screen.get_width(),main_screen.get_height() #bigwidth
    newx = x*(mw/bw)
    newy = y*(mh/bh)
    return pygame.Vector2((newx,newy))

def draw_selection(p_list,display):
    text_font = pygame.font.SysFont("Arial",10)
    for i,coord in enumerate(p_list):
        pygame.draw.circle(display,(255,0,0),coord,5)
        txt = text_font.render(f"{i+1}",True, (255,255,255))
        display.blit(txt,coord)    
    return display

def optimise_screen(p_list):
    tl = p_list[0]
    tr = p_list[1]
    bl = p_list[2]
    br = p_list[3]
    w1 = abs(tr[0] - tl[0])
    w2 = abs(br[0] - bl[0])
    h1 = abs(bl[1] - tl[1])
    h2 = abs(br[1] - tr[1])
    if h2>h1: h = h2
    else: h = h1
    if w2>w1: w = w2
    else: w = w1
    return (w,h)
 
def get_key_img(num,scale):
    return  pygame.transform.scale(pygame.image.load(f"assets/menu/{num}.png"),(scale,scale))

def press_key_img(num,scale):
    return  pygame.transform.scale(pygame.image.load(f"assets/menu/{num}_down.png"),(scale,scale))

def rend_score(surf,score):
    text_font = pygame.font.SysFont("Arial",50)
    txt = text_font.render(f"Score: {score}",True, (255,0,0))
    txt = pygame.transform.scale(txt,surf.get_size())
    surf.blit(txt,(0,0))
    return surf

def rend_pieces(surf,piece,typ):
    new_surf = pygame.Surface((400,100))
    text_font = pygame.font.SysFont("Arial",50)
    txt = text_font.render(f"{typ}:",True, (255,0,0))
    txt = pygame.transform.scale(txt,(200,100))
    new_surf.blit(txt,(0,0))
    if piece == None:
        piece_matrix = [[0,0,0,0]]
    else:
        piece_matrix = piece.matrix
    h = len(piece_matrix)
    w = len(piece_matrix[0])
    temp_surf = pygame.Surface((w*9,h*9))
    for y in range(len(piece_matrix)-1,-1,-1):
        for x in range(0,len(piece_matrix[y])):
            if piece_matrix[y][x] != 0:
                shape_num = piece_matrix[y][x]
                image = pygame.transform.scale_by(pygame.image.load(f"assets/{shape_num}.png"),0.6)
                coords = get_coords(x,y,image.get_width(),image.get_height())
                temp_surf.blit(image,(coords[0],coords[1]))
    temp_surf = temp_surf.convert_alpha()
    temp_surf.set_colorkey((0,0,0))
    temp_surf = pygame.transform.scale(temp_surf,(200,100))
    new_surf.blit(temp_surf,(200,0))
    new_surf = pygame.transform.scale(new_surf, surf.get_size())
    surf.blit(new_surf,(0,0))
    return surf

def start_game():
    pygame.init()
    
    screen = pygame.Surface((160, 320))
    big_screen = pygame.Surface((480,960))
    main_screen = pygame.display.set_mode((480,960),pygame.RESIZABLE)
    db_time = 250  # ms
    past_click = 250
    game_running = True
    game_tick = 1
    
    board = gc.Board()
    piece_type = random.choice(list(gc.tetrominoes.keys()))
    piece = getattr(gc, "Piece")(piece_type)
    next_piece_type = random.choice(list(gc.tetrominoes.keys()))
    next_piece = getattr(gc, "Piece")(next_piece_type)
    held_piece = None

    score_surf = pygame.Surface((480,960))
    next_surf = pygame.Surface((480,960))

    select_surf = pygame.Surface((main_screen.get_width()/8,main_screen.get_height()/5))

    select_surf.set_colorkey((0,0,0))
    select_scale = select_surf.get_height()/5.5
    key1 = press_key_img(1,select_scale)
    key2 = get_key_img(2,select_scale)
    key3 = get_key_img(3,select_scale)
    key4 = get_key_img(4,select_scale)

    setup_type = 1

    last_drop = time.time()
    drop_speed = 0.25 #smaller = harder 
    landed_pieces = []
    score = 0

    p_list = [] # for game screen
    score_list = []
    next_list = []
    held_list = []

    back_image = pygame.image.load("assets/startup.jpg")
    back_image = pygame.transform.scale(back_image, main_screen.get_size())
    path = None
    big_screen.fill((0,0,0))
    big_screen.set_colorkey((0,0,0))
    main_screen.blit(back_image,(0,0))    
    while game_running:
        main_screen.blit(back_image,(0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.DROPFILE:
                path = event.file
                try:
                    back_image = pygame.image.load(path).convert_alpha()
                    back_image = pygame.transform.rotate(back_image, -90)
                    back_image = pygame.transform.scale(back_image, main_screen.get_size())
                except: 
                    back_image = pygame.transform.scale(back_image, main_screen.get_size())
            if event.type == pygame.VIDEORESIZE:
                
                try:
                    back_image = pygame.image.load(path).convert_alpha()
                    back_image = pygame.transform.rotate(back_image, -90)
                    back_image = pygame.transform.scale(back_image, main_screen.get_size())
                except: 
                    back_image = pygame.transform.scale(back_image, main_screen.get_size())  

                main_screen.blit(back_image,(0,0))
            if event.type == pygame.KEYDOWN: 
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and game_tick == 1: piece = gc.rotate_move(board,piece)
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and game_tick == 1: piece = gc.left(board,piece)
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and game_tick == 1: piece = gc.right(board,piece)
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and game_tick == 1:   
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

                elif event.key == pygame.K_r:
                    big_screen.fill((0,0,0))
                    big_screen.set_colorkey((0,0,0))
                    main_screen.blit(back_image,(0,0))
                    if setup_type == 1: p_list = []
                    elif setup_type == 2: score_list = []
                    elif setup_type == 3: next_list = []
                    elif setup_type == 4: held_list = []
                elif event.key == pygame.K_ESCAPE:
                    game_tick = 1- game_tick
                elif event.key == pygame.K_1 and len(next_list) %4 == 0 and len(score_list) %4 == 0 and len(held_list) %4 == 0:
                    setup_type = 1
                    key1 = press_key_img(1,select_scale)
                    key2 = get_key_img(2,select_scale)
                    key3 = get_key_img(3,select_scale)
                    key4 = get_key_img(4,select_scale)
                elif event.key == pygame.K_2 and len(next_list) %4 == 0 and len(p_list) %4 == 0 and len(held_list) %4 == 0:
                    setup_type = 2
                    key2 = press_key_img(2,select_scale)
                    key1 = get_key_img(1,select_scale)
                    key3 = get_key_img(3,select_scale)
                    key4 = get_key_img(4,select_scale)
                elif event.key == pygame.K_3 and len(p_list) %4 == 0 and len(score_list) %4 == 0 and len(held_list) %4 == 0:
                    setup_type = 3
                    key3 = press_key_img(3,select_scale)
                    key2 = get_key_img(2,select_scale)
                    key1 = get_key_img(1,select_scale)
                    key4 = get_key_img(4,select_scale)
                elif event.key == pygame.K_4 and len(p_list) %4 == 0 and len(score_list) %4 == 0 and len(next_list) %4 == 0:
                    setup_type = 4
                    key4 = press_key_img(4,select_scale)
                    key3 = get_key_img(3,select_scale)
                    key2 = get_key_img(2,select_scale)
                    key1 = get_key_img(1,select_scale)
                                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                if len(p_list) < 4 and setup_type == 1:
                    coord = get_mini_coords(pygame.Vector2(mouse_coord),main_screen,big_screen)
                    p_list.append(coord)
                if len(score_list) < 4 and setup_type == 2:
                    coord = get_mini_coords(pygame.Vector2(mouse_coord),main_screen,big_screen)
                    score_list.append(coord)
                if len(next_list) < 4 and setup_type == 3:
                    coord = get_mini_coords(pygame.Vector2(mouse_coord),main_screen,big_screen)
                    next_list.append(coord)
                if len(held_list) < 4 and setup_type == 4:
                    coord = get_mini_coords(pygame.Vector2(mouse_coord),main_screen,big_screen)
                    held_list.append(coord)                
        big_screen = draw_selection(p_list,big_screen)    
        big_screen = draw_selection(score_list,big_screen)
        big_screen = draw_selection(next_list,big_screen)
        big_screen = draw_selection(held_list,big_screen)

        select_surf.blit(key1,(0,0))
        select_surf.blit(key2,(0,1.5*select_scale))
        select_surf.blit(key3,(0,3*select_scale))
        select_surf.blit(key4,(0,4.5*select_scale))

        if len(p_list) == 4:

            if game_tick == 1:
                last_drop,game_running,piece,board,landed_pieces,score,next_piece = gc.game_tick(last_drop,drop_speed,game_running,piece,board,landed_pieces,score,next_piece)
            score = int(score)
            screen = pygame.Surface(optimise_screen(p_list))

            rend_back(screen)
            render_board(screen,board,piece)
            
            rot_surf =  warp_surface(pygame.transform.scale_by(screen,3),p_list,big_screen.get_size())
            
            big_screen.blit(rot_surf,(0,0))            

        if len(score_list) == 4:
            score_surf = pygame.Surface(optimise_screen(score_list))

            score_surf = rend_score(score_surf,score)
            
            rot_surf =  warp_surface(pygame.transform.scale_by(score_surf,3),score_list,big_screen.get_size())
            big_screen.blit(rot_surf,(0,0))


        if len(next_list) == 4:
            next_surf = pygame.Surface(optimise_screen(next_list))

            next_surf = rend_pieces(next_surf,next_piece,"Next")

            rot_surf =  warp_surface(pygame.transform.scale_by(next_surf,3),next_list,big_screen.get_size())
            big_screen.blit(rot_surf,(0,0))

        if len(held_list) == 4:
            held_surf = pygame.Surface(optimise_screen(held_list))

            held_surf = rend_pieces(held_surf,held_piece,"Held")

            rot_surf =  warp_surface(pygame.transform.scale_by(held_surf,3),held_list,big_screen.get_size())
            big_screen.blit(rot_surf,(0,0))
            

        resized_screen = resize_screen(main_screen, big_screen)
        main_screen.blit(resized_screen,(0,0))
        main_screen.blit(select_surf,(main_screen.get_width()-select_surf.get_width(),0))
        pygame.display.flip()


    pygame.quit()

start_game()
