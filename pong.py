import pygame as pg
from random import randint ,random
import sys
pg.init()
pg.font.init()
pg.mixer.init()

#varibles
Screen_width,Screen_height = 900,600
player_speed = 6
enemy_speed = 3
ball_speed = [-4,3]
gameRunning = False
game_mode_easy = False
game_mode_hard = False
mode = 0
clock = pg.time.Clock()
score_player = 0
score_enemy = 0

#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

#56 X 200
PADDLESIZE = [8,70]
BALLSIZE = [10,10]
screen = pg.display.set_mode((Screen_width,Screen_height))
pg.display.set_caption("THE EPIC PONG by tigr studio")

#images
bg_img = pg.image.load(r"images\background.png")
bg_img = pg.transform.scale(bg_img,(Screen_width,Screen_height))
image_name_list = ["player","enemy","ball"]
image_list = {}
for i in image_name_list:
    path  = r'images\{}.png'.format(i)
    img = pg.image.load(path)
    image_list[i]= img
score_image = pg.image.load((r"images\number.png"))
score_image = pg.transform.scale(score_image,(10,32))

#sounds
sound_volume = 0.5
music_volume = 0.1
paddle_hit = pg.mixer.Sound(r'sounds\paddleHit.ogg')
paddle_hit.set_volume(sound_volume)
boundry_hit = pg.mixer.Sound(r'sounds\impactMetal_medium_001.ogg')
boundry_hit.set_volume(sound_volume)
kill = pg.mixer.Sound(r'sounds\score.ogg')
kill.set_volume(sound_volume)
pg.mixer.music.load(r"sounds\music.mp3")
pg.mixer.music.set_volume(music_volume)

#class
class Game():
    def __init__(self,player_image,player_speed,ball_image,ball_speed,enemy_image):
        self.player_image = player_image
        self.player_image = pg.transform.scale(self.player_image,PADDLESIZE)
        self.player_rect = self.player_image.get_rect()
        self.player_rect.center = (self.player_image.get_width()*3,Screen_height//2)
        self.player_speed = player_speed
        #ball
        self.ball_image = ball_image
        self.ball_image = pg.transform.scale(self.ball_image,BALLSIZE)
        self.ball_rect = self.ball_image.get_rect()
        self.ball_rect.center = (Screen_width//2,Screen_height//2)
        self.ball_speed = ball_speed
        #enemy
        self.enemy_image = enemy_image
        self.enemy_image = pg.transform.scale(self.enemy_image,PADDLESIZE)
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.center = (Screen_width-self.enemy_image.get_width()*3,Screen_height//2)
        
    def player_update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.player_rect.top > 10:
            self.player_rect.centery -= self.player_speed
        elif keys[pg.K_DOWN] and self.player_rect.bottom < Screen_height - 10:
            self.player_rect.centery += self.player_speed
        else:
            self.player_rect.centery += 0
        screen.blit(self.player_image,self.player_rect)

    def ball_update(self):
        global score_player , score_enemy
        self.time = pg.time.get_ticks()
        #ball after death
        if (self.ball_rect.left >= Screen_width - self.ball_image.get_width()):
            kill.play()
            pg.time.wait(1000)
            self.ball_rect.center = (Screen_width//2,Screen_height//2)
            self.ball_speed[0] *= -1
            self.ball_speed[1] *= -1
            score_player += 1
        #top and bottom
        if (self.ball_rect.top <= 10):
            boundry_hit.play()
            self.ball_speed[1] *= -1
        if (self.ball_rect.bottom > Screen_height - 10):
            boundry_hit.play()
            self.ball_speed[1] *= -1
        #player collision
        if self.ball_rect.right <= self.ball_image.get_width():
            kill.play()
            pg.time.wait(1000)
            self.ball_rect.center = (Screen_width//2,Screen_height//2)
            self.ball_speed[0] *= -1
            self.ball_speed[1] *= -1
            score_enemy += 1
        if self.ball_rect.colliderect(self.player_rect):
            if abs(self.ball_rect.left - self.player_rect.right) <= 5:
                paddle_hit.play()
                self.ball_speed[0] *= -1
        #enemy collision
        if (self.ball_rect.right >= Screen_width + self.ball_image.get_width()*2):
            self.ball_rect.center = (Screen_width//2,Screen_height//2)   
        if self.ball_rect.colliderect(self.enemy_rect):
            if abs(self.enemy_rect.left - self.ball_rect.right) <= 5:
                paddle_hit.play()
                self.ball_speed[0] *= -1
        self.ball_rect.centerx -= self.ball_speed[0]
        self.ball_rect.centery -= self.ball_speed[1]
        screen.blit(self.ball_image,self.ball_rect)

    def enemy_update(self):
        if (self.ball_rect.y < self.enemy_rect.top) and self.ball_rect.x >= Screen_width // 2:
            self.enemy_rect.y  -= (enemy_speed+mode)    
        if (self.ball_rect.y > self.enemy_rect.bottom)and self.ball_rect.x >= Screen_width // 2:
            self.enemy_rect.y  += (enemy_speed + mode)
        screen.blit(self.enemy_image,self.enemy_rect)

def draw_score(score,x,y,space):
    a = score
    #a=5
    for i in range(a):
        screen.blit(score_image,(x+i*space,y))

def drawFont(surf,text,size,color,color2,x,y):
    font = pg.font.SysFont("comicsansms",size)
    text_surface = font.render(text,True,color,color2)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    surf.blit(text_surface, text_rect)
    return text_rect , text_surface

def gameoverscreen():    
    global gameRunning ,game_mode_easy,game_mode_hard , ball_speed , mode , enemy_speed ,PADDLESIZE,BALLSIZE
    screen.fill((180,184,149))
    while not gameRunning:
        pos = pg.mouse.get_pos()
        Easy = drawFont(screen,"Easy",64,(35,34,43),(187,189,189),Screen_width//2 - 128,Screen_height//2)
        Hard = drawFont(screen,"Hard",64,(35,34,43),(187,189,189),Screen_width//2 + 128,Screen_height//2)
        Exit = drawFont(screen,"Exit",32,(3,3,27),(187,189,189),Screen_width//2,Screen_height//2 + Easy[1].get_height()*1.25)
        for event in pg.event.get():
            if Easy[0].collidepoint(pos):
                if pg.mouse.get_pressed()[0]:
                    game_mode_easy = True
                    gameRunning = True
            elif Hard[0].collidepoint(pos):
                if pg.mouse.get_pressed()[0]:
                    game_mode_hard = True
                    gameRunning = True                 
            if Exit[0].collidepoint(pos):
                if pg.mouse.get_pressed()[0]:
                    pg.quit()
                    sys.exit()        
        if game_mode_easy:
            mode = random()
            BALLSIZE = [20,20]
        elif game_mode_hard:
            PADDLESIZE = [8,35]
            ball_speed = [-5,3]
            enemy_speed = 6
        else:
            mode = randint(-1,1)
        pg.display.flip()
                
def draw_bg(image):
    screen.blit(image,(0,0))

#actors
game = Game(image_list["player"],player_speed,image_list["ball"],ball_speed,image_list["enemy"])
#main screen
pg.mixer.music.play(loops=-1)
run = True
while run:
    clock.tick(120)
    gameoverscreen()
    draw_bg(bg_img)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            exit
    game.player_update()
    game.enemy_update()
    game.ball_update()
    draw_score(score_enemy,Screen_width//2 + 100,16,16)
    draw_score(score_player, 100,16,16)
    pg.display.flip()
pg.quit()
