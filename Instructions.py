from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Instructions(QMainWindow):
    def __init__(self, start_fun, menu_fun):
        super().__init__()

        self.start_fun = start_fun
        self.menu_fun = menu_fun

        self.setWindowTitle("Solitaire")
        self.setGeometry(50,50,1000,600)

        layout = QVBoxLayout()

        titleLabel = QLabel("Instructions")
        titleLabel.setFont(QFont("Arial",60))
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(titleLabel)

        textLabels = []
        textLabels.append(QLabel("How to play Solitare:"))
        textLabels.append(QLabel("At each turn, the current state will look like this: "))
        textLabels.append(QLabel("[Insert Image]"))
        textLabels.append(QLabel("The deck shows the cards that you have left to use, displaying them 3 at a time,only able to use the right-most of the three, and gaining access to the other cards after using them."))
        textLabels.append(QLabel("The aim of the game is to add cards of the same suit from Ace to King in each stack in the correct order."))
        textLabels.append(QLabel("Each lane contains a stack of cards from high to low of alternating colours. Cards can move between lanes, but only if it is one rank below the card above it. Moving a card to another lane reveals the card that was above it. Only Kings can move to empty lanes."))
        textLabels.append(QLabel("For each go you have the option to access the next card in the deck, or the bottom card from each lane, and move it to the corresponding stack for that rank or another lane, if that is a legal move."))

        startButton = QPushButton("Start Game")
        startButton.setFixedSize(350,60)
        startButton.setFont(QFont("Arial",25))
        startButton.clicked.connect(self.start_fun)

        menuButton = QPushButton("Main Menu")
        menuButton.setFixedSize(350,60)
        menuButton.setFont(QFont("Arial",25))
        menuButton.clicked.connect(self.menu_fun)

        for label in textLabels:
            label.setFont(QFont("Arial",15))
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addWidget(label)

        layout.addWidget(startButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(menuButton, alignment=Qt.AlignmentFlag.AlignHCenter)

        widget = QWidget()
        widget.setMaximumWidth(1000)
        widget.setLayout(layout)
        self.setCentralWidget(widget)



