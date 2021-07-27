import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAMESPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    '''
        It Show Welcome Screen When Game is Start
    :return:
    '''
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAMESPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAMESPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if userclick onn creoss btn then close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #         is user click on space bar or up click start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAMESPRITES['background'], (0, 0))
                SCREEN.blit(GAMESPRITES['player'], (playerx, playery))
                SCREEN.blit(GAMESPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAMESPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getRandomPipe():
    '''
        This Function is used to creat the Random Pipe width and HEight
    :return:
    '''
    pipeheight = GAMESPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAMESPRITES['base'].get_height() - 1.6 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper pipe
        {'x': pipeX, 'y': y1},  # Lower pipe
    ]
    return pipe


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAMESPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAMESPRITES['pipe'][
            0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAMESPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                GAMESPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def mainGame():
    '''
    This is a Main Function of the Game , there is a location where Game is Initiate
    :return:
    '''
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    #     Create 2 Pipe for blitting on the scrren
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    #     My List of upper Pipe
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newpipe2[0]['y']}
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newpipe2[1]['y']}
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # Velcity while flapping
    playerFlapped = False  # its is True only when bird is Flying

    while True:
        for event in pygame.event.get():
            # if userclick onn creoss btn then close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #         is user click on space bar or up click start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)  # This Function true if player is
        # crashed
        if crashTest:
            return
        #           check for Score
        playerMidPos = playerx + GAMESPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAMESPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your Score is :{score}")
                GAME_SOUNDS['point'].play()
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerheighit = GAMESPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerheighit)

        #             Move pipes to the  left
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        #         Add a new pipe when the about to cross the left part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        #    If the pipe is Out od the screen
        if upperPipes[0]['x'] < -GAMESPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #     Lets Bit our Sprit now
        SCREEN.blit(GAMESPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAMESPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAMESPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAMESPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAMESPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAMESPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAMESPRITES['numbers'][digit], (Xoffset, SCREENWIDTH * 0.12))
        Xoffset += GAMESPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    #


if __name__ == '__main__':
    # This will the main Point from where our game will start
    pygame.init()
    FPSCLOCK = pygame.time.Clock();
    pygame.display.set_caption("Flappy Bird Game by Sakib")
    GAMESPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha())
    GAMESPRITES['message'] = pygame.image.load(
        'gallery/sprites/message.png').convert_alpha()
    GAMESPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAMESPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(
        PIPE).convert_alpha(), 180), pygame.image.load(PIPE).convert_alpha())
    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    #     Backgrouund Images
    GAMESPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAMESPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        welcomeScreen()
        mainGame()
