import pygame
import enum
import random
from PIL import Image

pygame.init()

#Set constant variables
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 640
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = DISPLAY_HEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (167, 196, 242)
GREEN = (0, 255, 0)

all_sprites = pygame.sprite.Group()

#Load images
title_background = pygame.image.load('./images/background.png')
strawberry_image = pygame.image.load('./images/strawberry.png')
gameover_bg = pygame.image.load('./images/background2.png')

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Flappy Fruit')
clock = pygame.time.Clock()

class GameStates(enum.Enum):
    title = 0
    play = 1
    gameover = 2

class Strawberry(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = strawberry_image
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAY_WIDTH / 4, DISPLAY_HEIGHT / 2)
        self.mask = pygame.mask.from_surface(self.image)
    #Automatic falling on screen without key presses
    def fall(self):
        self.rect.y += 2
        #print(self.rect.x)

    def flap(self):
        self.rect.y -= 8

class Upper_Pipe(pygame.sprite.Sprite):
    def __init__(self, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, height]).convert_alpha()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = 0
        self.speed = 1
        self.rect.x = DISPLAY_WIDTH - 50

    #automated moving to the left of the screen
    def update(self):
        self.rect.x -= self.speed
        

class Lower_Pipe(pygame.sprite.Sprite):
    def __init__(self,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, height]).convert_alpha()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = DISPLAY_HEIGHT - height
        self.rect.x = DISPLAY_WIDTH - 50
        self.speed = 1
    
    #Automated moving to the left of the screen
    def update(self):
        self.rect.x -= self.speed
        
        

#Method to display the title screen of the game
def start_screen():
    display.blit(title_background, (0,0))
    #Display the title
    title_font = pygame.font.SysFont('Calibri', 60)
    title_display = title_font.render('Flappy Fruit', False, WHITE)
    title_rect = title_display.get_rect()
    title_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 20)
    display.blit(title_display, title_rect)

    #Display to continue text
    next_font = pygame.font.SysFont('Calibri', 35)
    next_display = next_font.render('Press <SPACE> to continue', False, WHITE)
    next_rect = next_display.get_rect()
    next_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 45)
    display.blit(next_display, next_rect)

def gameover_screen():
    display.blit(gameover_bg, (0,0))
    end_font = pygame.font.SysFont('Calibri', 60)
    end_display = end_font.render('GAME OVER', False, BLACK)
    end_rect = end_display.get_rect()
    end_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    display.blit(end_display, end_rect)

def score_display(counter):
    score_font = pygame.font.SysFont('Calibri', 35)
    score_display = score_font.render(str(counter), False, BLACK)
    score_rect = score_display.get_rect()
    score_rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 4)
    display.blit(score_display, score_rect)
    


def main():
    score = 0
    done = False
    state = GameStates(0)
    #Create Sprite Groups
    obstacle_sprites = pygame.sprite.Group()
    character_sprites = pygame.sprite.Group()
    #Initialize character
    strawberry = Strawberry()
    character_sprites.add(strawberry)
    #Initialize obstacles
    init_height = random.choice([125, 225, 325])
    pipes = Upper_Pipe(init_height)
    pipes2 = Lower_Pipe(DISPLAY_HEIGHT - init_height - 200 )
    obstacle_sprites.add(pipes, pipes2)

    while done == False:
        clock.tick(120)
        #Handles events in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        if state == GameStates(0):
            start_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = GameStates(1)

        elif state == GameStates(1):
            strawberry.fall()
            pipes.update()
            pipes2.update()
            

            #Pipe collision with edge of screen
            if pipes.rect.x < -25:
                obstacle_sprites.empty()
                #Generate new pipes of different sizes
                new_height = random.choice([125, 225, 325])
                pipes = Upper_Pipe(new_height)
                pipes2 = Lower_Pipe(DISPLAY_HEIGHT - new_height - 200)
                obstacle_sprites.add(pipes, pipes2)
            
            #If pass through obstacles without collision, increment score
            if (pipes.rect.right == strawberry.rect.right):
                score += 1
           
            #Character movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    strawberry.flap()
            if strawberry.rect.y < 0 or strawberry.rect.y > DISPLAY_HEIGHT:
                state = GameStates(2)
            #Checks for pixel perfect collision using masks
            if pygame.sprite.spritecollide(strawberry, obstacle_sprites, False, pygame.sprite.collide_mask):
                state = GameStates(2)


            display.fill(SKY_BLUE)
            obstacle_sprites.draw(display)
            character_sprites.draw(display)
            score_display(score)

        elif state == GameStates(2):
            obstacle_sprites.empty()
            character_sprites.empty()
            gameover_screen()
            

        pygame.display.flip()

    pygame.quit()

main()