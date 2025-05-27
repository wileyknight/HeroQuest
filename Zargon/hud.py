import pygwidgets
from hudMenu import HudMenu

class HUD():
    def __init__(self, pygame, screen, gameItems):
        self.pygame = pygame
        self.screen = screen
        self.gameItems = gameItems
        self.panelLeft = pygwidgets.Image(self.screen, (7,15), 'images/panel_Left.png')
        self.icoAttack = pygwidgets.CustomButton(self.screen, (32,233), 'images/ico_attack.png')
        self.icoDefend = pygwidgets.CustomButton(self.screen, (83,233), 'images/ico_defense.png')
        self.icoHealth = pygwidgets.CustomButton(self.screen, (133,233), 'images/ico_health.png')
        self.icoMind = pygwidgets.CustomButton(self.screen, (184,233), 'images/ico_mind.png')
        self.icoAttackUp = pygwidgets.CustomButton(self.screen, (37,265), 'images/ico_up.png')
        self.icoDefendUp = pygwidgets.CustomButton(self.screen, (86,265), 'images/ico_up.png')
        self.icoHealthUp = pygwidgets.CustomButton(self.screen, (136,265), 'images/ico_up.png')
        self.icoMindUp = pygwidgets.CustomButton(self.screen, (184,265), 'images/ico_up.png')
        self.icoAttackDown = pygwidgets.CustomButton(self.screen, (37,317), 'images/ico_down.png')
        self.icoDefendDown = pygwidgets.CustomButton(self.screen, (86,317), 'images/ico_down.png')
        self.icoHealthDown = pygwidgets.CustomButton(self.screen, (136,317), 'images/ico_down.png')
        self.icoMindDown = pygwidgets.CustomButton(self.screen, (184,317), 'images/ico_down.png')
        self.txtAttack = pygwidgets.DisplayText(self.screen, (31,279), '0', 'prozalibresemibold', 26, 32, 28, (76,42,0), None, 'center')
        self.txtDefend = pygwidgets.DisplayText(self.screen, (80,279), '0', 'prozalibresemibold', 26, 32, 28, (76,42,0), None, 'center')
        self.txtHealth = pygwidgets.DisplayText(self.screen, (129,279), '0', 'prozalibresemibold', 26, 32, 28, (76,42,0), None, 'center')
        self.txtMind = pygwidgets.DisplayText(self.screen, (178,279), '0', 'prozalibresemibold', 26, 32, 28, (76,42,0), None, 'center')
        self.btnPassWalls = pygwidgets.CustomButton(self.screen, (22,934), 'images/btn_passWalls.png')
        self.btnSkipTurn = pygwidgets.CustomButton(self.screen, (22,992), 'images/btn_skipTurn.png')
        self.btnHeroItems = pygwidgets.CustomButton(self.screen, (22,352), 'images/btn_items.png')

        self.panelRight = pygwidgets.Image(self.screen, (1693,15), 'images/panel_Right.png')
        self.icoZargon = pygwidgets.CustomButton(self.screen, (1724,44), 'images/ico_zargon.png', disabled='images/ico_zargon-Off.png')
        self.btnEndTurn = pygwidgets.CustomButton(self.screen, (1708,249), 'images/btn_endTurn.png')
        self.btnInventoryItems = pygwidgets.CustomButton(self.screen, (1708,352), 'images/btn_items.png')
        self.btnSave = pygwidgets.CustomButton(self.screen, (1708,992), 'images/btn_save.png')

        self.showMenu = False
        self.floatMenu = pygwidgets.Image(self.screen, (823,200), 'images/menuBg.png')
        self.close = pygwidgets.CustomButton(self.screen, (230+823,18+200), 'images/btn_close.png')
        
        self.showTrapMenu = False
        self.moveMonster = pygwidgets.CustomButton(self.screen, (41+823,163+200), 'images/btn_moveMonster.png')
        self.killMonster = pygwidgets.CustomButton(self.screen, (41+823,230+200), 'images/btn_killMonster.png')

        self.showMonsterMenu = False
        self.revealTrap = pygwidgets.CustomButton(self.screen, (41+823,163+200), 'images/btn_revealTrap.png')
        self.removeTrap = pygwidgets.CustomButton(self.screen, (41+823,230+200), 'images/btn_removeTrap.png')
        
        self.players = []
        self.active = 0
        self.icoPlayers = [
            pygwidgets.CustomButton(self.screen, (38,44), 'images/ico_elfFemale.png'),
            pygwidgets.CustomButton(self.screen, (130,44), 'images/ico_barbarianMale.png'),
            pygwidgets.CustomButton(self.screen, (38,132), 'images/ico_wizard.png'),
            pygwidgets.CustomButton(self.screen, (130,132), 'images/ico_bard.png')
        ]
        self.showIco = [False,False,False,False]

        self.heroIconPos = [(38,44), (130,44), (38,132), (130,132)]
        self.heroIcons = []
        self.hudMenu = HudMenu(self.pygame, self.screen, self.gameItems)

    def eventListener(self, event, events):
        if len(self.players) > 1:
            for idx, player in enumerate(self.players):
                if self.icoPlayers[idx].handleEvent(event):
                    print('hero info', idx)
        if self.icoAttackUp.handleEvent(event):
            print('attack up')
        if self.icoAttackDown.handleEvent(event):
            print('attack down')
        if self.icoDefendUp.handleEvent(event):
            print('defend up')
        if self.icoDefendDown.handleEvent(event):
            print('defend down')
        if self.icoHealthUp.handleEvent(event):
            print('health up')
        if self.icoHealthDown.handleEvent(event):
            print('health down')
        if self.icoMindUp.handleEvent(event):
            print('mind up')
        if self.icoMindDown.handleEvent(event):
            print('mind down')
        if self.btnPassWalls.handleEvent(event):
            print('pass thru walls')
        if self.btnSkipTurn.handleEvent(event):
            print('next player turn')
        if self.btnEndTurn.handleEvent(event):
            print('End my turn')
        if self.btnHeroItems.handleEvent(event):
            print('hero stuff')
        if self.btnInventoryItems.handleEvent(event):
            print('get items')
        if self.btnSave.handleEvent(event):
            print('saving')
        if self.showMenu:
            if self.close.handleEvent(event):
                print('close')
                self.showMenu = False
                self.showMonsterMenu = False
                self.showTrapMenu = False
        self.hudMenu.eventListener(event, events)

    def drawHUD(self, gameItems, players, activePlayer):
        self.gameItems = gameItems
        self.players = players
        self.activePlayer = activePlayer
        self.panelLeft.draw()
        self.panelRight.draw()
        self.icoAttack.draw()
        self.icoDefend.draw()
        self.icoHealth.draw()
        self.icoMind.draw()
        self.icoZargon.draw()
        self.icoAttackUp.draw()
        self.icoAttackDown.draw()
        self.icoDefendUp.draw()
        self.icoDefendDown.draw()
        self.icoHealthUp.draw()
        self.icoHealthDown.draw()
        self.icoMindUp.draw()
        self.icoMindDown.draw()
        self.btnPassWalls.draw()
        self.btnSkipTurn.draw()
        self.btnEndTurn.draw()
        self.btnHeroItems.draw()
        self.btnInventoryItems.draw()
        self.btnSave.draw()
        self.txtAttack.draw()
        self.txtDefend.draw()
        self.txtHealth.draw()
        self.txtMind.draw()
        if len(self.players) > 1:
            for idx, player in enumerate(self.players):
                self.icoPlayers[idx].draw()
        if self.showMenu:
            self.createMenu()
        self.hudMenu.runMenu()

    def createMenu(self):
        self.floatMenu.draw()
        if self.showTrapMenu:
            self.trapMenu()
        if self.showMonsterMenu:
            self.monsterMenu()
        self.close.draw()

    def trapMenu(self):
        self.removeTrap.draw()
        self.revealTrap.draw()

    def monsterMenu(self):
        self.moveMonster.draw()
        self.killMonster.draw()