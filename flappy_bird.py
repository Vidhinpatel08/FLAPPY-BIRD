import random # USED IN RANDOM PIPES GENERATES
import sys # USED IN EXITS THE SCREEN 
import pygame  
from pygame.locals import * # BASIC PYGAME MODLE IMPORT

# GLOBAL VARIABLE INITIALIZE FOR GAME
FPS = 32 # FREAM PER SECONDS 
SCREENWIDTH = 289 # SCRREN WIDTH 
SCREENHEIGHT = 511 # SCRREN HEIGHT 
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) # INITIALIZE THE SCREEN WINDOW

GROUNDY = SCREENHEIGHT * 0.8 # BASE Y CO-ORDINATE
PLAYER = r'gallery\sprites\bird.png' 
BACKGROUND = r'gallery\sprites\background.png'
PIPE = r'gallery\sprites\pipe.png'
GAME_SPRITES = {}     # INITIALIZE DICT OF SPRITES 
GAME_SOUNDS = {}    # INITIALIZE DICT OF SOUNDS 


def welcomeScreen():
    """SHOWS WELCOME IMAGES ON THE SCRREN"""
    
    #  PLAYER SCRREN X & Y CO-ORDINATES
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)

    #  MESSAGE SCRREN X & Y CO-ORDINATES
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)

    #  BASE SCRREN X & Y CO-ORDINATES
    basex = 0

    while True :
        for event in pygame.event.get():
            # IF USER CLICK ON CREOSS(CLOSE) BUTTON ESCAPR OR DELETE, CLOSE THE GAME
            if event.type == QUIT  or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_DELETE)):
                pygame.quit()
                sys.exit()

            # IF USER PRESS THE ENTER OR NUMRICAL_ENTER, START THE GAME FOR THEM 
            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_KP_ENTER) :
                return
            
            else :
                # BLITTING SCRREN UNTILL ANY RESPOND 
                SCREEN.blit(GAME_SPRITES['background'],(0 , 0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))

                pygame.display.update() # SCRREN DON'T CHANGE UNTILL UPDATE
                FPSCLOCK.tick(FPS) # CONTROLL FPS(32) FRAM PER SECOND

def mainGame():
    """THIS IS MAIN FUNCTION, WHICH IS CONTAIN LOGIC OF THE GAME DURING RUNING"""
    score = 0

    #  PLAYER SCRREN X & Y CO-ORDINATES DURING THE RUN GAME
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)

    #  BASE SCRREN X & Y CO-ORDINATES
    basex = 0
   
    # CREATE 2 PIPES FOR BLITTING ON THE SCREEN
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # MY LIST OF UPPER PIPE
    upperPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newPipe1[0]['y']}, # X = SCREEN + 200 , Y = NewPipe1'S UPPER PIPE
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH /2), 'y' : newPipe2[0]['y']} # X = SCREEN + 200 + 1/2 SCREEN , Y = NewPipe2'S UPPER PIPE
    ]

    # MY LIST OF LOWER PIPE
    lowerPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newPipe1[1]['y']}, # X = SCREEN + 200 , Y = NewPipe1'S LOWER PIPE
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH /2), 'y' : newPipe2[1]['y']}  # X = SCREEN + 200 + 1/2 SCREEN , Y = NewPipe2'S LOWER PIPE
    ]

    # PIPE VELOCITY : (MOVE PIPE)
    pipeVelX = -4       # TRY AND RUN VALUES

    # PLAYER VELOCITY : (MOVE PLAYER) 
    playerVelY = -9     # TRY AND RUN VALUES
    playerMaxVelY = 10   # TRY AND RUN VALUES
    playerMinVelY = -8  # TRY AND RUN VALUES
    playerAccY = 1      # TRY AND RUN VALUES

    # PLAYER'S FLAYING OR FLAPPING
    playerFlapAccv = -8 # VELOCITY WHILE FLAPPING
    playerFlapped = False

    # GAME LOOP
    while True : 
        for event in pygame.event.get():

            # IF USER CLICK ON CREOSS(CLOSE) BUTTON ESCAPR OR DELETE, CLOSE THE GAME
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_DELETE)):
                pygame.quit()
                sys.exit()

            # IF USER PRESS THE SPACE OR UP KEY, FLAPPING PLAYER 
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) :
                # PLAYER IN SCREEN 
                if playery > 0 : 
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
                
        # COLIDE TESTING :
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # THIS FUNCTION RETURN TRUE IF PLAYER IS CRASHED
        if crashTest :
            return score
        
        #  CHECK FOR SCORE 
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2 # HALF OF PLAYER
        
        # FOR ALL PIPES 
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2 # HALF OF PIPE
            
            if pipeMidPos <= playerMidPos < pipeMidPos + 4 : # ONE + HALF OF PLAYER BETWEEN (HALF OF PIPE) AND (HALF OF PIPE + 4)
                score +=1
                # print(F"your Score is {score}")
                GAME_SOUNDS['point'].play()
        
        # PLAYER MOVED , (VELOCITY CHANGE)
        if playerVelY < playerMaxVelY and not playerFlapped :
            playerVelY += playerAccY

        # PLAYER ONLY ONE TIME FLAPPED, THEN FLAPPED FALSE (VELOCITY CHANGE)
        if playerFlapped :
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height() 
        
        #  PLAYER POSITION CHANGE
        playery += min(playerVelY, GROUNDY - playery - playerHeight) # MINIMUM OF (PLAYER VELOCITY) OR (SCREEN - PLAYERHIEGHT - GROUND (WICH IS 0))
        
        # MOVE PIPE TO THE LEFT 
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes) :
            upperPipe['x'] += pipeVelX # UPPER PIPE MOVE LEFT BY PIPE VELOCITY(-4)
            lowerPipe['x'] += pipeVelX # LOWER PIPE MOVE LEFT BY PIPE VELOCITY(-4)

        # ADD A NEW PIPE WHEN THE FIRST IS ABOUT TO CROSS THE LEFT MOST PART OF THE SCREEN 
        if  0 < upperPipes[0]['x'] < 5 : 
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # IF THE PIPE IS OUT OF THE SCREEN, REMOVE IT (X- AXIS)
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width() :
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # LET'S BLITTING OUR SPRITES
        SCREEN.blit(GAME_SPRITES['background'],(0, 0)) 
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y'])) # UPPER PIPE
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y'])) # LOWER PIPE
        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
        
        # GET DIGIT OF SCORE, THEN GET WIDTH OF TAKEN BY NUMBERS
        mydigit = [int(x) for x in list(str(score))] # GET SCORE IN LIST OF ELEMENTS
        width = 0 
        for digit in mydigit:
            width += GAME_SPRITES['numbers'][digit].get_width() # GET WIDTH OF TAKEN BY NUMBERS AND ADDED IN WIDTH 
        
        xoffset = (SCREENWIDTH - width) /2  # CENTER POINT OF THE SCREEN 

        for digit in mydigit :
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.05)) # BLITTING THE SCRORE
            xoffset += GAME_SPRITES['numbers'][digit].get_width() #   FOR NEXT DIGIT

        pygame.display.update() # SCRREN DON'T CHANGE UNTILL UPDATE
        FPSCLOCK.tick(FPS) # CONTROLL FPS(32) FRAM PER SECOND



