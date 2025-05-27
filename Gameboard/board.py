import pygame, sys
from boardconnection import Connection
from gamestate import GameState
from boardvars import BoardVars

gamevars = BoardVars()

#flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(gamevars.screenSize, vsync=1)

state = GameState(screen)

#Start connections
connection = Connection()
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
            connection.close()
            pygame.quit()
            sys.exit()
    
    state.drawGame()

    #Refresh the display and update the clock with the desired fps
    pygame.display.flip()
    fpsClock.tick(fps)

    if not connection.connected:
        if connection.connCount > 100:
            connection.connCount = 0
            print('reconnecting')
            connection.on_enter(state)
        else:
            connection.connCount += 1

