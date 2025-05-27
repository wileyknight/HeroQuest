import socket

class HeroVars():
    def __init__(self):
        self.screenSize = (800, 480)
        self.touchXY = [16200,9550]
        self.ip = "192.168.0.218"
    
    def getIP(self):
        ip = socket.gethostname()
        if 'player' not in ip:
            self.ip = ip
        return self.ip