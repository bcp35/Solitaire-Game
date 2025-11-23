from PyQt6.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

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
        textLabels.append(QLabel("At each turn, the current state will look like this: "))

        label = QLabel()
        pixmap = QPixmap("Images/GameStateExample.png")
        pixmap = pixmap.scaledToHeight(300)
        label.setPixmap(pixmap)
        textLabels.append(label)

        textLabels.append(QLabel("The aim of the game is to add cards of the same suit from Ace to King in each stack in the correct order."))
        textLabels.append(QLabel("Click on a card to pick it up, or the highest card in a lane to pick up many."))
        textLabels.append(QLabel("Click on a stack or lane to put the card down there, or the return button to put it back."))


        startButton = QPushButton("Start Game")
        startButton.setFixedSize(200,40)
        startButton.setFont(QFont("Arial",15))
        startButton.clicked.connect(self.start_fun)

        menuButton = QPushButton("Main Menu")
        menuButton.setFixedSize(200,40)
        menuButton.setFont(QFont("Arial",15))
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



