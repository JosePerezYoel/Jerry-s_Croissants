import pygame
from pygame.locals import *
import random
import sys
import pygame.freetype

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
CLOCK = pygame.time.Clock()

WINDOWSIZE = 800, 600

DISPLAY = pygame.Surface((400, 300))

RED = 255, 0, 0
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0

gamefont = pygame.freetype.Font("media/font/pixelated.ttf", 50)

WINDOW = pygame.display.set_mode((WINDOWSIZE))
pygame.display.set_caption("Jerry's Croissants")

BRICK_IMG = pygame.image.load("media/art/Brick_Wall.png")
BRICK_HEIGHT = BRICK_IMG.get_height()
BRICK_WIDTH = BRICK_IMG.get_width()




PLAYER_IMG = pygame.image.load("media/player_animation/idle/idle0.png").convert()
PLAYER_IMG.set_colorkey(RED)
CROISSANT_IMG = pygame.image.load("media/art/Croissant.png").convert()
CROISSANT_IMG.set_colorkey(RED)
LASER_IMG = pygame.image.load("media/art/Laser.png").convert()
LASER_IMG.set_colorkey(WHITE)
BOMB_IMG = pygame.image.load("media/art/Bomb.png").convert()
BOMB_IMG.set_colorkey(RED)
SHIELD_IMG = pygame.image.load("media/art/Shield.png").convert()
SHIELD_IMG.set_colorkey(WHITE)
JUMP_SOUND = pygame.mixer.Sound("media/sounds/jump_sound.wav")
JUMP_SOUND.set_volume(0.4)
GAMEOVER_SOUND = pygame.mixer.Sound("media/sounds/game_over.wav")
SHIELD_SOUND = pygame.mixer.Sound("media/sounds/shield.wav")
SHIELD_SOUND.set_volume(0.4)
EAT_SOUND = pygame.mixer.Sound("media/sounds/eat.wav")




def loadBackground(tile, tile_height, tile_width, xcount, ycount, startx=0, starty=0):
    # xcount and ycount is how many tiles you want on both axis
    # start x and start y is where on the window you want to start loading everything
    for x in range(xcount):
        for y in range(ycount):
            DISPLAY.blit(tile, (x * tile_height + startx, y * tile_width + starty))


global animation_frames
animation_frames = {}
def load_animation(path, frame_duration):
    global animation_frames
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((RED))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data
animation_database = {}
animation_database["idle"] = load_animation('media/player_animation/idle', [100,1,5,5,5,5,100])

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

player_action = 'idle'
player_frame = 0


def collision_test(entity, tiles):
    collisions = []
    for tile in tiles:
        if entity.colliderect(tile):
            collisions.append(tile)
    return collisions

def move(entity, movement, tiles):
    collision_types = {"top": False, "bottom": False, "left": False, "right": False}
    entity.x += movement[0]
    collisions = collision_test(entity, tiles)
    for tile in collisions:
        if movement[0] > 0:
            entity.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            entity.left = tile.right
    entity.y += movement[1]
    collisions = collision_test(entity, tiles)
    for tile in collisions:
        if movement[1] > 0:
            entity.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            entity.top = tile.bottom
            collision_types["top"] = True
    return entity, collision_types



