import numpy as np
import random

class Card:
    def __init__(self, suit_int, rank_int):
        self.suit = suits[suit_int]
        self.suit_int = suit_int
        self.rank_int = rank_int + 1
        self.rank_string = ranks[rank_int]
        self.rank_fullname = ranks_fullname[rank_int]
        self.colour = colours[suit_int // 2]
    def getSuit(self):
        return self.suit
    def getSuitInt(self):
        return self.suit_int
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
    def peek(self): #returns top card without removing
        if self.isEmpty():
            return None
        return Card(self.suit_int, self.top_rank - 1)
    def pop(self): #removes and returns the card at the top of the stack (if there is one)
        if self.isEmpty():
            return None
        self.top_rank -= 1
        return Card(self.suit_int, self.top_rank - 1)
    def getSuitInt(self):
        return self.suit_int
    def getDisplay(self):
        if self.top_rank == 0:
            return "[]"
        return self.suit[0] + ranks[self.top_rank-1]

class Lane:
    def __init__(self, cards,i):
        self.hidden_cards = cards[:-1]
        self.top_card = cards[-1]
        self.shown_cards = [self.top_card]
        self.num = i
    def isEmpty(self):
        return len(self.shown_cards) == 0
    def push(self, card): #puts this card on the lane (if legal)
        if self.top_card == None:
            if card.getRank() == 13:
                self.shown_cards.append(card)
                self.top_card = card
                return True
            return False
        if card.getColour() != self.top_card.getColour():
            if card.getRank() == self.top_card.getRank() - 1:
                self.shown_cards.append(card)
                self.top_card = card
                return True
        return False
    def peek(self): #returns top card without removing
        if self.isEmpty():
            return None
        return self.top_card
    def pop(self): #returns and removes the top card in the lane
        if self.isEmpty():
            return None
        card = self.shown_cards.pop()
        if len(self.shown_cards) == 0: #there was only one card shown - so one needs to be moved from hidden
            if len(self.hidden_cards) == 0:
                self.top_card = None
            else:
                self.top_card = self.hidden_cards.pop()
                self.shown_cards = [self.top_card]
        else:
            self.top_card = self.shown_cards[-1]
        return card
    def getNum(self):
        return self.num
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
        to_get = len(self.stock_pile)
        if to_get > 3:
            to_get = 3
        for i in range(to_get):
            self.waste_pile.append(self.stock_pile.pop())
    def reset(self): #moves all cards from the waste pile back to the stock pile
        self.stock_pile = self.waste_pile + self.stock_pile
        self.waste_pile = []
    def peek(self): #returns top card without removing
        if(len(self.waste_pile) == 0):
            return None
        card = self.waste_pile[-1]
        return card
    def pop(self): #returns and removes the top card from the waste pile
        if(len(self.waste_pile) == 0):
            return None
        card = self.waste_pile.pop()
        return card
    def getDisplay(self):
        return f"({len(self.stock_pile)}) {[c.getDisplayName() for c in self.getNextThree()]}"
        
class GameState:
    def __init__(self, pack):
        self.lanes = np.empty(7, dtype = object)
        self.distributeLanes(pack[0:28])
        self.deck = Deck(pack[28:])
        self.stacks = [Stack(i) for i in range(4)]
        self.card_in_hand = (None, 0) #int represents where the card came from so it can be returned: 1 means deck, 2-5 means stacks, 6-12 means lanes 
    def pickUpCard(self,card, last_loc): #sets the card in hand variable
        self.card_in_hand = (card, last_loc)
    def putDownCard(self):
        self.card_in_hand = (None, 0)
    def getCardInHand(self):
        return self.card_in_hand
    def distributeLanes(self,cards):
        start = 0
        for i in range(1,8):
            self.lanes[i-1] = Lane(cards[start:start+i],i)
            start += i
    def getDisplay(self):
        display = "Deck: " + self.deck.getDisplay() + " - Stacks: "
        for stack in self.stacks:
            display += stack.getDisplay() + " "
        display += "\nLanes: "
        i = 0
        for lane in self.lanes:
            i += 1
            display += f"{i}" + lane.getDisplay() + ", "
        if self.card_in_hand[0] != None:
            display += f"\nHeld Card: {self.card_in_hand[0].getDisplayName()}"
        return display
    def getDeck(self):
        return self.deck
    def getLane(self,i):
        return self.lanes[i]
    def getStack(self,i):
        return self.stacks[i]
    def updateDeck(self, deck):
        self.deck = deck
    def updateLane(self, lane):
        self.lanes[lane.getNum()] = lane
    def updateStack(self, stack):
        self.stacks[stack.getSuitInt] = stack
    

#Main
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
ranks_fullname = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
colours = ["Red", "Black"]

def MainMenu():
    print("Welcome to Solitare!")
    x = CheckOptions("Enter the number of the option you'd like to select:",["Start Game", "Instructions", "Exit"])
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

    x = CheckOptions("Select an option:",["Start Game", "Main Menu"])
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

def CheckOptions(text, options):
    valid = False
    while not valid:
        print(text)
        for i in range(len(options)):
            print(f"{i+1}: {options[i]}")
        inp = input(">>")
        if not inp.isdigit():
            print("Please enter a valid integer.")
        elif int(inp) < 1 or int(inp) > len(options):
            print("Please enter a number in the specified range")
        else:
            valid = True
            return int(inp)

def PickUpCard(game_state):
    x = CheckOptions("Select an option:", ["Deck","Stacks","Lanes","Give Up"])
    if x == 1:
        return TakeFromDeck(game_state)
    if x == 2:
        return TakeFromStacks(game_state)
    if x == 3:
        return TakeFromLanes(game_state)
    else:
        return CheckGiveUp(game_state)

def CheckGiveUp(game_state):
    x = CheckOptions("Are you sure you want to give up?", ["Yes", "No"])
    if x == 1:
        MainMenu()
    else:
        return PlayGame(game_state)

def PutDownCard(game_state):
    x = CheckOptions("Select an option:", ["Return Card","Stacks","Lanes","Give Up"])
    if x == 1:
        return ReturnCard(game_state)
    if x == 2:
        return PutOnStacks(game_state)
    if x == 3:
        return PutOnLanes(game_state)
    else:
        return CheckGiveUp(game_state)

def GameSetup():
    pack = GeneratePack()
    print("Shuffling pack...")
    pack = Shuffle(pack)
    print("Dealing cards...")
    game_state = GameState(pack.tolist()) #pack needs to be a list not array so that length can change
    game_state = PlayGame(game_state)

def PlayGame(game_state):
    print(game_state.getDisplay())
    if game_state.getCardInHand()[0] == None:
        game_state = PickUpCard(game_state)
    else:
        game_state = PutDownCard(game_state)
    PlayGame(game_state)

def TakeFromDeck(game_state):
    deck = game_state.getDeck()
    x = CheckOptions("Select an option:", ["Take from waste pile", "Draw cards from stock pile", "Return all cards to stock pile", "Back"])
    if x == 1: #new card in hand is card at top of waste pile
        card = deck.peek()
        if card == None:
            print("Cannot pick up from an empty waste pile.")
            return game_state
        game_state.pickUpCard(card,1)
    elif x == 2: #move three cards from the stock pile to the waste piie
        deck.next() 
        game_state.updateDeck(deck)
    elif x == 3: #move all cards from the waste pile to the stock pile
        deck.reset()
        game_state.updateDeck(deck)
    return game_state
        
def TakeFromStacks(game_state):
    x = CheckOptions("Select an Option:", ["Take from Hearts stack","Take from Diamonds stack","Take from Clubs stack","Take from Spades stack", "Back"])
    if x in range(1,5): #Option 1-4 correspond to a stack
        stack = game_state.getStack(x-1)
        card = stack.peek()
        if card == None:
            print("Cannot pick up from an empty stack.")
            return game_state
        game_state.pickUpCard(card,x+1) #new card is now being held
        return game_state
    return game_state

def TakeFromLanes(game_state):
    x = CheckOptions("Select an Option", ([f"Take from Lane {i}" for i in range(1,8)] + ["Back"]))
    if x in range(1,8): #Option 1-7 correspond to a lane
        lane = game_state.getLane(x-1)
        card = lane.peek()
        if card == None:
            print("Cannot pick up from an empty lane.")
            return game_state
        game_state.pickUpCard(card,x+5)
    return game_state

def ReturnCard(game_state):
    game_state.putDownCard()
    return game_state

def PutOnStacks(game_state):
    x = CheckOptions("Select an Option:", ["Add to stack", "Back"])
    if x == 1:
        card = game_state.getCardInHand()[0]
        stack = game_state.getStack(card.getSuitInt())
        b = stack.push(card)
        if b == True:
            game_state = RemoveCardFromLastLoc(game_state)
        else:
            print("Cannot place card onto this stack")
        return game_state
    return game_state

def PutOnLanes(game_state):
    x = CheckOptions("Select an Option", ([f"Add to Lane {i}" for i in range(1,8)] + ["Back"]))
    if x in range(1,8): #Option 1-7 correspond to a lane
        lane = game_state.getLane(x-1)
        b = lane.push(game_state.getCardInHand()[0])
        if b == True:
            game_state = RemoveCardFromLastLoc(game_state)
        else:
            print("Cannot place card onto this lane.")
        return game_state
    return game_state

def RemoveCardFromLastLoc(game_state):
    card, last_loc = game_state.getCardInHand()
    if last_loc == 1:
        game_state.getDeck().pop()
    elif last_loc in range(2,6):
        game_state.getStack(last_loc-2).pop()
    elif last_loc in range(6,13):
        game_state.getLane(last_loc-6).pop()
    game_state.putDownCard()
    return game_state

MainMenu()
