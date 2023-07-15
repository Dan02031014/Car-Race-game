import pygame
from pygame import mixer
import random
import time

mixer.init()
pygame.init()
pygame.font.init()

# Create game score
score = 0
score_increases = 1
font = pygame.font.SysFont('impact', 26)

score2 = 0
score_increases2 = 1
font2 = pygame.font.SysFont('impact', 26)

# Game Over fonts
game_over_font = pygame.font.SysFont('Verdana', 30)
Player1_Wasted = game_over_font.render("Player1 Wasted", True, (255, 0, 0))
Player2_Wasted = game_over_font.render("Player2 Wasted", True, (255, 0, 0))

# Create timer for USEREVENT for Enemies
pygame.time.set_timer(pygame.USEREVENT, 1200)

# colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 255, 0)

# Window dimensions and FPS
Sc_Width = 1200
Sc_Height = 700
road_size = 150
FPS = 60

# Create Window
screen = pygame.display.set_mode((Sc_Width, Sc_Height))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

# Create Bg for roads asphalt
asphalt = pygame.image.load('asphalt.png').convert_alpha()
asphalt = pygame.transform.scale(asphalt, (road_size * 6, Sc_Height))

# Create Bg for poison grass
grass = pygame.image.load('poison grass.png').convert_alpha()
grass = pygame.transform.scale(grass, (Sc_Width, Sc_Height))

# Create some dumb Sound
cd1 = pygame.mixer.Sound('Crash1.mp3')
cd1.set_volume(1)

cd2 = pygame.mixer.Sound('Crash2.mp3')
cd2.set_volume(1)

