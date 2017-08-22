import pygame, sys
from pygame.locals import *
from random import randint
import image_slicer
import os
from PIL import Image
from PIL import ImageOps

MATSIZE = int(input('Size of Side of Square Matrix: '))
d = MATSIZE*MATSIZE 
image_slicer.slice('img1.png', d)
for filename in os.listdir("."):
        if filename.startswith("img1_"):
                os.rename(filename, filename[5:])       
        for filename in os.listdir("."):
            for j in range(d):
                if filename.startswith("0"+str(j+1)+"_") and j+1 < 10:
                    os.rename(filename, (str(int(filename[4:5]) + MATSIZE*j)+ '.png'))
                elif filename.startswith("0"+str(j+1)+"_") and j+1 > 10:
                    os.rename(filename, (str(int(filename[4:6]) + MATSIZE*j)+ '.png'))    
x = (300/(2*MATSIZE))
x = x-1
for i in range(d):
    imgx = Image.open(str(i+1)+'.png')
    halfwidth = imgx.size[0] / 2
    halfheight = imgx.size[1] / 2
    imgcrop = imgx.crop(
        (
            halfwidth - x,
            halfheight - x,
            halfwidth + x,
            halfheight + x
        )
    )
    imgcrop.save(str(i+1)+'.png')
    imgx = Image.open(str(i+1)+'.png')
    imgborder = ImageOps.expand(imgx,border=5,fill='white')
    imgborder.save(str(i+1)+'.png')       

pygame.init()

INDS=300/MATSIZE
MP = 1
RANDOMIZEUPTO=1
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
NumberOfMoves =0
BLACK=(0,0,0)

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 400), 0, 32)
pygame.display.set_caption('Tile Game')

BlankSpace = (MATSIZE-1,MATSIZE-1)
WHITE = (255, 255, 255)
N=[]
for a in range(MATSIZE*MATSIZE-1):
    N.append(pygame.image.load(str(a+1)+'.png'))

#coord = [(0,0),(100,0),(200,0),(0,100),(100,100),(200,100),(0,200),(100,200),(200,200)]
coord =[]
curd={}
curd2={}

for a in range(MATSIZE):
    for b in range(MATSIZE):
        coord.append((b*INDS,a*INDS))
        curd[b,a]=b+a*MATSIZE
        curd2[b,a]=b+a*MATSIZE
curd[MATSIZE-1,MATSIZE-1]=-1
curd2[MATSIZE-1,MATSIZE-1]=-1
#curd2=curd

def possibleMove(mo):#Coded for a Square Matrix
    global BlankSpace
    if(mo=='LEFT'):
        n= BlankSpace[0] + 1
    elif(mo=='RIGHT'):
        n= BlankSpace[0] -1
    elif(mo=='UP'):
        n=BlankSpace[1]+1
    elif(mo=='DOWN'):
        n=BlankSpace[1]-1
    if(n>=0 and n<MATSIZE):
        return 1 #POSSIBLE
    else:
        return 0

def retPossibleMoves():
    a=[]
    if(BlankSpace[0]+1>=0 and BlankSpace[0]+1<MATSIZE):
        a.append('LEFT')
    if(BlankSpace[0]-1>=0 and BlankSpace[0]-1<MATSIZE):
        a.append('RIGHT')
    if(BlankSpace[1]+1>=0 and BlankSpace[1]+1<MATSIZE):
        a.append('UP')
    if(BlankSpace[1]-1>=0 and BlankSpace[1]-1<MATSIZE):
        a.append('DOWN')
    return a

def moveTo(mo, count=True):
    global BlankSpace
    global NumberOfMoves
    if(count):
        NumberOfMoves = NumberOfMoves+1
    if(mo=='LEFT'):
        ourx=(BlankSpace[0]+1)*INDS
        oury=BlankSpace[1]*INDS
        ours=curd[BlankSpace[0]+1,BlankSpace[1]]
        #print('LEFT '+'ourx ' + str(ourx) +' oury ' + str(oury) + 'ours ' + str(ours))
        while ourx>=(BlankSpace[0]*INDS):
            DISPLAYSURF.blit(N[ours], (ourx, oury))
            ourx=ourx-MP
        curd[BlankSpace]=curd[BlankSpace[0]+1, BlankSpace[1]];
        BlankSpace=(BlankSpace[0]+1, BlankSpace[1])
        curd[BlankSpace]=-1

    elif(mo=='RIGHT'):
        ourx=(BlankSpace[0]-1)*INDS
        oury=BlankSpace[1]*INDS
        ours=curd[BlankSpace[0]-1,BlankSpace[1]]
        #print("RIGHT "+'ourx ' + str(ourx) +' oury ' + str(oury) + 'ours ' + str(ours))
        while ourx<=(BlankSpace[0]*INDS):
            DISPLAYSURF.blit(N[ours], (ourx, oury))
            ourx=ourx+MP
        curd[BlankSpace]=curd[BlankSpace[0]-1, BlankSpace[1]];    
        BlankSpace=(BlankSpace[0]-1, BlankSpace[1])
        curd[BlankSpace]=-1

    elif(mo=='UP'):
        ourx=BlankSpace[0]*INDS
        oury=(BlankSpace[1]+1)*INDS
        ours=curd[BlankSpace[0],BlankSpace[1]+1]
        while oury>=(BlankSpace[1]*INDS):
            DISPLAYSURF.blit(N[ours], (ourx, oury))
            oury=oury-MP
        curd[BlankSpace]=curd[BlankSpace[0], BlankSpace[1]+1];
        BlankSpace=(BlankSpace[0], BlankSpace[1]+1)
        curd[BlankSpace]=-1

    elif(mo=='DOWN'):
        ourx=BlankSpace[0]*INDS
        oury=(BlankSpace[1]-1)*INDS
        ours=curd[BlankSpace[0],BlankSpace[1]-1]
        while oury<=(BlankSpace[1]*INDS):
            DISPLAYSURF.blit(N[ours], (ourx, oury))
            oury=oury+MP
        curd[BlankSpace]=curd[BlankSpace[0], BlankSpace[1]-1];
        BlankSpace=(BlankSpace[0], BlankSpace[1]-1)
        curd[BlankSpace]=-1

