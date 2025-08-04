import pygame
from pygame.locals import *
from Constants import *
from listPath import *
from Ship import *
from Torpedo import *

class Player():
    def __init__(self, name, lstPathShip):
        self.__name = name
        self.__listShips = [Ship(path[1], path[0], path[2]) for path in lstPathShip]
        self.__isMouseDown = False
        self.__firstPos = None # pos when player click mouse down
        self.__shipSelected = None # the ship player select to move
        self.isReady = False
        self.__listMyTorpedo = []
        self.__listEnermyTorpedo = []
        self.canFire = None
        self.numberCorrect = 0
        self.numberCorrectE = 0
        self.startTime = None # it is a time when player fire, it use for delay 3s after fire to know player fire correct or incorrect
        self.finishGame = None # it is a time when one of players win, delay 5s and return to mainscreen

    # check enermy fire correct or incorrect my ship
    def isCorrect(self, pos):
        for ship in self.__listShips:
            if ship.getHitBox().collidepoint(pos):
                return True
        return False

    # check fire is possible or not 
    def fire(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            firePos = pygame.mouse.get_pos()
            if FIELD_COORD[0] < firePos[0] and firePos[0] < FIELD_COORD[0] + FIELD_WIDTH and FIELD_COORD[1] < firePos[1] and firePos[1] < FIELD_COORD[1] + FIELD_HEIGHT:
                for oTorpedo in self.__listMyTorpedo:
                    if oTorpedo.getHitBox().collidepoint(firePos):
                        return False
                return firePos
        return False
            
    def fireTorpedo(self, window, loc, isCorrect, mineOrEnermy):
        oTorpedo = Torpedo(window, loc, listPathTopedoA, pathImages, isCorrect, 100)
        self.appendTorpedo(mineOrEnermy, oTorpedo)
    
    def appendTorpedo(self, enermyOrMine, oTorpedo): # True: mine, False: enermy
        if enermyOrMine:
            self.__listMyTorpedo.append(oTorpedo)
        else:
            self.__listEnermyTorpedo.append(oTorpedo)

    def draw(self, window):
        for ship in self.__listShips:
            ship.draw(window)


    def drawTorpedo(self, enermyOrMine):
        if enermyOrMine:
            for oTorpedo in self.__listMyTorpedo:
                if not oTorpedo.drawAnimation():
                    oTorpedo.draw()
        else:
            for oTorpedo in self.__listEnermyTorpedo:
                if not oTorpedo.drawAnimation():
                    oTorpedo.draw()

    def moveShip(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.__firstPos = pygame.mouse.get_pos()
            for ship in self.__listShips:
                if ship.getHitBox().collidepoint(self.__firstPos):
                    ship.rotate(True)
                    if ship.isCollideAnotherShip(self.__listShips) or ship.isOutOfField():
                        ship.rotate(False)
                    else:
                        ship.updateNewLoc()
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.__firstPos = pygame.mouse.get_pos()
            for ship in self.__listShips:
                if ship.getHitBox().collidepoint(self.__firstPos):
                    self.__shipSelected = ship
                    self.__isMouseDown = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.__isMouseDown == True:
            if self.__shipSelected.isCollideAnotherShip(self.__listShips) or self.__shipSelected.isOutOfField():
                self.__shipSelected.loc = self.__shipSelected.oldLoc
                self.__shipSelected.updateHitBox()
            else:
                self.__shipSelected.updateNewLoc()
            self.__isMouseDown = False
        
        if self.__isMouseDown:  
            if event.type == MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
                self.__shipSelected.updatePos(self.__firstPos, mousePos)

            