import random
import pygame
from pygame.locals import *

pygame.init()
FPS = 20
screen_width=600
screen_height=600
FramePerSec = pygame.time.Clock()
font=pygame.font.SysFont(None,60)
displaysurf = pygame.display.set_mode((screen_width, screen_height)) #размерите на полето
pygame.display.set_caption("Dots Game")

black=(0,0,0)
blue=(59,117,235)
red=(236,59,59)
#brown=(107,19,19)
f = (238, 224, 197)

currPlayer='X'
currColor=blue
squareX=0
squareY=0

def draw_grid():
    for x in range(100,screen_width-100,50):
        for y in range(100,screen_width-100,50):
           pygame.draw.circle(displaysurf,black,(x,y),5)

def isFreeLine(currLine,lines):

    for line in lines:
        if (line[0]==currLine[0] and line[1]==currLine[1]) or (line[0]==currLine[1] and line[1]==currLine[0]):
            return False
    return True

def isValidLine(currLine):
    dx = abs(currLine[0][0] - currLine[1][0])
    dy = abs(currLine[0][1] - currLine[1][1])
    if (dx == 50 and dy == 0) or (dx == 0 and dy == 50):
        return True
    return False

def checkForSquare(lines):
    new_squares = []
    for x in range(100, screen_width - 150, 50):
        for y in range(100, screen_width - 150, 50):
            top = ((x, y), (x + 50, y))
            right = ((x + 50, y), (x + 50, y + 50))
            bottom = ((x, y + 50), (x + 50, y + 50))
            left = ((x, y), (x, y + 50))
            # проверяваме дали всяка от 4-те линии съществува в списъка (в двете посоки)
            sides = [top, right, bottom, left]
            squareComplete = all(
                side in [(l[0], l[1]) for l in lines] or side[::-1] in [(l[0], l[1]) for l in lines]
                for side in sides
            )
            if squareComplete and (x, y) not in [sq[0] for sq in square]:
                new_squares.append((x, y))
    return new_squares

def checkForWinner():
    global squareX
    global squareY
    global allSquares
    if squareX+squareY==allSquares:
       return True
    return False

def draw_XO(square_list):
    for square_info in square_list:
        pos, letter, color = square_info
        text = font.render(letter, True, color)
        displaysurf.blit(text, (pos[0] + 15, pos[1] + 5))

def switchPlayer():
    global currPlayer
    global currColor
    if currPlayer=='X':
        currPlayer='O'
        currColor=red
    else:
        currPlayer='X'
        currColor=blue


running = True
start=None
end=None
lines=[]
square=[]
allSquares=pow(((screen_width-200)/50)-1,2)

while running:
    displaysurf.fill(f)  # фона отзад
    draw_grid()  # линиите на полето за игра
    text = font.render(f"X:{squareX}", True, black)
    displaysurf.blit(text, (100, 30))
    text = font.render(f"Y:{squareY}", True, black)
    displaysurf.blit(text, (200, 30))
    draw_XO(square)
    for line in lines:
        pygame.draw.line(displaysurf,line[2],line[0],line[1],3)
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()

            for x in range(100, screen_width - 100, 50):
                for y in range(100, screen_width - 100, 50):
                    if abs(pos[0] - x) <= 10 and abs(pos[1] - y) <= 10:
                        if start==None:
                            start=(x,y)
                        elif end==None:
                            end=(x,y)

            if start!=None and end!=None and start!=end:
                if isFreeLine((start,end,currColor),lines) and isValidLine((start,end,currColor)):
                    lines.append((start,end,currColor))
                    new_squares = checkForSquare(lines)

                    if new_squares:
                        for s in new_squares:
                            if currPlayer == 'X':
                                squareX += 1
                            else:
                                squareY += 1
                            square.append((s, currPlayer, currColor))
                        if checkForWinner():
                            if squareX>squareY:
                                    text=font.render("Победител е Х!",True,red)

                            elif squareX<squareY:
                                    text=font.render("Победител е Y!",True,red)

                            else:
                                    text = font.render("Равенство!", True, red)


                            draw_grid()
                            draw_XO(square)
                            for line in lines:
                                pygame.draw.line(displaysurf, line[2], line[0], line[1], 3)
                            displaysurf.blit(text, (100, 520))
                            pygame.display.update()
                            pygame.time.delay(3000)
                            running = False
                    else:
                        switchPlayer()
                    start = None
                    end = None
                else:
                    start = None
                    end = None

        if event.type == QUIT: #ако натисне Х
            running = False
    pygame.display.update()  # опресняваме екрана
    FramePerSec.tick(FPS)
pygame.quit()