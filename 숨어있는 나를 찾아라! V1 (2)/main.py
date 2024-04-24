import pygame
import random

pygame.init()

screen_size = (1080, 720) 
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

tile_size = 32

tile_width = 15
tile_height = 15
grid_pixel_width = tile_size * tile_width
grid_pixel_height = tile_size * tile_height

imageList = ['monki.jpg','panda.png','cat.png','dog.png','deer.png','fox.png','camel.png','gorilla.png']

closedImage = pygame.image.load('none.png')
closed = pygame.transform.scale(closedImage,(tile_size,tile_size))
openImage = pygame.image.load('empty.png')
open = pygame.transform.scale(openImage,(tile_size,tile_size))
mineImage = pygame.image.load('mine.png')
mine = pygame.transform.scale(mineImage,(tile_size,tile_size))
mineNoImage = pygame.image.load('noMine.png')
mineNo = pygame.transform.scale(mineNoImage,(tile_size,tile_size))
flagImage = pygame.image.load('flag.png')
flag = pygame.transform.scale(flagImage,(tile_size,tile_size))
bgImage = pygame.image.load('tileBg.png')
bg = pygame.transform.scale(bgImage,(2000,2000))
bgCoor = [-50,-50]

tile_state = []
tile_mineAround = []
tile_sizeMultiplier = []

done = True
clock = pygame.time.Clock()

crash = pygame.mixer.Sound("crash.wav")
crash.set_volume(0.7)

flagSound = pygame.mixer.Sound("flag.wav")
flagSound.set_volume(0.7)

pickSound = pygame.mixer.Sound("pick.wav")
pickSound.set_volume(0.7)

resetSound = pygame.mixer.Sound("reset.wav")
resetSound.set_volume(0.1)

explosion = pygame.mixer.Sound("explosion.wav")
explosion.set_volume(0.6)

fanfare = pygame.mixer.Sound("win.wav")
fanfare.set_volume(0.8)

