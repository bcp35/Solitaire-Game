from datetime import datetime
import numpy as np

from SolitaireCLI import Card, Deck, Stack, Lane, GameState, Shuffle
from GameWon import GameWon

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont, QPixmap

class CardGUI(Card):
    def __init__(self, suit_int, rank_int):
        super().__init__(suit_int,rank_int)
        self.image_location = f"Images/{self.suit[0]}{self.rank_string}.png"
    
    def getDisplayName(self):
        return self.image_location

class InvisibleButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFlat(True)
        self.setStyleSheet("background-color: rgba(0,0,0,0);border: none;") #make it transparent with no border

class DeckGUI(Deck):
    def __init__(self, pack):
        super().__init__(pack)
    def stockPileIsEmpty(self):
        return len(self.stock_pile) == 0
    def wastePileIsEmpty(self):
        return len(self.waste_pile) == 0
    def getDisplay(self):
        return (len(self.stock_pile), [c.getDisplayName() for c in self.getNextThree()])


class StackGUI(Stack):
    def __init__(self, suit_int):
        super().__init__(suit_int)
    def peek(self): #override to make a GUI Card
        if self.isEmpty():
            return None
        return CardGUI(self.suit_int, self.top_rank - 1)
    def getDisplay(self):
        return self.suit[0], self.top_rank

class LaneGUI(Lane):
    def __init__(self, cards, i):
        super().__init__(cards, i)
    def getDisplay(self):
        cards = []
        if self.isEmpty():
            return ["Images/empty.png"]
        for c in self.hidden_cards:
            cards.append("Images/back.png")
        for c in self.shown_cards:
            cards.append(c.getDisplayName())
        return cards
        
    

