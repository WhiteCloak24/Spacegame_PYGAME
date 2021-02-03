#MODULES
import pygame
import os
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w
pygame.font.init()

# CONSTANTS
WIDTH, HEIGHT = 900 , 500
FPS = 60
WHITE= (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
SHIP_WIDTH,SHIP_HEIGHT = 50,40
MOVE = 5
B_Vel = 8
MAX_BULLETS = 3


RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2



BORDER = pygame.Rect(WIDTH/2,0,10,HEIGHT)
BLUE_SHIP_IMAGE = pygame.image.load(r'F:\pygames\imgs\blus.png')
BLUE_SHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SHIP_IMAGE, (SHIP_WIDTH,SHIP_HEIGHT)), 220)
RED_SHIP_IMAGE = pygame.image.load(r'F:\pygames\imgs\reds.jpg')
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE,(SHIP_WIDTH,SHIP_HEIGHT)), 90)
SPACE = pygame.transform.scale(pygame.image.load(r'F:\pygames\imgs\space.png'), (WIDTH, HEIGHT))
Health_Font = pygame.font.SysFont('comicsans', 40)
Winner_Font = pygame.font.SysFont('comicsans' , 80,bold = True)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('First Game')

def window_update(blue,red,R_Bullets,B_Bullets,red_health,blue_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    R_HEALTH = Health_Font.render('Health: ' + str(red_health),1, RED)
    B_HEALTH = Health_Font.render('Health: ' + str(blue_health),1, BLUE)
    
    WIN.blit(BLUE_SHIP,(blue.x,blue.y))
    WIN.blit(RED_SHIP,(red.x,red.y))
    WIN.blit(R_HEALTH, (WIDTH - R_HEALTH.get_width()-175,50) )
    WIN.blit(B_HEALTH, (175,50) )
    for bullet in R_Bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in B_Bullets:
        pygame.draw.rect(WIN,BLUE, bullet)

    pygame.display.update()

def blue_move(pressed_keys,blue):
    if pressed_keys[K_a] and blue.x - MOVE > 0:
        blue.x -= MOVE 
    if pressed_keys[K_s] and blue.y + MOVE + SHIP_HEIGHT < HEIGHT:
        blue.y += MOVE
    if pressed_keys[K_d] and blue.x + MOVE + SHIP_WIDTH < BORDER.x:
        blue.x += MOVE
    if pressed_keys[K_w] and blue.y - MOVE > 0:
        blue.y -= MOVE
def red_move(pressed_keys,red) :
    if pressed_keys[K_LEFT] and red.x - BORDER.x > 0:
        red.x -= MOVE
    if pressed_keys[K_DOWN] and red.y + MOVE+ SHIP_HEIGHT < HEIGHT:
        red.y += MOVE
    if pressed_keys[K_RIGHT] and red.x - WIDTH + SHIP_WIDTH < 0:
        red.x += MOVE
    if pressed_keys[K_UP] and red.y - MOVE > 0:
        red.y -= MOVE

def bullet_move(red,blue,R_Bullets,B_Bullets):
    for bullet in R_Bullets:
        bullet.x -= B_Vel
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            R_Bullets.remove(bullet)
        elif bullet.x < 0 :
            R_Bullets.remove(bullet)
    for bullet in B_Bullets:
        bullet.x += B_Vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            B_Bullets.remove(bullet)
        elif bullet.x > WIDTH:
            B_Bullets.remove(bullet)
def Winner(text):
    WINNER = Winner_Font.render(text,1,GREEN)
    WIN.blit(WINNER,(WIDTH/2 - WINNER.get_width()/2,HEIGHT/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(200,250,SHIP_WIDTH,SHIP_HEIGHT)
    red = pygame.Rect(675,250,SHIP_WIDTH,SHIP_HEIGHT)

    blue_health = 10
    red_health = 10

    R_Bullets = []
    B_Bullets = []
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(B_Bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + SHIP_WIDTH ,blue.y+blue.height/2  + 10 ,10,5)
                    B_Bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(R_Bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y+red.height/2 ,10,5)
                    R_Bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == BLUE_HIT:
                blue_health -= 1
        winner =''
        if red_health <= 0:
            winner = 'Winner is BLUE'
        if blue_health <= 0:
            winner = 'Winner is RED'
        if winner != '':
            Winner(winner)
            break
        
        pressed_keys = pygame.key.get_pressed()
        blue_move(pressed_keys,blue)
        red_move(pressed_keys,red)
        bullet_move(red,blue,R_Bullets,B_Bullets)
        window_update(blue,red,R_Bullets,B_Bullets,red_health,blue_health)
        
    pygame.quit()

if __name__ == '__main__':
    main() 
