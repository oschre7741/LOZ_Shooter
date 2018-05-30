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
FONT_SM = pygame.font.Font('assets/fonts/LOZ_FONT.ttf', 24)
FONT_MD = pygame.font.Font('assets/fonts/LOZ_FONT.ttf', 32)
FONT_LG = pygame.font.Font('assets/fonts/LOZ_FONT.ttf', 64)
FONT_XL = pygame.font.Font('assets/fonts/LOZ_FONT.ttf', 96)

# Images
ship_img = pygame.image.load('assets/images/link.png')

damage1 = pygame.image.load('assets/images/ship_damage/damage1.png')
damage2 = pygame.image.load('assets/images/ship_damage/damage2.png')
damage3 = pygame.image.load('assets/images/ship_damage/damage3.png')
damage4 = pygame.image.load('assets/images/ship_damage/damage4.png')

ship_damage = [damage1, damage2, damage3, damage4]

laser_img = pygame.image.load('assets/images/arrow.png')
ufo_img = pygame.image.load('assets/images/ufo_img.png')
mob_img = pygame.image.load('assets/images/mob.png')
mob2_img = pygame.image.load('assets/images/mob2.png')
mob3_img = pygame.image.load('assets/images/mob3.png')
bomb_img = pygame.image.load('assets/images/bomb.png')

background = pygame.image.load('assets/images/background.png')
startscreen = pygame.image.load('assets/images/startscreen.png')
game_over = pygame.image.load('assets/images/game_over.png')
win_img = pygame.image.load('assets/images/win.png')

# Sounds
enemy_hit = pygame.mixer.Sound('assets/sounds/enemy_hit.wav')
enemy_die = pygame.mixer.Sound('assets/sounds/enemy_die.wav')
link_hit = pygame.mixer.Sound('assets/sounds/link_hit.wav')
link_death = pygame.mixer.Sound('assets/sounds/link_die.wav')

# Music
intro_music = 'assets/sounds/intro_music.ogg'
background_music = 'assets/sounds/main_music.ogg'
gameover_music = 'assets/sounds/game_over.ogg'
win_music = 'assets/sounds/win_music.ogg'
music = [intro_music, background_music, gameover_music, win_music]
current_music = 0

def start_music(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

# Stages
START = 0
PLAYING = 1
LOSE = 2
WIN = 3

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
        # print("Pew!")

    def update(self, bombs, mobs, ship):
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

        if player.shield <= 5:
            self.image = damage1

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
            
class UFO(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            enemy_hit.play()
            
        if len(hit_list) > 0:
            enemy_die.play()
            player.score += 1000
            self.kill()

class Fleet2:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 7

    def move(self):
        for e in enemy:
            e.rect.x += self.speed + 2
            e.rect.y += self.speed 

    def update(self):
        self.move()
            
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
        
        if len(mobs) == 0 and player.level > 3:
            current_music = 3
            start_music(music[current_music])
        
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

def game_setup():
    global x, y, image, lasers, bombs, mobs, player, ship, fleet, fleet2, ufo, enemy, stage

    # Set stage
    stage = START

    # Make game objects
    ship = Ship(450, 465, ship_img)

    # Make game objects
    mob1 = Mob(200, 64, mob_img)
    mob2 = Mob(400, 64, mob_img)
    mob3 = Mob(600, 64, mob_img)
    mob4 = Mob(800, 64, mob_img)
    mob5 = Mob(300, 14, mob_img)
    mob6 = Mob(500, 14, mob_img)
    mob7 = Mob(700, 14, mob_img)
   
    ufo = UFO(-500, -500, ufo_img)
    
    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    player.level = 1
    player.shield = 10

    enemy = pygame.sprite.GroupSingle()
    enemy.add(ufo)
    
    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7)
   
    lasers = pygame.sprite.Group()

    bombs = pygame.sprite.Group()
    
    fleet = Fleet(mobs)

    fleet2 = Fleet2(enemy)

def level_setup():
    global x, y, image, ship, lasers, player, mobs, bombs, fleet, fleet2, ufo, enemy
    
    # Make game objects
    mob1 = Mob(200, 64, mob_img)
    mob2 = Mob(400, 64, mob_img)
    mob3 = Mob(600, 64, mob_img)
    mob4 = Mob(800, 64, mob_img)
    mob5 = Mob(300, 14, mob_img)
    mob6 = Mob(500, 14, mob_img)
    mob7 = Mob(700, 14, mob_img)
    
    mob8 = Mob(100, 64, mob2_img)
    mob9 = Mob(300, 64, mob2_img)
    mob10 = Mob(500, 64, mob2_img)
    mob11 = Mob(700, 64, mob2_img)
    mob12 = Mob(900, 64, mob2_img)
    mob13 = Mob(200, 14, mob2_img)
    mob14 = Mob(400, 14, mob2_img)
    mob15 = Mob(600, 14, mob2_img)
    mob16 = Mob(800, 14, mob2_img)

    mob17 = Mob(200, 64, mob3_img)
    mob18 = Mob(400, 64, mob3_img)
    mob19 = Mob(600, 64, mob3_img)
    mob20 = Mob(800, 64, mob3_img)
    mob21 = Mob(200, -36, mob3_img)
    mob22 = Mob(400, -36, mob3_img)
    mob23 = Mob(600, -36, mob3_img)
    mob24 = Mob(800, -36, mob3_img)
    mob25 = Mob(300, 14, mob3_img)
    mob26 = Mob(500, 14, mob3_img)
    mob27 = Mob(700, 14, mob3_img)

    ufo = UFO(-500, -500, ufo_img)
    
    # Make sprite groups
    enemy = pygame.sprite.GroupSingle()
    enemy.add(ufo)
    
    mobs = pygame.sprite.Group()
    if player.level == 1:
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7)
    if player.level == 2:
        mobs.add(mob8, mob9, mob10, mob11, mob12, mob13, mob14, mob15, mob16)
    if player.level == 3:
        mobs.add(mob17, mob18, mob19, mob20, mob21, mob22, mob23, mob24, mob25, mob26, mob27)

    bombs = pygame.sprite.Group()

    fleet = Fleet(mobs)

    fleet2 = Fleet2(enemy)