# Create sound music
fun = pygame.mixer.music.load('dumb music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# for Enemies =================================================================================================
# Upload the image for enemies
enemy_img = ('enemy_car1.png', 'enemy_car2.png', 'enemy_car3.png', 'enemy_car4.png', 'enemy_car5.png.png')
enemy_list = []  # Create empty list for enemies

# add enemy to the empty list
for i in range(len(enemy_img)):
    enemy_list.append(pygame.image.load(enemy_img[i]).convert_alpha())

class Car(pygame.sprite.Sprite):

    def __init__(self, filename, x, y, Spr_W, Spr_H):
        super().__init__()
        self.image = pygame.Surface([Spr_W, Spr_H])
        self.rect = self.image.get_rect()
        self.Spr_W = Spr_W
        self.Spr_H = Spr_H

        # Draw the car (a rectangle!)
        self.x = x
        self.y = y
        self.rect.center = (x, y)

        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Spr_H, Spr_W))
        self.image = pygame.transform.rotate(self.image, 90)
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        self.rect.y -= 0
        if self.rect.y < 0:
            self.rect.y = Sc_Width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites_list.add(bullet)
        bullets.add(bullet)

    def steering(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            car1.rect.x -= 3
        if keys[pygame.K_d]:
            car1.rect.x += 3

        if keys[pygame.K_LEFT]:
            car2.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            car2.rect.x += 3

    def speeding(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car1.rect.y -= 10
        if car1.rect.y <= Sc_Height / 10:
            car1.rect.y = Sc_Height / 10

        if keys[pygame.K_UP]:
            car2.rect.y -= 10
        if car2.rect.y <= Sc_Height / 10:
            car2.rect.y = Sc_Height / 10

    def slowing(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            car1.rect.y += 10 / 2
        if car1.rect.y >= Sc_Height - 120:
            car1.rect.y = Sc_Height - 120

        if keys[pygame.K_DOWN]:
            car2.rect.y += 10 / 2
        if car2.rect.y >= Sc_Height - 120:
            car2.rect.y = Sc_Height - 120

    def edge(self):
        if car1.rect.x <= Sc_Width / 2 - road_size * 3:
            car1.rect.x = Sc_Width / 2 - road_size * 3
        if car1.rect.x >= Sc_Width / 2 - 60:
            car1.rect.x = Sc_Width / 2 - 60

        if car2.rect.x <= Sc_Width / 2:
            car2.rect.x = Sc_Width / 2
        if car2.rect.x >= Sc_Width / 2 + road_size * 3 - 60:
            car2.rect.x = Sc_Width / 2 + road_size * 3 - 60

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, enemy_img, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, 0)
        # self.x = x
        self.image = pygame.transform.scale(self.image, (60, 120)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 0)
        # добавляем в группу
        self.add(group)
        # у машин будет разная скорость
        self.speed = random.randint(5, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > Sc_Height:
            self.kill()

class Road(pygame.sprite.Sprite):
    def __init__(self, x, y, Rect_W, Rect_H, color):
        super().__init__()
        self.image = pygame.Surface((Rect_W, Rect_H))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.color = color

        self.x = x
        self.y = y
        self.rect.center = (x, y)
        self.Rect_W = Rect_W
        self.Rect_H = Rect_H

    def update(self):
        self.rect.y += 5
        if self.rect.bottom > Sc_Height:
            self.rect.top = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -20

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Objects for all Classes: ====================================================================================
# Objects - Sprites for Car Class:
car1 = Car('car1.png', Sc_Width / 2 - (road_size + (road_size / 2)), Sc_Height - 120, 60, 120)
car2 = Car('car2.png', Sc_Width / 2 + (road_size + (road_size / 2)), Sc_Height - 120, 60, 120)

# Objects - Sprites for Road Class:
RL1 = Road(Sc_Width / 2 - road_size * 2, 0, 3, 50, White)
RL2 = Road(Sc_Width / 2 - road_size, 0, 3, 50, White)
RL3 = Road(Sc_Width / 2 + road_size, 0, 3, 50, White)
RL4 = Road(Sc_Width / 2 + road_size * 2, 0, 3, 50, White)

rect1 = Road(Sc_Width / 2 - road_size * 3, Sc_Height, 3, Sc_Height * 2, Green)
rect2 = Road((Sc_Width / 2), Sc_Height, 3, Sc_Height * 2, Yellow)
rect3 = Road(Sc_Width / 2 + road_size * 3, Sc_Height, 3, Sc_Height * 2, Green)

# List for all sprites Groups: ================================================================================
all_sprites_list = pygame.sprite.Group()

# Class Bullet Sprite_Group
bullets = pygame.sprite.Group()

# Class Car sprite_Group:
sprites_rect_cars = pygame.sprite.Group()
sprites_rect_cars.add(car1, car2)

# Class Road sprite_Group:
# Lines:
sprites_rect_line = pygame.sprite.Group()
sprites_rect_line.add(RL1, RL2, RL3, RL4)
# Rects:
sprites_rect = pygame.sprite.Group()
sprites_rect.add(rect1, rect2, rect3)

# Class Enemy sprite_Group:
sprites_enemies1 = pygame.sprite.Group()
sprites_enemies2 = pygame.sprite.Group()


# All Groups - to the Main sprite_list:
all_sprites_list.add(sprites_rect_cars,
                     sprites_rect_line, sprites_rect)

# Condition for lines (Class Road) =============================================================================
for i in range(7):
    RL1 = Road(Sc_Width / 2 - road_size * 2, (RL1.y + 105), 3, 50, White)
    RL2 = Road(Sc_Width / 2 - road_size, (RL2.y + 105), 3, 50, White)
    RL3 = Road(Sc_Width / 2 + road_size, (RL3.y + 105), 3, 50, White)
    RL4 = Road(Sc_Width / 2 + road_size * 2, (RL4.y + 105), 3, 50, White)
    all_sprites_list.add(RL1, RL2, RL3, RL4)

# Main game loop ################################################################################################
carryOn = True
clock = pygame.time.Clock()
while carryOn:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            car1.shoot()
        if keys[pygame.K_KP_0]:
            car2.shoot()

        if event.type == pygame.USEREVENT:

            # Objects of enemy class
            enemy1 = Enemy(random.randrange(Sc_Width / 2 - (road_size * 3) + road_size / 2, # Start
                                            Sc_Width / 2 - road_size / 2, 149), # Stop & Step
                                            enemy_list[random.randrange(0, 5)], sprites_enemies1) # Range of enemies & Group


            enemy2 = Enemy(random.randrange(Sc_Width / 2 + road_size / 2, # Start
                                            Sc_Width / 2 + (road_size * 3) - road_size / 2, 149),  # Stop & Step
                                            enemy_list[random.randrange(0, 5)], sprites_enemies1)  # Range of enemies & Group

            sprites_enemies1.add(enemy1)
            sprites_enemies2.add(enemy2)
            all_sprites_list.add(sprites_enemies1, sprites_enemies2)

    # Collisions for car/enemies
    img = pygame.image.load('boom.png')
    img = pygame.transform.scale(img, (120, 60))

    if pygame.sprite.groupcollide(sprites_rect_cars, sprites_enemies2, True, True):
        screen.blit(img, (car2.rect.x - 10, car2.rect.y - 50))
        cd2.play()
        # Game Over for Player2
        screen.blit(Player2_Wasted, (Sc_Width / 2 + road_size, Sc_Height / 2))
        pygame.display.update()
        time.sleep(2)

    if pygame.sprite.groupcollide(sprites_rect_cars, sprites_enemies1, True, True):
        screen.blit(img, (car1.rect.x - 10, car1.rect.y - 50))
        cd1.play()
        # Game Over for Player1
        screen.blit(Player1_Wasted, (Sc_Width / 2 - road_size * 3, Sc_Height / 2))
        pygame.display.update()
        time.sleep(2)

    # Collisions for bullets/enemies
    bullet_exp = pygame.image.load('explosion.png')
    bullet_exp = pygame.transform.scale(bullet_exp, (120, 70))

    if pygame.sprite.groupcollide(bullets, sprites_enemies2, True, True):
        screen.blit(bullet_exp, (enemy2.rect.x - 10, enemy2.rect.y + 50))
        cd2.play()
        score2 += score_increases2

    if pygame.sprite.groupcollide(bullets, sprites_enemies1, True, True):
        screen.blit(bullet_exp, (enemy1.rect.x - 10, enemy1.rect.y + 50))
        cd1.play()
        score += score_increases

    # ############################################################################################################

    # updating of Methods
    car1.steering()
    car2.steering()

    car1.speeding()
    car2.speeding()

    car1.slowing()
    car2.slowing()

    car1.edge()
    car2.edge()

    all_sprites_list.update()

    # Refresh Screen ============================================================================================
    all_sprites_list.draw(screen)

    pygame.display.flip()
    screen.fill(Black)

    # Render the score
    Player1_score = font.render(f'player1 score: {score}', True, Black)
    Player2_score  = font2.render(f'player2 score: {score2}', True, Black)

    screen.blit(grass, (0, 0))
    screen.blit(asphalt, (Sc_Width / 2 - road_size * 3, 0))
    screen.blit(Player1_score, (10, 10))
    screen.blit(Player2_score, (Sc_Width - 180, 10))

pygame.quit()

