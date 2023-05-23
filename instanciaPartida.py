import pygame
import numpy as np
import random
import sys
import time

class Partida:

    pygame.init()
    pygame.font.init()

    # Define the game variables
    game_over = 0
    game_won = 0
    current_score = 0
    best_score = 0
    matrix = np.array([[0 for x in range(4)] for y in range(4)]) 
    
    # TODO Crear variables up, down, left, right to know faster if a move can be done


    # TODO Encapsular las variables de pygame en una funcion para que no sea necesario crearlas a menos que se vaya a jugar en la ventana
    # tambien cambiar el init para que solo se cree la ventana cuando se vaya a jugar

    # Define screen
    screen_width = 500
    screen_height = 500 

    screen = pygame.display.set_mode((screen_width, screen_height))
    # Define the colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    

    

    # Define font 
    font = pygame.font.SysFont('Comic Sans MS', 30)
    def __init__(self):
        # Define the screen size
        
        # Create the display window
        
        pygame.display.set_caption('2048') # Set the name of the display window

        self.addNumber()

    # Create up down left right functions
    def up(self):
        change = False
        #moves to right
        for i in range(4):
            arre=[0,0,0,0]
            for j in range(4):
                arre[j]=self.matrix[i][j]
            #mixup tiles in descending order
            #arre.reverse()
            iter1=0
            iter2=1
            while(iter1<4 and iter2<4):
                while(iter1<4 and arre[iter1]==0):
                    iter1+=1
                    iter2+=1
                while(iter2<4 and arre[iter2]==0):
                    iter2+=1
                if iter1<4 and iter2<4:
                    if(arre[iter1]==arre[iter2]):
                        # Fix the line below
                        change += arre[iter2] * 2
                        self.current_score = self.current_score + change
                        self.best_score=max(self.current_score,self.best_score)
                        arre[iter1]*=2
                        change = True
                        arre[iter2]=0
                iter1+=1
                iter2+=1
            #moves 0 to de edge
            for k in range(4):
                for j in range(3):
                    if arre[j]==0 and arre[j+1]!=0:
                        arre[j]=arre[j+1]
                        arre[j+1]=0
            #verify changes
            #arre.reverse()
            for j in range(4):
                if arre[j]!=self.matrix[i][j]:
                    change = True 
                self.matrix[i][j]=arre[j]
        return change

    def down(self): 
        change = False
        #moves to right
        for i in range(4):
            arre=[0,0,0,0]
            for j in range(4):
                arre[j]=self.matrix[i][j]
            #mixup tiles in descending order
            arre.reverse()
            iter1=0
            iter2=1
            while(iter1<4 and iter2<4):
                while(iter1<4 and arre[iter1]==0):
                    iter1+=1
                    iter2+=1
                while(iter2<4 and arre[iter2]==0):
                    iter2+=1
                if iter1<4 and iter2<4:
                    if(arre[iter1]==arre[iter2]):
                        change += arre[iter2] * 2
                        self.current_score = self.current_score + change
                        best_score=max(self.current_score,self.best_score)
                        arre[iter1]*=2
                        change = True
                        arre[iter2]=0
                iter1+=1
                iter2+=1
            #moves 0 to de edge
            for k in range(4):
                for j in range(3):
                    if arre[j]==0 and arre[j+1]!=0:
                        arre[j]=arre[j+1]
                        arre[j+1]=0
            #verify changes
            arre.reverse()
            for j in range(4):
                if arre[j]!=self.matrix[i][j]:
                    change = True
                self.matrix[i][j]=arre[j]
        return change

    def left(self):
        change = False
        #moves to right
        for i in range(4):
            arre=[0,0,0,0]
            for j in range(4):
                arre[j]=self.matrix[j][i]
            #mixup tiles in descending order
            #arre.reverse()
            iter1=0
            iter2=1
            while(iter1<4 and iter2<4):
                while(iter1<4 and arre[iter1]==0):
                    iter1+=1
                    iter2+=1
                while(iter2<4 and arre[iter2]==0):
                    iter2+=1
                if iter1<4 and iter2<4:
                    if(arre[iter1]==arre[iter2]):
                        change += arre[iter2] * 2
                        self.current_score = self.current_score + change
                        best_score=max(self.current_score,self.best_score)
                        arre[iter1]*=2
                        change = True
                        arre[iter2]=0
                iter1+=1
                iter2+=1
            #moves 0 to de edge
            for k in range(4):
                for j in range(3):
                    if arre[j]==0 and arre[j+1]!=0:
                        arre[j]=arre[j+1]
                        arre[j+1]=0
            #verify changes
            #arre.reverse()
            for j in range(4):
                if arre[j]!=self.matrix[j][i]:
                    change = True
                self.matrix[j][i]=arre[j]
        return change
        
    def right(self):
        change = False
        #moves to right
        for i in range(4):
            arre=[0,0,0,0]
            for j in range(4):
                arre[j]=self.matrix[j][i]
            #mixup tiles in descending order
            arre.reverse()
            iter1=0
            iter2=1
            while(iter1<4 and iter2<4):
                while(iter1<4 and arre[iter1]==0):
                    iter1+=1
                    iter2+=1
                while(iter2<4 and arre[iter2]==0):
                    iter2+=1
                if iter1<4 and iter2<4:
                    if(arre[iter1]==arre[iter2]):
                        change += arre[iter2] * 2
                        self.current_score = self.current_score + change
                        self.best_score=max(self.current_score,self.best_score)
                        arre[iter1]*=2
                        change = True
                        arre[iter2]=0
                iter1+=1
                iter2+=1
            #moves 0 to de edge
            for k in range(4):
                for j in range(3):
                    if arre[j]==0 and arre[j+1]!=0:
                        arre[j]=arre[j+1]
                        arre[j+1]=0
            #verify changes
            arre.reverse()
            for j in range(4):
                if arre[j]!=self.matrix[j][i]:
                    change = True
                self.matrix[j][i]=arre[j]
        return change


    def addNumber(self):
        #Create a number with 90% probability of being 2 and 10% of being 4
        number = 2
        if random.random() < 0.1:
            number = 4
        ceros = 0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    ceros = ceros + 1
        bandera = True 
        if(ceros > 0):
            while bandera:
                i = random.randint(0, 3)
                j = random.randint(0, 3)
                if self.matrix[i][j] == 0:
                    self.matrix[i][j] = number
                    bandera = False

    def checkGameOver(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return False
        for i in range(4):
            for j in range(4):
                if i < 3 and self.matrix[i][j] == self.matrix[i+1][j]:
                    return False
                if j < 3 and self.matrix[i][j] == self.matrix[i][j+1]:
                    return False
        return True

    def show(self):
        # Make this window so that it only closes when i click the cross button
        running = True
        while running:

            # Fill the screen with white
            self.screen.fill(self.white)

            # Draw the grid leaving 20% on the bottom for the score
            for i in range(4):
                for j in range(4):
                    pygame.draw.rect(self.screen, self.gray, (i*100+50, j*100+5, 100, 100), 2)

            # Draw the numbers
            for i in range(4):
                for j in range(4):
                    if self.matrix[i][j] != 0:   
                        text = self.font.render(str(self.matrix[i][j]), True, self.black)
                        self.screen.blit(text, (i*100 + 100 - text.get_width()/2, j*100 + 55 - text.get_height()/2))

            # Draw the score
            text = self.font.render('Score: ' + str(self.current_score), True, self.black)
            self.screen.blit(text, (20, 520))

            # Draw the best score
            text = self.font.render('Best: ' + str(self.best_score), True, self.black)
            self.screen.blit(text, (400, 520))

            # Draw the game over text
            if self.game_over == 1:
                text = self.font.render('Game Over', True, self.red)
                self.screen.blit(text, (200, 250))

            # Draw the game won text
            if self.game_won == 1:
                text = self.font.render('Game Won', True, self.green)
                self.screen.blit(text, (200, 250))

            # TODO: New up do not return true but a number that indicates the puntuation so if self.up() > 0 then addNumber()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.play("up") 
                    if event.key == pygame.K_DOWN:
                        self.play("down")
                    if event.key == pygame.K_LEFT:
                        self.play("left")
                    if event.key == pygame.K_RIGHT:
                        self.play("right")

            #Add a button to restart the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 200 < event.pos[0] < 300 and 410 < event.pos[1] < 460:
                        matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                        current_score = 0
                        self.addNumber()
                        self.addNumber()
                        game_over = 0
                        game_won = 0
            # Create the above button 
            pygame.draw.rect(self.screen, self.green, (210, 410, 80, 50))
            text = self.font.render('New', True, self.black)
            self.screen.blit(text, (200 + 50 - text.get_width()/2, 410 + 25 - text.get_height()/2))
            # Write the current score
            text = self.font.render('Puntaje: ' + str(self.current_score), True, self.black)
            self.screen.blit(text, (25, 415))
            # Write the best score
            text = self.font.render('Mejor: ' + str(self.best_score), True, self.black)
            self.screen.blit(text, (325, 415))


            pygame.display.update()

    def play(self, jugada = ""):
        puntos = 0
        if jugada == "up":
            puntos = self.up()
        elif jugada == "down":
            puntos = self.down()
        elif jugada == "left":
            puntos = self.left()
        elif jugada == "right":
            puntos = self.right()
        if puntos > 0:  
            self.addNumber()
        return puntos
    
    def reset(self):
        matrix = np.array([[0 for x in range(4)] for y in range(4)])
        current_score = 0
        self.addNumber()
        self.addNumber()
        game_over = 0
        game_won = 0

aux = Partida().show()