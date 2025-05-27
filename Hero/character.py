import pygwidgets

class Character():
    def __init__(self, screen):
        self.screen = screen
        self.bg1 = pygwidgets.Image(self.screen, (0, 0),"images/bg_barbarianMale.png")
        self.bg2 = pygwidgets.Image(self.screen, (0, 0),"images/bg_elfFemale.png")
        self.bg3 = pygwidgets.Image(self.screen, (0, 0),"images/bg_wizard.png")
        self.bg4 = pygwidgets.Image(self.screen, (0, 0),"images/bg_bard.png")
        self.up = pygwidgets.CustomButton(self.screen, (375, 190),"images/btn_arrowUp.png")
        self.down = pygwidgets.CustomButton(self.screen, (475, 190),"images/btn_arrowDown.png")
        self.left = pygwidgets.CustomButton(self.screen, (425, 290),"images/btn_arrowLeft.png")
        self.right = pygwidgets.CustomButton(self.screen, (425, 90),"images/btn_arrowRight.png")
        self.inventory = pygwidgets.CustomButton(self.screen, (570, 0),"images/btn_inventory.png")
        self.showBg = 0

    def eventListener(self, event, clientname, send):
        if self.up.handleEvent(event):
            send({"messageType":"MOVE","player":clientname,"direction":"U"})
        if self.down.handleEvent(event):
            send({"messageType":"MOVE","player":clientname,"direction":"D"})
        if self.left.handleEvent(event):
            send({"messageType":"MOVE","player":clientname,"direction":"L"})
        if self.right.handleEvent(event):
            send({"messageType":"MOVE","player":clientname,"direction":"R"})

    def addToScreen(self):
        char = eval("self.bg"+str(self.showBg))
        char.draw()
        self.up.draw()
        self.down.draw()
        self.left.draw()
        self.right.draw()
        self.inventory.draw()