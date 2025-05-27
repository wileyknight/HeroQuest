import pygame, pygwidgets
from gamevars import GameVars

class ButtonMap():
    def __init__(self, screen):
        self.screen = screen
        self.gamevars = GameVars()
        self.buttons = []
        self.createButtons()

    def createButtons(self):
        posX = 0
        posY = 0
        btnX = []
        for _y in range(self.gamevars.unitsY):
            for _x in range(self.gamevars.unitsX):
                btnX.append(pygwidgets.CustomButton(self.screen, (posX+self.gamevars.boardPos["x"], posY+self.gamevars.boardPos["y"]),"images/button.png"))
                if posX+self.gamevars.unit < self.gamevars.unit*self.gamevars.unitsX:
                    posX = posX+self.gamevars.unit
                else:
                    posX = 0
            self.buttons.append(btnX)
            posY = posY+self.gamevars.unit

    def eventListener(self, event, heroLoc):
        for _y in range(len(self.buttons)):
            for _x in self.buttons[_y]:
                if _x.handleEvent(event):
                    # Move Hero to area
                    btnLoc = list(_x.getLoc())
                    btnLoc[0] = btnLoc[0] - self.gamevars.boardPos["x"]
                    btnLoc[1] = btnLoc[1] - self.gamevars.boardPos["y"]
                    heroLoc(btnLoc)

    def addToScreen(self):
        for _y in range(len(self.buttons)):
            for _x in self.buttons[_y]:
                _x.draw()