import pygame
from random import randint

class GameWindow:
    def __init__(self,shared_obj=None,window_title:str='snake',winx:int=600,winy:int=600,font_style:str='monospace',font_size:int=16) -> None:
        pygame.init()
        self.winx=winx
        self.winy=winy
        self.win=pygame.display.set_mode((winx,winy)) # defining the size of the game window
        pygame.display.set_caption(window_title) # window title
        self.clock=pygame.time.Clock() # init clock : this will define how many frames we are gonn have each sec
        self.my_font=pygame.font.SysFont(font_style,font_size) # defoault font
        self.shared_obj=shared_obj
    
    def exit_game(self):
        '''Simply quitting from the program'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
    
    



class SnakeGame(GameWindow):
    class Body:
        def __init__(self,x,y,weight,height,vel,colour,distance=0):
            self.x=x
            self.y=y
            self.weight=weight
            self.height=height
            self.vel=vel
            self.distance=distance
            self.colour=colour
        def draw(self,win):
            pygame.draw.rect(win,self.colour,(self.x,self.y,self.weight,self.height))

        
    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)
        self.score=0
        self.run=False
        self.right=False
        self.left=False
        self.up=False
        self.down=True
        self.bodyparts=[[0,0]]
        self.foodcoordinates=list(range(0,401,50))
        self.food=self.Body(100,100,45,45,0,(255,255,0))

    def main_loop(self):
        self.run=True
        i=0
        while self.run:
            self.clock.tick(24)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.run=False

            self.strore_key_events()
            self.change_direction()

            if i%10==0:
                self.move_snake_body()
                self.check_food_is_found()
                self.check_eaten_himself()
                self.redefine_game_window()
            i+=1
        
        self.exit_game()

            
    def strore_key_events(self):
        self.key_events=pygame.key.get_pressed()

    def change_direction(self):
        if not self.up and (self.key_events[pygame.K_DOWN] or self.shared_obj['0']=='thumbs down'):
            self.right=False
            self.left=False
            self.up=False
            self.down=True
            print('down...')
        if not self.down and (self.key_events[pygame.K_UP] or self.shared_obj['0']=='thumbs up'):
            self.right=False
            self.left=False
            self.up=True
            self.down=False
            
        if not self.right and (self.key_events[pygame.K_LEFT] or self.shared_obj['0']=='okay'):
            self.right=False
            self.left=True
            self.up=False
            self.down=False
        if not self.left and (self.key_events[pygame.K_RIGHT] or self.shared_obj['0']=='peace'):
            self.right=True
            self.left=False
            self.up=False
            self.down=False

    def move_snake_body(self):
        if len(self.bodyparts)!=1:
            l=len(self.bodyparts)-1
            while l!=0:
                if self.bodyparts.index(self.bodyparts[l])!=0:
                    if self.bodyparts[l][0]!=self.bodyparts[l-1][0]:
                        move=self.bodyparts[l-1][0]
                        self.bodyparts[l][0]=move
                    elif self.bodyparts[l][1]!=self.bodyparts[l-1][1]:
                        move=self.bodyparts[l-1][1]
                        self.bodyparts[l][1]=move
                l-=1
        if self.right:
            move=self.bodyparts[0][0]
            move+=50
            self.bodyparts[0][0]=move
        elif self.left:
            move=self.bodyparts[0][0]
            move-=50
            self.bodyparts[0][0]=move
        elif self.up:
            move=self.bodyparts[0][1]
            move-=50
            self.bodyparts[0][1]=move
        elif self.down:
            move=self.bodyparts[0][1]
            move+=50
            self.bodyparts[0][1]=move
        if self.bodyparts[0][0]>self.winx-50:
            self.bodyparts[0][0]=0
        elif self.bodyparts[0][0]<0:
            self.bodyparts[0][0]=self.winx-50
        if self.bodyparts[0][1]>self.winy-50:
            self.bodyparts[0][1]=0
        elif self.bodyparts[0][1]<0:
            self.bodyparts[0][1]=self.winy-50

        

    def check_food_is_found(self):
        if self.food.x == self.bodyparts[0][0] and self.food.y == self.bodyparts[0][1]:
            self.score += 1
            self.food.x = self.foodcoordinates[randint(0, 8)]
            self.food.y = self.foodcoordinates[randint(0, 8)]
            body_on_food = False
            while not body_on_food:
                for body in self.bodyparts:
                    if body[0] == self.food.x and body[1] == self.food.y:
                        self.food.x = self.foodcoordinates[randint(0, 8)]
                        self.food.y = self.foodcoordinates[randint(0, 8)]
                        break
                    else:
                        body_on_food = True

            if len(self.bodyparts) == 1:  # add body if only the head exists
                if self.right:
                    coordx = self.bodyparts[0][0]
                    coordy = self.bodyparts[0][1]
                    self.bodyparts.append([coordx-50, coordy])
                elif self.left:
                    coordx = self.bodyparts[0][0]
                    coordy = self.bodyparts[0][1]
                    self.bodyparts.append([coordx+50, coordy])
                elif self.up:
                    coordx = self.bodyparts[0][0]
                    coordy = self.bodyparts[0][1]
                    self.bodyparts.append([coordx, coordy+50])
                elif self.down:
                    coordx = self.bodyparts[0][0]
                    coordy = self.bodyparts[0][1]
                    self.bodyparts.append([coordx, coordy-50])
            else: # if not only the head exists
                if self.bodyparts[len(self.bodyparts)-1][0] < self.bodyparts[len(self.bodyparts)-2][0]:
                    coordx = self.bodyparts[len(self.bodyparts)-1][0]-50
                    coordy = self.bodyparts[len(self.bodyparts)-1][1]
                    self.bodyparts.append([coordx, coordy])
                elif self.bodyparts[len(self.bodyparts)-1][0] > self.bodyparts[len(self.bodyparts)-2][0]:
                    coordx = self.bodyparts[len(self.bodyparts)-1][0]+50
                    coordy = self.bodyparts[len(self.bodyparts)-1][1]
                    self.bodyparts.append([coordx, coordy])
                elif self.bodyparts[len(self.bodyparts)-1][1] > self.bodyparts[len(self.bodyparts)-2][1]:
                    coorx = self.bodyparts[len(self.bodyparts)-1][0]
                    coory = self.bodyparts[len(self.bodyparts)-1][1]+50
                    self.bodyparts.append([coorx, coory])
                elif self.bodyparts[len(self.bodyparts)-1][1] < self.bodyparts[len(self.bodyparts)-2][1]:
                    coordx = self.bodyparts[len(self.bodyparts)-1][0]
                    coordy = self.bodyparts[len(self.bodyparts)-1][1]-50
                    self.bodyparts.append([coordx, coordy])
    
    def check_eaten_himself(self):
        l=0
        for body in self.bodyparts:
            if l!=0:
                if self.bodyparts[0][0]==body[0] and self.bodyparts[0][1]==body[1]:
                    self.run=False
                    print('Ohh...You ate yourself')
            l+=1
        if len(self.bodyparts)!=1:
            if self.bodyparts[0][0]==self.bodyparts[len(self.bodyparts)-1][0] and self.bodyparts[0][1]==self.bodyparts[len(self.bodyparts)-1][1]:
                self.run=False
                print('Ohh...You ate yourself')
    
    def redefine_game_window(self):
        self.win.fill((255,255,255))

        self.food.draw(self.win)
        if self.bodyparts:
            for bodykoordinates in self.bodyparts:
                if self.bodyparts.index(bodykoordinates)==0:
                    pygame.draw.rect(self.win,(100,0,100),(bodykoordinates[0],bodykoordinates[1],45,45))
                else:
                    pygame.draw.rect(self.win,(200,200,0),(bodykoordinates[0],bodykoordinates[1],45,45))
        scoretext=self.my_font.render('Score: '+str(self.score),1,(100,100,100))
        self.win.blit(scoretext,(20,20))
        pygame.display.update()


if __name__=='__main__':
    game_win_args={'shared_obj':{'0':''}}
    game=SnakeGame(**game_win_args)
    game.main_loop()
    