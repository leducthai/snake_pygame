import pygame
from datetime import timedelta, datetime
from random import choice
from collections import OrderedDict

scr_width , scr_height = 800 , 600
play_width , play_height = 600 , 600

class poob:
    def __init__(self ) -> None:
        self.archieve = OrderedDict()
        self.poob_color = (153 , 153 , 0)

    def is_in(self , xy):
        if self.archieve.get(xy , None) != None:
            return True
        return False

    def check_exp(self):
        ls = list(self.archieve.keys())
        if ls:
            kei = ls[0]
            if self.archieve[kei] <= datetime.now():
                self.archieve.pop(kei)

    def add_poob(self , xy):
        if self.archieve.get(xy , None) != None:
            self.archieve.pop(xy)
        self.archieve[xy] = datetime.now() + timedelta(seconds=5.1)

    def draw_poobs(self , screen):
        for i , j in self.archieve.keys():
            pygame.draw.rect(screen , self.poob_color , (j*10 , i*10 , 10 , 10))


class snake_infor:
    def __init__(self) -> None:
        self.color = [(102 , 153 , 0) , (51 , 102 , 0) , (102 , 153 , 51) , (0 , 204 , 0) , (0 , 51 , 0) , (0 ,255 , 0) , (0 , 153 , 102) , (0 , 102 , 51)]
        self.sick_color = [(255 , 102 , 102) , (255 , 204 , 153) , (153 , 102 , 102) , (255 , 102 , 51) , (255  ,204 , 51) , (255 , 51 , 51), (255 , 255 , 0) , (153 , 0 , 102) , (102 , 0 , 153) , (153 , 0 , 51) , (204 , 0 , 51)]
        self.pos = [(30,30) , (30,31)]
        self.dir = 'l'
        self.is_sick = False
        self.sick_exp = 0

    def move_head(self ):
        if self.dir == 'l':
            self.pos.append((self.pos[-1][0] , self.pos[-1][1] - 1))
        if self.dir == 'r':
            self.pos.append((self.pos[-1][0] , self.pos[-1][1] + 1))
        if self.dir == 'u':
            self.pos.append((self.pos[-1][0] - 1 , self.pos[-1][1]))
        if self.dir == 'd':
            self.pos.append((self.pos[-1][0] + 1 , self.pos[-1][1]))
    
    def move_tail(self):
        self.pos.pop(0)
    
    def get_color_nomal(self):
        return choice(self.color)

    def get_sick_cl(self):
        return choice(self.sick_color)

    def lost(self):
        a , b = self.pos[-1]
        if (a , b) in self.pos[:-1]:
            return True
        if 0 > a or a > 59 or 0 > b or b > 59:
            return True
        return False

    def draw_snake(self , screen):
        if self.is_sick:
            for x , y in self.pos:
                pygame.draw.rect(screen , self.get_sick_cl() , (y*10 , x*10 , 10 , 10))
        else:
            for x , y in self.pos:
                pygame.draw.rect(screen , self.get_color_nomal() , (y*10 , x*10 , 10 , 10))


def draw_init(screen):
    pygame.draw.rect(screen , (255 , 153 , 102) , (600 , 0 , 200 , 600))
    pygame.draw.rect(screen , (255 , 102 , 51) , (610 , 300 , 180 , 50) , 1)
    pygame.draw.rect(screen , (153 , 51 , 51) , (650 , 500 , 100 , 50))

def draw_infor(screen , score):
    font_snake_game = pygame.font.SysFont('Arial' , size= 50 , bold= True)
    text1 = font_snake_game.render("SNAKE" , True , (0 , 51 , 51))
    text5 = font_snake_game.render("game" , True , (0 , 51 , 51))

    font_score = pygame.font.SysFont('Arial' , size=40 , bold= True)
    text2 = font_score.render("Score" , True ,(0 , 51 , 0))

    font_num = pygame.font.SysFont("Arial" , size=30 , bold= True)
    text3 = font_num.render(str(score) , True , (0 , 0 , 0) )

    font_retry = pygame.font.SysFont('Arial' , size=30 , bold= True)
    text4 = font_retry.render("Retry" , True , (153 , 0 , 0))

    screen.blit(text1 , (620 , 50))
    screen.blit(text5 , (650 , 100))
    screen.blit(text2 , (650 , 250))
    screen.blit(text3 , (620 , 310))
    screen.blit(text4 , (660 , 510))

