# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
TITLE = "The Legend of Zelda"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Images
ship_img = pygame.image.load('images/link.png')
laser_img = pygame.image.load('images/arrow.png')
mob_img = pygame.image.load('images/mob.png')
bomb_img = pygame.image.load('images/bomb.png')
background = pygame.image.load('images/background.png')
startscreen = pygame.image.load('images/startscreen.png')
game_over = pygame.image.load('images/game_over.png')

# Sounds
enemy_hit = pygame.mixer.Sound('sounds/enemy_hit.wav')
enemy_die = pygame.mixer.Sound('sounds/enemy_die.wav')
link_hit = pygame.mixer.Sound('sounds/link_hit.wav')
link_death = pygame.mixer.Sound('sounds/link_die.wav')


intro_music = 'sounds/intro_music.ogg'
background_music = 'sounds/main_music.ogg'
gameover_music = 'sounds/game_over.ogg'
music = [intro_music, background_music, gameover_music]
current_music = 0

def start_music(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

# Stages
START = 0
PLAYING = 1
END = 2

def setup():
    global x, y, image, lasers, bombs, mobs, player, ship, fleet, stage
    
    stage = START
    
    # Game classes
    class Ship(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()

            self.image = image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
            self.speed = 5
            self.shield = 10

        def move_left(self):
            self.rect.x -= self.speed
            
        def move_right(self):
            self.rect.x += self.speed

        def shoot(self):
            laser = Laser(laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)
            print("Pew!")

        def update(self, bombs, mobs):
            hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

            for hit in hit_list:
                link_hit.play()
                self.shield -= 1

            hit_list = pygame.sprite.spritecollide(self, mobs, False, pygame.sprite.collide_mask)
            if len(hit_list) > 0:
                self.shield = 0

            if self.shield == 0:
                stage = END
                pygame.mixer.music.stop()
                link_death.play()
                self.kill()

    class Laser(pygame.sprite.Sprite):
        
        def __init__(self, image):
            super().__init__()

            self.image = image
            self.rect = self.image.get_rect()
            
            self.speed = 7

        def update(self):
            self.rect.y -= self.speed

            if self.rect.bottom < 0:
                self.kill()

    class Mob(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()

            self.image = image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
            self.shield = 3

        def drop_bomb(self):
            bomb = Bomb(bomb_img)
            bomb.rect.centerx = self.rect.centerx
            bomb.rect.centery = self.rect.bottom
            bombs.add(bomb)

        def update(self, lasers):
            hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

            for hit in hit_list:
                enemy_hit.play()
                self.shield -= 1
                
            if len(hit_list) > 0 or self.shield == 0:
                enemy_die.play()
                self.kill()


            if self.rect.top > 650:
                self.kill()

    class Bomb(pygame.sprite.Sprite):
        
        def __init__(self, image):
            super().__init__()

            self.image = image
            self.rect = self.image.get_rect()
            
            self.speed = 5
            
        def update(self):
            self.rect.y += self.speed

            if self.rect.top > 650:
                self.kill()
        
    class Fleet:

        def __init__(self, mobs):
            self.mobs = mobs
            self.moving_right = True
            self.speed = 6
            self.bomb_rate = 60

        def move(self):
            reverse = False
            
            for m in mobs:
                if self.moving_right:
                    m.rect.x += self.speed
                    if m.rect.right >= WIDTH:
                        reverse = True
                else:
                    m.rect.x -= self.speed
                    if m.rect.left <=0:
                        reverse = True

            if reverse == True:
                self.moving_right = not self.moving_right
                for m in mobs:
                    m.rect.y += 32
                

        def choose_bomber(self):
            rand = random.randrange(0, self.bomb_rate)
            all_mobs = mobs.sprites()
            
            if len(all_mobs) > 0 and rand == 0:
                return random.choice(all_mobs)
            else:
                return None

        def update(self):
            self.move()

            bomber = self.choose_bomber()
            if bomber != None:
                bomber.drop_bomb()

        
    # Make game objects
    ship = Ship(450, 465, ship_img)
    mob1 = Mob(128, 64, mob_img)
    mob2 = Mob(256, 64, mob_img)
    mob3 = Mob(384, 64, mob_img)

    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3)

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)

# Game loop
setup()

if stage == START:
    start_music(music[current_music])
    pygame.mixer.music.play(-1)

if stage == PLAYING:
    current_music = 1
    pygame.mixer.music.play(-1)
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()

        if stage == START:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    stage = PLAYING
                    currrent_music = (current_music + 1) % len(music)
                    start_music(music[current_music])
                    
        elif stage == PLAYING:            
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                ship.move_left()
            elif pressed[pygame.K_RIGHT]:
                ship.move_right()

        elif stage == END:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    setup()
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs, mobs)
        lasers.update()
        mobs.update(lasers)
        bombs.update()
        fleet.update()

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == START:
        screen.blit(startscreen, (0, 0))

    if stage == PLAYING:
        screen.blit(background, (0, 0))
        lasers.draw(screen)
        player.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)

    if stage == END:
        screen.blit(game_over, (0, 0))


    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
