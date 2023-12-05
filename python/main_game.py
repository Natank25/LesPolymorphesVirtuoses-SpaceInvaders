import pygame
import sys
import classes

pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders")
bg = pygame.image.load('../img/background.png')

running = True


listeEnnemis = []
for indice in range(classes.Ennemi.NbEnnemis):
    vaisseau = classes.Ennemi()
    listeEnnemis.append(vaisseau)
0

while running:
    screen.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    pygame.display.update()



pygame.quit()