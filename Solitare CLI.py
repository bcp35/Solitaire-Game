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
    print(f"Deck: [{x}]. Next Cards: [H3,DJ,S10]")
    print(f"Stacks: [H2] [D3] [] [SA]")
    print(f"Lanes: [HJ] [*,D4] [*,*,D5] [*,*,*,SK] [*,*,*,*,C9] [*,*,*,*,*,CA] [*,*,*,*,*,*,H6]")

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
    for i in range(len(deck)):
        n = random.randint(i,len(deck)-1)
        temp = deck[i]
        deck[i] = deck[n]
        deck[n] = temp
    return deck

def GameSetup():
    pack = GeneratePack()
    print("Shuffling deck...")
    pack = Shuffle(pack)


MainMenu()
