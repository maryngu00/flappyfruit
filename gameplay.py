import pygame
from PIL import Image
import random

#Constant Values
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 200, 0)

display_width = 480
display_height = 640

pipe_space = 100

pygame.init()
window = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
state = 0




## Class of pipe obstacles
class Upper_Pipe(pygame.sprite.Sprite):
    def __init__(self, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, height]).convert_alpha()
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = 0
        self.rect.x = display_width - 50

    #automated moving to the left of the screen
    def update(self):
        self.rect.x -= 1
    

class Lower_Pipe(pygame.sprite.Sprite):
    def __init__(self,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, display_height - height - pipe_space]).convert_alpha()
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = height + pipe_space
        self.rect.x = display_width - 50
    
    #Automated moving to the left of the screen
    def update(self):
        self.rect.x -= 1

    

## Class of Strawberry characters
class Strawberry(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./images/strawberry.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = (display_width / 4, display_height / 2)
        self.mask = pygame.mask.from_surface(self.image)
    #Automatic falling on screen without key presses
    def update(self):
        self.rect.y += 1


    def flap(self):
        self.rect.y -= 5
        

        

## Game object to initialize gameplay, characters, and obstacles
class Game(object):
    def __init__(self):
        self.points = 0
        self.gameover = False

        #self.obstacle_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()

        
        self.top_pipe = Upper_Pipe(200)
        self.bottom_pipe = Lower_Pipe(200)

        #if top_pipe.rect.left < 0 and bottom_pipe.rect.left < 0:
         #   new_height = random.choice([100, 200, 300, 400, 500])
          #  top_pipe = Upper_Pipe(new_height)
           # bottom_pipe = Lower_Pipe(new_height)
            #self.all_sprites.add(top_pipe)
            #self.all_sprites.add(bottom_pipe)
        

        #self.obstacle_list.add(top_pipe)
        #self.all_sprites.add(top_pipe)
        #self.obstacle_list.add(bottom_pipe)
        #self.all_sprites.add(bottom_pipe)

        self.character = Strawberry()
        self.all_sprites.add(self.character)

    

    def event_handler(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.character.flap()
        #if self.character.rect.top < 0 or self.character.rect.bottom > display_height:
         #   self.gameover = True
        if self.top_pipe.rect.left < 0 and self.bottom_pipe.rect.left < 0:
            new_height = random.choice([100, 200, 300, 400, 500])
            self.top_pipe = Upper_Pipe(new_height)
            self.bottom_pipe = Lower_Pipe(new_height)
            self.all_sprites.add(self.top_pipe)
            self.all_sprites.add(self.bottom_pipe)
        
        pygame.display.flip()
        return False


    def game_logic(self):
        if self.gameover == False:
            self.all_sprites.update()

    def screen_display(self, window):
        #condition to make gameover true (collision)
        window.fill((0,0,255))
        if self.gameover == True:
            window.fill((255,0,0))
        
        if self.gameover == False:
            self.all_sprites.draw(window)

        pygame.display.flip()



def intro_screen(window):
    start_screen = True
    while start_screen == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen = False
        window.fill(white)
        text_font = pygame.font.SysFont('Calibri', 60)
        text_display = text_font.render('Flappy Fruit', False, black)
        text_surface = text_display.get_rect()
        text_surface.center = (display_width/2, display_height/2)
        window.blit(text_display,text_surface)
        pygame.display.flip()

def main():
    new_game = Game()
    done = False
    while done == False:
        done = new_game.event_handler(window)
        new_game.game_logic()
        new_game.screen_display(window)
        clock.tick(190)

    pygame.quit()

intro_screen(window)
main()