# Game helper functions
def show_title_screen():
    screen.blit(startscreen, [0, 0])

def show_stats(player):
    score_text = FONT_MD.render('Score: ' + str(player.score), 1, GREY)
    screen.blit(score_text, [600, 10])

    score_text = FONT_MD.render('Level: ' + str(player.level), 1, GREY)
    screen.blit(score_text, [600, 50])

    score_text = FONT_MD.render('Health: ' + str(player.shield), 1, GREY)
    screen.blit(score_text, [600, 90])

def show_end():
    screen.blit(game_over, (0, 0))

    restart = FONT_MD.render('Press R to Restart', 1, WHITE)
    t_rect = restart.get_rect()
    t_rect.centerx = WIDTH / 2
    t_rect.centery = HEIGHT / 1.5

    screen.blit(restart, t_rect)

    quit_game = FONT_MD.render('Press X to Quit', 1, WHITE)
    t_rect = quit_game.get_rect()
    t_rect.centerx = WIDTH / 2
    t_rect.centery = HEIGHT / 1.35

    screen.blit(quit_game, t_rect)

    
def show_win():
    pygame.mixer.music.stop()
    screen.blit(win_img, (0, 0))
    
    restart = FONT_MD.render('Press R to Restart', 1, WHITE)
    screen.blit(restart, [5, 45])

    quit_game = FONT_MD.render('Press X to Quit', 1, WHITE)
    screen.blit(quit_game, [5, 5])

    
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

if stage == WIN:
    current_music = 3
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_setup()
                stage = START
                current_music = 0
                start_music(music[current_music])

    if stage == WIN:    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_setup()
                stage = START
                current_music = 0
                start_music(music[current_music])
                    
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs, mobs, ship)
        lasers.update()
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
        enemy.update(lasers, player)
        fleet2.update()

        if len(player) == 0:
            stage = LOSE
            current_music = 2
            start_music(music[current_music])

        if len(mobs) == 0:
            player.level += 1
            level_setup()

        if player.level == 4:
            stage = WIN
            current_music = 3
            start_music(music[current_music])
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == START:
        show_title_screen()

    if stage == PLAYING:
        screen.blit(background, (0, 0))
        lasers.draw(screen)
        player.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        enemy.draw(screen)
        show_stats(player)

    if stage == LOSE:
        show_end()
        show_stats(player)

    if stage == WIN:
        show_win()

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
