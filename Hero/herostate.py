
import pygwidgets
from choosecharacter import ChooseCharacter
from character import Character
from heroconnection import Connection

class HeroState():
    def __init__(self, screen, gamevars):
            self.screen = screen
            self.gamevars = gamevars
            self.showWaiting = False
            self.showChoose = True
            self.showCharacter = False
            self.showEnter = False
            self.chrSelectScreen = ChooseCharacter(self.screen)
            self.character = Character(self.screen)
            self.connectScreen = pygwidgets.Image(self.screen, (0,0), "images/bg_connect.png")
            self.waitScreen = pygwidgets.Image(self.screen, (0,0), "images/wait.png")
            self.enterScreen = pygwidgets.Image(self.screen, (0,0), "images/enterXelXor.png")
            self.btnEnter = pygwidgets.CustomButton(self.screen, (532,0), "images/btn_enter.png")
            self.clientname = "player1"
            self.characterBg = 0
            self.myTurn = False
            self.connection = Connection()

    def eventListener(self, event):
        if self.showChoose:
            self.chrSelectScreen.eventListener(event, self.clientname, self.connection.send_message, self.chooseCharacter)
        if self.showEnter:
             if self.btnEnter.handleEvent(event):
                  self.showEnter = False
                  self.showCharacter = True
        if self.showCharacter:
             self.character.eventListener(event, self.clientname, self.connection.send_message)

    def drawGame(self):
        if not self.connection.connected:
            self.connectScreen.draw() 
        if self.showChoose and self.connection.connected:
            self.chrSelectScreen.addToScreen()
        if self.showWaiting:
            self.waitScreen.draw()
        if self.showEnter:
             self.enterScreen.draw()
             self.btnEnter.draw()
        if self.showCharacter:
             self.character.addToScreen()

    def chooseCharacter(self, num):
         self.character.showBg = num
         self.showWaiting = True
         self.showChoose = False