def Randomize(upto):
    for a in range(upto):
        moves=retPossibleMoves()        
        moveTo(moves[randint(0, len(moves)-1)], False)
        pygame.display.update()
        fpsClock.tick(FPS)

def RandomizeTillSpace():
    while True:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_SPACE:
                return
        moves=retPossibleMoves()        
        moveTo(moves[randint(0, len(moves)-1)], False)
        pygame.display.update()
        fpsClock.tick(FPS)     

def Show():
    DISPLAYSURF.fill(WHITE)
    for a in range(MATSIZE*MATSIZE-1):
        DISPLAYSURF.blit(N[a], coord[a])   
    pygame.display.update()
    BlankSpace = (MATSIZE-1,MATSIZE-1)

DISPLAYSURF.fill(WHITE)
for a in range(MATSIZE*MATSIZE-1):
    DISPLAYSURF.blit(N[a], coord[a])   
pygame.display.update()         

#rect(Surface, color, Rect, width=0) -> Rect
Randomize(RANDOMIZEUPTO)

while True: # the main game loop
    pygame.display.set_caption('Tile Game    ('+str(NumberOfMoves)+" Moves)")
    events = pygame.event.get()
    for event in events:
        if event.type == KEYUP:
            if event.key in (K_LEFT, K_a) and possibleMove('LEFT'):
                moveTo('LEFT')
            elif event.key in (K_RIGHT, K_d) and possibleMove('RIGHT'):
                moveTo('RIGHT')
            elif event.key in (K_UP, K_w) and possibleMove('UP'):
                moveTo('UP')
            elif event.key in (K_DOWN, K_s) and possibleMove('DOWN'):
                moveTo('DOWN')
        if event.type == QUIT:
            for i in range(d):
                os.remove(str(i+1)+'.png')
            pygame.quit()
            sys.exit()
        
        mouse = pygame.mouse.get_pos()

        mousepress=pygame.mouse.get_pressed()
        if(390>mouse[0]>310 and 100>mouse[1]>50 and mousepress[0]):
            #print(curd)
            #print(curd2)
            NumberOfMoves=0
            RandomizeTillSpace();
        if(390>mouse[0]>310 and 100>mouse[1]>50):
            pygame.draw.rect(DISPLAYSURF, (30,144,255), (310,50,80,50))
        else:
            pygame.draw.rect(DISPLAYSURF, (0,191,255), (310,50,80,50))



        if(390>mouse[0]>310 and 200>mouse[1]>150 and mousepress[0]):
            #NumberOfMoves=0
            Show();
            #print('some')
        if(390>mouse[0]>310 and 200>mouse[1]>150):
            pygame.draw.rect(DISPLAYSURF, (30,144,255), (310,150,80,50))
        else:
            pygame.draw.rect(DISPLAYSURF, (0,191,255), (310,150,80,50))



        pygame.draw.rect(DISPLAYSURF, (255,255,255), (100,310,200,80))
        
        smallText = pygame.font.Font("freesansbold.ttf",20)
        bigText = pygame.font.Font("freesansbold.ttf",30)

        textSurf = smallText.render('Jumble', True, (0,0,0))
        textSurf3 = smallText.render('Show', True, (0,0,0))
        textSurf2 = smallText.render('You WON!',True, (0,0,0))

        textRectObj = textSurf.get_rect()
        textRectObj3 = textSurf3.get_rect()
        textRectObj2 = textSurf2.get_rect()

        textRectObj.center = ( (310+(80/2)), (50+(50/2)) )
        textRectObj3.center = ( (310+40), (175))
        textRectObj2.center = ( (100+100), (310+40))

        DISPLAYSURF.blit(textSurf, textRectObj)
        DISPLAYSURF.blit(textSurf3, textRectObj3)
        
        if(curd==curd2):
            DISPLAYSURF.blit(textSurf2, textRectObj2)

    pygame.display.update()
    fpsClock.tick(FPS)
