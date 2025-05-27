import re
from gamevars import GameVars

class GridMap():
    def __init__(self):
        self.boardX = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.gamevars = GameVars()
        
    def getGrid(self, pos, abs=False):
        blockPos = self.seperate(pos)
        _x = 0
        _y = self.gamevars.unit*(int(blockPos[1])-1)
        if blockPos[0] in self.boardX:
            for i, a in enumerate(self.boardX):
                if a == blockPos[0]:
                    _x = self.gamevars.unit*i
        if not abs:
            _x = _x + self.gamevars.boardPos['x']
            _y = _y + self.gamevars.boardPos['y']

        return (_x,_y)
    
    def seperate(self, pos):
        return re.findall(r"[^\W\d_]+|\d+", pos)
    
    def getPos(self, grid):
        _x = int(grid[1] / self.gamevars.unit)
        _x = self.boardX[_x]
        _y = str(grid[0] / self.gamevars.unit)
        return _x+_y
    
    def getBlockSurrounding(self, pos):
        gridpos = self.seperate(pos)
        gridpos[1] = int(gridpos[1])
        boardXIdx = self.boardX.index(gridpos[0])
        posU = None
        posD = None
        posL = None
        posR = None
        gridU = None
        gridD = None
        gridL = None
        gridR = None
        if gridpos[1]-1 > 0:
            posU = gridpos[0]+str(gridpos[1]-1)
            gridU = self.getGrid(posU, abs=True)
        if gridpos[1]+1 < 20:
            posD = gridpos[0]+str(gridpos[1]+1)
            gridD = self.getGrid(posD, abs=True)
        if boardXIdx-1 > -1:
            posL = self.boardX[boardXIdx-1]+str(gridpos[1])
            gridL = self.getGrid(posL, abs=True)
        if boardXIdx+1 < len(self.boardX):
            posR = self.boardX[boardXIdx+1]+str(gridpos[1])
            gridR = self.getGrid(posR, abs=True)

        return {
            'U': (posU, gridU),
            'D': (posD, gridD),
            'L': (posL, gridL),
            'R': (posR, gridR)
        }
