from grid import GridMap

class Player():
    def __init__(self, client, sendMessage, boardMatrix):
        self.name = ""
        self.type = ""
        self.health = 0
        self.damage = 0
        self.defense = 0
        self.mind = 0
        self.gold = 0
        self.inventory = [],
        self.weapons = [],
        self.armor = [],
        self.pos = ""
        self.grid = None
        self.gridmap = GridMap()
        self.boardMatrix = boardMatrix
        self.pi_socket = client['socket']
        self.pi_address = client['address']
        self.pi_name = client['client']
        self.sendMessage = sendMessage
        self.passThrough = "walls" # 0=nothing 1=hero 2=monster 3=block/furniture

    def move(self, data):
        surrounding = self.gridmap.getBlockSurrounding(self.pos)
        if self.passThrough == "":
            if self.boardMatrix.board[self.pos][data["direction"]]:
                pos = None
                pos, grid = surrounding[data["direction"]]
                if self.boardMatrix.board[pos]["blocked"] < 2 and pos != None:
                    self.pos = pos
                    self.grid = grid
        if self.passThrough == "walls":
            if self.boardMatrix.board[self.pos][data["direction"]] != None:
                pos = None
                pos, grid = surrounding[data["direction"]]
                if (self.boardMatrix.board[pos]["blocked"] < 2 or self.boardMatrix.board[pos]["blocked"] == 3) and pos != None:
                    self.pos = pos
                    self.grid = grid
        if self.passThrough == "monster":
            if self.boardMatrix.board[self.pos][data["direction"]]:
                pos = None
                pos, grid = surrounding[data["direction"]]
                if self.boardMatrix.board[pos]["blocked"] < 3 and pos != None:
                    self.pos = pos
                    self.grid = grid
        return {"pos":self.pos,"grid":self.grid}
    
    def setStart(self, pos, saveData):
        self.pos = pos
        self.grid = self.gridmap.getGrid(pos, abs=True)
        self.type = saveData.type
        self.name = saveData.name
        self.health = saveData.health
        self.damage = saveData.damage
        self.defense = saveData.armor
        self.mind = saveData.mind
        self.gold = saveData.gold
        self.inventory = saveData.invertory
        self.weapons = saveData.weapons
        self.armor = saveData.armor