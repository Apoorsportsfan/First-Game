import pygame
import sys
import pandas as pd
import random
# starting the sound class and methods in order to make it faster
pygame.mixer.pre_init()


# Global Variables/Initial Conditions
clock = pygame.time.Clock()
game_on = True
title_screen = True
single_player = False
game_over = False
display_end_scene = False
prompt = False
lives_start_value = 6
level_number = 1
keys_gained = 0


# rotating image on title screen
index = 0
degrees = list(range(-45, 46))


# Screen
screen_height = 800
screen_width = 1234
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('Assets/Background.png').convert()


# scoreboard universals
# starting font in order to create the fonts for the leaderboard
pygame.font.init()
# player username string that will be updated as they add letters
user_name = ""
# temporary name to look for
temp_name = "tempn"
# font for all the leaderboard text objects
base_font = pygame.font.SysFont('Bahnschrift', 45)
name_inst_font = pygame.font.SysFont('segoescript', 40)
# a sprite group to hold all the text objects
best_scores = pygame.sprite.Group()
ask_for_name = False
display_leaderboard = False
# new high_score variable
new_HS = False
# create a rectangle around the text of peoples name
name_enter_box = pygame.Rect(0, 0, 160, 65)
name_enter_box.center = (screen_width/2, screen_height/2)


# UI Y value for single player
ui_y_value = screen_height - ((screen_height - 683) / 2)


# speed
player_speed = 3
monster_speed = 6


# coordinates for levels
# avatar, monsters (x, y, 0 = move along x, 1 = move along y), treasure, key, door, extra lives
Level_1_cd = [(50, 50), (1178, 626, 0), (379, 52, 1), (870, 52, 1), (671, 624), (1084, 540), (1184, 50)]
Level_2_cd = [(1159, 410), (767, 145, 0), (871, 151, 1), (194, 614, 1), (643, 633, 0),  # player(0) and monster(1-4)
              (1164, 608), (225, 60), (473, 53), (74, 613),  # treasures(5-6) and keys(7-8)
              (638, 330), (555, 420) # door(9) and heart(10)
              ]
Level_3_cd = [(687, 295),  # player (0)
              (55, 200, 0), (771, 55, 0), (59, 303, 0), (884, 294, 1),  # monsters (1-4)
              (976, 429, 1), (360, 512, 0), (155, 624, 0), (583, 624, 0),  # monsters (5-8)
              (50, 200), (50, 608), (1175, 410), (60, 306), (1167, 182),  # keys (9-11) chests (12-13)
              (1170, 300), (578, 300)  # door (14) # extra live (15)
              ]


# multiplayer variables
multiplayer = False
# player and monster coordinates
Multi_cd = [
    (1161, 52), (68, 52),  # players
    (181, 54, 1), (795, 293, 0), (1055, 54, 1),  # TOP HALF MONSTERS
    (58, 522, 0), (428, 386, 0),(1165, 521, 0)  # BOTTOM HALF MONSTERS
]
# potential chest spawning coordinates
Chest_cd = [
    (615, 51), (615, 622), (59, 338), (1166, 338), (614, 339), (314, 338), (914, 338), (65, 623), (1163, 623)
]
# setting a timer to spawn chests
SPAWNCHEST = pygame.USEREVENT
# TODO play around with speed of chest spawning (I need another player to test this)
pygame.time.set_timer(SPAWNCHEST, 15000)


class Player(pygame.sprite.Sprite):
    # loading in the image for the player character
    avatar = pygame.transform.scale(pygame.image.load('Assets/Player_Avatar.png').convert_alpha(), (70, 65))

    def __init__(self, cd):
        self.x = cd[0]
        self.y = cd[1]
        # safe coordinates for movement
        self.safe_x = self.x
        self.safe_y = self.y
        # this is considered player 1
        self.player1 = True

        self.lives = lives_start_value
        self.points = 0

        # player is dead sound
        self.sound = pygame.mixer.Sound('Assets/Audio_Files/Dead_Sound.mp3')

        super().__init__()
        # image to draw
        self.image = self.avatar
        # location of where to draw image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # everytime a new frame is ran update the location
        self.rect.center = (self.x, self.y)
        self.points = self.points

    # checking what keys are pressed down and moving accordingly
    def check_keys(self, keys):
        # if the right and left keys are not pressed allow up and down movement
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            if keys[pygame.K_DOWN]:
                self.y += player_speed
            if keys[pygame.K_UP]:
                self.y -= player_speed
        # if the up and down keys are not pressed allow left and right movement
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            if keys[pygame.K_RIGHT]:
                self.x += player_speed
            if keys[pygame.K_LEFT]:
                self.x -= player_speed


class Player2(pygame.sprite.Sprite):
    avatar = pygame.transform.scale(pygame.image.load('Assets/Player_Avatar_2.png').convert_alpha(), (70, 65))

    def __init__(self, cd):
        self.x = cd[0]
        self.y = cd[1]
        # safe coordinates for movement
        self.safe_x = self.x
        self.safe_y = self.y
        # this is not considered player 1
        self.player1 = False

        self.lives = lives_start_value
        self.points = 0

        # dead sound
        self.sound = pygame.mixer.Sound('Assets/Audio_Files/Dead_Sound.mp3')

        super().__init__()
        # image to draw
        self.image = self.avatar
        # location of where to draw image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # update location of drawing
        self.rect.center = (self.x, self.y)
        self.points = self.points

    # checking what keys are down and moving accordingly
    def check_keys(self, keys):
        # if the a and d keys are not pressed allow up and down movement
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            if keys[pygame.K_s]:
                self.y += player_speed
            if keys[pygame.K_w]:
                self.y -= player_speed
        # if the s and w keys are not pressed allow up and down movement
        if not keys[pygame.K_s] and not keys[pygame.K_w]:
            if keys[pygame.K_d]:
                self.x += player_speed
            if keys[pygame.K_a]:
                self.x -= player_speed


class Monster(pygame.sprite.Sprite):
    # image for the monster
    monster = pygame.transform.scale(pygame.image.load('Assets/Monster.png').convert_alpha(), (65, 65))

    def __init__(self, cd, start_speed):
        # starting coordinates of monster
        self.x = cd[0]
        self.y = cd[1]
        # what direction are they moving (0 = x, 1 = y)
        self.move_d = cd[2]
        # starting safe coordinates
        self.safe_x = cd[0]
        self.safe_y = cd[1]
        # speed of monster
        self.speed = start_speed

        # monster collision sound effect
        self.sound = pygame.mixer.Sound('Assets/Audio_Files/Monster_Rawr.mp3')

        super().__init__()
        # image to draw
        self.image = self.monster
        # location to draw image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # update drawing location
        self.rect.center = (self.x, self.y)
        # update the speed
        self.speed = self.speed
        # update safe non-wall location
        self.safe_x = self.safe_x
        self.safe_y = self.safe_y

    def move(self, coord, speed):
        # subtract speed from the current location
        coord = coord - speed
        return coord

    def change_speed(self, speed):
        # make speed the opposite sign so the monster goes in the opposite direction
        speed = -speed
        return speed


