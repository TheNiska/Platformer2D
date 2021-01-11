import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 14)
WINDOW_SIZE = (896, 560)
pygame.display.set_caption('Platformer')
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((448, 280))
# 14 тайлов на экране в ширину и 8.75 в высоту
IMAGE_SCALE = 2
'''
player_image = pygame.image.load('ruby_rose_sprite.png')
player_image_flipped = pygame.transform.flip(player_image, True, False)

player_image = pygame.transform.scale(player_image, (round(player_image.get_width()/IMAGE_SCALE),
                                                     round(player_image.get_height()/IMAGE_SCALE)))
player_image_flipped = pygame.transform.scale(player_image_flipped, (round(player_image_flipped.get_width()/IMAGE_SCALE),
                                                                     round(player_image_flipped.get_height()/IMAGE_SCALE)))
player_images = (player_image, player_image_flipped)
'''

# tile size 32 x 32
TILE_SIZE = 32

grass = pygame.image.load('tiles/grass_block.png') # 1
ground = pygame.image.load('tiles/ground.png')  # 2

true_scroll = [0, 0]

global animation_frames
animation_frames = {}
def load_animation(path, frames_duration):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frames_duration:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)

        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_database = {}
animation_database['idle'] = load_animation('animation/idle', [70, 70])
animation_database['run'] = load_animation('animation/run', [10])
player_action = 'idle'
player_frame = 0
player_flip = False



def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row.split(',')))
    return game_map

game_map = load_map('game_map')

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 70, 350]]]


'''
background_hills = []
for i in range(4):
    scalar = (i + 1)*0.2
    if i < 2:
        background_hills.append((scalar, pygame.image.load('background/bg' + str(i+1) + '.png')))
    else:
        background_hills.append((scalar, pygame.image.load('background/b' + str(i+1) + '.png')))
'''
bg = pygame.image.load('background/b1.png')
bg_tree = pygame.image.load('background/b4.png')

# функция, которая принимает прямоугольник и список тайлов, а выводит список тайлов, с которыми 
# есть столкновение.
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


#-moving-function--------------------------------------------------------------------------------#
# сначала двигаемся на фрейм по оси x и смотрим, есть ли столкновения, а потом так же по оси y
def move(rect, movement, tiles): # movement = [x,y]
    collision_types = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True


    return rect, collision_types
#------------------------------------------------------------------------------------------------#


# задаём булевские переменные движется ли объект вправо или влево
moving_left = False
moving_right = False

# расположение игрока на оси x и y, и его ускорение по оси y

player_y_momentum = 0
air_timer = 0 # сколько фреймов подряд мы находимся в воздухе
air_count = 0 # сколько прыжков мы сделали находясь в воздухе


player_rect = pygame.Rect(100, 100, animation_frames['idle_0'].get_width(), 
                                   animation_frames['idle_0'].get_height())

test_rect = pygame.Rect(100, 100, 100, 50)

while  True:
    display.fill((146, 244, 255)) # заполняем экран цветом
    
    #-расчёт расположения камеры----------------------------------------#
    true_scroll[0] += (player_rect.x - true_scroll[0] - 150) / 15
    true_scroll[1] += (player_rect.y - true_scroll[1] - 150) / 15
    scroll = true_scroll[:]
    scroll[0] = round(scroll[0])
    scroll[1] = round(scroll[1])

    if scroll[0] < 0:
        scroll[0] = 0
    elif scroll[0] > len(game_map[0])*TILE_SIZE - 448:
        scroll[0] = len(game_map[0])*TILE_SIZE - 448
    if scroll[1] < 0:
        scroll[1] = 0
    #-------------------------------------------------------------------#

    
    #scroll = [1, 1]
    '''
    pygame.draw.rect(display, 0x666666, pygame.Rect(0, 170, 300, 80))
    for ob in background_objects:
        ob_rect = pygame.Rect(ob[1][0] - scroll[0]*ob[0], ob[1][1] - scroll[1]*ob[0],
                              ob[1][2], ob[1][3])
        if ob[0] == 0.5:
            pygame.draw.rect(display, 0xF2DFB4, ob_rect)
        else:
            pygame.draw.rect(display, 0x9B634C, ob_rect)
    '''
    '''
    #-рисуем паралакс фон-----------------------------------------------------------#
    for ob in background_hills:
        display.blit(ob[1], (-scroll[0]*ob[0], -50-scroll[1]*ob[0]))
    #-------------------------------------------------------------------------------#
    '''
    display.blit(bg, (-scroll[0]*0.1, -scroll[1]*0.1))
    display.blit(bg_tree, (-scroll[0]*0.5, -scroll[1]*0.5))


    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
            elif tile == '2':
                display.blit(ground, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)) # добавляем в список тайл, и его координаты, если 
                                                                  # этот тайл может сталкиваться
            x += 1

        y += 1



    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum / 1.5 # использовать делитель для изменения скорости прыжка
    player_y_momentum += 0.4
    if player_y_momentum > 8:
        player_y_momentum = 8

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    elif player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True
    elif player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')


    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']: # если мы столкнулись с тайлом снизу, то не надо увеличивать ускорения падения
        player_y_momentum = 0
        air_timer = 0
        air_count = 0
    else:
        air_timer += 1
    if collisions['top']:
        player_y_momentum = 0




    # если игрок двигается вправо, то надо рисовать правый спрайт, если влево - левый,
    # а если игрок стоит на месте, то надо смотреть на предыдущие значения движения

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]

    display.blit(pygame.transform.flip(player_img, player_flip, False), 
                                      (player_rect.x - scroll[0], player_rect.y - scroll[1]))


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
                was_left = False
            if event.key == K_LEFT:
                moving_left = True
                was_left = True
            if event.key == K_UP or event.key ==  K_SPACE:
                #if air_timer < 20:
                    #player_y_momentum = -6
                if not collisions['bottom']:
                    if air_count < 2:
                        air_count +=1
                        player_y_momentum = -7
                else:
                    player_y_momentum = -7


        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    text = str(clock.get_fps())
    textsurface = myfont.render(text, False, (0, 0, 0))
    display.blit(textsurface,(0,0))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)