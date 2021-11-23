import pygame
from random import randint
from multiprocessing import Manager
import multiprocessing as mp
from gesture_detection import start_recognition


def main():
    # starting the gesture recognising process
    manager=Manager()
    shared_dict=manager.dict()
    shared_dict['0']=''
    gesture_rec_proc=mp.Process(target=start_recognition,args=(shared_dict,))
    #gesture_rec_proc.start()
    # rest is game
    pygame.init()
    winX=600
    winY=600
    score=0
    win=pygame.display.set_mode((winX,winY))
    pygame.display.set_caption('Snake')
    clock=pygame.time.Clock()
    myfont=pygame.font.SysFont('monospace',16)  #declaring font


    class body():
        def __init__(self,x,y,weight,height,vel,colour,distance=0):
            self.x=x
            self.y=y
            self.weight=weight
            self.height=height
            self.vel=vel
            self.distance=distance
            self.colour=colour
        def draw(self):
            pygame.draw.rect(win,self.colour,(self.x,self.y,self.weight,self.height))



    def redefinegamewindow():
        win.fill((255,255,255))

        food.draw()
        if bodyparts:
            for bodykoordinates in bodyparts:
                if bodyparts.index(bodykoordinates)==0:
                    pygame.draw.rect(win,(100,0,100),(bodykoordinates[0],bodykoordinates[1],45,45))
                else:
                    pygame.draw.rect(win,(200,200,0),(bodykoordinates[0],bodykoordinates[1],45,45))
        scoretext=myfont.render('Score: '+str(score),1,(100,100,100))
        win.blit(scoretext,(20,20))
        pygame.display.update()


    food=body(100,100,45,45,0,(255,255,0))

    i=0
    right=True
    left=False
    up=False
    down=False
    bodyparts=[[0,0]]
    foodcoordinates=list(range(0,401,50))

    run=True
    while run:
        clock.tick(24)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        keys=pygame.key.get_pressed()


        if not up and (keys[pygame.K_DOWN] or shared_dict['0']=='thumbs down'):
            right=False
            left=False
            up=False
            down=True
        if not down and (keys[pygame.K_UP] or shared_dict['0']=='thumbs up'):
            right=False
            left=False
            up=True
            down=False
        if not right and (keys[pygame.K_LEFT] or shared_dict['0']=='okay'):
            right=False
            left=True
            up=False
            down=False
        if not left and (keys[pygame.K_RIGHT] or shared_dict['0']=='peace'):
            right=True
            left=False
            up=False
            down=False
        if i%10==0:
            if len(bodyparts)!=1:
                l=len(bodyparts)-1
                while l!=0:
                    if bodyparts.index(bodyparts[l])!=0:
                        if bodyparts[l][0]!=bodyparts[l-1][0]:
                            move=bodyparts[l-1][0]
                            bodyparts[l][0]=move
                        elif bodyparts[l][1]!=bodyparts[l-1][1]:
                            move=bodyparts[l-1][1]
                            bodyparts[l][1]=move
                    l-=1
            if right:
                move=bodyparts[0][0]
                move+=50
                bodyparts[0][0]=move
            elif left:
                move=bodyparts[0][0]
                move-=50
                bodyparts[0][0]=move
            elif up:
                move=bodyparts[0][1]
                move-=50
                bodyparts[0][1]=move
            elif down:
                move=bodyparts[0][1]
                move+=50
                bodyparts[0][1]=move
            if bodyparts[0][0]>winX-50:
                bodyparts[0][0]=0
            elif bodyparts[0][0]<0:
                bodyparts[0][0]=winX-50
            if bodyparts[0][1]>winY-50:
                bodyparts[0][1]=0
            elif bodyparts[0][1]<0:
                bodyparts[0][1]=winY-50

            if food.x==bodyparts[0][0] and food.y==bodyparts[0][1]:
                score+=1
                food.x=foodcoordinates[randint(0,8)]
                food.y=foodcoordinates[randint(0,8)]
                body_on_food=False
                while not body_on_food:
                    for body in bodyparts:
                        if body[0]==food.x and body[1]==food.y:
                            food.x=foodcoordinates[randint(0,8)]
                            food.y=foodcoordinates[randint(0,8)]
                            break
                        else:
                            body_on_food=True


                if len(bodyparts)==1:
                    if right:
                        coordx=bodyparts[0][0]
                        coordy=bodyparts[0][1]
                        bodyparts.append([coordx-50,coordy])
                    elif left:
                        coordx=bodyparts[0][0]
                        coordy=bodyparts[0][1]
                        bodyparts.append([coordx+50,coordy])
                    elif up:
                        coordx=bodyparts[0][0]
                        coordy=bodyparts[0][1]
                        bodyparts.append([coordx,coordy+50])
                    elif down:
                        coordx=bodyparts[0][0]
                        coordy=bodyparts[0][1]
                        bodyparts.append([coordx,coordy-50])
                else:
                    if bodyparts[len(bodyparts)-1][0]<bodyparts[len(bodyparts)-2][0]:
                        coordx=bodyparts[len(bodyparts)-1][0]-50
                        coordy=bodyparts[len(bodyparts)-1][1]
                        bodyparts.append([coordx,coordy])
                    elif bodyparts[len(bodyparts)-1][0]>bodyparts[len(bodyparts)-2][0]:
                        coordx=bodyparts[len(bodyparts)-1][0]+50
                        coordy=bodyparts[len(bodyparts)-1][1]
                        bodyparts.append([coordx,coordy])
                    elif bodyparts[len(bodyparts)-1][1]>bodyparts[len(bodyparts)-2][1]:
                        coorx=bodyparts[len(bodyparts)-1][0]
                        coory=bodyparts[len(bodyparts)-1][1]+50
                        bodyparts.append([coorx,coory])
                    elif bodyparts[len(bodyparts)-1][1]<bodyparts[len(bodyparts)-2][1]:
                        coordx=bodyparts[len(bodyparts)-1][0]
                        coordy=bodyparts[len(bodyparts)-1][1]-50
                        bodyparts.append([coordx,coordy])
            l=0
            for body in bodyparts:
                if l!=0:
                    if bodyparts[0][0]==body[0] and bodyparts[0][1]==body[1]:
                        run=False
                        print('Ohh...You ate yourself')
                l+=1
            if len(bodyparts)!=1:
                if bodyparts[0][0]==bodyparts[len(bodyparts)-1][0] and bodyparts[0][1]==bodyparts[len(bodyparts)-1][1]:
                    run=False
                    print('Ohh...You ate yourself')

        redefinegamewindow()
        i+=1
    pygame.quit()
    print('Score: '+str(score))


if __name__=='__main__':
    main()