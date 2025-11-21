from SolitaireCLI import Card, Deck, Stack, GameState

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QGridLayout, QSpacerItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class CardGUI(Card):
    def __init__(self, suit_int, rank_int):
        super().__init__(self,suit_int,rank_int)
        self.image_location = f"Images/{self.suit[0]}{self.rank_string}.png"
    
    def getDisplayName(self):
        return self.image_location

class GameStateGUI(GameState):
    def __init__(self, pack, start_time):
        super().__init__(self,pack,star_time)


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Solitaire")
        self.setGeometry(50,50,1000,600)

        layout = QGridLayout()
        layout.setContentsMargins(75,10,75,10)

        layout.addWidget(self.createImage("Images/empty.png"),0,0)
        layout.addWidget(self.createImage("Images/empty.png"),0,1)

        layout.addWidget(self.createImage("Images/empty.png"),0,3)
        layout.addWidget(self.createImage("Images/empty.png"),0,4)
        layout.addWidget(self.createImage("Images/empty.png"),0,5)
        layout.addWidget(self.createImage("Images/empty.png"),0,6)

        spacer = QSpacerItem(1000,200)
        layout.addItem(spacer,3,0,1,7)

        layout.addWidget(self.createImage("Images/empty.png"),2,0)
        layout.addWidget(self.createImage("Images/empty.png"),2,1)
        layout.addWidget(self.createImage("Images/empty.png"),2,2)
        layout.addWidget(self.createImage("Images/empty.png"),2,3)
        layout.addWidget(self.createImage("Images/empty.png"),2,4)
        layout.addWidget(self.createImage("Images/empty.png"),2,5)
        layout.addWidget(self.createImage("Images/empty.png"),2,6)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def createImage(self,loc):
        label = QLabel()
        pixmap = QPixmap(loc)
        pixmap = pixmap.scaledToHeight(150)
        label.setPixmap(pixmap)
        return label

app = QApplication([])
game_window = GameWindow()

active_window = game_window
active_window.show()
app.exec()

game_state = GameState()