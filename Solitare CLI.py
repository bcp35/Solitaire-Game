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
    
def GameSetup():
    print("Shuffling deck...")

def Instructions():
    print("How to play Solitare:")


MainMenu()
