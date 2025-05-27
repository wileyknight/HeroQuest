import pygwidgets

class ChooseCharacter():
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygwidgets.Image(screen, (0, 0), 'images/HeroChooseBg.png')
        self.logo = pygwidgets.Image(screen, (18, 13), 'images/logoChr.png')
        self.char1 = pygwidgets.CustomButton(self.screen, (205, 41),"images/btn_barbarianMale.png")
        self.char2 = pygwidgets.CustomButton(self.screen, (345, 41),"images/btn_elfFemale.png")
        self.char3 = pygwidgets.CustomButton(self.screen, (485, 41),"images/btn_wizard.png")
        self.char4 = pygwidgets.CustomButton(self.screen, (625, 41),"images/btn_bard.png")

    def eventListener(self, event, clientname, send, chooseCharacter):
        if self.char1.handleEvent(event):
            send({"messageType":"CHARACTER","character":"Barbarian Male","player":clientname})
            chooseCharacter(1)
        if self.char2.handleEvent(event):
            send({"messageType":"CHARACTER","character":"Elf Female","player":clientname})
            chooseCharacter(2)
        if self.char3.handleEvent(event):
            send({"messageType":"CHARACTER","character":"Wizard","player":clientname})
            chooseCharacter(3)
        if self.char4.handleEvent(event):
            send({"messageType":"CHARACTER","character":"Bard","player":clientname})
            chooseCharacter(4)

    def addToScreen(self):
        self.bg.draw()
        self.logo.draw()
        self.char1.draw()
        self.char2.draw()
        self.char3.draw()
        self.char4.draw()