class Treasure(pygame.sprite.Sprite):
    # image for chest
    chest = pygame.transform.scale(pygame.image.load('Assets/chest.png').convert_alpha(), (83, 65))

    def __init__(self, cd):
        # coordinate for drawing
        self.x = cd[0]
        self.y = cd[1]
        self.sound = pygame.mixer.Sound('Assets/Audio_Files/Chest_sound.mp3')

        super().__init__()
        # image to draw
        self.image = self.chest
        # location to draw
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class Key(pygame.sprite.Sprite):
    # image for key
    key = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets/Key.png').convert_alpha(), (69, 28)), 90)

    def __init__(self, cd):
        # coordinates to draw key
        self.x = cd[0]
        self.y = cd[1]
        # key collision sound
        self.sound = pygame.mixer.Sound('Assets/Audio_Files/Key_Sound.mp3')

        super().__init__()
        # image to draw
        self.image = self.key
        # where to draw image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class Door(pygame.sprite.Sprite):
    # image for door
    door = pygame.transform.scale(pygame.image.load('Assets/Door.png').convert(), (56, 48))

    def __init__(self, cd):
        # coordinates on where to draw door
        self.x = cd[0]
        self.y = cd[1]

        super().__init__()
        # image to draw
        self.image = self.door
        # where to draw
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class ExtraLife(pygame.sprite.Sprite):
    # image for extra life
    heart_img = pygame.transform.scale(pygame.image.load('Assets/heart.png').convert_alpha(), (65, 65))

    def __init__(self, cd):
        # location on where to draw
        self.x = cd[0]
        self.y = cd[1]

        super().__init__()
        # image to draw
        self.image = self.heart_img
        # where to draw
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # coordinates on where to draw
        self.x = x
        self.y = y

        super().__init__()
        # image to draw
        self.image = pygame.image.load('Assets/Pile_Of_Coins.png').convert_alpha()
        # where to draw
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class ScoreTexts(pygame.sprite.Sprite):

    def __init__(self, Place, Name, Score, x):

        # parts of text
        self.place = str(Place + 1)  # 1st, 2nd, 3rd, etc
        self.name = str(Name)  # name of person who got the score
        self.score = str(Score)  # score of person
        self.font = base_font  # font of the object
        # combining everything into 1 string
        self.txt = self.font.render(self.place + ": " + self.name + " " + self.score, True, (255, 255, 255))

        # coordinates
        self.y = (Place+1) * screen_height/12  # as the place number increases the name goes further down on the screen
        self.x = x

        super().__init__()
        self.image = self.txt  # setting the image as the text
        self.rect = self.txt.get_rect(midleft=(self.x, self.y))  # where to draw the text object


# Levels
class LevelOne(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image to draw
        self.image = pygame.image.load('Assets/Level_1.png').convert_alpha()
        # where to draw
        self.rect = self.image.get_rect(topleft=(0, 0))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class LevelTwo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image to draw
        self.image = pygame.image.load('Assets/Level_2.png').convert_alpha()
        # where to draw
        self.rect = self.image.get_rect(topleft=(0, 0))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class LevelThree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image to draw
        self.image = pygame.image.load('Assets/Level_3.png').convert_alpha()
        # where to draw
        self.rect = self.image.get_rect(topleft=(0, 0))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


class MultiLevel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image to draw
        self.image = pygame.image.load('Assets/Multi_Level.png').convert_alpha()
        # where to draw
        self.rect = self.image.get_rect(topleft=(0, 0))
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)


# screen displays
def update_screen(level_sprites, door_sprites, player_sprite, monsters, treasures, extra_lives,
                  points, keys, minutes, seconds, lives, keys_gained, level_number):
    # background/level
    screen.blit(background, (0, 0))

    # level
    level_sprites.draw(screen)

    # door
    door_sprites.draw(screen)

    # update location of and then draw player
    player_sprite.update()
    player_sprite.draw(screen)

    # treasure
    treasures.draw(screen)

    # update location of and then draw the monsters
    monsters.draw(screen)
    monsters.update()

    # key
    keys.draw(screen)

    # extra lives
    extra_lives.draw(screen)

    # user interface
    display_timer(minutes, seconds)
    display_points(points, (850, ui_y_value))
    display_lives(lives)
    display_instructions()
    display_keys(keys_gained, level_number)

    pygame.display.update()
    clock.tick(60)


def draw_title_screen(screen, background, degrees):
    # avatar on screen
    avatar_head = pygame.transform.scale2x(Player.avatar)
    avatar_head = pygame.transform.rotate(avatar_head, degrees)
    avatar_rect = avatar_head.get_rect(center=(screen_width / 3, screen_height / 3))

    # chest on screen
    chest = pygame.transform.scale2x(Treasure.chest)
    chest = pygame.transform.rotate(chest, degrees)
    chest_rect = chest.get_rect(center=(2 * screen_width / 3, screen_height / 3))

    # Title
    title_font = pygame.font.SysFont('segoescript', 80)
    title_txt = title_font.render("Treasure Hunting", True, (0, 0, 0))
    title_txt_rect = title_txt.get_rect(center=(screen_width / 2, screen_height / 6))

    # Instructions
    instruction_font = pygame.font.SysFont('segoescript', 40)
    instruction_txt = instruction_font.render("Press space to start single player", True, (0, 0, 0))
    instruction_txt_rect = instruction_txt.get_rect(center=(screen_width / 2, 2 * screen_height / 3))

    instruction_txt_2 = instruction_font.render("Press esc to exit the game", True, (0, 0, 0))
    instruction_txt_2_rect = instruction_txt_2.get_rect(center=(screen_width / 2, 2 * screen_height / 3 + 50))

    instruction_txt_3 = instruction_font.render("Press m to play multiplayer", True, (0, 0, 0))
    instruction_txt_3_rect = instruction_txt_3.get_rect(center=(screen_width / 2, 2 * screen_height / 3 + 100))

    # animating stuff to screen
    screen.blit(background, (0, 0))
    screen.blit(avatar_head, avatar_rect)
    screen.blit(chest, chest_rect)
    screen.blit(title_txt, title_txt_rect)
    screen.blit(instruction_txt, instruction_txt_rect)
    screen.blit(instruction_txt_2, instruction_txt_2_rect)
    screen.blit(instruction_txt_3, instruction_txt_3_rect)

    pygame.display.update()
    clock.tick(60)


def exit_prompt_screen():
    # background for txt
    prompt_background = pygame.transform.scale(pygame.image.load('Assets/prompt_background.png'), (650, 150))
    prompt_rect = prompt_background.get_rect(center=(screen_width / 2, screen_height / 2))

    # uniform distance from center
    d_from_center = 50

    # quit text
    quit_font = pygame.font.SysFont('segoescript', 40)
    quit_txt = quit_font.render("Press Right To Quit", True, (255, 255, 255))
    quit_txt_rect = quit_txt.get_rect(center=(screen_width / 2, screen_height / 2 - d_from_center))

    # return text
    return_font = quit_font
    return_txt = return_font.render("Press Space To Return", True, (255, 255, 255))
    return_txt_rect = return_txt.get_rect(center=(screen_width / 2, screen_height / 2))

    title_txt = return_font.render("Press T To Go To Title Screen", True, (255, 255, 255))
    title_txt_rect = title_txt.get_rect(center=(screen_width / 2, screen_height / 2 + d_from_center))

    # drawing stuff to screen
    screen.blit(prompt_background, prompt_rect)
    screen.blit(quit_txt, quit_txt_rect)
    screen.blit(return_txt, return_txt_rect)
    screen.blit(title_txt, title_txt_rect)

    pygame.display.update()
    clock.tick(60)


