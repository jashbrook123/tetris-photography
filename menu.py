import pygame
import regular as st
import sys
import text_surface as txt

    
def main_menu():
    pygame.init()
    with open("assets/score.txt","r") as score_file:
        score_data = score_file.read().split()
    high_score, last_score = int(score_data[0]),int(score_data[1])  
    menu_running = True
    menu_screen = pygame.display.set_mode((800,800))
    menu_background = pygame.image.load("assets/main_menu.png")
    play_rect = pygame.Rect(187,284,435,129)
    quit_rect = pygame.Rect(173,619,496,112)
    
    while menu_running:
        menu_screen.blit(menu_background, (0,0))
        menu_screen.blit(txt.text_to_surf(str(high_score),2),(488,479))
        menu_screen.blit(txt.text_to_surf(f"last game: {last_score}",1.5),(50,175))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False                 
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coord = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_coord) == True:
                    menu_running = False
                    pygame.quit()
                    final_score = st.start_game()
                    with open("assets/score.txt","w") as score_file:
                        if final_score > high_score:
                            score_file.write(f"{final_score}\n{final_score}")
                        else:
                            score_file.write(f"{high_score}\n{final_score}")
                    main_menu()
                if quit_rect.collidepoint(mouse_coord):
                    pygame.quit()
                    sys.exit()
                    
                
        if menu_running: pygame.display.flip()
    pygame.quit()
    sys.exit()

main_menu()
