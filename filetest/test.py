import pygame
from Constants import *
from pygame.locals import *
import sys
from Playertest import *
from listPath import *


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
oPlayer1 = Player("vinh", lstPathShip)
field = pygame.image.load(grand_dir + "/assets/images/field.png").convert_alpha()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()
        # oPlayer1.moveShip(event)
        res = oPlayer1.fire(event)
        if res != False:
            oPlayer1.fireTorpedo(window, res, True)


    keys = pygame.key.get_pressed()
    


    window.fill(WHITE)
    window.blit(field, FIELD_COORD)
    oPlayer1.draw(window)
    oPlayer1.drawTorpedo(True)
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND) 
    fps = int(clock.get_fps())
    pygame.display.set_caption(f"BatleShip (FPS: {fps})")
