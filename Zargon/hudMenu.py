import pygwidgets
from pygame_menu import locals
from pygame_menu.examples import create_example_window
from pygame_menu._scrollarea import ScrollArea
from pygame_menu.utils import make_surface

import itertools
from typing import Generator
from gamevars import GameVars

class HudMenu():
    def __init__(self, pygame, screen, gameItems):
        self.pygame = pygame
        self.screen = screen
        self.gameItems = gameItems
        self.gameVars = GameVars()
        
        self.LEGEND = 'Area {}x{}\nWorld {}x{}\nPress [ESC] to change'
        self.W_SIZE = 191  # Width of window size
        self.H_SIZE = 509  # Height of window size
        self.WORLDS = {
            '1': {'pos': (22, 405),
                'win': (self.W_SIZE, self.H_SIZE),
                'size': (self.W_SIZE, self.H_SIZE * 2)}
        }
        self.area = ScrollArea(
            self.W_SIZE, self.H_SIZE,
            scrollbars=(
                locals.POSITION_EAST
            )
        )
        
        self.worlds = self.iter_world(self.area)
        next(self.worlds)


    def make_world(self, width: int, height: int, text: str = ''):
        world = make_surface(width, height)
        myButton = pygwidgets.TextButton(world, (0, 0), 'text1', 150, 30, (255,255,255), (105,49,46), (105,49,46), (105,49,46), 'prozalibre', 20)
        myButton.draw()

        return world

    # noinspection PyProtectedMember
    def iter_world(self, area) -> Generator:
        for name in itertools.cycle(self.WORLDS):
            params = self.WORLDS[name]
            area._rect.width = params['win'][0]
            area._rect.height = params['win'][1]
            area.set_world(self.make_world(params['size'][0], params['size'][1]))
            area.set_position(*params['pos'])
            yield params

    def eventListener(self, event, events) -> None:
        self.area.update(events)

    def runMenu(self) -> None:
        self.pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.area.get_rect()  # Inflate to see area overflow in case of bug
        )
        self.area.draw(self.screen)