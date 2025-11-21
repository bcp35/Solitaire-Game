from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MainMenu(QMainWindow):
    def __init__(self, start_fun, instr_fun, exit_fun):
        super().__init__()

        self.start_fun = start_fun
        self.instr_fun = instr_fun
        self.exit_fun = exit_fun

        self.setWindowTitle("Solitaire")
        self.setGeometry(50,50,1000,600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,10,0,10)
        layout.setSpacing(20)

        titleLabel = QLabel("Welcome to Solitaire!")
        titleLabel.setFont(QFont("Arial",70))
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        menuLabel = QLabel("Main Menu")
        menuLabel.setFont(QFont("Arial",60))
        menuLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        startButton = QPushButton("Start Game")
        startButton.setFixedSize(350,60)
        startButton.setFont(QFont("Arial",25))
        startButton.clicked.connect(start_fun)
        
        instrButton = QPushButton("Instructions")
        instrButton.setFixedSize(350,60)
        instrButton.setFont(QFont("Arial",25))
        instrButton.clicked.connect(instr_fun)
        
        exitButton = QPushButton("Exit")
        exitButton.setFixedSize(350,60)
        exitButton.setFont(QFont("Arial",25))
        exitButton.clicked.connect(exit_fun)
        
        layout.addWidget(titleLabel)
        layout.addWidget(menuLabel)

        layout.addSpacing(100)

        layout.addWidget(startButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(instrButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(exitButton, alignment=Qt.AlignmentFlag.AlignHCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)