pygame.mixer.music.load("mus.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)

mineStack = 0

exploded = False

def getTile(ind):
    if (ind > -1 and ind < tile_width * tile_height):
        return tile_state[ind];
    else:
        return 'none';

tilesLeft = 0

def openTile(ind, chording = False):
    if ((getTile(ind) == 'opened' and not chording) or (chording and tile_mineAround[ind] == 0)): return;
    if              (getTile(ind) == 'flagged' or getTile(ind) == 'flaggedMine'):
        return
    global exploded,mineStack,tilesLeft,explosion
    if (getTile(ind) == 'closedMine'):
        explosion.play()
        exploded = True
        return
    flagAround = 0
    returner = False
    for i in range(-1,2):
        for e in range(-1,2):
            if (tileGetOffset(ind,e,i) == 'closedMine'):
                returner = True
                if (not chording):
                    tile_mineAround[ind] += 1
            if (tileGetOffset(ind,e,i) == 'flaggedMine'):
                if (not chording):
                    tile_mineAround[ind] += 1
                flagAround += 1
            if (tileGetOffset(ind,e,i) == 'flagged'):
                flagAround += 1
                
    if not chording:
        tile_state[ind] = 'opened'
        mineStack += 1
        tilesLeft -= 1
        

    if (returner and not chording): return
    if (tile_mineAround[ind] != flagAround and chording): return

    for i in range(-1,2):
        for e in range(-1,2):
            if (tileGetOffset(ind,e,i) == 'closed'):
                openTile(ind + e + (i * tile_width))
            if (tileGetOffset(ind,e,i) == 'closedMine' and chording):
                explosion = pygame.mixer.Sound("explosion.wav")
                explosion.set_volume(0.6)
                explosion.play()
                exploded = True
               

def tileGetOffset(base,x,y):
    if ((base % tile_width + x) > -1 and (base % tile_width + x) < tile_width):
        return getTile(base+x+(y*tile_width))
    else: return 'none';

def runGame():
    global tile_size, done, tile_height, tile_state, tile_width, mineStack, exploded,tilesLeft 
    done = True
    mineCount = 0

    monkiImage = pygame.image.load(random.choice(imageList))
    monki = pygame.transform.scale(monkiImage,(tile_size * tile_width,tile_size * tile_height))

    exploded = False
    won = False
    gameOverScroll = -200
    tilesLeft = 0

    tile_sizeMultiplier = []
    tile_state = []

    for i in range(0,tile_width*tile_height):
        st = random.randint(0,8)
        tile_mineAround.append(0)
        tile_sizeMultiplier.append(1)
        if (st == 0):
            tile_state.append('closedMine')
            mineCount += 1
        else:
            tilesLeft += 1
            tile_state.append('closed')

    font = pygame.font.SysFont("tcapitals", tile_size - 5)
    font2 = pygame.font.SysFont(None, 60)
    font3 = pygame.font.SysFont("niagarasolid", 200)

    while done:
        clock.tick(60)

        mButtonPress = False 

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # 종료조건 
                done=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mButtonPress = True
            if event.type == pygame.KEYDOWN:
                if event == pygame.K_r:
                    done = False
        
        bgCoor[0] += 1
        bgCoor[1] += 1
        if bgCoor[0] >= 0:
            bgCoor[0] -= 50
            bgCoor[1] -= 50
        
        screen.blit(bg,(bgCoor[0],bgCoor[1]))

        screen.blit(monki,(tile_size + 300,tile_size + 150))
        
        for x in range(1,tile_width + 1):
            for y in range(1,tile_height + 1):
                index = y + tile_width * (x - 1) - 1
                coor = (x * tile_size + 300, y * tile_size + 150)
                curTile = getTile(index)

                if mButtonPress and not exploded and not won:
                    mineStack = 0
                    if pygame.mouse.get_pressed() == (True,False,False):
                        if (pygame.mouse.get_pos()[0] in range(coor[0], coor[0] + tile_size)) and (pygame.mouse.get_pos()[1] in range(coor[1], coor[1] + tile_size)):
                            openTile(index, curTile == 'opened')
                            if (mineStack > 0):
                                crash.set_volume(0.2 + mineStack / 500)
                                crash.play()
                    if pygame.mouse.get_pressed() == (False,False,True):
                        if (pygame.mouse.get_pos()[0] in range(coor[0], coor[0] + tile_size)) and (pygame.mouse.get_pos()[1] in range(coor[1], coor[1] + tile_size)):
                            if curTile == "closed" and mineCount > 0:
                                tile_state[index] = "flagged"
                                mineCount -= 1
                                flagSound.play()
                            if curTile == "flagged":
                                tile_state[index] = "closed"
                                mineCount += 1
                                pickSound.play()
                            if curTile == "closedMine" and mineCount > 0:
                                tile_state[index] = "flaggedMine"
                                mineCount -= 1
                                flagSound.play()
                            if curTile == "flaggedMine":
                                tile_state[index] = "closedMine"
                                mineCount += 1
                                pickSound.play()
                    if tilesLeft <= 0:
                        won = True
                        fanfare.play()
                        mineCount = 0
                                
                if curTile == 'opened':
                    tile_sizeMultiplier[index] = pygame.math.lerp(tile_sizeMultiplier[index],0,0.1)
                    coor = (pygame.math.lerp(coor[0],coor[0] + tile_size / 2, 1 - tile_sizeMultiplier[index]),pygame.math.lerp(coor[1],coor[1] + tile_size / 2, 1 - tile_sizeMultiplier[index]))

                
                if not won:
                    open = pygame.transform.scale(openImage,(tile_size * tile_sizeMultiplier[index],tile_size * tile_sizeMultiplier[index]))

                    if curTile == 'closed':
                        screen.blit(closed, coor)
                    elif curTile == 'closedMine':
                        if (exploded): screen.blit(mine, coor)
                        else: screen.blit(closed, coor)
                    elif curTile == 'flagged':
                        if (exploded): screen.blit(mineNo, coor)
                        else: screen.blit(flag, coor)
                    elif curTile == 'flaggedMine':
                        screen.blit(flag, coor)
                    elif not exploded:
                        screen.blit(open, coor)
                        if (tile_mineAround[index] > 0):
                            teext = font.render(f"{tile_mineAround[index]}", True, (255,50,50))
                            screen.blit(teext,[coor[0] - 5,coor[1] - 8])

                        
        teextt = font2.render(f"{mineCount}", True, (255,255,255),(0,0,0))
        screen.blit(teextt,[10,10])
        
        if (exploded):
            pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() + (1 - pygame.mixer.music.get_volume())) * 0.2)
            gameOverScroll += (-8 - gameOverScroll) * 0.2
            gameovatext = font3.render(f"GAME OVER", True, (255,0,0))
            screen.blit(gameovatext,[315,gameOverScroll])
        else:
            pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() + (0.7 - pygame.mixer.music.get_volume())) * 0.2)

        pygame.display.update() 

while 1:
    runGame()
    resetSound.play()
    tile_mineAround = []
pygame.quit()