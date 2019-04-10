# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window

WIDTH = 1600
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Wonder Woman & The Battle For The Universe"
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
GREEN = (100, 255, 100)
BLUE = (30, 112, 219)


# Fonts
Font = pygame.font.Font
FONT_SM = Font(None, 24)
FONT_MD = Font(None, 32)
FONT_LG = Font(None, 64)
FONT_XL = Font("assets/fonts/spacerangerboldital.ttf", 96)
comic_font = Font("assets/fonts/comic_font.ttf", 165)
battle_font = Font("assets/fonts/battle_font.ttf", 98)
comic2_font = Font("assets/fonts/comic_font.ttf", 80)
jedi_font = Font("assets/fonts/Starjedi.ttf", 35)

# Images
load = pygame.image.load
wonder_woman_img = load("assets/images/wonder_woman.png").convert_alpha()
laser_img = load("assets/images/laserGreen.png").convert_alpha()
enemy_img = load("assets/images/shipYellow_manned.png").convert_alpha()
enemy2_img = load("assets/images/shipPink_manned.png").convert_alpha()
enemy3_img = load("assets/images/shipGreen_manned.png").convert_alpha()
bomb_img = load("assets/images/laserRed.png").convert_alpha()
title_img = load("assets/images/wonder_woman_title.png").convert_alpha()
background = load("assets/images/space_background.png").convert_alpha()
whole_background_img = load("assets/images/wonder_woman_background1.png").convert_alpha()
heart_img = load("assets/images/heart_img.png").convert_alpha()
alien_heart_img = load("assets/images/alien_life_img.png").convert_alpha()
lost_background_img = load("assets/images/lost_background.png").convert_alpha()
left_wonder_woman_img = load("assets/images/left_wonder_woman.png").convert_alpha()
mega_mob_img = load("assets/images/small_mega_mob_img.gif").convert()
mega_bomb_img = load("assets/images/mega_bomb.png").convert_alpha()
win_background_img = load("assets/images/win_background.png").convert_alpha()
bonus_img = load("assets/images/alien_life_img.png").convert_alpha()
pink_damaged_img = load("assets/images/shipPink_damage.png").convert_alpha()
green_damaged_img = load("assets/images/shipGreen_damage2.png").convert_alpha()
yellow_damaged_img = load("assets/images/shipYellow_damage2.png").convert_alpha()

# Sounds
sound = pygame.mixer.Sound
EXPLOSION = sound('assets/sounds/explosion.ogg')
pew = sound('assets/sounds/pew.ogg')
hurt = sound('assets/sounds/hurt.ogg')

playing_music = "assets/sounds/background.ogg"

lost_music = "assets/sounds/my_own_music.ogg"
starting_music = "assets/sounds/starting_music.ogg"
winning_music = "assets/sounds/winning_music.ogg"


# Stages
START = 0
PLAYING = 1
LOST = 2
WON = 3
END = 4

# Game classes
class Wonder_woman(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        

        self.speed = 3

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        print()
        print("Pew!")

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        
    def update(self):
        global stage
        '''check screen edges'''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH: 
            self.rect.right = WIDTH

        '''check bombs'''
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            print()
            print("LOST A LIFE!")
            hurt.play()
            player.score += -2
            player.strength_bar += -1

        '''check powerups'''
        bonus_hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)
        
        for hit in bonus_hit_list:
            print()
            print("Gained your lives")
            hit.apply(self)

            
        '''check mobs'''
        mob_hit_list = pygame.sprite.spritecollide(self, mobs, False, pygame.sprite.collide_mask)

        
        for hit in mob_hit_list:
            player.score += -3
            self.kill()
            stage = LOST

            
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 5



    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

            
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 3
        


    def update(self):
        self.rect.y += self.speed
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)
        
        if self.rect.bottom < 0:
            self.kill()

        if len(hit_list) > 0:
            self.kill()
            print()
            print("You got a bomb!")

            
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def drop_bomb(self):
        print()
        print("Bwwamp!")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.top
        bombs.add(bomb)

    def update(self):
       hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)
       if len(hit_list) > 0:
           player.score += 2
           self.kill()
           print()
           print("BOOM!")
     
            
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.drop = 30
        self.moving_right = True
        self.drop_speed = 20
        self.bomb_rate = 60 # lower the number = faster the bomb
        self.cleared = False
        self.defeated = False

        
    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True
                    
        if hits_edge:
            self.reverse()
            self.move_down()
        
    def reverse(self):
        self.moving_right = not self.moving_right
            
    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop
            
    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def change_speed(self):
        if len(mobs) == 12:
            for m in mobs:
                self.speed = 10
                
        if len(mobs) == 6:
            for m in mobs:
                self.speed = 17
     
        if len(mobs) == 1:
            for m in mobs:
                self.speed = 35
            for l in lasers:
                self.speed = 10
                
    def update(self):
        self.move()
        self.choose_bomber()
        self.change_speed()

