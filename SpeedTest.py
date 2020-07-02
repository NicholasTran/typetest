import time
import pygame
from pygame.locals import *
import random
import sys

WHITE=(255,255,255)
BGCOLOR = (20, 20, 19)
TEXTBOXCOLOR = (38, 37, 36)
INPUTCOLOR= (133, 133, 133)

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
FPS = 60

class gameContainers:
    def __init__(self):
        self.bankline1 = ''
        self.bankline2 = ''
        self.bankline3 = ''
        self.bankline4 = ''
        self.masterbank = []
        self.input_text=[]
        self.input_word=''
        self.wpm = 0
        self.accuracy = 0
        self.totalWords = 0
        self.missedWords = 0
        self.correctWords = 0
        self.currentWord = ''
        self.totalCharacters = 0

def initialize():
    screen.fill(BGCOLOR)  # Fill the screen with background color.
    screen.fill(TEXTBOXCOLOR, (20, 50, 1040, 200)) #textbox
    screen.fill(INPUTCOLOR, (20, 275, 670, 50)) #user input box
    screen.fill(TEXTBOXCOLOR, (715, 275, 160, 50)) #Time box
    screen.fill(TEXTBOXCOLOR, (900, 275, 160, 50)) #Reset box
    pygame.display.update()


def reset_params(currentState):
        currentState.bankline1 = ''
        currentState.bankline2 = ''
        currentState.bankline3 = ''
        currentState.bankline4 = ''
        currentState.input_text=[]
        currentState.input_word=''
        currentState.wpm = 0
        currentState.accuracy = 0
        currentState.totalWords = 0
        currentState.missedWords = 0
        currentState.correctWords = 0
        currentState.currentWord = ''
        currentState.totalCharacters=0

        #grab random words from txt file and add to
        f = open('wordbank.txt').read().splitlines()
        for x in range(10):
            x = random.choice(f)
            currentState.bankline1 = currentState.bankline1 + x + '  '
            x = random.choice(f)
            currentState.bankline2 = currentState.bankline2 + x + '  '
            x = random.choice(f)
            currentState.bankline3 = currentState.bankline3 + x + '  '
            x = random.choice(f)
            currentState.bankline4 = currentState.bankline4 + x + '  '

        #Populate master bank
        currentState.masterbank = currentState.bankline1.split() + currentState.bankline2.split() + currentState.bankline3.split() + currentState.bankline4.split()
        #clear textbox
        screen.fill(TEXTBOXCOLOR, (20, 50, 1040, 200)) #textbox
        pygame.display.update()
        


initialize()
user = gameContainers()
font = pygame.font.SysFont(None, 40)
inputtext = font.render(user.input_word, True, WHITE)

inputbox = inputtext.get_rect()
inputbox.topleft = (25, 285)
cursor = Rect(inputbox.topright, (3, inputbox.height))

bank1 = font.render(user.bankline1, True, WHITE)
bankbox1 = bank1.get_rect()
bankbox1.topleft = (30,75)

bank2 = font.render(user.bankline2, True, WHITE)
bankbox2 = bank2.get_rect()
bankbox2.topleft = (30,115)

bank3 = font.render(user.bankline3, True, WHITE)
bankbox3 = bank3.get_rect()
bankbox3.topleft = (30,155)

bank4 = font.render(user.bankline4, True, WHITE)
bankbox4 = bank4.get_rect()
bankbox4.topleft = (30,195)

resettext = font.render('RESET', True, WHITE)
resetbox = resettext.get_rect()
resetbox.topleft = (920, 290)
screen.blit(resettext, resetbox)

