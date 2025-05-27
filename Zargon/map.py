import pygwidgets, json
from rooms import RoomCovers
from grid import GridMap

class GameMap():
    def __init__(self, screen, boardMatrix, mapName):
        self.screen = screen
        self.grid = GridMap()
        self.boardMatrix = boardMatrix
        self.mapInfo = self.getMaps()
        self.startPos = self.mapInfo[mapName]["start"]
        self.boardImage = pygwidgets.Image(screen, (0, 0), self.mapInfo[mapName]["image"])
        self.doors = self.mapInfo[mapName]["doors"]
        self.secrets = self.mapInfo[mapName]["secrets"]
        self.traps = self.mapInfo[mapName]["traps"]
        self.monsters = self.mapInfo[mapName]["monsters"]
        self.blocks = self.mapInfo[mapName]["blocks"]
        self.monsterPos = []
        self.doorPos = []
        self.trapPos = []
        self.reveal = None
        self.doorImg = {
            'U':'images/doorUp.png',
            'D':'images/doorDown.png',
            'L':'images/doorLeft.png',
            'R':'images/doorRight.png',
        }
        self.monsterImg = {
            'A':'images/abomination.png',
            'G':'images/goblin.png',
            'O':'images/orc.png',
            'Z':'images/zombie.png',
            'D':'images/dread.png',
            'M':'images/mummy.png',
            'G':'images/gargoyle.png',
            'S':'images/skeleton.png',
        }
        self.trapImg = {
            'P':'images/pit.png',
            'R':'images/rocks.png',
            'S':'images/spear.png',
            'C':'images/chest2.png',
        }
        for monster in self.monsters:
            m = self.grid.seperate(monster)
            self.monsterPos.append(pygwidgets.CustomButton(self.screen, self.grid.getGrid(m[0]+str(m[1])), self.monsterImg[m[2]]))
            self.boardMatrix.board[m[0]+str(m[1])]['blocked'] = 2

        for door in self.doors:
            d = self.grid.seperate(door)
            self.doorPos.append(pygwidgets.CustomButton(self.screen, self.grid.getGrid(d[0]+str(d[1])), self.doorImg[d[2]]))
            
        for trap in self.traps:
            t = self.grid.seperate(trap)
            self.trapPos.append(pygwidgets.CustomButton(self.screen, self.grid.getGrid(t[0]+str(t[1])), self.trapImg[t[2]]))
            self.boardMatrix.board[t[0]+str(t[1])]['trap'] = t[2]

        for block in self.blocks:
            self.boardMatrix.board[block]['blocked'] = 3

        self.roomcovers = RoomCovers(screen)
        self.room = None
        
        
    def populate(self, showMonsters=False):
        for trap in self.trapPos:
                trap.draw()
        
        if showMonsters:
            for monster in self.monsterPos:
                monster.draw()

        for door in self.doorPos:
                door.draw()

        #self.roomcovers.roomcover()
        
        if self.reveal != None:
            self.roomcovers.anim.update()
            self.roomcovers.rooms[int(self.reveal)].set_alpha(self.roomcovers.anim.value)
        
    def eventListener(self, event, sendMessage, hud):
        for idx, door in enumerate(self.doorPos):
            if door.handleEvent(event):
                d = self.grid.seperate(self.doors[idx])
                #self.roomcovers.visibility[int(d[3])] = False
                sendMessage('board', {'messageType': 'OPEN', 'door': self.doors[idx]})
                pos = d[0]+str(d[1])
                self.reveal = d[3]
                self.roomcovers.anim.start()
                self.boardMatrix.board[pos][d[2]] = True
                surroundBlock = self.grid.getBlockSurrounding(pos)
                if d[2] == 'U' and surroundBlock[d[2]] != None:
                    up = surroundBlock['U'][0]
                    self.boardMatrix.board[up]['D'] = True
                    del self.doors[idx]
                    del self.doorPos[idx]
                if d[2] == 'D' and surroundBlock[d[2]] != None:
                    down = surroundBlock['D'][0]
                    self.boardMatrix.board[down]['U'] = True
                if d[2] == 'L' and surroundBlock[d[2]] != None:
                    left = surroundBlock['L'][0]
                    self.boardMatrix.board[left]['R'] = True
                if d[2] == 'R' and surroundBlock[d[2]] != None:
                    right = surroundBlock['R'][0]
                    self.boardMatrix.board[right]['L'] = True

        for idx, monster in enumerate(self.monsterPos):
            if monster.handleEvent(event):
                hud.showMenu = True
                hud.showMonsterMenu = True
                #m = self.grid.seperate(self.monster[idx])

        for idx, trap in enumerate(self.trapPos):
            if trap.handleEvent(event):
                hud.showMenu = True
                hud.showTrapMenu = True
                #m = self.grid.seperate(self.monster[idx])

    def getMaps(self):
        with open('maps.json') as load_file:
            return json.load(load_file)