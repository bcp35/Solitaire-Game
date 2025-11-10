import numpy as np
import random

class Card:
    def __init__(self, suit_int, rank_int):
        self.suit = suits[suit_int]
        self.rank_int = rank_int + 1
        self.rank_string = ranks[rank_int]
        self.rank_fullname = ranks_fullname[rank_int]
        self.colour = colours[suit_int // 2]
    def getSuit(self):
        return self.suit
    def getRank(self):
        return self.rank_int
    def getColour(self):
        return self.colour
    def getDisplayName(self):
        return self.suit[0] + self.rank_string
    def getFullName(self):
        return self.rank_fullname + " of " + self.suit

class Stack:
    def __init__(self, suit_int):
        self.suit_int = suit_int
        self.suit = suits[suit_int]
        self.top_rank = 0
    def isEmpty(self):
        return self.top_rank == 0
    def isFull(self):
        return self.top_rank == 13
    def push(self, card): #puts this card on the top of the stack (if legal)
        if not self.isFull():
            if card.getSuit() == self.suit:
                if card.getRank() == self.top_rank + 1:
                    self.top_rank += 1
                    return True
        return False
    def pop(self): #removes and returns the card at the top of the stack (if there is one)
        if self.isEmpty():
            return None
        self.top_rank -= 1
        return Card(self.suit_int, self.top_rank - 1)
    def getDisplay(self):
        if self.top_rank == 0:
            return "[]"
        return self.suit[0] + self.top_rank

class Lane:
    def __init__(self, cards):
        self.hidden_cards = cards[:-1]
        self.top_card = cards[-1]
        self.shown_cards = [self.top_card]
    def isEmpty(self):
        return len(self.shown_cards) == 0
    def push(self, card): #puts this card on the lane (if legal)
        if card.getColour() != self.top_card.getColour():
            if card.getRank() == self.top_card.getRank() - 1:
                self.shown_cards.append(card)
                self.top_card = card
                return True
        return False
    def pop(self): #gets the top card in the lane
        if self.isEmpty():
            return None
        card = self.shown_cards.pop()
        if len(self.shown_cards) == 0: #there was only one card shown - so one needs to be moved from hidden
            self.top_card = self.hidden_cards.pop()
            self.shown_cards = [self.top_card]
        else:
            self.top_card = self.shown_cards[-1]
        return card
    def getDisplay(self):
        display = "["
        for c in self.hidden_cards:
            display += "*,"
        for c in self.shown_cards:
            display += c.getDisplayName() + ","
        return display[:-1] + "]" #gets rid of last character (comma) and adds closing square bracket
        

class Deck:
    def __init__(self, pile):
        self.stock_pile = pile #the first element indicates the top of the pile
        self.waste_pile = [] #last element indicates the retrievable card
    def getNextThree(self): #gives the top 3 cards in the waste pile
        return self.waste_pile[-3:]
    def next(self): #moves (at most) 3 cards from stock pile to waste pile
        self.waste_pile.extend(self.stock_pile[:3])
    def reset(self): #moves all cards from the waste pile back to the stock pile
        self.stock_pile = self.waste_pile + self.stock_pile
    def pop(self): #returns and removes the top card from the waste pile
        card = self.waste_pile.pop()
        return card
    def getDisplay(self):
        return f"({len(self.stock_pile)}) {self.getNextThree()}"
        
class GameState:
    def __init__(self, pack):
        self.lanes = np.empty(7, dtype = object)
        self.distributeLanes(pack[0:28])
        self.deck = Deck(pack[28:])
        self.stacks = [Stack(i) for i in range(4)]
    def distributeLanes(self,cards):
        start = 0
        for i in range(1,8):
            self.lanes[i-1] = Lane(cards[start:start+i])
            start += i
    def getDisplay(self):
        display = "Deck: " + self.deck.getDisplay() + " - Stacks: "
        for stack in self.stacks:
            display += stack.getDisplay() + " "
        display += "\nLanes: "
        for lane in self.lanes:
            display += lane.getDisplay() + " "
        return display


suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
ranks_fullname = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
colours = ["Red", "Black"]

def MainMenu():
    print("Welcome to Solitare!")
    print("Enter the number of the option you'd like to select:")
    print(" 1. Start Game")
    print(" 2. Instructions")
    print(" 3. Exit")
    x = int(input("Enter a number: "))
    if x == 1:
        GameSetup()
    elif x == 2:
        Instructions()
    elif x == 3:
        exit()

def Instructions():
    print("How to play Solitare:")
    print("At each turn, the current state will look like this: ")
    x=10
    print(f"Deck: ({x}) [H3,DJ,S10]")
    print(f"Stacks: [H2] [D3] [] [SA]")
    print(f"Lanes: [HJ,C10] [DK] [*,*,D5] [*,*,*,SK] [*,*,*,*,C9] [*,*,*,D4,S3,D2,CA] [*,*,*,*,S7,H6]")

    print("\nThe deck shows the cards that you have left to use, displaying them 3 at a time, only able to use the right-most of the three, and gaining access to the other cards after using them.")
    print("The aim of the game is to add cards of the same suit from Ace to King in each stack in the correct order.")
    print("Each lane contains a stack of cards from high to low of alternating colours. Cards can move between lanes, but only if it is one rank below the card above it. Moving a card to another lane reveals the card that was above it. Only Kings can move to empty lanes.")

    print("\n For each go you have the option to access the next card in the deck, or the bottom card from each lane, and move it to the corresponding stack for that rank or another lane, if that is a legal move.")

    print(" 1. Start Game")
    print(" 2. Main Menu")
    x = int(input("Enter a number: "))
    if x == 1:
        GameSetup()
    elif x == 2:
        MainMenu()

def GeneratePack():
    pack = np.empty(52, dtype = object)
    for i in range(4):
        for j in range(13):
            pack[13*i + j] = Card(i, j)
    return pack

def Shuffle(deck):
    for j in range(3): #shuffling 3 times
        for i in range(len(deck)):
            n = random.randint(i,len(deck)-1)
            temp = deck[i]
            deck[i] = deck[n]
            deck[n] = temp
    return deck

def GameSetup():
    pack = GeneratePack()
    print("Shuffling pack...")
    pack = Shuffle(pack)
    print("Dealing cards...")
    game_state = GameState(pack.tolist()) #pack needs to be a list not array so that length can change

MainMenu()
