from datetime import datetime
import numpy as np

from SolitaireCLI import Card, Deck, Stack, Lane, GameState, Shuffle

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QGridLayout, QSpacerItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class CardGUI(Card):
    def __init__(self, suit_int, rank_int):
        super().__init__(suit_int,rank_int)
        self.image_location = f"Images/{self.suit[0]}{self.rank_string}.png"
    
    def getDisplayName(self):
        return self.image_location

class DeckGUI(Deck):
    def __init__(self, pack):
        super().__init__(pack)
    def getDisplay(self):
        return (len(self.stock_pile), [c.getDisplayName() for c in self.getNextThree()])


class StackGUI(Stack):
    def __init__(self, suit_int):
        super().__init__(suit_int)
    def getDisplay(self):
        return self.suit[0], self.top_rank

class LaneGUI(Lane):
    def __init__(self, cards, i):
        super().__init__(cards, i)
    def getDisplay(self):
        cards = []
        for c in self.hidden_cards:
            cards.append("Images/back.png")
        for c in self.shown_cards:
            cards.append(c.getDisplayName())
        return cards
        
    

class GameStateGUI(GameState):
    def __init__(self, pack, start_time, game_window):
        super().__init__(pack,start_time)
        self.deck = DeckGUI(pack[28:]) #overwrite: class must be DeckGUI
        self.stacks = [StackGUI(i) for i in range(4)] #overwrite: class must be StackGUI
        self.game_window = game_window
        self.getDisplay() 
    def distributeLanes(self,cards): #overwrite: class must be LaneGUI
        start = 0
        for i in range(1,8):
            self.lanes[i-1] = LaneGUI(cards[start:start+i],i)
            start += i
    def getDisplay(self):
        #set up the deck
        num_cards, first_three = self.deck.getDisplay()
        if num_cards == 0:
            game_window.setEmpty(0,0)
        else:
            game_window.setHidden(0,0)
        
        deck_cell = QWidget() #allowing putting multiple cards within a single cell of the grid layout
        deck_cell.setFixedHeight(150)

        for i in range(len(first_three)):
            widget = game_window.createImage(first_three[i])
            widget.setParent(deck_cell)
            widget.move(i*25,0)

        game_window.replaceCard(0,1,deck_cell,1,2)


        #set up the stacks
        for i in range(4):
            stack = self.stacks[i]
            suit, rank_int = stack.getDisplay()
            if rank_int == 0:
                game_window.setEmpty(0,i+3)
            else:
                name = suit + ranks[rank_int-1]
                game_window.replaceCard(0,i+3,game_window.createImage("Images/" + suit + ranks[rank_int] + ".png"))

        #set up the lanes
        for i in range(7):
            lane = self.lanes[i]
            lane_cell = QWidget()
            cards = lane.getDisplay()
            lane_cell.setFixedHeight(600)

            for j in range(len(cards)):
                card = cards[j]
                widget = game_window.createImage(card)
                widget.setParent(lane_cell)
                widget.move(0,j*25)
            
            game_window.replaceCard(2,i,lane_cell)


ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"] #conversion from integer rank into string

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Solitaire")
        self.setGeometry(50,50,1000,600)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(75,10,75,10)

        self.layout.addWidget(self.createImage("Images/empty.png"),0,0)
        self.layout.addWidget(self.createImage("Images/empty.png"),0,1,1,2)

        self.layout.addWidget(self.createImage("Images/empty.png"),0,3)
        self.layout.addWidget(self.createImage("Images/empty.png"),0,4)
        self.layout.addWidget(self.createImage("Images/empty.png"),0,5)
        self.layout.addWidget(self.createImage("Images/empty.png"),0,6)

        self.layout.addItem(QSpacerItem(1000,200),3,0,1,7) #adds a gap below the lanes for better formatting

        self.layout.addWidget(self.createImage("Images/empty.png"),2,0)
        self.layout.addWidget(self.createImage("Images/empty.png"),2,1)
        self.layout.addWidget(self.createImage("Images/empty.png"),2,2)
        self.layout.addWidget(self.createImage("Images/empty.png"),2,3)
        self.layout.addWidget(self.createImage("Images/empty.png"),2,4)
        self.layout.addWidget(self.createImage("Images/empty.png"),2,5)
        self.layout.addWidget(self.createImage("Images/empty.png"),2,6)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
            
    
    def replaceCard(self,row_num,col_num,new,row_span=1,col_span=1): #making row span and col span optional, set to 1 initially but can be changed, allowing elements that span more than one cell in the grid
        item = self.layout.itemAtPosition(row_num,col_num)
        if item: #check that item exists
            item.widget().setParent(None)
        self.layout.addWidget(new,row_num,col_num, row_span, col_span)
    
    def addNextTo(self,row_num,col_num,new):
        self.layout.addWidget(new,row_num,col_num+1)

    def setEmpty(self,row_num,col_num):
        widget = self.createImage("Images/empty.png")
        self.replaceCard(row_num, col_num, widget)

    def setHidden(self,row_num,col_num):
        widget = self.createImage("Images/back.png")
        self.replaceCard(row_num, col_num, widget)

    def createImage(self,loc):
        label = QLabel()
        pixmap = QPixmap(loc)
        pixmap = pixmap.scaledToHeight(150)
        label.setPixmap(pixmap)
        return label

def GameSetup():
    pack = Shuffle(GeneratePack())
    game_state = GameStateGUI(pack.tolist(),datetime.now(), game_window)

def GeneratePack():
    pack = np.empty(52, dtype = object)
    for i in range(4):
        for j in range(13):
            pack[13*i + j] = CardGUI(i, j)
    return pack

app = QApplication([])
game_window = GameWindow()

active_window = game_window
active_window.show()

GameSetup()

app.exec()