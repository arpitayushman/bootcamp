from distutils.util import run_2to3
import pygame
from piece import Piece 
from board import Board 
import os
from time import sleep
import tkinter as tk
from tkinter import messagebox

class Game:
    '''initialize the Board in Game,Load pygame,screen Size,piece Size, solving the flags'''
    def __init__(self, size, prob):
        self.board = Board(size, prob)
        pygame.init()
        self.sizeScreen = 800, 800
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (self.sizeScreen[0] // size[1], self.sizeScreen[1] // size[0])
        self.loadPictures()


    '''loading pictures in pygame'''
    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName 
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img
            
    def run(self):
        '''running the game,dealing with events like mouse'''
        running = True
        while running:
            for event in pygame.event.get():
                '''if gamer quits '''
                if event.type == pygame.QUIT:
                    running = False
                '''if gamer opens block'''
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]  #if gamer rightclicks
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
            self.screen.fill((0,0,0))
            self.draw()
            pygame.display.flip() #updating the entire screen
            #if win#
            if self.board.getWon():
                self.win()
                running = False
            #if lose#
            if self.board.getLost():
                self.lost()
                running = False
        pygame.quit()   #quiting the game
        
    #drawing the cells on board
    def draw(self):
        topLeft = (0, 0)
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft) #printing the image'''
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        #getting the image string name
        if piece.getClicked(): #either number or bomb
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if (self.board.getLost()): #if lost
            if (piece.getHasBomb()): 
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block' #if flag not bomb else empty block
        return 'flag' if piece.getFlagged() else 'empty-block'

    def handleClick(self, position, flag):
        #sending the position to board where clicked
        index = tuple(int(pos // size) for pos, size in zip(position, self.pieceSize))[::-1] 
        self.board.handleClick(self.board.getPiece(index), flag)
    def win(self):
        #win - display
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        root = tk.Tk().withdraw()
        messagebox.showinfo('','Congrats!! YOU WON')
        sleep(3)
    def lost(self):
        #lost - display
        root = tk.Tk().withdraw()
        messagebox.showinfo('','OOPS!!! You Lost')