#Game Loop
running = True
while running:
    start = False
    reset_params(user)
    inputtext = font.render(user.input_word, True, WHITE)
    screen.blit(inputtext, inputbox)
    #Draw text that user has to input
    bank1 = font.render(user.bankline1, True, WHITE)
    screen.blit(bank1, bankbox1)
    bank2 = font.render(user.bankline2, True, WHITE)
    screen.blit(bank2, bankbox2)
    bank2 = font.render(user.bankline2, True, WHITE)
    screen.blit(bank2, bankbox2)
    bank3 = font.render(user.bankline3, True, WHITE)
    screen.blit(bank3, bankbox3)
    bank4 = font.render(user.bankline4, True, WHITE)
    screen.blit(bank4, bankbox4)
    screen.fill(BGCOLOR, (300, 340, 480, 375)) #textbox
    pygame.display.update()
    

    #Idle Loop Until user enters something
    while (start==False):
        #Draw flashing cursor
        screen.fill(INPUTCOLOR, (20, 275, 670, 50)) #user input boxx
        screen.blit(inputtext, inputbox)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, WHITE, cursor)
        screen.fill(TEXTBOXCOLOR, (730, 275, 140, 50)) #Time box
        timetext = font.render(str(60), True, WHITE)
        timebox = timetext.get_rect()
        timebox.topleft = (750, 290)
        screen.blit(timetext, timebox)
        pygame.display.update()

        #Check for keyboard input to start
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                
            if event.type == KEYDOWN:
                if (event.key != K_SPACE) and (event.key != K_ESCAPE) and (event.key != K_RETURN) and (event.key != K_TAB):
                    user.input_word += event.unicode
                    start = True


    startTime = time.perf_counter()
    redo = False
    #Timer Has started, continue looping until timer runs out
    while (time.perf_counter() - startTime <= 60):
        #Draw Time
        screen.fill(TEXTBOXCOLOR, (730, 275, 140, 50)) #Time box
        timetext = font.render(str(int(60 - (time.perf_counter() - startTime))), True, WHITE)
        timebox = timetext.get_rect()
        timebox.topleft = (750, 290)
        screen.blit(timetext, timebox)
        pygame.display.update()
        
        
        if (redo == True):
            # Clear user input box
            inputtext = font.render(user.input_word, True, WHITE)
            inputbox.size=inputtext.get_size()
            screen.fill(INPUTCOLOR, (20, 275, 670, 50)) #user input box

            user.input_word = ''
            inputtext = font.render(user.input_word, True, WHITE)
            inputbox.size=inputtext.get_size()
            cursor.topleft = inputbox.topright

            screen.fill(INPUTCOLOR, (20, 275, 670, 50)) #user input boxx
            screen.blit(inputtext, inputbox)
            if time.time() % 1 > 0.5:
                pygame.draw.rect(screen, WHITE, cursor)
            
            screen.blit(inputtext, inputbox)
            pygame.display.update()
            reset_params(user)
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            #On Keyboard Press
            if event.type == KEYDOWN and event.key != K_RETURN:
                if event.key == K_BACKSPACE:
                    if len(user.input_word)>0:
                        user.input_word = user.input_word[:-1]
                elif event.key == K_SPACE:
                    user.input_word.strip()
                    if (user.input_word.strip() == ''):
                        continue
                    else:
                        user.input_text.append(user.input_word)
                        user.totalWords += 1
                        user.input_word=''
                    #Check if reached end of line
                    if (user.totalWords % 10 == 0):
                        user.bankline1 = user.bankline2
                        user.bankline2 = user.bankline3
                        user.bankline3 = user.bankline4
                        user.bankline4=''
                        f = open('wordbank.txt').read().splitlines()
                        for x in range(10):
                            x = random.choice(f)
 
                            user.bankline4 = user.bankline4 + x + '  '
                            user.masterbank.append(x)
                        screen.fill(TEXTBOXCOLOR, (20, 50, 1040, 200)) #textbox
                        bank1 = font.render(user.bankline1, True, WHITE)
                        screen.blit(bank1, bankbox1)
                        bank2 = font.render(user.bankline2, True, WHITE)
                        screen.blit(bank2, bankbox2)
                        bank2 = font.render(user.bankline2, True, WHITE)
                        screen.blit(bank2, bankbox2)
                        bank3 = font.render(user.bankline3, True, WHITE)
                        screen.blit(bank3, bankbox3)
                        bank4 = font.render(user.bankline4, True, WHITE)
                        screen.blit(bank4, bankbox4)
                        pygame.display.update()

                elif event.key == K_ESCAPE:
                    start = False
                    redo = True
                    reset_params(user)
                    break
        
                else:
                    user.input_word += event.unicode

            #on Mouse Press
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                #Seeing if within reset box bounds
                if (x >= 900 and x <= 1060 and y >=275 and y <= 325):
                    start = False
                    redo = True
                    reset_params(user)
                    break

            #Draw Text that user is inputting
            inputtext = font.render(user.input_word, True, WHITE)
            inputbox.size=inputtext.get_size()
            cursor.topleft = inputbox.topright

        screen.fill(INPUTCOLOR, (20, 275, 670, 50)) #user input boxx
        screen.blit(inputtext, inputbox)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, WHITE, cursor)
        pygame.display.update()

    #Game is now over, time to calculate score
    for w in user.input_text:
        user.totalCharacters += len(w)
        user.totalCharacters += 1
        if w.lower() in user.masterbank:
            user.correctWords += 1
        else:
            user.missedWords +=1

    if redo ==True:
        continue
    if user.totalWords == 0:
        user.wpm = 0
        user.accuracy = 0
    else:
        user.accuracy = (user.correctWords * 100) / user.totalWords
        user.wpm = round((user.totalCharacters/5) - user.missedWords)


    #Printing out results
    screen.fill(TEXTBOXCOLOR, (300, 340, 480, 230)) #textbox
    scoretext = font.render("WPM: {0}".format(user.wpm), True, WHITE)
    scorebox = scoretext.get_rect(center = (540, 400))
    screen.blit(scoretext, scorebox)
    scoretext = font.render("Total Characters {0}".format(user.totalCharacters), True, WHITE)
    scorebox = scoretext.get_rect(center = (540, 440))
    screen.blit(scoretext, scorebox)
    scoretext = font.render("Missed Words: {0}".format(user.missedWords), True, WHITE)
    scorebox = scoretext.get_rect(center = (540, 480))
    screen.blit(scoretext, scorebox)
    scoretext = font.render("Accuracy: {0}%".format(int(user.accuracy)), True, WHITE)
    scorebox = scoretext.get_rect(center = (540, 520))
    screen.blit(scoretext, scorebox)
    pygame.display.update()

    restart = False
    while restart == False:
         for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            #on Mouse Press
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                #Seeing if within reset box bounds
                if (x >= 900 and x <= 1060 and y >=275 and y <= 325):
                    start = False
                    restart = True
                    reset_params(user)
                    break
        
    