def game_over_display(points, best_scores):
    # red background for text
    GO_background = pygame.transform.scale(pygame.image.load('Assets/Game_Over_background.png'), (400, 110))
    GO_rect = GO_background.get_rect(center=(2 * screen_width / 3, screen_height / 3))

    # red background for other text (slightly lower than the first)
    GO_background_2 = pygame.transform.scale(pygame.image.load('Assets/Game_Over_background.png'), (650, 140))
    GO_rect_2 = GO_background_2.get_rect(center=(2 * screen_width / 3, screen_height/2 + 20))

    # telling player game is over
    # TODO find blood font
    GO_font = pygame.font.SysFont('segoescript', 40)
    GO_txt = GO_font.render("GAME IS OVER!", True, (255, 255, 255))
    GO_txt_rect = GO_txt.get_rect(center=(2 * screen_width / 3, screen_height / 3))

    # Restart game instructions
    GO_instructions = pygame.font.SysFont('segoescript', 40)
    GO_instruc_txt = GO_instructions.render("Press Space To Restart Game", True, (255, 255, 255))
    Go_instruc_rect = GO_instruc_txt.get_rect(center=(2 * screen_width / 3, screen_height/2 - 20))

    # exiting game instructions
    GO_exit_txt = GO_instructions.render("Press ESC To Exit Game", True, (255, 255, 255))
    GO_exit_rect = GO_exit_txt.get_rect(center=(2 * screen_width / 3, screen_height/2 + 20))

    # going back to title screen instructions
    GO_title_txt = GO_instructions.render("Press T To Go To Title Screen", True, (255, 255, 255))
    GO_title_rect = GO_title_txt.get_rect(center=(2 * screen_width / 3, screen_height / 2 + 60))

    # putting stuff on screen
    # displaying leaderboard
    leaderboard(best_scores)
    screen.blit(GO_background, GO_rect)
    screen.blit(GO_background_2, GO_rect_2)
    screen.blit(GO_txt, GO_txt_rect)
    screen.blit(GO_instruc_txt, Go_instruc_rect)
    screen.blit(GO_exit_txt, GO_exit_rect)
    screen.blit(GO_title_txt, GO_title_rect)
    # display points person gained during game
    display_points(points, (1.75 * screen_width / 3, 2 * screen_height / 3))

    pygame.display.update()
    clock.tick(60)


def transition_screen(degrees, old_points, level_points, time_points, points, lives_left):
    screen.blit(background, (0, 0))

    # congrats message
    congrats_font = pygame.font.SysFont('segoescript', 40)
    congrats_txt = congrats_font.render("YOU FINISHED THE LEVEL! CELEBRATION TIME!", True, (255, 255, 255))
    if lives_left < 3:
        congrats_txt = congrats_font.render("You made it but at what cost?", True, (255, 255, 255))
    if level_number >= 3:
        congrats_txt = congrats_font.render("YOU CAN SEE THE GLOW OF THE TREASURE ROOM!", True, (255, 255, 255))
    congrats_txt_rect = congrats_txt.get_rect(center=(screen_width/2, screen_height/7))

    # player moving head
    avatar_head = pygame.transform.scale2x(Player.avatar)
    avatar_head = pygame.transform.rotate(avatar_head, degrees)
    avatar_rect = avatar_head.get_rect(center=(screen_width / 2, screen_height / 4))

    # old points
    old_points = str(old_points)
    old_p_font = pygame.font.SysFont('Bahnschrift', 45)
    old_p_font_txt = old_p_font.render("Previous Points: " + old_points, True, (255, 255, 255))
    old_p_font_rect = old_p_font_txt.get_rect(center=(screen_width/2, 6 * screen_height/14))

    # Level Points
    level_points = str(level_points)
    level_p_txt = old_p_font.render("Level Points: " + level_points, True, (255, 255, 255))
    level_p_rect = level_p_txt.get_rect(center=(screen_width / 2, 7 * screen_height /14))

    # time points
    time_points = str(time_points)
    time_p_txt = old_p_font.render("Time Bonus: " + time_points, True, (255, 255, 255))
    time_p_rect = time_p_txt.get_rect(center=(screen_width/2, 8 * screen_height/14))

    if level_number > 3:
        lives_points = lives_left * 15
        lives_points = str(lives_points)

        live_p_txt = old_p_font.render("Life Points: " + lives_points, True, (255, 255, 255))
        live_p_rect = live_p_txt.get_rect(center=(screen_width/2, 9 * screen_height/14))

        screen.blit(live_p_txt, live_p_rect)


    # total points
    points = str(points)
    total_p_txt = old_p_font.render("Total Points: " + points, True, (255, 255, 255))
    total_p_rect = total_p_txt.get_rect(center=(screen_width/2, 10 * screen_height/14))

    # lives left
    lives_left = str(lives_left)
    ll_txt = old_p_font.render("Lives Left: " + lives_left, True, (255, 255, 255))
    ll_rect = ll_txt.get_rect(center=(screen_width/2, 11 * screen_height/14))

    # instructions
    instruc_font = pygame.font.SysFont('segoescript', 20)
    instruc_txt = instruc_font.render("Press Space To Continue To Next Level", True, (255, 255, 255))
    instruc_rect = instruc_txt.get_rect(center=(screen_width/2, 12 * screen_height/14))

    instruc_txt_2 = instruc_font.render("Press ESC To Exit Game", True, (255, 255, 255))
    instruc_rect_2 = instruc_txt_2.get_rect(center=(screen_width/2, 13 * screen_height/14))

    # drawing things to screen
    screen.blit(congrats_txt, congrats_txt_rect)
    screen.blit(avatar_head, avatar_rect)
    screen.blit(old_p_font_txt, old_p_font_rect)
    screen.blit(level_p_txt, level_p_rect)
    screen.blit(time_p_txt, time_p_rect)
    screen.blit(total_p_txt, total_p_rect)
    screen.blit(ll_txt, ll_rect)
    screen.blit(instruc_txt, instruc_rect)
    screen.blit(instruc_txt_2, instruc_rect_2)

    # updating display and frame rate
    pygame.display.update()
    clock.tick(60)


def ending_cutscene(avatar, monster, x_value, x_value_2, lives):

    screen.blit(background, (0, 0))

    ending_cutscene_sprites = pygame.sprite.Group()

    # pile of money
    coin = Coins(3 * screen_width/4, screen_height/2)

    # chests
    chest_left = Treasure((3 * screen_width/5, 2.15 * screen_height/3))
    chest_center = Treasure((2.15 * screen_width/3, 2.17 * screen_height/3))
    chest_right = Treasure((2.5 * screen_width/3, 2.2 * screen_height/3))

    # player
    avatar.x = x_value
    cutscene_font = pygame.font.SysFont('Bahnschrift', 25)

    # next step text
    instruc_font = pygame.font.SysFont('segoescript', 20)
    instruc_txt = instruc_font.render("Press Right To Continue To Leaderboard", True, (255, 255, 255))
    instruc_rect = instruc_txt.get_rect(center=(screen_width / 2, screen_height / 1.2))

    # two different endings, 1 if you get more than 3 lives and 1 if you get less than or equal to 3 lives
    if avatar.x and x_value >= screen_width/3:
        if lives >= 3:
            # player text
            cutscene_txt = cutscene_font.render("I FINALLY FOUND THE TREASURE ROOM!", True, (255, 255, 255))
            cutscene_txt_rect = cutscene_txt.get_rect(center=(screen_width / 3, 3 * screen_height / 5))

            screen.blit(cutscene_txt, cutscene_txt_rect)
            screen.blit(instruc_txt, instruc_rect)
        if lives < 3:
            cutscene_txt = cutscene_font.render("What was that sound?", True, (255, 255, 255))
            cutscene_txt_rect = cutscene_txt.get_rect(center=(screen_width / 3, 3 * screen_height / 5))
            # updating the monsters x_value so he moves right
            monster.x = x_value_2

            screen.blit(cutscene_txt, cutscene_txt_rect)
            screen.blit(monster.image, (monster.x, monster.y))

    # drawing treasure pile
    ending_cutscene_sprites.add(coin, chest_left, chest_center, chest_right)
    ending_cutscene_sprites.draw(screen)
    ending_cutscene_sprites.update()
    # drawing avatar
    screen.blit(avatar.image, (avatar.x, avatar.y))

    # if the monster gets close to the player the screen becomes red
    if lives < 3 and monster.x >= screen_width/3:
        dead = pygame.transform.scale(pygame.image.load('Assets/Game_Over_background.png'), (screen_width, screen_height))
        b_rect = dead.get_rect(topleft=(0, 0))

        # instructions
        instruc_txt = instruc_font.render("Press Right To Continue To Leaderboard", True, (255, 255, 255))
        instruc_rect = instruc_txt.get_rect(center=(screen_width/2, screen_height/2))

        # drawing stuff to screen
        screen.blit(dead, b_rect)
        screen.blit(instruc_txt, instruc_rect)

    # updating display and frame rate
    pygame.display.update()
    clock.tick(60)


