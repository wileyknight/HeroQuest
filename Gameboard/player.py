from grid import GridMap

class Player():
    def __init__(self, pos, grid, boardMatrix):
        self.pos = pos
        self.grid = grid
        self.gridmap = GridMap()
        self.boardMatrix = boardMatrix

    def move(self, data):
        surrounding = self.gridmap.getBlockSurrounding(self.pos)
        if self.boardMatrix.board[self.pos][data["direction"]]:
            pos = None
            pos, grid = surrounding[data["direction"]]

            if self.boardMatrix.board[pos]["blocked"] < 2 and pos != None:
                self.pos = pos
                self.grid = grid
        
        return {"pos":self.pos,"grid":self.grid}