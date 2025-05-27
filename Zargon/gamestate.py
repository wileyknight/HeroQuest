import pygwidgets, json
from player import Player
from grid import GridMap
from map import GameMap
from boardMatrix import BoardMatrix
from herosight import HeroSight
from hud import HUD
from dmserver import Connection, RunServer

class GameState():
    def __init__(self, screen, pygame):
        self.pygame = pygame
        self.screen = screen
        self.players = [None,]
        self.activePlayer = 1
        self.connection = Connection()
        self.server = RunServer(self.connection)
        
        self.board = False
        self.sendMessage = None
        self.characters = self.loadSave()
        self.showSplash = False  # change to True
        self.showChoose = False
        self.showIntro = False
        self.chooseMap = "Forsaken Tunnels of Xel-Xor"  # change to ""
        self.mapReady = False
        self.showGame = True# change to False

        self.gridmap = GridMap()
        self.boardMatrix = BoardMatrix()
        self.gameMap = GameMap(self.screen, self.boardMatrix, self.chooseMap) # change to none
        self.oldPos = None
        self.gameItems = self.getGameItems()
        self.hud = HUD(self.pygame, self.screen, self.gameItems)
        self.herosight = HeroSight(screen)
        
        self.splash = pygwidgets.Image(self.screen, (0,0), 'images/splash.png')
        self.chooseMapImg = pygwidgets.Image(self.screen, (0,0), 'images/chooseMap.png')
        self.btnForsaken = pygwidgets.CustomButton(self.screen, (558,464), 'images/btn_forsaakenTunnels_1.png')
        self.btnEnterGame = pygwidgets.CustomButton(self.screen, (844,980), 'images/btn_startGame.png')
        self.icoPlayers = [
            None,
            pygwidgets.Image(self.screen, (395,484), 'images/ico_elfFemale.png'),
            pygwidgets.Image(self.screen, (395,594), 'images/ico_barbarianMale.png'),
            pygwidgets.Image(self.screen, (395,704), 'images/ico_wizard.png'),
            pygwidgets.Image(self.screen, (395,814), 'images/ico_bard.png')
        ]
        self.showIco = [None, False,False,False,False]
        self.startcover = pygwidgets.Image(self.screen, (678,741), 'images/splashMessage.png')
        self.introductionImg = pygwidgets.Image(self.screen, (0,0), 'images/introductionText.png')
        self.btnEnter = pygwidgets.Image(self.screen, (747,939), 'images/btn_enter.png')
        self.btnStartGame = pygwidgets.CustomButton(self.screen, (794,908), 'images/btn_startGame.png')
        self.start = pygwidgets.CustomButton(self.screen, (794,908), 'images/start.png')
        self.pText = pygwidgets.DisplayText(self.screen, (743,838), 'PLAYERS: ', fontName='prozalibreextrabold', fontSize=36, width=None, height=None, textColor=(105, 29, 46), backgroundColor=None, justified='left')
        self.nText = pygwidgets.DisplayText(self.screen, (933,835), '0', fontName='prozalibreextrabold', fontSize=42, width=None, height=None, textColor=(105, 29, 46), backgroundColor=None, justified='left')
        self.bText = pygwidgets.DisplayText(self.screen, (982,838), 'BOARD: ', fontName='prozalibreextrabold', fontSize=36, width=None, height=None, textColor=(105, 29, 46), backgroundColor=None, justified='left')
        self.check = pygwidgets.Image(self.screen, (1153,841), 'images/checkmark.png')

    def addSplash(self):
        self.splash.draw()
        self.start.draw() #(794,793)
        self.startcover.draw()
        self.nText.setValue(len(self.players-1))
        self.pText.draw()
        self.nText.draw()
        self.bText.draw()
        if self.board:
            self.check.draw()

    def drawGame(self):
        if self.showSplash:
            self.addSplash()

        if self.showChoose:
            self.chooseMapImg.draw()
            self.btnForsaken.draw()
            if self.mapReady:
                self.btnStartGame.draw()
            if self.players > 1:
                for idx, player in enumerate(self.players):
                    if player != None:
                        if self.showIco[idx]:
                            pass
                self.icoPlayers[idx].draw()

        if self.showIntro:
            self.introductionImg.draw()
            self.btnEnter.draw()

        if self.showGame:
            self.gameMap.boardImage.draw()
            self.gameMap.populate(showMonsters=True)
            self.updatePlayer()
            self.hud.drawHUD(self.gameItems, self.players, self.activePlayer)

    def eventListener(self, event, events):
        if self.showSplash:
            if self.start.handleEvent(event):
                self.showSplash = False
                self.showChoose = True
                players = []

                for p in self.players:
                    if self.players != None:
                        items = p.__dict__
                        players.append({'client': items['pi_name']})
                self.sendMessage('board', {'messageType': 'PLAYERS', 'players': players})
        
        if self.showChoose:
            if self.btnForsaken.handleEvent(event):
                self.chooseMap = "Forsaken Tunnels of Xel-Xor"
                self.gameMap = GameMap(self.screen, self.boardMatrix, self.chooseMap)
                self.oldPos = self.gameMap.startPos
                self.mapReady = True
                self.sendMessage('board', {'messageType': 'MAP', 'map': self.chooseMap})
            if self.btnStartGame.handleEvent(event):

                for player in self.players:
                    if self.players != None:
                        player.setStart(self.gameMap.startPos, self.characters[self.chooseMap][player.pi_name])
                        self.sendMessage(player.pi_name, self.characters[self.chooseMap][player.pi_name])
                self.showChoose = False
                self.showIntro = True
                self.sendMessage('board', {'messageType': 'INTRO'})

        if self.showIntro:
            if self.btnEnter.handleEvent(event):
                self.showIntro = False
                self.showGame = True
                self.sendMessage('board', {'messageType': 'START'})
                self.sendMessage('player1', {'messageType': 'START'})
        
        if self.showGame:
            self.gameMap.eventListener(event, self.sendMessage, self.hud)
            self.hud.eventListener(event, events)

    def addPlayer(self, client, send_message):
        if self.sendMessage == None:
            self.sendMessage = send_message
        self.players.append(Player(client, send_message, self.boardMatrix))
        self.players = sorted(self.players, key=lambda x: x.pi_name)

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
        if len(self.players) > 1 and self.showSplash == False:
            if self.players != None and self.activePlayer > 0:
                self.herosight.DrawTrail(self.players[self.activePlayer])
                self.herosight.DrawSight(self.players)

    def getGameItems(self):
        with open('items.json') as load_file:
            return json.load(load_file)
        
    def loadSave(self):
        with open('saves.json') as load_file:
            return json.load(load_file)
    
    def saveGame(self):
        data = {}
        with open('saves.json','w') as store_file:
            json.dump(data,store_file)

    def pretend(self, arg1, arg2, arg3):
        pass
        