def end_game_instructions(best_scores, new_HS):
    leaderboard(best_scores)

    # congrats message
    congrats_txt = base_font.render("YOU COMPLETED THE GAME! NICE JOB!", True, (255, 255, 255))
    congrats_txt_rect = congrats_txt.get_rect(center=(2 * screen_width/3, screen_height/3))

    # instructions
    instruc_txt = base_font.render("Press Space To Restart The Game!", True, (255, 255, 255))
    instruc_txt_rect = instruc_txt.get_rect(center=(2 * screen_width/3, screen_height/2))

    instruc_txt_2 = base_font.render("Press T To Go To Title Screen!", True, (255, 255, 255))
    instruc_txt_rect_2 = instruc_txt_2.get_rect(center=(2 * screen_width / 3, 1.25 * screen_height / 2))

    # if there is a new high score then put a celebration message
    if new_HS:
        HS_font = pygame.font.SysFont('Bahnschrift', 20)
        congrats_HS_txt = HS_font.render("IT SEEMS LIKE WE GOT AN UPDATE ON THE LEADERBOARD!", True, (255, 255, 255))
        congrats_HS_txt_rect = congrats_HS_txt.get_rect(center=(2*screen_width/3, 7.5 * screen_height/18))

        screen.blit(congrats_HS_txt, congrats_HS_txt_rect)

    # drawing stuff
    screen.blit(congrats_txt, congrats_txt_rect)
    screen.blit(instruc_txt, instruc_txt_rect)
    screen.blit(instruc_txt_2, instruc_txt_rect_2)

    pygame.display.update()
    clock.tick(60)


