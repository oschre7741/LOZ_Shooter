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
GREY = (244, 244, 244)

# Fonts
FONT_SM = pygame.font.Font('fonts/Triforce.ttf', 24)
FONT_MD = pygame.font.Font('fonts/Triforce.ttf', 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font(None, 96)

# Images
ship_img = pygame.image.load('images/link.png')
laser_img = pygame.image.load('images/arrow.png')
mob_img = pygame.image.load('images/mob.png')
mob2_img = pygame.image.load('images/mob2.png')
mob3_img = pygame.image.load('images/mob3.png')
bomb_img = pygame.image.load('images/bomb.png')

background = pygame.image.load('images/background.png')
background2 = pygame.image.load('images/background2.png')
startscreen = pygame.image.load('images/startscreen.png')
game_over = pygame.image.load('images/game_over.png')
win_img = pygame.image.load('images/win.png')

# Sounds
enemy_hit = pygame.mixer.Sound('sounds/enemy_hit.wav')
enemy_die = pygame.mixer.Sound('sounds/enemy_die.wav')
link_hit = pygame.mixer.Sound('sounds/link_hit.wav')
link_death = pygame.mixer.Sound('sounds/link_die.wav')


intro_music = 'sounds/intro_music.ogg'
background_music = 'sounds/main_music.ogg'
gameover_music = 'sounds/game_over.wav'
music = [intro_music, background_music, gameover_music]
current_music = 0

def start_music(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

# Stages
START = 0
PLAYING = 1
LOSE = 2
WIN = 3

def level_setup():
    global x, y, image, lasers, player, mobs, bombs, fleet

    class Mob(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()

            self.image = image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def drop_bomb(self):
            bomb = Bomb(bomb_img)
            bomb.rect.centerx = self.rect.centerx
            bomb.rect.centery = self.rect.bottom
            bombs.add(bomb)

        def update(self, lasers, player):
            hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

            for hit in hit_list:
                enemy_hit.play()
                
            if len(hit_list) > 0:
                enemy_die.play()
                player.score += 100
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
    mob1 = Mob(200, 64, mob2_img)
    mob2 = Mob(400, 64, mob2_img)
    mob3 = Mob(600, 64, mob2_img)
    mob4 = Mob(800, 64, mob2_img)
    mob5 = Mob(300, 14, mob2_img)
    mob6 = Mob(500, 14, mob2_img)
    mob7 = Mob(700, 14, mob2_img)
    '''
    mob8 = Mob(200, 64, mob2_img)
    mob9 = Mob(400, 64, mob2_img)
    mob10 = Mob(600, 64, mob2_img)
    mob11 = Mob(800, 64, mob2_img)
    mob12 = Mob(300, 14, mob2_img)
    mob13 = Mob(500, 14, mob2_img)
    mob14 = Mob(700, 14, mob2_img)

    mob15 = Mob(200, 64, mob3_img)
    mob16 = Mob(400, 64, mob3_img)
    mob17 = Mob(600, 64, mob3_img)
    mob18 = Mob(800, 64, mob3_img)
    mob19 = Mob(300, 14, mob3_img)
    mob20 = Mob(500, 14, mob3_img)
    mob21 = Mob(700, 14, mob3_img)
    '''
    # Make sprite groups
    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7)
    '''
    if player.level == 2:
        mobs.add(mob8, mob9, mob10, mob11, mob12, mob13, mob14)
    if player.level == 3:
        mobs.add(mob15, mob16, mob17, mob18, mob19, mob20, mob21)
    '''    

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)
    
def game_setup():
    global x, y, image, lasers, bombs, mobs, player, ship, fleet, stage
    
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
            if self.rect.x <= 0:
                self.rect.x = 0
            
        def move_right(self):
            self.rect.x += self.speed
            if self.rect.x >= 928:
                self.rect.x = 928

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
                player.shield -= 1

            hit_list = pygame.sprite.spritecollide(self, mobs, False, pygame.sprite.collide_mask)
            if len(hit_list) > 0:
                player.shield = 0

            if player.shield == 0:
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

        def drop_bomb(self):
            bomb = Bomb(bomb_img)
            bomb.rect.centerx = self.rect.centerx
            bomb.rect.centery = self.rect.bottom
            bombs.add(bomb)

        def update(self, lasers, player):
            hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

            for hit in hit_list:
                enemy_hit.play()
                
            if len(hit_list) > 0:
                enemy_die.play()
                player.score += 100
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

    # Make game objects
    mob1 = Mob(200, 64, mob2_img)
    mob2 = Mob(400, 64, mob2_img)
    mob3 = Mob(600, 64, mob2_img)
    mob4 = Mob(800, 64, mob2_img)
    mob5 = Mob(300, 14, mob2_img)
    mob6 = Mob(500, 14, mob2_img)
    mob7 = Mob(700, 14, mob2_img)
    '''
    mob8 = Mob(200, 64, mob2_img)
    mob9 = Mob(400, 64, mob2_img)
    mob10 = Mob(600, 64, mob2_img)
    mob11 = Mob(800, 64, mob2_img)
    mob12 = Mob(300, 14, mob2_img)
    mob13 = Mob(500, 14, mob2_img)
    mob14 = Mob(700, 14, mob2_img)

    mob15 = Mob(200, 64, mob3_img)
    mob16 = Mob(400, 64, mob3_img)
    mob17 = Mob(600, 64, mob3_img)
    mob18 = Mob(800, 64, mob3_img)
    mob19 = Mob(300, 14, mob3_img)
    mob20 = Mob(500, 14, mob3_img)
    mob21 = Mob(700, 14, mob3_img)
    '''

    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    player.level = 1
    player.shield = 10
    
    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7)
    '''
    if player.level == 2:
        mobs.add(mob8, mob9, mob10, mob11, mob12, mob13, mob14)
    if player.level == 3:
        mobs.add(mob15, mob16, mob17, mob18, mob19, mob20, mob21)
    '''    
    lasers = pygame.sprite.Group()

    bombs = pygame.sprite.Group()
    
    fleet = Fleet(mobs)

    # Set stage
    stage = START

