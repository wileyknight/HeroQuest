import pygame, sys, threading
from buttonmap import ButtonMap
from dmserver import Connection, RunServer
from gamestate import GameState
from gamevars import GameVars

gamevars = GameVars()
#flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(gamevars.screenSize, vsync=1)

'''Initialize pygame and setup variables'''
pygame.init()
fpsClock = pygame.time.Clock()

state = GameState(screen, pygame)
runonce = False
#Start connections
#py_connection = Connection()
#hqServer = RunServer(py_connection)
print("Server is listening for incoming connections...\n")

# Setup Room

#buttonmap = ButtonMap(screen)

#recieve_thread = threading.Thread(target=hqServer.connectPi, args=(state,))
#recieve_thread.daemon = True
#recieve_thread.start()



'''Main loop.'''
while True:
    screen.fill((20, 20, 20))
    #Listen for events and perform corresponding actions
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            #hqServer.close()
            pygame.quit()
            sys.exit()
        #buttonmap.eventListener(event, updateHeroLoc)
        state.eventListener(event, events)
    
    state.drawGame()
    #buttonmap.addToScreen()

    #Refresh the display and update the clock with the desired fps
    pygame.display.flip()
    fpsClock.tick(gamevars.fps)

    if runonce == False:
        runonce = True
        #hqServer.connectPi(state)