import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
WINDOW_SIZE = (600, 400)
pygame.display.set_caption('Platformer')
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

player_image = pygame.image.load('player_changed.png').convert()
player_image.set_colorkey((255, 255, 255))
player_image_flipped = player_image
player_image = pygame.transform.flip(player_image, True, False)

player_image = pygame.transform.scale(player_image, (round(player_image.get_width()/2.5),
                                                     round(player_image.get_height()/2.5)))
player_image_flipped = pygame.transform.scale(player_image_flipped, (round(player_image_flipped.get_width()/2.5),
                                                                     round(player_image_flipped.get_height()/2.5)))
player_images = (player_image, player_image_flipped)

grass = pygame.image.load('tile2.png') # 1
lava = pygame.image.load('tile3.png')  # 2

true_scroll = [1, 1]

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

was_left = False

# расположение игрока на оси x и y, и его ускорение по оси y

player_y_momentum = 0
air_timer = 0 # сколько фреймов подряд мы находимся в воздухе


player_rect = pygame.Rect(100, 30, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

while  True:
    display.fill((146, 244, 255)) # заполняем экран цветом

    #-расчёт расположения камеры----------------------------------------#
    true_scroll[0] += (player_rect.x - true_scroll[0] - 114) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 75) / 20
    scroll = true_scroll[:]
    scroll[0] = round(scroll[0])
    scroll[1] = round(scroll[1])
    #-------------------------------------------------------------------#

    pygame.draw.rect(display, 0x666666, pygame.Rect(0, 170, 300, 80))
    for ob in background_objects:
        ob_rect = pygame.Rect(ob[1][0] - scroll[0]*ob[0], ob[1][1] - scroll[1]*ob[0],
                              ob[1][2], ob[1][3])
        if ob[0] == 0.5:
            pygame.draw.rect(display, 0xF2DFB4, ob_rect)
        else:
            pygame.draw.rect(display, 0x9B634C, ob_rect)
                              

                              


    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass, (x*16 - scroll[0], y*16 - scroll[1]))
            elif tile == '2':
                display.blit(lava, (x*16 - scroll[0], y*16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16, y*16, 16, 16)) # добавляем в список тайл, и его координаты, если 
                                                                  # этот тайл может сталкиваться
            x += 1

        y += 1



    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']: # если мы столкнулись с тайлом снизу, то не надо увеличивать ускорения падения
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    if collisions['top']:
        player_y_momentum = 0




    # если игрок двигается вправо, то надо рисовать правый спрайт, если влево - левый,
    # а если игрок стоит на месте, то надо смотреть на предыдущие значения движения
    if moving_right:
        display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    elif moving_left:
        display.blit(player_image_flipped, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    else:
        if was_left:
            display.blit(player_image_flipped, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        else:
            display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))


    #pygame.draw.rect(display, (0, 0, 0), player_rect, 2)


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
                if air_timer < 20:
                    player_y_momentum = -3

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)