def getRandomPipe() :
    """GENERATED POSITIONS OF TWO PIPES(ONE BOTTOM STRAIGHT AND ONE TOP ROTATED) FOR BILITTING ON THE SCRREN"""

    pipeHeight = GAME_SPRITES['pipe'][0].get_height() # GETTING PIPE HEIGHT
    offset = SCREENHEIGHT/3 # ATLEAST THREED ONE PART OF SCREEN HIGHT IS OFFSET

    pipex = SCREENWIDTH + 10 # X CO-ORDINATES OF PIPE
    
    # Y2 CO-ORDINATES OF PIPE (LOWER PIPE)
    y2 =   offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))

    # Y1 CO-ORDINATES OF PIPE (UPPPER PIPE), WHICH IS GOING IN NEGATIVE
    y1 = pipeHeight - y2 + offset
    
    # RETURN 'pipe' DICT WHICH CONTAIN X & Y CO-ORDINATES
    pipe = [
        {'x' : pipex , 'y' : -y1}, # UPPER PIPE
        {'x' : pipex , 'y' : y2}   # LOWER PIPE
    ]
    return pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    """THIS FUNCTION RETURN TRUE IF PLAYER IS CRASHED"""

    # IF PLAYER TOUCH GROUND  OR OUT OF SKY 
    if playery > GROUNDY-25 or playery < 0 :
        GAME_SOUNDS['hit'].play()
        return True
    
    # IF TOUCH UPPER PIPE
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        # IF (PLAERS'X IN SIDED WIDTH)  AND ALSO (PLAYER'S Y CO-ORDINATE INSIDED UPPPER_PIPE'S END OF Y CO-ORDINAT)
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()): 
            GAME_SOUNDS['hit'].play()
            return True
              
    # # IF TOUCH LOWER PIPE
    for pipe in lowerPipes:
        # IF( PLAYER'S ENDING Y CO-ORDINATE INSIDED PIPE'S Y CORDINATES) AND ALSO (PLAYER'S X CO-ORDINATE INSIDE PIPE'S WIDTH)
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] ) and abs(playerx - pipe['x']) <  GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True    
    # IF NOT ANY CRASHING RETURN FALSE
    return False