# Game helper functions
def show_title_screen():
    screen.blit(startscreen, [0, 0])

def show_stats(player):
    score_text = FONT_MD.render('Score: ' + str(player.score), 1, GREY)
    screen.blit(score_text, [32, 28])

    score_text = FONT_MD.render('Level: ' + str(player.level), 1, GREY)
    screen.blit(score_text, [32, 60])

    score_text = FONT_MD.render('Health: ' + str(player.shield), 1, GREY)
    screen.blit(score_text, [32, 92])

def show_end():
    screen.blit(game_over, (0, 0))

    restart = FONT_MD.render('Press R to Restart', 1, WHITE)
    screen.blit(restart, [385, 35])
    

# Game loop
game_setup()

if stage == START:
    start_music(music[current_music])
    pygame.mixer.music.play(-1)

if stage == PLAYING:
    current_music = 1
    pygame.mixer.music.play(-1)

if stage == LOSE:
    current_music = 2
    pygame.mixer.music.play(-1)
    
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.quit()
                
            if stage == START:
                if event.key == pygame.K_KP_ENTER:
                    stage = PLAYING
                    current_music = 1
                    start_music(music[current_music])
            if event.key == pygame.K_SPACE and stage == PLAYING:
                ship.shoot()
                                  
    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    if stage == LOSE:
        current_music = 2
        start_music(music[current_music])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_setup()

    if stage == WIN:    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_setup()
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs, mobs)
        lasers.update()
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()

        if len(player) == 0:
            stage = LOSE

        if len(mobs) == 0:
            player.level += 1
            level_setup()

        if len(mobs) == 0 and player.level == 5:
            stage = WIN

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == START:
        show_title_screen()

    if stage == PLAYING:
        screen.blit(background, (0, 0))
        lasers.draw(screen)
        player.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        show_stats(player)

    if stage == LOSE:
        show_end()
        show_stats(player)

    if stage == WIN:
        pygame.mixer.music.stop()
        screen.blit(win_img, (0, 0))

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
