import pygame
import random

WIDTH=700
HEIGHT=700

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE=(255,255,255)

BODYSIZE=50
INITLEN=3
LEFT=0
UP=1
RIGHT=2
DOWN=3

BodyList=[]
Game_Over=False

def getInitDir(x_pos,y_pos):
    if(x_pos>=WIDTH/2):
        return LEFT
    else:
        return RIGHT

def randomPos():
    x_pos=random.randint(2,WIDTH/BODYSIZE-INITLEN)*BODYSIZE
    y_pos=random.randint(2,HEIGHT/BODYSIZE-INITLEN)*BODYSIZE
    return (x_pos,y_pos)

def initSnake():
    ranPos=randomPos()
    head=[ranPos[0],ranPos[1],getInitDir(ranPos[0],ranPos[1])]
    BodyList.append(head)
    for i in range(0,INITLEN-1):
        addBody(BodyList)

def addBody(BodyList):
    direction=BodyList[len(BodyList)-1][2]
    if direction==LEFT:
        x_pos=BodyList[len(BodyList)-1][0]+BODYSIZE
        y_pos=BodyList[len(BodyList)-1][1]
    elif direction==RIGHT:
        x_pos=BodyList[len(BodyList)-1][0]-BODYSIZE
        y_pos=BodyList[len(BodyList)-1][1]
    elif direction==UP:
        x_pos=BodyList[len(BodyList)-1][0]
        y_pos=BodyList[len(BodyList)-1][1]+BODYSIZE
    else:
        x_pos=BodyList[len(BodyList)-1][0]
        y_pos=BodyList[len(BodyList)-1][1]-BODYSIZE
    BodyList.append([x_pos,y_pos,direction])

def DrawBodies(BodyList):
    for body in BodyList:
        if BodyList.index(body)!=0:
            pygame.draw.rect(SCREEN,GREEN,pygame.Rect(body[0],body[1],BODYSIZE,BODYSIZE))
        else:
            pygame.draw.rect(SCREEN,RED,pygame.Rect(body[0],body[1],BODYSIZE,BODYSIZE))
        
    
    

def SelfMoveBody(BodyList):
    for body in BodyList:
        moveBody(body)
    DrawBodies(BodyList)

def moveBody(body):
    direction=body[2]
    if direction==RIGHT:
        body[0]+=BODYSIZE
    elif direction==UP:
        body[1]-=BODYSIZE
    elif direction==LEFT:
        body[0]-=BODYSIZE
    else:
        body[1]+=BODYSIZE
    

#check and refresh DIRECTION
def refreshDir(BodyList):

    i=len(BodyList)-1
    while i>=1:
        BodyList[i][2]=BodyList[i-1][2]
        i-=1

def checkCollision(BodyList):
    for body in BodyList:
        if body[0]<0 or body[0]>=WIDTH or body[1]<0 or body[1]>=HEIGHT:
            return True
    
        else:
            temp=BodyList.copy()
            temp.remove(body)
            for x in temp:
                if body[0]==x[0] and body[1]==x[1]:
                    return True
    return False

def newBall(BodyList):
    x_pos=random.randint(0,WIDTH/BODYSIZE-1)*BODYSIZE+int(BODYSIZE*0.5)
    y_pos=random.randint(0,HEIGHT/BODYSIZE-1)*BODYSIZE+int(BODYSIZE*0.5)
    for body in BodyList:
        if body[0]==x_pos and body[1]==y_pos:
            newBall(BodyList)
    return [x_pos,y_pos]

def drawBall(ball):
    pygame.draw.circle(SCREEN,BLUE,ball,int(BODYSIZE/2))
def checkEat(BodyList,ball):
    for body in BodyList:
        if body[0]==ball[0]-int(BODYSIZE/2) and body[1]==ball[1]-int(BODYSIZE/2):
            ball=newBall(BodyList)
            addBody(BodyList)
    return ball
        




pygame.init()
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
initSnake()

pygame.time.set_timer(pygame.USEREVENT+1,1000)

ball=newBall(BodyList)
while not Game_Over:
   
    for event in pygame.event.get():
        SCREEN.fill((0,0,0))
        if event.type==pygame.QUIT:
            Game_Over=True
        if event.type==pygame.KEYDOWN:
            
        
            if event.key==pygame.K_UP:
                refreshDir(BodyList)
                BodyList[0][2]=UP
                SelfMoveBody(BodyList)
                    
            if event.key==pygame.K_DOWN:
                refreshDir(BodyList)
                BodyList[0][2]=DOWN
                SelfMoveBody(BodyList)
            
            if event.key==pygame.K_LEFT:
                refreshDir(BodyList)
                BodyList[0][2]=LEFT
                SelfMoveBody(BodyList)

            if event.key==pygame.K_RIGHT:
                refreshDir(BodyList)
                BodyList[0][2]=RIGHT
                SelfMoveBody(BodyList)
                print(BodyList)
                
            
            Game_Over=checkCollision(BodyList)
                
            
        if event.type==pygame.USEREVENT+1:
           
            refreshDir(BodyList)
            SelfMoveBody(BodyList)
            print(BodyList)
            
            Game_Over=checkCollision(BodyList)
    ball=checkEat(BodyList,ball)
    drawBall(ball)
    DrawBodies(BodyList)
    pygame.display.flip()
    
    