def game():
    global PLAYER_IMG
    PLAYER_AREA = pygame.Rect(16, 14, 368, 272)

    player_rect = pygame.Rect(200, 300, PLAYER_IMG.get_width() - 4, PLAYER_IMG.get_height() - 4)

    rects = [pygame.Rect(0, 0, 16, 800), pygame.Rect(0, 0, 800, 10), pygame.Rect(384, 0, 16, 800),
             pygame.Rect(0, 287, 800, 16)]

    moving_left = False
    moving_right = False
    shield = False

    player_y_momentum = 0
    jump_count = 0
    jump_limit = 4
    jump = -5
    level = 0

    Croissant_objs = []

    Laser_objs = []

    Bomb_objs = []
    possible_cords = []
    for x in range(1, 24):
        possible_cords.append(x * 16)

    bomb_timer = 0
    laser_timer = 0
    shield_timer = 300

    shield_timer_white = pygame.Rect(73, 20, 150, 10)
    gameover = False
    loadBackground(BRICK_IMG, BRICK_HEIGHT, BRICK_WIDTH, 25, 19)
    player_frame = 0
    while not gameover:
        if shield_timer <= 0:
            shield_timer_width = 0

        shield_timer_width = shield_timer / 2
        shield_timer_green = pygame.Rect(73, 20, shield_timer_width, 10)
        shield_rect = pygame.Rect(player_rect.x - 5, player_rect.y - 6, 24, 24)

        DISPLAY.fill(BLACK)

        backround = loadBackground(BRICK_IMG, BRICK_HEIGHT, BRICK_WIDTH, 25, 19)
        pygame.draw.rect(DISPLAY, BLACK, PLAYER_AREA)
        pygame.draw.rect(DISPLAY, WHITE, shield_timer_white)
        pygame.draw.rect(DISPLAY, GREEN, shield_timer_green)
        laser_timer += 1
        bomb_timer += 1
        shield_timer += 1
        laser_cooldown = 180 - level * 10
        if laser_cooldown <= 30:
            laser_cooldown = 30

        if laser_timer >= laser_cooldown:
            laser_timer = 0
            Laser_objs.append(Laser(-200, player_rect.y + 10, 'left'))
            Laser_objs.append(Laser(-225, player_rect.y + 10, 'left'))
            Laser_objs.append(Laser(-250, player_rect.y + 10, 'left'))
            Laser_objs.append(Laser(500, player_rect.y - 10, 'right'))
            Laser_objs.append(Laser(475, player_rect.y - 10, 'right'))
            Laser_objs.append(Laser(450, player_rect.y - 10, 'right'))

        bomb_cooldown = laser_cooldown

        if bomb_timer >= bomb_cooldown and level > 5:
            bomb_timer = 0
            Bomb_objs.append(Bomb(random.choice(possible_cords), -40))


        for laser in Laser_objs:
            laser.render()
            laser.move()
            if laser.collision_test(shield_rect) and shield == True:
                Laser_objs.remove(laser)
            if laser.collision_test(player_rect):
                gameover = True

        for croissant in Croissant_objs:
            croissant.render()
            if croissant.collision_test(player_rect):
                jump_limit += 1
                EAT_SOUND.play()
                Croissant_objs.remove(croissant)
        if len(Croissant_objs) == 0:
            level += 1
            jump_limit = 4
            for i in range(level):
                Croissant_objs.append(Croissant(random.randint(16, 370), random.randint(14, 270)))

        for bomb in Bomb_objs:

            bomb.render()
            bomb.move()
            if bomb.collision_test(shield_rect) and shield == True:
                Bomb_objs.remove(bomb)

            if bomb.collision_test(player_rect):
                gameover = True

        player_movement = [0, 0]

        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        if player_y_momentum > 3:
            player_y_momentum = 3

        player_y_momentum += 0.2

        player_movement[1] += player_y_momentum

        player_rect, collisions = move(player_rect, player_movement, rects)

        if collisions["bottom"]:
            jump_count = 0
            player_y_momentum = 0
        if collisions["top"]:
            player_y_momentum = 0

        if shield == True:
            shield_timer -= 7
            DISPLAY.blit(SHIELD_IMG, (player_rect.x - 5, player_rect.y - 6))
        if shield_timer < 0:
            shield = False
        if shield_timer > 300:
            shield_timer = 300

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        PLAYER_IMG = animation_frames[player_img_id]
        DISPLAY.blit(PLAYER_IMG, (player_rect.x, player_rect.y))


        surf = pygame.transform.scale(DISPLAY, WINDOWSIZE)
        WINDOW.blit(surf, (0, 0))
        gamefont.render_to(WINDOW, (40, 40), "JL: " + str(jump_limit), (255, 255, 255))
        gamefont.render_to(WINDOW, (40, 80), "LVL: " + str(level), (255, 255, 255))
        if jump_count == jump_limit:
            gamefont.render_to(WINDOW, (40, 40), "JL: " + str(jump_limit), (255, 0, 0))

        if gameover == True:
            GAMEOVER_SOUND.play()
            pygame.mixer.music.play(-1)


        if shield == True:
            pass

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:

                if event.key == K_w:
                    jump_count += 1
                    if jump_count <= jump_limit:
                        player_y_momentum = jump
                        JUMP_SOUND.play()
                if event.key == K_RSHIFT:
                    if shield_timer >= 0:
                        shield = True
                        SHIELD_SOUND.play()
                if event.key == K_a:
                    moving_left = True
                if event.key == K_d:
                    moving_right = True
            if event.type == KEYUP:
                if event.key == K_w:
                    up = False
                if event.key == K_RSHIFT:
                    shield = False
                if event.key == K_a:
                    moving_left = False
                if event.key == K_d:
                    moving_right = False

        CLOCK.tick(60)
        pygame.display.flip()

    return gameover


def main_menu():
    running = True
    pygame.mixer.music.load("media/sounds/game_music.wav")
    pygame.mixer.music.play(-1)
    while running:
        gamefont = pygame.freetype.Font("media/font/pixelated.ttf", 20)
        WINDOW.fill(BLACK)
        BUTTON1 = pygame.Rect(350, 300, 100, 50)
        BUTTON2 = pygame.Rect(350, 360, 100, 50)
        font = pygame.font.Font("media/font/pixelated.ttf", 50)
        text = font.render("Jerry's Croissants", True, WHITE)
        text_rect = text.get_rect(center=(400, 200))
        text_play = font.render("Play", True, BLACK)
        text_rect_play = text_play.get_rect(center=(400, 320))
        text_options = font.render("Help", True, BLACK)
        text_options_rect = text_options.get_rect(center=(400, 380))
        pygame.draw.rect(WINDOW, (255, 255, 0), BUTTON2)




        mx, my = pygame.mouse.get_pos()
        if BUTTON1.collidepoint((mx, my)):
            pygame.draw.rect(WINDOW, RED, BUTTON1)
            if click:
                pygame.mixer.music.stop()
                game()
        else:
            pygame.draw.rect(WINDOW, (255, 255, 0), BUTTON1)


        if BUTTON2.collidepoint((mx, my)):
            pygame.draw.rect(WINDOW, RED, BUTTON2)
            gamefont.render_to(WINDOW, (40, 40), "WASD  to  move.", (255, 255, 255))
            gamefont.render_to(WINDOW, (40, 80), "Right  shift  for  shield.", (255, 255, 255))
            gamefont.render_to(WINDOW, (40, 120), "JL  stands  for  jump  limit,  eat  croissants  to  increase  it  for  one  level.", (255, 255, 255))

        gamefont.render_to(WINDOW, (630, 570), "Made by Jose Perez", (255, 255, 255))
        WINDOW.blit(text, text_rect)
        WINDOW.blit(text_play, text_rect_play)
        WINDOW.blit(text_options, text_options_rect)
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == QUIT:
                pygame.quit()

        pygame.display.flip()
main_menu()