def scoreScreen(score, highScoreRecored):
    """THIS IS THE SCORE PRINTING FUNCTION """
    
    #  PLAYER SCRREN X & Y CO-ORDINATES
    playerx = int((SCREENWIDTH - GAME_SPRITES['player'].get_width())/2)
    playery = int((SCREENHEIGHT*0.9 + GAME_SPRITES['scorebg'].get_height())/2)

    #  SCORE_BOARED SCRREN X & Y CO-ORDINATES
    scorebgx = int((SCREENWIDTH-GAME_SPRITES['scorebg'].get_width())/2)
    scorebgy = int(SCREENHEIGHT*0.13)

    #  BASE SCRREN X & Y CO-ORDINATES
    basex = 0

    while True :
        for event in pygame.event.get():  # FEATCHING EVENTS..
            # IF USER CLICK ON CREOSS(CLOSE) BUTTON ESCAPR OR DELETE, CLOSE THE GAME
            if event.type == QUIT  or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_DELETE)):
                pygame.quit()
                sys.exit()

            # IF USER PRESS THE ENTER OR NUMRICAL_ENTER, START THE NEW GAME
            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_KP_ENTER) :
                return
            
            else :
                # BLITTING SCRREN UNTILL ANY RESPOND 
                SCREEN.blit(GAME_SPRITES['background'],(0, 0))
                SCREEN.blit(GAME_SPRITES['scorebg'],(scorebgx, scorebgy))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))

                # GET DIGIT OF SCORE, THEN GET WIDTH OF TAKEN BY NUMBERS
                mydigit = [int(x) for x in list(str(score))] # LIST OF SCORE DIGIT      
                width = 0 
                for digit in mydigit:
                    width += GAME_SPRITES['numbers'][digit].get_width() # GET WIDTH OF TAKEN BY NUMBERS AND ADDED IN WIDTH 
                xoffset = (SCREENWIDTH - width) /2  # CENTER POINT OF THE SCREEN 

                for digit in mydigit :
                    SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.25)) # BLITTING THE SCRORE
                    xoffset += GAME_SPRITES['numbers'][digit].get_width() #   FOR NEXT DIGIT

                # GET DIGIT OF HIGHSCORE, THEN GET WIDTH OF TAKEN BY NUMBERS
                highScore = [int(x) for x in list(str(highScoreRecored))]  # LIST OF HIGH_SCORE DIGIT      
                width = 0 
                for digit in highScore:
                    width += GAME_SPRITES['numbers'][digit].get_width() # GET WIDTH OF TAKEN BY NUMBERS AND ADDED IN WIDTH 
                xoffset = (SCREENWIDTH - width) /2  # CENTER POINT OF THE SCREEN 

                for digit in highScore :
                    SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.42)) # BLITTING THE SCRORE
                    xoffset += GAME_SPRITES['numbers'][digit].get_width() #   FOR NEXT DIGIT

                pygame.display.update() # SCRREN DON'T CHANGE UNTILL UPDATE
                FPSCLOCK.tick(FPS) # CONTROLL FPS(32) FRAM PER SECOND

if __name__ == "__main__":
    # Game Stating Point
    
    # BASIC COMMAND TO TO INITLIZE PYGAME 
    pygame.init() #  INITLIZE PYGAME  ALL MODLUE
    FPSCLOCK = pygame.time.Clock() # CONTROL THE FPS IN GAME
    pygame.display.set_caption("Flappy Bird") # TITLE OF THW WINDOW

    # ADDED ALL IMAGES Dict Of SPRITES 
    GAME_SPRITES['numbers'] = (
        pygame.image.load( r"gallery\sprites\0.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\1.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\2.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\3.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\4.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\5.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load(r"gallery\sprites\6.png").convert_alpha(),  #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\7.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\8.png").convert_alpha(), #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
        pygame.image.load( r"gallery\sprites\9.png").convert_alpha()  #   OPTIMIZE FOR GAME (BLITTING TIME CHANGE IMAGES WITH ALPHS)
    )
    GAME_SPRITES['message'] = pygame.image.load( r"gallery\sprites\message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load( r"gallery\sprites\base.png").convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180), # ROTATE PIPE AT 180 DEG.
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert() # DURING BLITTING TIME CHNAGE ONLY IMAGES
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha() # BLITTING TIME CHANGE IMAGES WITH ALPHS
    GAME_SPRITES['scorebg'] = pygame.image.load(r"gallery\sprites\scorebg.png").convert() # BLITTING TIME CHANGE IMAGES WITH ALPHS

    # ADDED ALL IMAGES Dict Of SOUNDS 
    GAME_SOUNDS['die'] = pygame.mixer.Sound(r'gallery\audio\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound(r'gallery\audio\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound(r'gallery\audio\point.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(r'gallery\audio\wing.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(r'gallery\audio\swoosh.wav')

    welcomeScreen()     # SHOWS WELCOME SCRREN UNTILL USER PRESS THE BUTTON (ENTER / NUMRICAL_ENTER) 
    while True :    
        score = mainGame() # THIS IS THE MAIN FUNCTION 

        # CHANGE HIGHSCORE IN FILE AND GET HIGH SCORE
        with open(r'scoreBored.txt','r') as f:
            highScoreRecored = f.read() # FEACHING HIGH_SCORE FROM FILE
            # IF SCORE IS BIGGER THEN HIGH_SCORE THEN CHANGE
            if score > int(highScoreRecored) :
                highScoreRecored == score 
                with open(r'scoreBored.txt','w') as f:
                    f.write(f'{score}') # OVERRIGHT THE NEW SCORE IN FILE

        scoreScreen(score,highScoreRecored) # THIS IS THE SCORE PRINTING FUNCTION 
        
