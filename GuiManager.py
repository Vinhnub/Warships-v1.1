import pygame
from Constants import *
import pygwidgets
from Player import *
from listPath import *
from Signal import *
from MyWidgets import AnimatedButton, AnimatedImage, CustomText


class Gui():
    
    def __init__(self, window, network):
        self.window = window
        self.player = None
        self.goFirst = True # who create room will go first
        self.startTimeTurn = None # timer to change turn
        self.dataToSend = Signal("findmatch", None, None)
        self.network = network
        self.soundFire = None
        self.createRoomBtn = AnimatedButton(self.window, (420, 350), [resource_path("assets/images/buttons/btncreateroom_u.png")], [resource_path("assets/images/buttons/btncreateroom_d.png")])
        self.joinRoomBtn = AnimatedButton(self.window, (455, 450), [resource_path("assets/images/buttons/btnjoinroom_u.png")], [resource_path("assets/images/buttons/btnjoinroom_d.png")])
        self.exitBtn = AnimatedButton(self.window, (467, 550), [resource_path("assets/images/buttons/btnexitgame_u.png")], [resource_path("assets/images/buttons/btnexitgame_d.png")])
        self.readyBtn = AnimatedButton(self.window, (450, 700), [resource_path("assets/images/buttons/btnready_u.png")], [resource_path("assets/images/buttons/btnready_d.png")])
        self.screen = "mainscreen" # mainscreen, createroom, joinroom, prepare,  myturn, enermyturn
        self.idRoomInput = pygwidgets.InputText(self.window, (500, 360), fontSize=80, width=200)
        self.__idText =  CustomText(window, (445, 365), "", resource_path("fonts/PressStart2P-Regular.ttf"), 80)
        self.__timerText = CustomText(window, (10, 10), "", resource_path("fonts/PressStart2P-Regular.ttf"), 80)
        self.winOrLose = [AnimatedImage(window, (0, 0), [resource_path("assets/images/win.png")]),
                          AnimatedImage(window, (0, 0), [resource_path("assets/images/lose.png")])]
        self.__dictWidgets = {
            "mainscreen": [AnimatedImage(window, (0, 0), [resource_path("assets/images/background_4.png")]),
                           AnimatedImage(window, (200, 150), listWarShips, 500),
                           AnimatedImage(window, (0, WINDOW_HEIGHT - 15), [resource_path("assets/images/author.png")])
                           ],
            "createroom": [AnimatedImage(window, (0, 0), [resource_path("assets/images/background_1.png")]),
                           AnimatedImage(window, (400, 350), [resource_path("assets/images/table.png")]),
                           ],
            "joinroom": [AnimatedImage(window, (0, 0), [resource_path("assets/images/background_2.png")])],
            "prepare": [AnimatedImage(window, (0, 0), [resource_path("assets/images/background_5.png")]),
                        AnimatedImage(window, FIELD_COORD, [resource_path("assets/images/field.png")]),
                        AnimatedImage(window, (450, 700), [resource_path("assets/images/ready.png")])
                        ],
            "myturn": [AnimatedImage(window, (0, 0), [resource_path("assets/images/background_3.png")]),
                       AnimatedImage(window, FIELD_COORD, [resource_path("assets/images/field.png")]),],
            "enermyturn": [AnimatedImage(window, (0, 0), [resource_path("assets/images/background_3.png")]),
                           AnimatedImage(window, FIELD_COORD, [resource_path("assets/images/field.png")])]
        }

    def changeToMyTurn(self):
        self.screen = "myturn"
        self.player.startTime = None
        self.startTimeTurn = pygame.time.get_ticks()
        self.player.canFire = True
        self.dataToSend.set("changeturn", None)

    def changeToEnermyTurn(self):
        self.screen = "enermyturn"
        self.startTimeTurn = pygame.time.get_ticks()
        self.player.canFire = True
        self.dataToSend.set("waiting", None)

    def isFinishGame(self):
        if self.player != None:
            if self.player.numberCorrect == 17: # sum of ship cell = 17
                self.winOrLose[0].draw()
                if self.player.finishGame == None:
                    self.player.finishGame = pygame.time.get_ticks()
            elif self.player.numberCorrectE == 17:
                self.winOrLose[1].draw()
                if self.player.finishGame == None:
                    self.player.finishGame = pygame.time.get_ticks()
            if self.player != None:
                if self.player.finishGame != None:
                    return (pygame.time.get_ticks() - self.player.finishGame >= 5000)
        return False
        

    def reset(self, isFinish):
        if isFinish:
            self.dataToSend = Signal("findmatch", None, None)
            self.player = None
            self.startTimeTurn = None
            self.screen = "mainscreen"

    def createPlayer(self):
        self.player = Player("You", lstPathShip)
        return self.player    

    def draw(self, screen):
        if screen == "mainscreen":
            for oWidget in self.__dictWidgets[screen]:
                oWidget.draw()
            self.createRoomBtn.draw()
            self.joinRoomBtn.draw()
            self.exitBtn.draw()  
        elif screen == "createroom":
            for oWidget in self.__dictWidgets[screen]:
                oWidget.draw()
            self.__idText.setText(str(self.dataToSend.getId()))
            self.__idText.draw()
        elif screen == "prepare":
            for oWidget in self.__dictWidgets[screen]:
                oWidget.draw()
            if (not self.player.isReady): self.readyBtn.draw()
            self.player.draw(self.window)
        elif screen == "joinroom":
            for oWidget in self.__dictWidgets[screen]:
                oWidget.draw()
            self.idRoomInput.draw()
        elif screen == "myturn":
            for oWidget in self.__dictWidgets[screen]:
                oWidget.draw()
            self.player.drawTorpedo(True)   
            self.__timerText.setText(str(int((TIME_EACH_TURN - pygame.time.get_ticks() + self.startTimeTurn)/1000)))
            self.__timerText.draw()
        elif screen == "enermyturn":
            for oWidget in self.__dictWidgets[screen]:
                oWidget.draw()
            self.player.draw(self.window)
            self.player.drawTorpedo(False)
            self.__timerText.setText(str(int((TIME_EACH_TURN - pygame.time.get_ticks() + self.startTimeTurn)/1000)))
            self.__timerText.draw() 
            