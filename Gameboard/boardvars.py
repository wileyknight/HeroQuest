import socket

class BoardVars():
    def __init__(self):
        self.unit = 110
        self.unitsX = 26
        self.unitsY = 19
        self.boardPos = {"x":490,"y":35}
        self.screenSize = (3840, 2160)
        self.ip = "192.168.0.218"
    
    def getIP(self):
        ip = socket.gethostname()
        if 'player' not in ip:
            self.ip = ip
        return self.ip