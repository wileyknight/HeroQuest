import pygame, json, sys
from pygame._sdl2.touch import *
from herostate import HeroState
from herovars import HeroVars

gamevars = HeroVars()

flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(gamevars.screenSize, vsync=1)

state = HeroState(screen, gamevars)

'''Start the connection'''

#connection = Connection()
print("Attempting to connect to server\n")

'''Initialize pygame and setup variables'''
pygame.init()
fps = 15
fpsClock = pygame.time.Clock()

pygame.mouse.set_visible(False)

'''Main loop.'''
while True:
    screen.fill((20, 20, 20))
    #Listen for events and perform corresponding actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if state.connection.connected:
                state.connection.disconnect()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                if state.connection.connected:
                    state.connection.disconnect()
                pygame.quit()
                sys.exit()
        #Add the button handlers
        state.eventListener(event)

    state.drawGame()

        #Refresh the display and update the clock with the desired fps
    pygame.display.flip()
    fpsClock.tick(fps)

    if not state.connection.connected:
        if state.connection.connCount > 100:
            state.connection.connCount = 0
            print('reconnecting')
            state.connection.on_enter(state)
        else:
            state.connection.connCount += 1
