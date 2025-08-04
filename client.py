import pygame
from Constants import *
from pygame.locals import *
import sys
from Player import *
from Network import *
from Signal import *
from GuiManager import *
import random

# Test

serverIp = input("Enter server ip to connect:")
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
main = Gui(window, NetWork(serverIp))
main.soundFire = pygame.mixer.Sound(resource_path("assets/sounds/sound_fire.wav"))

while True:
    # handle event from keyboard, button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if main.screen == "createroom" or main.screen == "joinroom":
                if event.key == pygame.K_ESCAPE:
                    main.screen = "mainscreen"
                    main.dataToSend.setId(None)
        
        if main.screen == "mainscreen":
            if main.createRoomBtn.handleEvent(event):
                main.screen = "createroom"
                main.goFirst = True
                main.dataToSend.setId(random.randint(1000, 9999))
                main.dataToSend.setData(True) # this command to tell server that just create room can start match not double joinroom
            if main.joinRoomBtn.handleEvent(event):
                main.screen = "joinroom"
                main.dataToSend.setData(None)
                main.goFirst = False
            if main.exitBtn.handleEvent(event):
                pygame.quit()
                sys.exit()

        if main.screen == "joinroom":
            if main.idRoomInput.handleEvent(event):
                main.dataToSend.setId(main.idRoomInput.getValue())

        if main.player != None and main.screen == "prepare":
            main.player.moveShip(event)
            if main.readyBtn.handleEvent(event):
                main.player.isReady = True

        # check in myturn if player fire
        if main.screen == "myturn":
            if main.player.canFire: firePos = main.player.fire(event)
            if firePos != False and main.player.canFire:
                main.soundFire.play()
                main.dataToSend.set("shooting", firePos)
                main.player.startTime = pygame.time.get_ticks()


    # find match with idroom 
    if main.dataToSend.getId() != None and (main.screen == "createroom" or main.screen == "joinroom"):
        result = main.network.send(main.dataToSend)
        if result.getId() != None and result.getType() == "findmatch":
            main.screen = "prepare"
            main.dataToSend.set("isready", None)
            main.createPlayer()

        elif result.getId() == None and main.screen == "joinroom":
            print("Id not exist!")
            main.dataToSend.setId(None)
    

    # check if 2 player is ready and start match
    elif main.screen == "prepare":
        main.dataToSend.setData(main.player.isReady)
        result = main.network.send(main.dataToSend)
        if (result.getData() != False) and main.player.isReady:
            if main.goFirst: main.changeToMyTurn()
            else: main.changeToEnermyTurn()
        
    # logic in mine turn 
    elif main.screen == "myturn":
        result = main.network.send(main.dataToSend)
        if result.getData() != None and main.player.canFire and result.getType() == "waiting":
            if result.getData() == True: main.player.numberCorrect += 1
            main.player.fireTorpedo(window, main.dataToSend.getData(), result.getData(), True)
            main.player.canFire = False

        elif (result.getType() == "changeturn" and pygame.time.get_ticks() - main.startTimeTurn > TIME_EACH_TURN) or (result.getType() == "changeturn" and (not main.player.canFire)):
            main.changeToEnermyTurn()

        if (not main.player.canFire) and pygame.time.get_ticks() - main.player.startTime > 3000: 
            main.dataToSend.set("changeturn", None)
        
    # logic in enermy turn
    elif main.screen == "enermyturn":
        result = main.network.send(main.dataToSend)
        if result.getData() != None and result.getType() == "shooting" and main.player.canFire:
            res = main.player.isCorrect(result.getData())
            if res: main.player.numberCorrectE += 1
            main.dataToSend.setData(res)
            main.player.fireTorpedo(window, result.getData(), False, False)
            main.player.canFire = False

        elif (result.getType() == "changeturn" and pygame.time.get_ticks() - main.startTimeTurn > TIME_EACH_TURN) or (result.getType() == "changeturn" and (not main.player.canFire)):
            main.changeToMyTurn()
    

    
    window.fill(BLACK)
    
    # check if one of players win
    main.draw(main.screen)
    main.reset(main.isFinishGame())


    pygame.display.update()
    
    
    clock.tick(FRAMES_PER_SECOND) 
    fps = int(clock.get_fps())
    pygame.display.set_caption(f"WAR SHIP (FPS: {fps})")