class GameStateGUI(GameState):
    def __init__(self, pack, start_time, game_window):
        super().__init__(pack,start_time)
        self.deck = DeckGUI(pack[28:]) #override: class must be DeckGUI
        self.stacks = [StackGUI(i) for i in range(4)] #override: class must be StackGUI
        self.check_give_up = False #whether the user has just pressed the give up button
        self.game_window = game_window
        self.getDisplay() 
    def distributeLanes(self,cards): #override: class must be LaneGUI
        start = 0
        for i in range(1,8):
            self.lanes[i-1] = LaneGUI(cards[start:start+i],i)
            start += i
    def buttonPress(self, function):
        function()
        self.getDisplay()
    def stockPilePress(self):
        if self.deck.stockPileIsEmpty():
            self.deck.reset()
        else:
            self.deck.next()
    def wastePilePress(self):
        if not self.deck.wastePileIsEmpty():
            if self.card_in_hand[0] == [None]:
                self.pickUpCard(self.deck.peek(),1) #last_loc = 1 means deck
    def stackPress(self,i):
        c = self.getCardInHand()[0][0]
        if c == None: #if not currently holding a card, attempt to pick it up from the stack
            self.pickUpCard(self.stacks[i].peek(),i+2) #last_loc values for stacks range from 2-5 (0+2 - 3+2)        
        else:
            if len(self.getCardInHand()[0]) == 1: #can only push 1 card onto stack
                if self.stacks[i].push(c):
                    self.RemoveCardFromLastLoc()
    def lanePress(self,lane_num,card_num):
        card_num = self.lanes[lane_num-1].getNumShownCards() - card_num + 1#card_num was counted top to bottom, but should be bottom to top
        cs = self.getCardInHand()[0]
        if cs == [None]:
            if card_num <= self.lanes[lane_num-1].getNumShownCards():
                self.pickUpCards(self.lanes[lane_num-1].peekMany(card_num),lane_num+5) #take a certain number of cards from the appropriate lane. last_loc values for stakcs range from 6-12(1+5 - 7+5)
        else:
            if self.lanes[lane_num-1].push(cs):
                self.RemoveCardFromLastLoc()
    def ReturnCard(self):
        super().ReturnCard()
        self.getDisplay() #as well as returning the card, update the display
    def CheckGiveUp(self):
        self.check_give_up = not self.check_give_up
    def checkIfGivingUp(self):
        return self.check_give_up
    def getDisplay(self):
        #check if the game has been won yet
        if self.gameWon():
            self.game_window.EndGame(datetime.now()-self.start_time)
            return

        #set up the deck
        num_cards, first_three = self.deck.getDisplay()
        if num_cards == 0:
            self.game_window.setEmpty(0,0)
        else:
            self.game_window.setHidden(0,0)
        deck_cell = QWidget() #allowing putting multiple cards within a single cell of the grid layout
        deck_cell.setFixedHeight(150)

        for i in range(len(first_three)):
            widget = self.game_window.createImage(first_three[i])
            widget.setParent(deck_cell)
            widget.move(i*25,0)

        self.game_window.replaceCard(0,1,deck_cell,1,2)

        self.game_window.createButton(lambda: self.buttonPress(self.stockPilePress),0,0) #using lambda allows parameter passing
        self.game_window.createButton(lambda: self.buttonPress(self.wastePilePress),0,1, col_span=2, width=156) #size of card + 2 overlapping

        #set up the stacks
        for i in range(4):
            stack = self.stacks[i]
            suit, rank_int = stack.getDisplay()
            if rank_int == 0:
                self.game_window.setEmpty(0,i+3)
            else:
                name = suit + ranks[rank_int-1]
                self.game_window.replaceCard(0,i+3,self.game_window.createImage("Images/" + name + ".png"))

        self.game_window.createButton(lambda: self.buttonPress(lambda: self.stackPress(0)),0,3)
        self.game_window.createButton(lambda: self.buttonPress(lambda: self.stackPress(1)),0,4)
        self.game_window.createButton(lambda: self.buttonPress(lambda: self.stackPress(2)),0,5)
        self.game_window.createButton(lambda: self.buttonPress(lambda: self.stackPress(3)),0,6)


        #set up the lanes
        for i in range(7):
            lane = self.lanes[i]
            lane_cell = QWidget()
            cards = lane.getDisplay()
            lane_cell.setFixedHeight(600)
            lane_cell.setFixedWidth(106)

            for j in range(len(cards)):
                card = cards[j]
                widget = self.game_window.createImage(card)
                widget.setParent(lane_cell)
                widget.move(0,j*25)

            lane_cell.setStyleSheet("background-color: rgb(30,30,30)") #adding a background colour to the lanes, the same colour as the window background, completely writes over the older cards
            
            self.game_window.replaceCard(2,i,lane_cell)

        #Attempted to use iteration, however when inserting variables into the function for the button press, 
        #the value of the variable when the button was pressed mattered, not when it was created, causing many problems
        #Therefore it has to be done manually, a lot of repeated/redundant code, but seemingly unavoidable

        #Lane1
        lane = self.lanes[0]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(1,13)))  
        self.game_window.placeButton(button_cell,2,0)


        #Lane2
        lane = self.lanes[1]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(2,13)))  
        self.game_window.placeButton(button_cell,2,1)


        #Lane3
        lane = self.lanes[2]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(3,13)))  
        self.game_window.placeButton(button_cell,2,2)


        #Lane4
        lane = self.lanes[3]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(4,13)))  
        self.game_window.placeButton(button_cell,2,3)


        #Lane5
        lane = self.lanes[4]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(5,13)))  
        self.game_window.placeButton(button_cell,2,4)


        #Lane 6
        lane = self.lanes[5]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(6,13)))  
        self.game_window.placeButton(button_cell,2,5)


        #Lane7
        lane = self.lanes[6]
        button_cell = QWidget()
        button_cell.setFixedSize(106,600)
        
        cards = lane.getDisplay()

        if lane.isEmpty():
            button = InvisibleButton()
            button.setFixedSize(106,150)
            button.setParent(button_cell)
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,1))) 
        
        num_shown_cards = lane.getNumShownCards()
        num_hidden_cards = len(cards) - num_shown_cards

        if num_shown_cards >= 1:
            button = InvisibleButton()
            if num_shown_cards == 1:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(0+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,1))) 
        if num_shown_cards >= 2:
            button = InvisibleButton()
            if num_shown_cards == 2:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(1+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,2))) 
        if num_shown_cards >= 3:
            button = InvisibleButton()
            if num_shown_cards == 3:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(2+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,3))) 
        if num_shown_cards >= 4:
            button = InvisibleButton()
            if num_shown_cards == 4:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(3+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,4))) 
        if num_shown_cards >= 5:
            button = InvisibleButton()
            if num_shown_cards == 5:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(4+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,5))) 
        if num_shown_cards >= 6:
            button = InvisibleButton()
            if num_shown_cards == 6:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(5+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,6))) 
        if num_shown_cards >= 7:
            button = InvisibleButton()
            if num_shown_cards == 7:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(6+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,7))) 
        if num_shown_cards >= 8:
            button = InvisibleButton()
            if num_shown_cards == 8:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(7+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,8))) 
        if num_shown_cards >= 9:
            button = InvisibleButton()
            if num_shown_cards == 9:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(8+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,9))) 
        if num_shown_cards >= 10:
            button = InvisibleButton()
            if num_shown_cards == 10:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(9+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,10))) 
        if num_shown_cards >= 11:
            button = InvisibleButton()
            if num_shown_cards == 11:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(10+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,11))) 
        if num_shown_cards >= 12:
            button = InvisibleButton()
            if num_shown_cards == 12:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(11+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,12)))
        if num_shown_cards >= 13:
            button = InvisibleButton()
            if num_shown_cards == 13:
                button.setFixedSize(106,150)
            else:
                button.setFixedSize(106,25)
            button.setParent(button_cell)
            button.move(0,25*(12+num_hidden_cards))
            button.clicked.connect(lambda: self.buttonPress(lambda: self.lanePress(7,13)))  
        self.game_window.placeButton(button_cell,2,6)

        extra_buttons_cell = QWidget()
        extra_buttons_cell.setFixedSize(100,245)

        #return button
        return_button = QPushButton()
        return_button.setFixedSize(100,100)
        return_button.setText("Return")
        if self.card_in_hand[0] != [None]:
            return_button.setStyleSheet("background-color: blue;")
            return_button.clicked.connect(lambda: self.buttonPress(self.ReturnCard))
        else:
            return_button.setStyleSheet("background-color: grey")
        return_button.setParent(extra_buttons_cell)
        return_button.move(0,145)

        #give up button
        giveup_button = QPushButton()
        giveup_button.setFixedSize(100,100)
        giveup_button.setText("Give Up")
        if self.checkIfGivingUp() == True:
            giveup_button.setStyleSheet("background-color: grey;")
        else:
            giveup_button.setStyleSheet("background-color: red;")
        giveup_button.clicked.connect(lambda: self.buttonPress(self.CheckGiveUp))
        giveup_button.setParent(extra_buttons_cell)
        giveup_button.move(0,35)

        #confirm give up button
        if self.checkIfGivingUp():
            confirm_giveup_button = QPushButton()
            confirm_giveup_button.setFixedSize(100,25)
            confirm_giveup_button.setText("Confirm Give Up")
            confirm_giveup_button.setStyleSheet("background-color: red;")
            confirm_giveup_button.clicked.connect(lambda: self.buttonPress(self.game_window.getMenuFun()))
            confirm_giveup_button.setParent(extra_buttons_cell)

        self.game_window.replaceCard(2,8,extra_buttons_cell)

        
 
ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"] #conversion from integer rank into string

