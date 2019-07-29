import pygame
from PIL import Image

pygame.init()
global state

state = 0

display_width = 480
display_height = 640
obstacle_width = 60
obstacle_height = display_height



black = (0,0,0)
white = (255,255,255)
sky_blue = (167, 196, 242)

display = pygame.display.set_mode((display_width, display_height))
display.fill(white)
display_rect = display.get_rect()
pygame.display.set_caption("Flappy Fruit")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

#image loading
start_background = pygame.image.load('./images/background.png')

class Strawberry(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('./images/strawberry.png')
        self.image = pygame.transform.scale(img, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = (display_width / 4, display_height / 2)
    
    def update(self):
        self.rect.y += 1


    def movement(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.rect.y -= 5
                    print("move")

    def collision(self):
        if self.rect.top < 0 or self.rect.bottom > display_height:
            global state
            state = 2
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init_(self):
        pygame.sprite.Sprite.init(self)
        self.image = pygame.Surface((50, randrange ))

        

def text_display_center(text, font, font_size, color, y_coord):
    text_font = pygame.font.SysFont(font, font_size)
    text_display = text_font.render(text, False, white)
    text_surface = text_display.get_rect()
    text_surface.center = (display_width/2, y_coord)
    display.blit(text_display,text_surface)






def main():
    run = True
    state = 0
    strawberry = Strawberry()
    all_sprites.add(strawberry)
    while run:
        clock.tick(60)
        events = pygame.event.get()
        strawberry.movement()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        if state == 0:
            display.blit(start_background,(0,0))
            text_display_center('Flappy Fruit', "Calibri", 60, white,
                 display_height/2)
            text_display_center('<Press Space to Continue>', "Calibri", 
                30, white, display_height/2 + 50)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    display.fill(sky_blue)
                    state = 1
                    
                    

        if state == 1:
            pygame.event.pump()
            strawberry.collision()
            strawberry.movement()
            all_sprites.update()
            all_sprites.draw(display)

        if state == 2:
            display.fill(white)
            text_display_center('Game Over', 'Calibri', 60, black, display_height/2)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = 0
        
        print(state)
        pygame.display.flip()

main()