def play_level(level, coordinates):
    global level_number
    global start_ticks
    global best_scores
    global keys_gained
    # misc booleans
    global prompt, game_over, single_player, title_screen, display_leaderboard

    # if someone closes the window end program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # if there are no lives then go to the game over while loop
    if avatar.lives <= 0:
        game_over = True
    else:
        pass

    # getting time left in level
    time_left, minutes_left, seconds_left = get_time(start_ticks)

    # if there is no time left program goes to game over while loop
    if time_left <= 0:
        game_over = True
    else:
        pass

    # checking what keyboard keys are pressed
    keys = pygame.key.get_pressed()
    # if key is escape then go to esc prompt screen
    if keys[pygame.K_ESCAPE]:
        prompt = True
    else:
        pass

    # esc prompt screen loop, pauses action in game
    while prompt:
        prompt, title_screen, single_player = check_exit_game(prompt, title_screen, single_player)

    # game over loop
    if game_over:
        # resetting leaderboard sprite group and other leaderboard variables
        best_scores.empty()
        user_name = ""
        ask_for_name = False
        display_leaderboard = False
        new_HS = False
        best_scores, new_HS = get_and_update_best_scores(avatar.points, user_name, ask_for_name, new_HS)
    while game_over:
        # checking if someone closes the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys2 = pygame.key.get_pressed()
        # if space bar is pressed reset the game
        if keys2[pygame.K_SPACE]:
            keys_gained, start_ticks, level_number, game_over = reset_game(game_over)
        # if escape is pressed exit the game
        if keys2[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys2[pygame.K_t]:
            game_over = False
            single_player = False
            title_screen = True

        # game over display
        game_over_display(avatar.points, best_scores)

    # wall collision player and movement
    collide_wall_player(avatar, level)

    # monster movement
    for m in monster_sprites:
        monsters_move(m, level)
        avatar.lives, avatar.points, avatar.x, avatar.y = player_monster_collision(m, avatar, coordinates, avatar.lives, avatar.points)

    # treasure collision
    avatar.points = treasure_collision(treasure_sprites, avatar, avatar.points)

    # key collision
    keys_gained = key_collision(key_sprites, avatar, keys_gained)

    # extra life collision
    avatar.lives = life_collision(lives_sprites, avatar, avatar.lives)

    # door collision
    level_number = door_collision(door_sprite, avatar, level_number, keys_gained)

    # drawing stuff to screen
    update_screen(level_sprites, door_sprite, player_sprite, monster_sprites, treasure_sprites, lives_sprites,
                  avatar.points, key_sprites, minutes_left, seconds_left, avatar.lives, keys_gained, level_number)


# UI Functions
def display_timer(minutes, seconds, cd=(1150, ui_y_value)):
    # there is less then 1 minute left then make the color red else make the color white
    if minutes < 1:
        key_color = (255, 0, 0)
    else:
        key_color = (255, 255, 255)
    # timer text
    timer_txt = str(minutes) + ":" + str(seconds)
    timer_font = pygame.font.SysFont('Bahnschrift', 40)
    timer_txt = timer_font.render(timer_txt, True, key_color)
    timer_txt_rect = timer_txt.get_rect(center=cd)

    screen.blit(timer_txt, timer_txt_rect)


def display_points(points, cd, center=False):
    # turning points into a string
    points = "Points: " + str(points)
    points_font = pygame.font.SysFont('Bahnschrift', 45)
    points_txt = points_font.render(points, True, (255, 255, 255))
    # if there no center paramater was passed the default is false so go to midleft part of rect
    # if True is passed then go to center of rect
    if not center:
        points_txt_rect = points_txt.get_rect(midleft=cd)
    if center:
        points_txt_rect = points_txt.get_rect(center=cd)

    screen.blit(points_txt, points_txt_rect)


def display_lives(lives, cd=(650, ui_y_value), center=False):
    # turning lives into strings
    lives = "Lives: " + str(lives)
    lives_font = pygame.font.SysFont('Bahnschrift', 45)
    lives_txt = lives_font.render(lives, True, (255, 255, 255))
    # if there no center paramater was passed the default is false so go to midleft part of rect
    # if True is passed then go to center of rect
    if not center:
        lives_txt_rect = lives_txt.get_rect(midleft=cd)
    if center:
        lives_txt_rect = lives_txt.get_rect(center=cd)

    screen.blit(lives_txt, lives_txt_rect)


def display_instructions():
    # movement instructions
    move_txt = "Press Arrow Keys To Move"
    move_font = pygame.font.SysFont('Bahnschrift', 30)
    move_txt = move_font.render(move_txt, True, (255, 255, 255))
    move_txt_rect = move_txt.get_rect(midleft=(25, ui_y_value - 30))

    # escape prompt instructions
    esc_txt = "Press esc to exit"
    esc_font = pygame.font.SysFont('Bahnschrift', 30)
    esc_txt = esc_font.render(esc_txt, True, (255, 255, 255))
    esc_txt_rect = esc_txt.get_rect(center=(move_txt_rect.midbottom[0], ui_y_value + 10))

    screen.blit(move_txt, move_txt_rect)
    screen.blit(esc_txt, esc_txt_rect)


def display_keys(keys_p, level_number):
    # if the player has the correct number of keys then change the color of the keys text from red to green
    key_color = None
    if keys_p < level_number:
        key_color = (255, 0, 0)
    if keys_p == level_number:
        key_color = (0, 255, 0)

    # turning keys gained into a string
    keys_txt = "Keys: " + str(keys_p)
    keys_font = pygame.font.SysFont('Bahnschrift', 45)
    keys_txt = keys_font.render(keys_txt, True, key_color)
    keys_txt_rect = keys_txt.get_rect(midleft=(450, ui_y_value))

    screen.blit(keys_txt, keys_txt_rect)


# Game Play functions
def check_exit_game(prompt, title_screen, single_player):
    # checking if someone wants to close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw the display
    exit_prompt_screen()

    # if key is right exit game, if key is t go to title screen, if key is space continue game
    keys2 = pygame.key.get_pressed()
    if keys2[pygame.K_RIGHT]:
        pygame.quit()
        sys.exit()
    # if space is pressed then exit prompt screen and stay in single player
    if keys2[pygame.K_SPACE]:
        prompt = False
        title_screen = False
        single_player = True
    # if t is pressed than exit prompt screen and go to title screen
    if keys2[pygame.K_t]:
        prompt = False
        title_screen = True
        single_player = False

    return prompt, title_screen, single_player


def get_time(start_ticks, minutes=3):
    # getting the amount of time between the current time and starting time
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    # amount of time left (in seconds)
    time_left = (minutes * 60) - seconds

    # dividing time left by 60 to get minutes and seconds
    minutes_left, seconds_left = divmod(time_left, 60)
    minutes_left = round(minutes_left)
    seconds_left = round(seconds_left)

    # if there are 60 seconds left than make seconds 0 and add 1 to minutes because 60 seconds is a minute
    if seconds_left == 60:
        seconds_left = 0
        minutes_left = minutes_left + 1
    # if there are less than 10 seconds left before the next minute put a 0 in front of it to make it 2 digits
    if seconds_left < 10:
        seconds_left = "0" + str(seconds_left)

    # return time left in level, minutes left in level, seconds left in level
    return time_left, minutes_left, seconds_left


def monsters_move(m, level):
    collide_wall_monster = pygame.sprite.collide_mask(m, level)
    # if no collision with wall update current coordinates
    if not collide_wall_monster:
        # update safe coodinates if there is not collision
        m.safe_x = m.x
        m.safe_y = m.y
        if m.move_d == 0:
            m.x = m.move(m.x, m.speed)
        if m.move_d == 1:
            m.y = m.move(m.y, m.speed)

    # if collision with wall change direction and go back to last non collision location
    elif collide_wall_monster:
        m.speed = m.change_speed(m.speed)
        m.x = m.safe_x
        m.y = m.safe_y
    else:
        pass


# collisions between stuff
def collide_wall_player(player, level):
    collide_wall = pygame.sprite.collide_mask(player, level)
    # if there is no collision with level walls update the current coordinates into the x_pos, y_pos variables
    if not collide_wall:
        keys = pygame.key.get_pressed()
        player.safe_x = player.x
        player.safe_y = player.y
        player.check_keys(keys)
    # if there is a collision with the walls then go back to previous non-collision position
    elif collide_wall:
        player.x = player.safe_x
        player.y = player.safe_y
    else:
        pass


def treasure_collision(t_sprites, player, points):
    # loop through t_sprites group and check for collision with player
    for t in t_sprites:
        collide_t = pygame.sprite.collide_mask(player, t)
        if collide_t:
            t.sound.play()
            # remove treasure from group and add points
            t_sprites.remove(t)
            t.kill()
            points += 100

    return points


def key_collision(key_sprites, player, keys_gained):
    # loop through key sprite group
    for k in key_sprites:
        collide_k = pygame.sprite.collide_mask(player, k)
        if collide_k:
            k.sound.play()
            # remove key from sprite group and add key to keys_gained
            key_sprites.remove(k)
            k.kill()
            keys_gained += 1
        else:
            pass

    return keys_gained


def player_monster_collision(m, player, cd, lives, points):
    collide_m = pygame.sprite.collide_mask(player, m)
    if collide_m:
        # play the collision sound
        m.sound.play()
        # if there is a collision then take away a life and take away points, then reset player position
        lives -= 1
        points -= 10
        # if the player is player 1 then go to the first tuple
        if player.player1:
            player.x, player.y = cd[0]
        # if the player is player 2 then go to the second tuple (only applies to multiplayer)
        if not player.player1:
            player.x, player.y = cd[1]
    else:
        pass

    return lives, points, player.x, player.y


def door_collision(door_group, player, level_number, keys_gained):
    for door in door_group:
        collide_d = pygame.sprite.collide_mask(player, door)
        # if there is a collision with the door and the player has the correct number of keys break while loop
        if collide_d and keys_gained == level_number:
            level_number += 1
        else:
            pass
    return level_number


def life_collision(hearts, player, lives):
    # check for collision, if collision then add a life to lives
    for heart in hearts:
        collide_h = pygame.sprite.collide_mask(player, heart)
        if collide_h:
            lives_sprites.remove(heart)
            heart.kill()
            lives += 1

    return lives


# transition/reset functions
def time_points(points, minutes_left, seconds_left):
    # turn seconds left into an integer
    seconds_left = int(seconds_left)
    time_points = round((minutes_left * 60 + seconds_left) / 4)
    # add bonus points to the points
    points = points + time_points

    return points, time_points


def clear_sprite_groups():
    # empty all of the sprite groups
    level_sprites.empty()
    player_sprite.empty()
    monster_sprites.empty()
    treasure_sprites.empty()
    key_sprites.empty()
    door_sprite.empty()
    lives_sprites.empty()


def reset_var(TF):
    # TF stands for True False as boolian has another use
    avatar.lives = lives_start_value
    avatar.points = 0
    keys_gained = 0
    start_ticks = pygame.time.get_ticks()
    level_number = 1
    TF = False

    return keys_gained, start_ticks, level_number, TF


def reset_game(TF):
    # TF stands for True False as boolian has another use
    clear_sprite_groups()

    # player
    avatar.x, avatar.y = Level_1_cd[0]
    avatar.safe_x, avatar.safe_y = Level_1_cd[0]
    player_sprite.add(avatar)

    # monsters
    monster_sprites.add(monster_L1_1, monster_L1_2, monster_L1_3)
    # treasures
    treasure_L1 = Treasure(Level_1_cd[4])
    treasure_sprites.add(treasure_L1)
    # keys
    key_L1 = Key(Level_1_cd[5])
    key_sprites.add(key_L1)
    # door
    door_sprite.add(door_L1)
    # level
    level_sprites.add(level_1)

    keys_gained, start_ticks, level_number, TF = reset_var(TF)

    return keys_gained, start_ticks, level_number, TF


def create_level_2_objects():
    # player
    avatar.x, avatar.y = Level_2_cd[0]
    avatar.safe_x, avatar.safe_y = Level_2_cd[0]
    player_sprite.add(avatar)

    # Monsters
    # Top Middle Monster
    monster_L2_1 = Monster(Level_2_cd[1], monster_speed+2)
    # Top Right Monster
    monster_L2_2 = Monster(Level_2_cd[2], monster_speed/2 - 1)
    # Bottom Left Monster
    monster_L2_3 = Monster(Level_2_cd[3], monster_speed/2)
    # Bottom Right Monster
    monster_L2_4 = Monster(Level_2_cd[4], monster_speed-1)
    monster_sprites.add(monster_L2_1, monster_L2_2, monster_L2_3, monster_L2_4)

    # Treasures
    # Bottom Right
    treasure_L2_right = Treasure(Level_2_cd[5])
    # Top Left
    treasure_L2_left = Treasure(Level_2_cd[6])
    treasure_sprites.add(treasure_L2_right, treasure_L2_left)

    # Keys
    # Top Middle
    key_L2_Top = Key(Level_2_cd[7])
    # Bottom Left
    key_L2_Bottom = Key(Level_2_cd[8])
    key_sprites.add(key_L2_Top, key_L2_Bottom)

    # Door
    door_L2 = Door(Level_2_cd[9])
    door_sprite.add(door_L2)

    # Extra Life
    EL = ExtraLife(Level_2_cd[10])
    lives_sprites.add(EL)


def create_level_3_objects():

    # player
    avatar.x, avatar.y = Level_3_cd[0]
    avatar.safe_x, avatar.safe_y = Level_3_cd[0]
    player_sprite.add(avatar)

    # monsters
    monster_L3_1 = Monster(Level_3_cd[1], monster_speed/3)
    monster_L3_2 = Monster(Level_3_cd[2], monster_speed/1.85)
    monster_L3_3 = Monster(Level_3_cd[3], monster_speed/2.1)
    monster_L3_4 = Monster(Level_3_cd[4], monster_speed/4)
    monster_L3_5 = Monster(Level_3_cd[5], monster_speed/2)
    monster_L3_6 = Monster(Level_3_cd[6], monster_speed/2.1)
    monster_L3_7 = Monster(Level_3_cd[7], monster_speed-1)
    monster_L3_8 = Monster(Level_3_cd[8], monster_speed/1.6)
    monster_sprites.add(monster_L3_1, monster_L3_2, monster_L3_3, monster_L3_4,
                        monster_L3_5, monster_L3_6, monster_L3_7, monster_L3_8)


    # keys
    key_L3_BL = Key(Level_3_cd[9])
    key_L3_TM = Key(Level_3_cd[10])
    key_L3_BR = Key(Level_3_cd[11])
    key_sprites.add(key_L3_BL, key_L3_TM, key_L3_BR)

    # chests
    chest_L = Treasure(Level_3_cd[12])
    chest_R = Treasure(Level_3_cd[13])
    treasure_sprites.add(chest_L, chest_R)

    # door
    door_L3 = Door(Level_3_cd[14])
    door_sprite.add(door_L3)

    # Extra Life
    EL = ExtraLife(Level_3_cd[15])
    lives_sprites.add(EL)


# leaderboard functions
def leaderboard(score_display_group):
    # draw the leaderboard
    screen.blit(background, (0, 0))
    score_display_group.draw(screen)


def get_name(name, ask_name):
    for event in pygame.event.get():
        # checking if people want to leave the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # checking if there are keys being pressed
        if event.type == pygame.KEYDOWN:
            # removing a letter from the string if backspace is pressed
            if event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            # if the name is the temp name then just return the name, do not allow them to advance
            elif name == temp_name:
                return name, ask_name
            # pressing enter to move on
            elif event.key == pygame.K_RETURN:
                name = name
                ask_name = False
            # if the name is longer than 5 letters then stop them from adding letters
            elif len(name) == 5:
                name = name
            # add a letter to the name
            else:
                name += event.unicode
    return name, ask_name


def display_name_asker(user_name, ask_for_name, lb_names, index):
    screen.blit(background, (0, 0))
    # getting users name
    user_name, ask_for_name = get_name(user_name, ask_for_name)

    # displaying user entered name
    name_display = base_font.render(user_name, True, (255, 255, 255))
    name_display_rect = name_display.get_rect(center=(screen_width / 2, screen_height / 2))
    # displaying instructions
    name_inst_txt = name_inst_font.render("Enter your name and then press enter!", True, (255, 255, 255))
    name_inst_rect = name_inst_txt.get_rect(center=(screen_width / 2, screen_height / 3))
    # box around name
    pygame.draw.rect(screen, (255, 255, 255), name_enter_box, 2)

    # drawing stuff to screen
    screen.blit(name_display, name_display_rect)
    screen.blit(name_inst_txt, name_inst_rect)
    pygame.display.update()
    clock.tick(60)

    # updating the values of the top scores based on the user input
    lb_names[index] = user_name

    return user_name, ask_for_name, lb_names


def get_old_scores(points):
    # appending player score to file
    lb_txt = open('Assets/lb.txt', 'a')
    lb_txt.write(temp_name + "," + str(points))
    lb_txt.close()

    # getting all 11 scores and getting rid of the lowest one
    lb = pd.read_csv('Assets/lb.txt')
    lb = lb.sort_values(by='score', ascending=False)
    lb.reindex
    lb = lb.iloc[:-1,:]

    names = []
    scores = []

    # putting all values into lists for easy use
    for x in range(0, 10):
        for y in range(0, 2):
            if y == 0:
                names.append(lb.iat[x, y])
            if y == 1:
                scores.append(lb.iat[x, y])

    return names, scores, lb


def get_and_update_best_scores(points, user_name, ask_for_name, new_HS):
    # getting the names from the lb.txt file and splitting the dataframe into 2 lists for easier use
    lb_names, lb_scores, lb_df = get_old_scores(points)

    # seeing if the player score is in the top 10 scores
    if temp_name in lb_names:
        index = lb_names.index(temp_name)
        ask_for_name = True
        new_HS = True

    # getting user to input name if they got into the top 10 scores
    while ask_for_name:
        user_name, ask_for_name, lb_names = display_name_asker(user_name, ask_for_name, lb_names, index)

    # saving the top scores to the high score file
    if temp_name not in lb_names:
        try:
            lb_df.replace({temp_name: str(lb_names[index])}, inplace=True)
        except:
            pass
    lb_df.to_csv('Assets/lb.txt', sep=",", index=None)

    # creating sprites to quickly display all the scores
    for num in range(0, 10):
        append = ScoreTexts(num, lb_names[num], lb_scores[num], screen_width / 8)
        best_scores.add(append)

    return best_scores, new_HS


# multiplayer functions
def multi_display(level_sprites, player_sprite, treasures, monsters, minutes, seconds):
    # background/level
    screen.blit(background, (0, 0))

    # level
    level_sprites.draw(screen)

    # player
    player_sprite.update()
    player_sprite.draw(screen)

    # treasure
    treasures.draw(screen)

    # monster
    monsters.draw(screen)
    monsters.update()

    # UI based on the player
    for p in player_sprite:
        if p.player1:
            display_points(p.points, (12 * screen_width / 15, ui_y_value))
            display_lives(p.lives, (5.5 * screen_width / 9, ui_y_value))
        if not p.player1:
            display_points(p.points, (screen_width / 16, ui_y_value))
            display_lives(p.lives, (2.5 * screen_width / 9, ui_y_value))
    display_timer(minutes, seconds, (screen_width/2, ui_y_value))

    # instructions for each player
    instruc_txt_player_1 = "Press Arrow Keys To Move"
    instruc_txt_player_2 = "Press WASD To Move"

    # font for instructions
    instruc_font = pygame.font.SysFont('segoescript', 20)

    # turning strings into text objects
    instruc_txt_player_1 = instruc_font.render(instruc_txt_player_1, True, (255, 255, 255))
    instruc_txt_player_2 = instruc_font.render(instruc_txt_player_2, True, (255, 255, 255))

    # where to put instructions
    instruc_txt_player_1_rect = instruc_txt_player_1.get_rect(center=(4.5 * screen_width/6, ui_y_value - 35))
    instruc_txt_player_2_rect = instruc_txt_player_2.get_rect(center=(1.5 * screen_width/6, ui_y_value - 35))

    # draw the instructions
    screen.blit(instruc_txt_player_1, instruc_txt_player_1_rect)
    screen.blit(instruc_txt_player_2, instruc_txt_player_2_rect)

    # update screen
    pygame.display.update()
    clock.tick(60)


def multi_objects():

    # players
    player_1 = Player(Multi_cd[0])
    player_2 = Player2(Multi_cd[1])
    player_sprite.add(player_1, player_2)

    # creating 1 starting chest
    chest = Treasure(pick_spawn_point())
    treasure_sprites.add(chest)

    for num in range(2, 8):
        # creating the monsters for the multiplayer levels
        append = Monster(Multi_cd[num], monster_speed/2)
        monster_sprites.add(append)


def pick_spawn_point():
    # pick a random coordinate from Chest_cd list
    new_chest_cd = random.choice(Chest_cd)
    return new_chest_cd


def multi_game_over_display(players):
    screen.blit(background, (0, 0))

    # turning the sprite group into a list
    players = players.sprites()

    # displaying points
    display_points(players[0].points, (2.25 * screen_width/3, screen_height/2), True)
    display_points(players[1].points, (1.5 * screen_width/6, screen_height/2), True)

    # displaying lives
    display_lives(players[0].lives, (2.25 * screen_width/3, 1.2 * screen_height/2), True)
    display_lives(players[1].lives, (1.5 * screen_width/6, 1.2 * screen_height/2), True)

    # player 1 head
    player_1_head = pygame.transform.scale2x(players[0].image)
    player_1_head_rect = player_1_head.get_rect(center=(4.5 * screen_width/6, screen_height/3))

    # player 2 head
    player_2_head = pygame.transform.scale2x(players[1].image)
    player_2_head_rect = player_2_head.get_rect(center=(1.5 * screen_width/6, screen_height/3))

    # drawing heads to the screen
    screen.blit(player_1_head, player_1_head_rect)
    screen.blit(player_2_head, player_2_head_rect)

    # declaring the winner
    winner_text = "WINNER"
    winner_text = name_inst_font.render(winner_text, True, (255, 255, 255))
    # winner is declared by points
    if players[0].points > players[1].points:
        winner_text_rect = winner_text.get_rect(center=(4.5 * screen_width/6, screen_height/6))
    elif players[0].points < players[1].points:
        winner_text_rect = winner_text.get_rect(center=(1.5 * screen_width / 6, screen_height / 6))
    # lives are the tie breaker
    elif players[0].points == players[1].points:
        if players[0].lives > players[1].lives:
            winner_text_rect = winner_text.get_rect(center=(4.5 * screen_width / 6, screen_height / 6))
        elif players[0].lives < players[1].lives:
            winner_text_rect = winner_text.get_rect(center=(1.5 * screen_width / 6, screen_height / 6))
        elif players[0].lives == players[1].lives:
            winner_text = name_inst_font.render("IT'S A TIE", True, (255, 255, 255))
            winner_text_rect = winner_text.get_rect(center=(screen_width/2, screen_height / 6))

    # drawing winner declaring
    screen.blit(winner_text, winner_text_rect)

    # TODO put instructions at the bottom of the screen
    # Instructions
    instr = "Press Space To Play Again"
    instr_2 = "Press ESC To Exit"
    instr_3 = "Press T To Go To Title Screen"

    # restart instructions
    instr_font = pygame.font.SysFont('segoescript', 25)
    instruc_txt = instr_font.render(instr, True, (255, 255, 255))
    instruc_rect = instruc_txt.get_rect(center=(screen_width/2, 1.5 * screen_height/2))

    # exiting program instructions
    exit_txt = instr_font.render(instr_2, True, (255, 255, 255))
    exit_rect = exit_txt.get_rect(center=(screen_width/2, 1.6 * screen_height/2))

    # going to title screen instructions
    title_txt = instr_font.render(instr_3, True, (255, 255, 255))
    title_txt_rect = title_txt.get_rect(center=(screen_width/2, 1.7 * screen_height/2))

    # draw the instructions
    screen.blit(instruc_txt, instruc_rect)
    screen.blit(exit_txt, exit_rect)
    screen.blit(title_txt, title_txt_rect)

    # update screen
    pygame.display.update()
    clock.tick(60)


pygame.init()

# level 1 sprites
# creating player sprite for level 1
avatar = Player(Level_1_cd[0])
player_sprite = pygame.sprite.Group()
player_sprite.add(avatar)

# creating monster sprites for level 1
# bottom left monster
monster_L1_1 = Monster(Level_1_cd[1], monster_speed)
# far left monster
monster_L1_2 = Monster(Level_1_cd[2], monster_speed)
# upper right monster
monster_L1_3 = Monster(Level_1_cd[3], monster_speed / 3)
# monster sprite group
monster_sprites = pygame.sprite.Group()
monster_sprites.add(monster_L1_1, monster_L1_2, monster_L1_3)

# treasure sprites for level 1
treasure_L1 = Treasure(Level_1_cd[4])
treasure_sprites = pygame.sprite.Group()
treasure_sprites.add(treasure_L1)

# key sprites for level 1
key_L1 = Key(Level_1_cd[5])
key_sprites = pygame.sprite.Group()
key_sprites.add(key_L1)

# creating level 1 sprites
level_1 = LevelOne()
level_sprites = pygame.sprite.Group()
level_sprites.add(level_1)

# door sprite for level 1
door_L1 = Door(Level_1_cd[6])
door_sprite = pygame.sprite.Group()
door_sprite.add(door_L1)

# lives sprite group
lives_sprites = pygame.sprite.Group()

# Title Screen
while game_on:
    while title_screen:
        # checking if window closes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # degree to rotate image
        degree_num = degrees[index]

        draw_title_screen(screen, background, degree_num)

        # adding index for degree and flipping arrays if index is greater than or equal to 90
        index += 1
        if index >= 90:
            degrees.reverse()
            index = 0

        # seeing if esc or space bar is being pressed down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            title_screen = False
            single_player = True
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif keys[pygame.K_m]:
            title_screen = False
            multiplayer = True

    # getting start time
    start_ticks = pygame.time.get_ticks()

    while single_player:
        # Game play Level 1
        while level_number == 1:
            play_level(level_1, Level_1_cd)

            # breaking out of loop if the player wants to go back to the title screen
            if not single_player:
                keys_gained, start_ticks, level_number, single_player = reset_game(single_player)
                break

        # Transition from 1st to 2nd level
        if level_number > 1:
            next_level = False

            # resetting degrees index
            index = 0
            degrees = list(range(-45, 46))

            # setting previous points before level completion
            old_points = 0
            # points gained from just level
            level_1_points = avatar.points

            # giving bonus for completing level faster

            try:
                avatar.points, time_points_var = time_points(avatar.points, minutes_left, seconds_left)
            except NameError:
                points = 0
                time_points_var = 0

            # showing the transition screen
            while not next_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # degree is the the value of the degrees list at index position
                degree_num = degrees[index]

                transition_screen(degree_num, old_points, level_1_points, time_points_var, avatar.points, avatar.lives)

                # increase index and if index is bigger or equal to 90 then reverse list and reset index
                index += 1
                if index >= 90:
                    degrees.reverse()
                    index = 0

                # seeing if they want to leave the game or continue game
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    next_level = True

            # total points after level 1
            old_points = avatar.points

            # Getting variables ready for level 2
            # clearing sprite groups to get ready for level 2
            clear_sprite_groups()

            level_2 = LevelTwo()
            level_sprites.add(level_2)

            # resetting variables
            keys_gained = 0
            start_ticks = pygame.time.get_ticks()

            create_level_2_objects()

        # level 2
        while level_number == 2:
            play_level(level_2, Level_2_cd)

            # breaking out of loop if the player wants to go back to the title screen
            if not single_player:
                keys_gained, start_ticks, level_number, single_player = reset_game(single_player)
                break

        # Transition from 2nd to 3rd level
        if level_number > 2:
            next_level = False

            # resetting degrees index
            index = 0
            degrees = list(range(-45, 46))

            # points gained from just level
            level_2_points = avatar.points - old_points

            # giving bonus for completing level faster
            try:
                avatar.points, time_points_var = time_points(avatar.points, minutes_left, seconds_left)
            except NameError:
                points = 0
                time_points_var = 0

            # showing the transition screen
            while not next_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # degree is the the value of the degrees list at index posiiton
                degree_num = degrees[index]

                transition_screen(degree_num, old_points, level_2_points, time_points_var, avatar.points, avatar.lives)

                # increase index and if index is bigger or equal to 90 then reverse list and reset index
                index += 1
                if index >= 90:
                    degrees.reverse()
                    index = 0

                # seeing if they want to leave the game or continue game
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    next_level = True

            # total points after level 2
            old_points = avatar.points

            # Getting variables ready for level 3
            # clearing sprite groups to get ready for level 3
            clear_sprite_groups()

            level_3 = LevelThree()
            level_sprites.add(level_3)

            # resetting variables
            keys_gained = 0
            start_ticks = pygame.time.get_ticks()

            create_level_3_objects()

        # Level 3
        while level_number == 3:
            play_level(level_3, Level_3_cd)

            # breaking out of loop if the player wants to go back to the title screen
            if not single_player:
                keys_gained, start_ticks, level_number, single_player = reset_game(single_player)
                break

        # Transition from 3rd level to end of game
        if level_number > 3:
            next_level = False

            # resetting degrees index
            index = 0
            degrees = list(range(-45, 46))

            # points of just level
            level_3_points = avatar.points - old_points
            # giving bonus for lives left
            lives_points = avatar.lives * 15
            avatar.points = avatar.points + lives_points

            # giving bonus for completing level faster
            try:
                avatar.points, time_points_var = time_points(avatar.points, minutes_left, seconds_left)
            except NameError:
                points = 0
                time_points_var = 0

            # showing the transition screen
            while not next_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # degree is the the value of the degrees list at index position
                degree_num = degrees[index]

                transition_screen(degree_num, old_points, level_3_points, time_points_var, avatar.points, avatar.lives)

                # increase index and if index is bigger or equal to 90 then reverse list and reset index
                index += 1
                if index >= 90:
                    degrees.reverse()
                    index = 0

                # seeing if they want to leave the game or continue game
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    next_level = True

            # Ending Cutscene
            # setting display_end_scene to true so that it displays the ending cutscene

            display_end_scene = True

            # setting x value of avatar in cutscene
            x_value = 50
            x_value_2 = -50
            cut_avatar = Player((x_value, 2 * screen_height / 3))
            cut_monster = Monster((x_value_2, 2 * screen_height/3, 0), monster_speed)

            while display_end_scene:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                ending_cutscene(cut_avatar, cut_monster, x_value, x_value_2, avatar.lives)
                # stopping the avatar from moving it reaches 1/3 of the screen if it is not there then move it right
                if cut_avatar.x >= screen_width/3:
                    x_value = cut_avatar.x
                    if cut_monster.x >= screen_width/3:
                        cut_avatar.sound.play()
                        x_value_2 = cut_monster.x
                    else:
                        x_value_2 += monster_speed
                else:
                    x_value += player_speed

                # checking to see if people press space to leave the cutscene
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_RIGHT]:
                    display_end_scene = False

            # getting and updating leaderboard
            best_scores.empty()
            user_name = ""
            ask_for_name = False
            display_leaderboard = False
            new_HS = False
            best_scores, new_HS = get_and_update_best_scores(avatar.points, user_name, ask_for_name, new_HS)

            display_leaderboard = True

            while display_leaderboard:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # resetting game
                            keys_gained, start_ticks, level_number, display_leaderboard = reset_game(display_leaderboard)
                        if event.key == pygame.K_t:
                            # resetting game and going to title screen
                            keys_gained, start_ticks, level_number, display_leaderboard = reset_game(display_leaderboard)
                            single_player = False
                            title_screen = True
                end_game_instructions(best_scores, new_HS)

    # multiplayer
    if multiplayer:
        clear_sprite_groups()

        # resetting variables
        start_ticks = pygame.time.get_ticks()

        multi_objects()
        multi_level = MultiLevel()
        level_sprites.add(multi_level)

    while multiplayer:
        # if people close the program close the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWNCHEST:
                new_chest = Treasure(pick_spawn_point())
                treasure_sprites.add(new_chest)

        # getting time left
        time_left, minutes_left, seconds_left = get_time(start_ticks, 5)

        if time_left <= 0:
            game_over = True
        else:
            pass

        # checking what keyboard keys are pressed
        keys = pygame.key.get_pressed()
        # if key is escape then go to esc prompt screen
        if keys[pygame.K_ESCAPE]:
            prompt = True
        else:
            pass

        # esc prompt screen loop, pauses action in game
        while prompt:
            prompt, title_screen, multiplayer = check_exit_game(prompt, title_screen, multiplayer)

        while game_over:
            # exiting program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys2 = pygame.key.get_pressed()
            # if space bar is pressed reset the game
            if keys2[pygame.K_SPACE]:
                # clearing sprite groups
                clear_sprite_groups()
                # repopulating sprite groups
                multi_objects()
                start_ticks = pygame.time.get_ticks()
                level_sprites.add(multi_level)
                # resetting spawn chest timer
                pygame.time.set_timer(SPAWNCHEST, 0)
                pygame.time.set_timer(SPAWNCHEST, 15000)

                # breaking out of while loop
                game_over = False
            # if escape is pressed exit the game
            elif keys2[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            # if t is reset game to single player populated and then exit game_over loop and multiplayer loop
            elif keys2[pygame.K_t]:
                keys_gained, start_ticks, level_number, multiplayer = reset_game(multiplayer)
                game_over = False
            else:
                multi_game_over_display(player_sprite)

        # loop for this stuff to happen to both players
        for p in player_sprite:
            # player wall collision and movement
            collide_wall_player(p, multi_level)
            # checking lives
            if p.lives <= 0:
                game_over = True
            # checking for treasure collision
            p.points = treasure_collision(treasure_sprites, p, p.points)

        # monster movement
        for m in monster_sprites:
            monsters_move(m, multi_level)
            for p in player_sprite:
                p.lives, p.points, p.x, p.y = player_monster_collision(m, p, Multi_cd, p.lives, p.points)

        if not multiplayer:
            # killing these objects so they do not take up memory
            for chest in treasure_sprites:
                chest.kill()
            for player in player_sprite:
                player.kill()
            for monster in monster_sprites:
                monster.kill()
            multi_level.kill()

            # resetting other game variables
            keys_gained, start_ticks, level_number, multiplayer = reset_game(multiplayer)
            title_screen = True
            break
        multi_display(level_sprites, player_sprite, treasure_sprites, monster_sprites, minutes_left, seconds_left)