def draw_game_over(screen):
    font = pygame.font.SysFont('Arial' , size= 50 , bold= True)
    text = font.render('Game Over' , True , (255,255,255))
    screen.blit(text , (150 , 275))

def get_pos(sn_ar , po_ar):
    x = choice(range(60))
    y = choice(range(60))
    while True:     
        if (x , y) in sn_ar or po_ar.is_in((x , y)):
            x = choice(range(60))
            y = choice(range(60))
        else:
            break
    return (x , y) 

def draw_apple(screen , pos):
    pygame.draw.rect(screen , (255 , 0 , 0) , (pos[1]*10 , pos[0]*10 , 10 , 10 ))


def main():
    go = True
    while go:
        pygame.init()
        screen = pygame.display.set_mode((scr_width , scr_height))
        score = 0
        snake = snake_infor()
        poob_ls = poob()
        run = True
        speed = 0.1
        time_count = 0
        clock = pygame.time.Clock()
        can_change_dir = True
        apple_pos = get_pos(snake.pos , poob_ls)
        game_over = True

        while run:
            screen.fill((0,0,0))
            poob_ls.check_exp()
            if snake.is_sick == True:
                if snake.sick_exp <= datetime.now():
                    snake.is_sick = False

            time_count += clock.get_rawtime()
            clock.tick()

            if time_count / 1000 >= speed:
                time_count = 0
                snake.move_head()
                can_change_dir = True
                
                if snake.pos[-1] == apple_pos:
                    apple_pos = get_pos(snake.pos , poob_ls)
                    poob_ls.add_poob(snake.pos[0])
                    score += 1
                elif poob_ls.is_in(snake.pos[-1]):
                    snake.is_sick = True
                    snake.sick_exp = datetime.now() + timedelta(seconds=5)
                    snake.move_tail()
                    poob_ls.archieve.pop(snake.pos[-1])
                else:
                    snake.move_tail()
                if snake.lost():
                    run = False
                    game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    go = False
                    game_over = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mous_x , mous_y = pygame.mouse.get_pos()
                    if event.button == 1 and 650 <= mous_x <= 750 and 500 <= mous_y <= 550:
                        run = False
                        game_over = False
                        go = True

                if event.type == pygame.KEYDOWN:
                    if snake.is_sick == False:
                        if event.key == pygame.K_DOWN:
                            if snake.dir not in ['u' , 'd'] and can_change_dir:
                                snake.dir = 'd'
                                can_change_dir = False
                        if event.key == pygame.K_UP:
                            if snake.dir not in ['u' , 'd'] and can_change_dir:
                                snake.dir = 'u'
                                can_change_dir = False
                        if event.key == pygame.K_LEFT:
                            if snake.dir not in ['l' , 'r'] and can_change_dir:
                                snake.dir = 'l'
                                can_change_dir = False
                        if event.key == pygame.K_RIGHT:
                            if snake.dir not in ['l' , 'r'] and can_change_dir:
                                snake.dir = 'r'
                                can_change_dir = False
                    else:
                        if event.key == pygame.K_DOWN:
                            if snake.dir not in ['u' , 'd'] and can_change_dir:
                                snake.dir = 'u'
                                can_change_dir = False
                        if event.key == pygame.K_UP:
                            if snake.dir not in ['u' , 'd'] and can_change_dir:
                                snake.dir = 'd'
                                can_change_dir = False
                        if event.key == pygame.K_LEFT:
                            if snake.dir not in ['l' , 'r'] and can_change_dir:
                                snake.dir = 'r'
                                can_change_dir = False
                        if event.key == pygame.K_RIGHT:
                            if snake.dir not in ['l' , 'r'] and can_change_dir:
                                snake.dir = 'l'
                                can_change_dir = False

            poob_ls.draw_poobs(screen)
            draw_apple(screen , apple_pos)
            snake.draw_snake(screen)
            draw_init(screen )
            draw_infor(screen , score)
            pygame.display.update()
        
        while game_over:
            screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    go = False
                    game_over = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mous_x , mous_y = pygame.mouse.get_pos()
                    if event.button == 1 and 650 <= mous_x <= 750 and 500 <= mous_y <= 550:
                        game_over = False
                        go = True

            draw_game_over(screen)
            draw_init(screen )
            draw_infor(screen , score)
            pygame.display.update()




main()
    