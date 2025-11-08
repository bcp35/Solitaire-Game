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