class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def apply(self, wonder_woman):
        player.strength_bar = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
        
        
# Game helper functions
def show_title_screen():
    '''text'''
    space_txt = comic_font.render("Press Space", True, WHITE)


    '''blit images/text'''
    screen.blit(whole_background_img, [0,0])
    screen.blit(space_txt, [WIDTH/2 - space_txt.get_width()/2 , HEIGHT/2 - space_txt.get_height()/2])


def show_won_screen():
    '''text'''
    won_end_txt = comic_font.render("YOU WON!", True, WHITE)
    score_txt = battle_font.render("SCORE = " + str(player.score), 1, WHITE)
    end_time_txt = battle_font.render("TIME = " + str(ticks//refresh_rate), 1, WHITE)
    high_score_txt1 = jedi_font .render("Your perfect score will be recorded. Enter your name.", True, WHITE)

    '''screen blit'''
    screen.blit(win_background_img, [0,0])
    screen.blit(won_end_txt, [WIDTH/2 - won_end_txt.get_width()/2 , HEIGHT/6 - won_end_txt.get_height()/6])
    screen.blit(score_txt, [WIDTH/2 - score_txt.get_width()/2 , 660])
    screen.blit(end_time_txt, [WIDTH/2 - end_time_txt.get_width()/2 , 760])
    show_high_score()
    stage = END

def show_lost_screen():
    '''text'''
    lost_end_txt = comic2_font.render("THE ALIENS HAVE WON!", True, WHITE)
    score_txt = battle_font.render("SCORE = " + str(player.score), 1, WHITE)
    end_time_txt = battle_font.render("TIME = " + str(ticks//refresh_rate), 1, WHITE)
    high_score_txt2 = jedi_font .render("Your score will not be recorded.", True, WHITE)

    '''screen blit'''
    screen.blit(lost_background_img, [0,0])
    screen.blit(lost_end_txt, [WIDTH/2 - lost_end_txt.get_width()/2 , HEIGHT/6 - lost_end_txt.get_height()/6])
    screen.blit(score_txt, [WIDTH/2 - score_txt.get_width()/2 , HEIGHT/3 - score_txt.get_height()/3])
    screen.blit(end_time_txt, [WIDTH/2 - end_time_txt.get_width()/2 , HEIGHT/2 - end_time_txt.get_height()/2])
    screen.blit(high_score_txt2, [WIDTH/2 - high_score_txt2.get_width()/2 , 870])
    stage = END
    
def show_stats():
    timer = ticks//refresh_rate  
    
    '''text'''
    timer_txt = battle_font.render(str(timer), 1, BLUE)
    score_txt = battle_font.render(str(player.score), 1, RED)
    
    '''blit text'''
    screen.blit(timer_txt, [1500, 20])
    screen.blit(score_txt, [10, 20])
    
    '''Changing elements'''
    if player.strength_bar == 3:
        screen.blit(heart_img, [100,10])
        screen.blit(heart_img, [200, 10])
        screen.blit(heart_img, [300, 10])

    elif player.strength_bar == 2:
        screen.blit(heart_img, [100,10])
        screen.blit(heart_img, [200, 10])

    elif player.strength_bar == 1:
        screen.blit(heart_img, [100,10])
    
def record_high_score():
    if player.score == 38:
        input_file = open("high_score.txt","a")
        name = input("enter your name: ")
        print("Your Highscore has been recorded")
        print(name,file=input_file)
        input_file.close()
        file = open('high_score.txt', 'r') 
        names = file.readlines()
        file.close()

def show_high_score():
    file = open('high_score.txt', 'r') 
    names = file.read().splitlines()
    perfect_players_txt = jedi_font.render("Last five perfect scorers: " + str(names[-5:]), True, WHITE)
    screen.blit(perfect_players_txt, [WIDTH/3 - perfect_players_txt.get_width()/3 , 890])
    file.close()

def set_music(track):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    if track != None:  
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)

def setup():
    global stage, done, ticks
    global player, wonder_woman, lasers, mobs, fleet, bombs, powerups
    
    ''' Make game objects '''
    wonder_woman = Wonder_woman(wonder_woman_img)
    wonder_woman.rect.centerx = WIDTH/2
    wonder_woman.rect.bottom = HEIGHT
    
    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(wonder_woman)

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
    mob1 = Mob(0, 400, enemy_img)
    mob2 = Mob(200, 400, enemy_img)
    mob3 = Mob(400, 400, enemy_img)
    mob4 = Mob(600, 400, enemy_img)
    mob5 = Mob(800, 400, enemy_img)
    mob6 = Mob(1000, 400, enemy_img)
    mob7 = Mob(1200, 400, enemy_img)
    '''enemy 2'''
    mob8 = Mob(100, 200, enemy2_img)
    mob9 = Mob(300, 200, enemy2_img)
    mob10 = Mob(500, 200, enemy2_img)
    mob11 = Mob(700, 200, enemy2_img)
    mob12 = Mob(900, 200, enemy2_img)
    mob13 = Mob(1100, 200, enemy2_img)
    '''enemy 3'''
    mob14 = Mob(200, 0, enemy3_img)
    mob15 = Mob(400, 0, enemy3_img)
    mob16 = Mob(600, 0, enemy3_img)
    mob17 = Mob(800, 0, enemy3_img)
    mob18 = Mob(1000, 0, enemy3_img)

    '''final enemy'''
    mega_mob = Mob(800, -400, mega_mob_img)
            
    mobs = pygame.sprite.Group()
    
    mobs.add(mob1,mob2,mob3,mob4,mob5,mob6,mob7)
    mobs.add(mob8,mob9,mob10,mob11,mob12,mob13)
    mobs.add(mob14,mob15,mob16,mob17,mob18, mega_mob)

    fleet = Fleet(mobs)

    '''bonus'''
    
    powerup1 = HealthPowerUp(800, -2000, bonus_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)
    
    '''stats'''
    ticks = 0
    player.score = 0
    player.strength_bar = 3
    
    ''' set stage '''
    stage = START
    done = False
    '''music'''
    
    set_music(starting_music)
    

# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    set_music(playing_music)
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    wonder_woman.shoot()
                    pew.play()
            elif stage == LOST:
                if event.key == pygame.K_SPACE:
                    stage = END
                    setup()
            elif stage == WON:
                if event.key == pygame.K_SPACE:
                    stage = END
                    setup()
            elif stage == END():
                if event.key == pygame.K_SPACE:
                    setup()

                    
    pressed = pygame.key.get_pressed()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        
        if pressed[pygame.K_LEFT]:
            wonder_woman.move_left()
        elif pressed[pygame.K_RIGHT]:
            wonder_woman.move_right()

        player.update()
        lasers.update()
        fleet.update()
        mobs.update()
        bombs.update()
        ticks += 1
        powerups.update()
        

        
        if len(mobs) == 0:
            set_music(winning_music)
            record_high_score()
            stage = WON
               
        if player.strength_bar <= 0:
            set_music(lost_music)
            stage = LOST


        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(background, [0,0])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    powerups.draw(screen)
    
    show_stats()
    
    
    if stage == START:
        show_title_screen()
    elif stage == LOST:
        show_lost_screen()
    elif stage == WON:
        show_won_screen()

    
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
