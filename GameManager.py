from MainMenu import MainMenu
from Instructions import Instructions
from PyQt6.QtWidgets import QApplication

def OpenInstructions():
    main_window.hide()
    instr_window.show()

def OpenMainMenu():
    instr_window.hide()
    main_window.show()

def StartGame():
    print("Start Game now")

def Exit():
    QApplication.quit()

app = QApplication([])

main_window = MainMenu(StartGame, OpenInstructions, Exit)
instr_window = Instructions(StartGame, OpenMainMenu)

active_window = main_window
active_window.show()
app.exec()