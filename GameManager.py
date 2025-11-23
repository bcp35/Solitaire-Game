from MainMenu import MainMenu
from Instructions import Instructions
from SolitaireGUI import GameWindow
from PyQt6.QtWidgets import QApplication

class GameManager():
    def __init__(self):
        self.main = MainMenu(self.StartGame, self.OpenInstructions, self.Exit)
        self.instr = Instructions(self.StartGame, self.OpenMainMenu)
        self.game = GameWindow(self.OpenMainMenu, self.StartGame)
        self.active_window = self.main
        self.active_window.show()
    def getActive(self):
        return self.active_window

    def OpenInstructions(self):
        self.active_window.hide()
        self.active_window = self.instr
        self.active_window.show()

    def OpenMainMenu(self):
        self.active_window.hide()
        self.active_window = self.main
        self.active_window.show()

    def StartGame(self):
        self.active_window.close()
        self.game = GameWindow(self.OpenMainMenu, self.StartGame) #reinitialising to ensure game state is not saved and new game is started next time
        self.active_window = self.game
        self.active_window.show()

    def Exit(self):
        QApplication.quit()


app = QApplication([])
manager = GameManager()
app.exec()