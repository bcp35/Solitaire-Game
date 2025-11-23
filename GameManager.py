from MainMenu import MainMenu
from Instructions import Instructions
from SolitaireGUI import GameWindow
from PyQt6.QtWidgets import QApplication

def OpenInstructions():
    active_window.hide()
    instr_window.show()

def OpenMainMenu():
    active_window.hide()
    main_window.show()

def StartGame():
    active_window.hide()
    game_window.show()

def Exit():
    QApplication.quit()

app = QApplication([])

main_window = MainMenu(StartGame, OpenInstructions, Exit)
instr_window = Instructions(StartGame, OpenMainMenu)
game_window = GameWindow(OpenMainMenu)

active_window = main_window
active_window.show()
app.exec()