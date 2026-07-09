import pygame


def get_image(char):
    image = pygame.image.load(f"assets/text/{char}.png").convert_alpha()
    image.set_colorkey((255,255,255))
    return image

def text_to_surf(text,SF): #scale factor
    characters = ['0','1','2','3','4','5','6','7','8','9',
                  'a','b','c','d','e','f','g','h','i','j',
                  'k','l','m','n','o','p','q','r','s','t',
                  'u','v','w','x','y','z']

    surf = pygame.Surface((800,200),pygame.SRCALPHA)
    y = 0 
    x = 0
    for char in text:
        if char in characters:
            image = get_image(char)
            surf.blit(image,(x,y))
            x+=40
        elif char == " ":
            x+=40
    surf = pygame.transform.scale(surf,(600,100))
    surf = pygame.transform.scale_by(surf,SF)
    return surf
