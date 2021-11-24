import pygame
from random import randint
import multiprocessing as mp
from gesture_detection import GestureRecognition

class GameWindow:
    '''
    Class which every game should inherit.
    Initialises the game window, like a stage for the game, everything happens here.

    Params
    ======

    winx,winy: size of the window
    clock: every pygame game needs a clock. Determines how many frames will happen in each second.
    my_font: declares default font
    sahred_obj: python multiprocessing.Manager().dict() object. Enables gestures. (form:{'0':''})

    '''
    def __init__(self,window_title:str='snake',winx:int=600,winy:int=600,font_style:str='monospace',font_size:int=16) -> None:
        pygame.init()
        self.winx=winx
        self.winy=winy
        self.win=pygame.display.set_mode((winx,winy)) # defining the size of the game window
        pygame.display.set_caption(window_title) # window title
        self.clock=pygame.time.Clock() # init clock : this will define how many frames we are gonn have each sec
        self.my_font=pygame.font.SysFont(font_style,font_size) # defoault font
    
    def exit_game(self):
        '''Simply quitting from the program'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
    
    



class SnakeGame(GameWindow):
    '''
    SnakeGame inherits GameWindow

    Params
    ======

    score: you get a score each time you eat food with the snake
    run: bool for the main loop
    up,down,right,left: indicates the direction of the snake\'s head
    bodyparts: coordinate of every bodypart
    food: the exact renderable food element
    '''
    class Body:
        '''
        Represents any element on the map (food, snake head, sneak body).
        
        Params
        =======
        
        x,y : position of the element
        weight,height: size of the elment
        vel: velocity (it vill add vel to the x or the y every time the snake moves)
        colour: color of the element

        '''
        def __init__(self,x,y,width,height,vel,colour,distance=0):
            self.x=x
            self.y=y
            self.width=width
            self.height=height
            self.vel=vel
            self.distance=distance
            self.colour=colour
        def draw(self,win):
            '''Rendering the element'''
            pygame.draw.rect(win,self.colour,(self.x,self.y,self.width,self.height))

        
    def __init__(self) -> None:
        super().__init__()
        self.score=0
        self.run=False
        self.right=False
        self.left=False
        self.up=False
        self.down=True
        self.bodyparts=[[0,0]]
        self.foodcoordinates=list(range(0,401,50))
        self.food=self.Body(100,100,45,45,0,(255,255,0))

        self.manager=mp.Manager()
        self.shared_obj=self.manager.dict()
        self.shared_obj['0']=''

        self.gesture_detection_class=GestureRecognition(self.shared_obj)

    def main_loop(self):
        '''
        Main loop of the game.
        Everythin happens here.
        '''
        self.start_gesrure_recognition()
        self.run=True
        i=0
        while self.run:
            self.clock.tick(24) # the game will display 24 frames per second
            for event in pygame.event.get(): # check if an exit event occurs
                if event.type==pygame.QUIT:
                    self.run=False

            self.strore_key_events()
            self.change_direction()

            if i%10==0: # indicates that in every second the snake can only move at max twice
                self.move_snake_body()
                self.check_food_is_found()
                self.check_eaten_himself()
                self.redefine_game_window()
            i+=1
        
        self.exit_game() # after the main loop we exit the game

            
    def strore_key_events(self):
        '''Storing the key-press events.'''
        self.key_events=pygame.key.get_pressed()

    def change_direction(self):
        '''
        Set direction of the snake\'s head. 
        You can change the direction with the arrow keys or with the given gestures.
        up: thumbs up
        right: piece
        down: thumbs down
        left: left
        Gestures are obtained from a dict shared object.
        '''
        if not self.up and (self.key_events[pygame.K_DOWN] or self.shared_obj['0']=='thumbs down'):
            self.right=False
            self.left=False
            self.up=False
            self.down=True
        elif not self.down and (self.key_events[pygame.K_UP] or self.shared_obj['0']=='thumbs up'):
            self.right=False
            self.left=False
            self.up=True
            self.down=False
        elif not self.right and (self.key_events[pygame.K_LEFT] or self.shared_obj['0']=='okay'):
            self.right=False
            self.left=True
            self.up=False
            self.down=False
        elif not self.left and (self.key_events[pygame.K_RIGHT] or self.shared_obj['0']=='peace'):
            self.right=True
            self.left=False
            self.up=False
            self.down=False

    def move_snake_body(self):
        '''
        All of the coordinates of the bodyparts of the snake is in the self.bodyparts var.
        We first move the last bodypart to the place of the previous before the last bodipart and so on.
        In the end we move the head in the correct direction.
        If only the head exists we only move the head. 
        '''
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
        '''
        If the coordinate of the head of the snake (self.bodyparts[0]) is the same as the food\'s coordinates
        we add a score, place the food to a random place, and attach a new body element on the snake. 
        '''
        if self.food.x == self.bodyparts[0][0] and self.food.y == self.bodyparts[0][1]: # checking if the snake ate some food, if yes we reposition the food
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
        '''
        If the coordinates of the head is the same of any of the other bodypart\'s coordinates, the game ends.
        '''
        l=0
        for body in self.bodyparts:
            if l!=0:
                if self.bodyparts[0][0]==body[0] and self.bodyparts[0][1]==body[1]:
                    self.run=False
                    print('Ohh...You ate yourself')
            l+=1
        # if len(self.bodyparts)!=1:
        #     if self.bodyparts[0][0]==self.bodyparts[len(self.bodyparts)-1][0] and self.bodyparts[0][1]==self.bodyparts[len(self.bodyparts)-1][1]:
        #         self.run=False
        #         print('Ohh...You ate yourself')
    
    def redefine_game_window(self):
        '''
        Drawing method.
        '''
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

    def start_gesrure_recognition(self):
        proc=mp.Process(target=self.gesture_detection_class.start_gesture_detection)
        proc.start()
        #proc.join()

# import multiprocessing as mp
# mp.set_start_method('spawn')

# if __name__=='__main__':
#     game_win_args={'0':''}
    
#     game=SnakeGame(shared_obj=game_win_args)
#     process=mp.Process(target=game.main_loop)
#     process.run()
#     #process.join()
    
if __name__=='__main__':
    game=SnakeGame()
    game.main_loop()