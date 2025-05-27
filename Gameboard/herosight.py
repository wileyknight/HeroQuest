import pygame, pygwidgets
from boardvars import BoardVars
from tween import *

class HeroSight():
    def __init__(self, screen):
        self.screen = screen
        self.boardvars = BoardVars()
        self.maskPos = {"x":self.boardvars.boardPos['x'],"y":self.boardvars.boardPos['y']}
        self.maskCenter = self.boardvars.unit * 3
        # Area Mask
        self.revealImage = pygame.image.load('images/Mask-7x7.png').convert_alpha()
        self.revealArea = pygame.Surface((self.boardvars.unit * 7, self.boardvars.unit * 7))
        self.revealArea.fill("black")
        self.trailArea = pygame.Surface(pygame.display.get_window_size())
        self.heroColors = [(255,0,0),(255,255,0),(0,255,0),(0, 0,255)]
        self.heroTrail = []
        self.animXY = Tween(
            begin=0,
            end=self.boardvars.unit,
            duration=500,
            easing=Easing.LINEAR,
            easing_mode=EasingMode.IN_OUT,
            boomerang=False,
            loop=False
        )
        self.animTrail = Tween(
            begin=0,
            end=255,
            duration=500,
            easing=Easing.LINEAR,
            easing_mode=EasingMode.IN_OUT,
            boomerang=False,
            loop=False
        )

    def DrawSight(self, players, showMask=False):
        if showMask:
            self.revealMask = pygame.Surface(self.boardvars.screenSize, flags=pygame.SRCALPHA)
            self.revealMask.fill("black")

            for i in players:
                self.revealMask.blit(self.revealImage, (i.grid[0]-self.maskCenter,i.grid[1]-self.maskCenter), special_flags=pygame.BLEND_RGBA_SUB)
            self.screen.blit(self.revealMask, (self.maskPos["x"], self.maskPos["y"]))

        for i, player in enumerate(players):
            pygame.draw.rect(self.screen, self.heroColors[i], pygame.Rect(player.grid[0]+self.maskPos["x"],player.grid[1]+self.maskPos["y"],self.boardvars.unit,self.boardvars.unit), 5)

        t = pygwidgets.DisplayText(self.screen, loc=(150, 150), value=str(len(self.heroTrail)), fontName='ProzaLibre-Bold', fontSize=256, width=None, height=None, textColor=(255, 255, 0), backgroundColor=None, justified='left')
        t.draw()

    def DrawTrail(self, player):
        moveCount = len(self.heroTrail)
        if player.grid in self.heroTrail:
            self.heroTrail.remove(player.grid)
        if moveCount > 0:
            for trail in self.heroTrail:
                imp = pygame.image.load("images/heroTrail.png").convert_alpha()
                imp.set_alpha(255)
                self.screen.blit(imp, (trail[0]+self.maskPos['x'],trail[1]+self.maskPos['y']))