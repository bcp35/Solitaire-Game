from PyQt6.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class GameWon(QMainWindow):
    def __init__(self,time_taken, menu_fun, start_fun):
        super().__init__()
        self.time_taken = time_taken
        self.menu_fun = menu_fun
        self.start_fun = start_fun

        self.setWindowTitle("Solitaire")
        self.setGeometry(100,100,400,400)

        container = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("You Won!")
        title_label.setFont(QFont("Arial",60))
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label)

        time_label = QLabel(f"Time taken: {self.time_taken}")
        time_label.setFont(QFont("Arial",40))
        time_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(time_label)

        start_button = QPushButton("New Game")
        start_button.setFixedSize(200,50)
        start_button.setFont(QFont("Arial",20))
        start_button.clicked.connect(self.startFun)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        menu_button = QPushButton("Main Menu")
        menu_button.setFixedSize(200,50)
        menu_button.setFont(QFont("Arial",20))
        menu_button.clicked.connect(self.menuFun)
        layout.addWidget(menu_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def startFun(self):
        self.start_fun()
        self.hide()
    
    def menuFun(self):
        self.menu_fun()
        self.hide()

