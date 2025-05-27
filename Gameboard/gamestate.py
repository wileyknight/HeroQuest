import pygwidgets
from player import Player
from grid import GridMap
from map import GameMap
from boardMatrix import BoardMatrix
from herosight import HeroSight

class GameState():
    def __init__(self, screen):
        self.screen = screen
        self.players = []
        self.activePlayer = 0
        self.gridmap = GridMap()
        self.boardMatrix = BoardMatrix()
        self.gameMap = GameMap(self.screen, self.boardMatrix)
        self.herosight = HeroSight(screen)
        self.oldPos = self.gameMap.startPos
        self.splash = pygwidgets.Image(self.screen, (0,0), 'images/gameboardBg.png')
        self.introductionImg = pygwidgets.Image(self.screen, (0,0), 'images/introductionText.png')
        self.showSplash = True
        self.showIntro = False
        self.showGame = False

    def addSplash(self):
        self.splash.draw()

    def drawGame(self):
        if self.showSplash:
            self.addSplash()
        
        if self.showIntro:
            self.introductionImg.draw()

        if self.showGame:
            self.gameMap.boardImage.draw()
            self.gameMap.populate()
    
            self.updatePlayer()

    def addPlayer(self):
        self.players.append(Player(self.gameMap.startPos, self.gridmap.getGrid(self.gameMap.startPos, abs=True), self.boardMatrix))

    def removePlayer(self, player):
        self.players.pop(player)

    def movePlayer(self, index, direction):
        self.oldPos = self.players[index].grid
        newPos = self.players[index].move(direction)
        self.herosight.heroTrail.append(self.oldPos)
        if self.boardMatrix.board[newPos['pos']]['trap'] != 0:
            self.players[index].health -= 1
            trap = self.boardMatrix.board[newPos['pos']]['trap']
            if trap == 'S':
                print('Speared')
                self.boardMatrix.board[newPos['pos']]['trap'] = 0
            if trap == 'R':
                print('You got rocked')
                self.boardMatrix.board[newPos['pos']]['blocked'] = 3
            if trap == 'P':
                print('You"ve fallen into a pit')
                self.boardMatrix.board[newPos['pos']]['trap']

    def updatePlayer(self):
        if len(self.players) > 0:
            self.herosight.DrawTrail(self.players[self.activePlayer])
            self.herosight.DrawSight(self.players, True)

    def openDoor(self, selected):
        self.gameMap.openDoor(selected)
        