class GameWindow(QMainWindow):
    def __init__(self, menu_fun,start_fun):
        super().__init__()
        self.menu_fun = menu_fun #function to call when the game ends
        self.start_fun = start_fun #function to call when user chooses to play again

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

        pack = Shuffle(GeneratePack().tolist())
        game_state = GameStateGUI(pack, datetime.now(), self)
            
    def getMenuFun(self):
        return self.menu_fun

    def EndGame(self,time):
        self.game_won_screen = GameWon(time,self.menu_fun,self.start_fun) #produces a screen that tells the user they've won
        self.hide()
        self.game_won_screen.show()

    def replaceCard(self,row_num,col_num,new,row_span=1,col_span=1): #making row span and col span optional, set to 1 initially but can be changed, allowing elements that span more than one cell in the grid
        for i in range(row_span):
            for j in range(col_span): #for loops are necessary for items that take up multiple cells in the grid
                item = self.layout.itemAtPosition(row_num+i,col_num+j)
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

    def createButton(self,fun,row_num,col_num,row_span=1,col_span=1,width=106,height=150): #by default should be size of a card
        button = InvisibleButton()
        button.setFixedSize(width,height)
        button.clicked.connect(fun) #using lambda allows parameter passing
        self.placeButton(button,row_num,col_num,row_span,col_span)

    def placeButton(self,button,row_num,col_num,row_span=1,col_span=1): 
        self.layout.addWidget(button,row_num,col_num,row_span,col_span)

def GeneratePack(): #cannot use SolitaireCLI's Generate Method as that uses Card not CardGUI
    pack = np.empty(52, dtype = object)
    for i in range(4):
        for j in range(13):
            pack[13*i + j] = CardGUI(i, j)
    return pack