import pygame, pygwidgets
from tween import *

class RoomCovers():
    def __init__(self, screen):
        self.screen = screen
        self.roomSize = [(0,0),(440, 330),(440, 330),(330, 550),(440, 550),(440, 550),(330, 550),(440, 440),(440, 440),(440, 440),(440, 440),(660, 550),(440, 440),(220, 330),(220, 330),(440, 440),(440, 550),(330, 550),(440, 440),(440, 440),(440, 550),(330, 440),(440, 440)]
        self.roomPos = [(0,0),(600, 145),(1040, 145),(1480, 145),(600, 475),(1040, 475),(2030, 145),(2360, 145),(2800, 145),(2360, 585),(2800, 585),(1590, 805),(600, 1135),(1040, 1135),(1260, 1135),(600, 1575),(1040, 1465),(1480, 1465),(2360, 1135),(2800, 1135),(2030, 1465),(2470, 1575),(2800, 1575)]
        self.rooms = []
        self.visibility = []
        for idx, size in enumerate(self.roomSize):
            self.rooms.append(pygame.Surface(size))
            self.visibility.append(True)
        self.anim = Tween(
            begin=255,
            end=0,
            duration=1000,
            easing=Easing.QUAD,
            easing_mode=EasingMode.OUT,
            boomerang=False,
            loop=False
        )

    def roomcover(self):
        for idx, room in enumerate(self.rooms):
            if self.visibility[idx]:
                self.screen.blit(room, self.roomPos[idx])