import pygame
import time

pygame.init()

window = pygame.display.set_mode((180, 180))

pygame.display.set_caption("Window")

gameLoop = True

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()

x, y = 90, 90

p = 0
pMax = 20

save_stateR = y
save_stateF = y
save_state2 = y

xMAX = 180
xMIN = 0
yMAX = 180
yMIN = 0

activeX, activeY = 0, 0

while gameLoop:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            gameLoop = False

        if (event.type == pygame.KEYDOWN):

            if (event.key == pygame.K_RIGHT):
                activeX = 1

            if (event.key == pygame.K_LEFT):
                activeX = -1

            if (event.key == pygame.K_UP):
                activeY = 1





        if (event.type == pygame.KEYUP):

            if (event.key == pygame.K_RIGHT):
                activeX = 0

            if (event.key == pygame.K_LEFT):
                activeX = 0

            if (event.key == pygame.K_UP):
                activeY = 0

    window.fill(black)


    x += activeX
    if activeY == 1:
        y -=1
    if save_stateR > y:
        y -=1
        save_stateR -=1
    if  save_state2-11 == y:
        save_stateR = y
        y += 1
    if save_stateF < y:
        y +=1
        save_stateF +=1
    if save_state2+10 == y:
        save_stateF = y





    x = xMIN if x < xMIN else xMAX if x > xMAX else x

    y = yMIN if y < yMIN else yMAX if y > yMAX else y



    pygame.draw.rect(window, white, (x, y, 5, 5))
    clock.tick(120)

    pygame.display.flip()

pygame.quit()