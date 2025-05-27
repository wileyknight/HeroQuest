import socket

class GameVars():
    def __init__(self):
        self.unit = 55
        self.unitsX = 26
        self.unitsY = 19
        self.boardPos = {"x":245,"y":18}
        self.screenSize = (1920, 1080)
        self.ip = "192.168.0.218"
        self.fps = 15
    
    def getIP(self):
        ip = socket.gethostname()
        if 'player' not in ip:
            self.ip = ip
        return self.ip