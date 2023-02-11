

import random
import sys
from winsound import PlaySound # We will use sys.exit to exit the program
import pygame
from  pygame.locals  import *





# Global variables for the game
FPS=32
SCREENWIDTH=600
SCREENHEIGHT=380
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
# FORMATTEDBG=pygame.Surface((SCREENWIDTH,SCREENHEIGHT))


GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='gallery\\fb11.png'
BACKGROUND='gallery\\bg11.jpg'
PIPE='gallery\\pipe1.png'
def welcomeScreen():
    '''Shows welcome images in the screen'''
    playerx=int(SCREENHEIGHT/4)
    playery=int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/1.1)
    messagex=int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.000000000000000001)
    # basex=0
    while True:
        for event in pygame.event.get():
            #when player presse cross button, close the button
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit

            #if the user presse space or up key, sart the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                    
                
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery)) 
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                # SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY)) 
                pygame.display.update() 
                FPSCLOCK.tick(FPS)          
def mainGame():
    score=0
    playerx=int(SCREENWIDTH/9)
    playery=int(SCREENHEIGHT/2)
    #create two pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    #my list of upper pipes
    upperPipes=[
        {'x':SCREENWIDTH+500,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+500+(SCREENWIDTH/2),'y':newPipe2[0]['y']}

    ]
     # my List of lower pipes
    lowerPipes= [
        {'x': SCREENWIDTH+0, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+0+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]
    pipeVelX=-5
    playervelY=-4
    playerMaxVelY=10
    playerMinvelY=-8
    playerAccY=10
    playerFlapAccv=-4 #velocity while flapping
    playerFlapped=False

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    # playervelY=playerFlapAccv
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
                    
            if event.type==KEYDOWN and (event.key==K_DOWN):
                if playery>0:
                    # playervelY=playerFlapAccv
                    playerFlapped=False
                    GAME_SOUNDS['wing'].play()
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes) 
            #This function returns true if the player crashes
        if crashTest:
                return
            #check for score
        playerMidpos=playerx+ (GAME_SPRITES['player'].get_width())/2 
        for pipe in upperPipes:
                pipeMidPos=pipe['x'] +GAME_SPRITES['pipe'][0].get_width()/2
                if pipeMidPos <= playerMidpos<pipeMidPos + 4:
                    score+=1
                    print(f"Your score is {score}")
                    GAME_SOUNDS['point'].play()
        if playervelY<playerMaxVelY and not playerFlapped:
             playervelY+=playerAccY
        
        if playerFlapped==True:
            # playerFlapped=False
            # playerHeight=GAME_SPRITES['player'].get_height()
            playery=playery -6
            # min(playervelY,playery-playerHeight)
        
        if playerFlapped==False:
            # playerFlapped=True
            playery=playery +6
            
                 #move pipes to the left
        for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
                    upperpipe['x']+=pipeVelX
                    lowerpipe['x']+=pipeVelX
                    #Add a new pipe when the first is about to cross to the leftmost
        if 0<upperPipes[0]['x']<5:
                        newpipe=getRandomPipe()
                        upperPipes.append(newpipe[0])
                        lowerPipes.append(newpipe[1])

                    # if the pipe is out of the screen remove it
        if upperPipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
                        upperPipes.pop(0)
                        lowerPipes.pop(0)
                    
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        #  SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        # myDigits = [int(x) for x in list(str(score))]
        # width = 0
        # for digit in myDigits:
        #     width += GAME_SPRITES['numbers'][digit].get_width()
        # Xoffset = (SCREENWIDTH - width)/2   
        # for digit in myDigits:
        #     SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
        #     Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes,lowerPipes):
    if playery>SCREENHEIGHT  or playery<0:
        GAME_SOUNDS['die'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        
        if(playery== GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['die'].play()
            return True

    # for pipe in lowerPipes:
    #     if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
    #         GAME_SOUNDS['die'].play()
    #         return True

    return False    
def getRandomPipe():
    '''generate positions of two pipes(one bottom straight and one top rototated) for blitting on the screen'''
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/6
    y2=offset+random.randrange(0,int(SCREENHEIGHT)-1.2*offset)
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipeX,'y':-y1},#upper pipe
        {'x':pipeX,'y':y2}#lower pipe 
    ]
        
    return pipe

if __name__=="__main__":
    #This will be the main point from where our game will start
    pygame.init() #Initializes pygame all modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Birdie By SUresh Subedi ')
    GAME_SPRITES['numbers']=(
        pygame.image.load("gallery\\0-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\1-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\2-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\3-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\4-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\5-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\6-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\7-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\8-Number-PNG.png").convert_alpha(),
        pygame.image.load("gallery\\9-Number-PNG.png").convert_alpha()
    )
    GAME_SPRITES['message']=pygame.image.load('gallery\\mmm.png').convert_alpha()
    # GAME_SPRITES['base']=pygame.image.load('gallery\\msg1.png').convert_alpha()
    GAME_SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

    #Game sounds
    GAME_SOUNDS['die']=pygame.mixer.Sound('audio\death.mp3')
    GAME_SOUNDS['background']=pygame.mixer.Sound('audio\gameplay.mp3')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('audio\wings.mp3')
    GAME_SOUNDS['point']=pygame.mixer.Sound('audio\point.mp3')

    

    while True:
        GAME_SOUNDS['background'].play
        welcomeScreen() #Shows welcome screen to the user until the player presses any button
        mainGame()

