import pygame, sys, os, random

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Last Tower')
size = width, height = 600, 500
screen = pygame.display.set_mode(size,0,32)

font = pygame.font.SysFont(None, 30)
 
def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("tower.png", -1, scale = 0.5)
        self.rect.center = (300,250)
        screen = pygame.display.get_surface()
        self.fist_offset = (-235, -80)
        self.life = 5000
        self.punching = False

class Wizard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("wizard.jpeg", -1, scale = 0.4)
        self.rect.center = (random.randrange(50,550),random.randrange(50,450))
        screen = pygame.display.get_surface()
        self.fist_offset = (-235, -80)
        self.amount = 100

class Aim(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("aim.png", -1, scale = 0.5)
        self.fist_offset = (-50, -50)
        self.punching = False

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        self.punching = False

def main_menu():
    click = False
    while True:

        pygame.mouse.set_visible(True)
 
        screen.fill((0,190,255))
        draw_text('Choose difficulty:', font, (0,0,0), screen, 210, 40)
 
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(200, 100, 200, 50)
        button_2 = pygame.Rect(200, 180, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game("EASY")
        if button_2.collidepoint((mx, my)):
            if click:
                game("HARD")
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
 
        draw_text('EASY', font, (255,255,255), screen, 270, 115)
        draw_text('HARD', font, (255,255,255), screen, 270, 195)


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
def game(difficulty):
    amount = 100 if difficulty == "EASY" else 500
    speed = [3,3] if difficulty == "EASY" else [5,5]
    pygame.mouse.set_visible(False)
    tower = Tower()
    score = 0
    wizard = Wizard()    
    aim = Aim()
    ob = pygame.sprite.Group(wizard)
    allsprites = pygame.sprite.RenderPlain((tower, wizard, aim))

    running = True
    while running:
        mainClock.tick(60)
        screen.fill((0,128,0))
       
        draw_text("Mode: %s" % difficulty, font, (255, 255, 255), screen, 20, 20)
        draw_text("Score: %s" % score, font, (255, 255, 255), screen, 400, 20)
        draw_text("Defense: %s" % tower.life, font, (255, 255, 255), screen, 400, 40)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if aim.punch(wizard):
                    wizard = Wizard()
                    allsprites = pygame.sprite.RenderPlain((tower, wizard, aim))
                    ob = pygame.sprite.Group(wizard)
                    score += 100

            elif event.type == pygame.MOUSEBUTTONUP:
                aim.unpunch()
                next
        
        wizard.rect = wizard.rect.move(speed)
        if wizard.rect.left < 0 or wizard.rect.right > width:
            speed[0] = -speed[0]
        if wizard.rect.top < 0 or wizard.rect.bottom > height:
            speed[1] = -speed[1]

        collided = pygame.sprite.spritecollide(tower, ob, True)
        for i in collided:
            tower.life -= amount
            if tower.life > 0:
                wizard = Wizard()
                allsprites = pygame.sprite.RenderPlain((tower, wizard, aim))
                ob = pygame.sprite.Group(wizard)
            else:
                game_over(difficulty=difficulty, score=score)
                running = False

        allsprites.update()

        screen.blit(screen, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

def game_over(difficulty, score):
    running = True
    while running:
        pygame.mouse.set_visible(True)
        pygame.display.update()
        mainClock.tick(60)
        screen.fill((0,0,0))
        
        draw_text("Mode: %s" % difficulty, font, (255, 255, 255), screen, 20, 20)
        draw_text("Score: %s" % score, font, (255, 255, 255), screen, 400, 20)
        draw_text("GAME OVER", pygame.font.SysFont(None, 50), (255, 0, 0), screen, 190, 200)
        draw_text("Press Esc to play again, you can do better ;)", font, (255, 255, 255), screen, 90, 270)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

main_menu()
