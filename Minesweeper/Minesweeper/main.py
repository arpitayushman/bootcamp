import sys
from game import Game

def main():
    size = 0,0
    string = input("Please enter the difficulty level: \n B: for Beginner \n I: for Intermediate \n E: for Expert \n")
    if string == 'B':
        size = 9,9
    elif string == 'I':
        size = 16,16
    elif string == 'E':
        size = 30,16
    else:
        print("Enter Valid Character")
        return
    prob = 0.15
    g = Game(size, prob)
    g.run()

if __name__ == '__main__':
    main()