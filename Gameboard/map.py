import pygwidgets
from rooms import RoomCovers
from grid import GridMap

class GameMap():
    def __init__(self, screen, boardMatrix):
        self.screen = screen
        self.grid = GridMap()
        self.boardMatrix = boardMatrix
        self.startPos = 'A19'
        self.boardImage = pygwidgets.Image(screen, (0, 0), 'images/Forsaken_Tunnels_Of_Xor-Xel.png')
        self.doors = ['C14D15','C15U12','C18D0','C19U15','E12R13','F12L12','F19D0','G9D0','G10U5','G13D16','G14U13','I5R3','I10D14','I11U0','I13D16','I14U14','J5L5','L6D0','L7U3','S10D18','S11U0','U13R19','U16R22','V13L18','V16L21','X14D22','X15U19']
        self.secrets = ['R13D','T18D']
        self.traps = ['C13R','F16S','G8S','I5S','I16S','K5P','K7R','K13R','M13R','O7S','O15R','O18S','P18S','Q7S','Q12S','Q15R','Q18S','S13P','T13R','T16R']
        self.monsters = ['B11S','C11Z','D11S','E11Z','F7S','F17S','F18S','G5S','G7S','G16M','H5Z','H16S','J2Z','L4S','L6S','M15A','N13Z','Q8Z','S14S','T12S','T14S','U13S','V15Z','V17Z','W13S','W16D','X13S']
        self.blocks = ['A18','D19','F10','G6','H8','I12','J3','K3','M6','M14','N6','N14','U10','V19','X12']
        self.furniture = ['']
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
        }
        for monster in self.monsters:
            m = self.grid.seperate(monster)
            self.monsterPos.append(pygwidgets.Image(self.screen, self.grid.getGrid(m[0]+str(m[1])), self.monsterImg[m[2]]))
            self.boardMatrix.board[m[0]+str(m[1])]['blocked'] = 2

        for door in self.doors:
            d = self.grid.seperate(door)
            self.doorPos.append(pygwidgets.CustomButton(self.screen, self.grid.getGrid(d[0]+str(d[1])), self.doorImg[d[2]]))
            
        for trap in self.traps:
            t = self.grid.seperate(trap)
            self.trapPos.append(pygwidgets.Image(self.screen, self.grid.getGrid(t[0]+str(t[1])), self.trapImg[t[2]]))
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

        self.roomcovers.roomcover()
        
        if self.reveal != None:
            self.roomcovers.anim.update()
            self.roomcovers.rooms[int(self.reveal)].set_alpha(self.roomcovers.anim.value)
        
    def openDoor(self, selected):
        for idx, door in enumerate(self.doorPos):
            if self.doors[idx] == selected:
                d = self.grid.seperate(self.doors[idx])
                #self.roomcovers.visibility[int(d[3])] = False
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