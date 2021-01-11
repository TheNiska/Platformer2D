import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 14)
WINDOW_SIZE = (896, 560)
pygame.display.set_caption('Platformer')
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((448, 280))
# 14 тайлов на экране в ширину и 8.75 в высоту

class Player():
    def __init__(self, rect):
        self.isMovingLeft = False
        self.isMovingRight = False
        self.rect = rect
        self.activity = 'idle'
        self.flip = False
        self.frame = 0
        self.speed_x = 2
        self.momentumY = 0
        self.momentum_change_rate = 0.4
        self.air_timer = 0
        self.air_count = 0
        self.movement = [0, 0]
        self.isGrounded = True

    
    def move(self, tiles):
        # сначала двигаемся на фрейм по оси x и смотрим, есть ли столкновения, а потом так же по оси y
        self.movement = [0, 0]

        if self.isMovingRight:
            self.movement[0] += self.speed_x
        elif self.isMovingLeft:
            self.movement[0] -= self.speed_x

        self.movement[1] += self.momentumY / 1.2 # использовать делитель для изменения скорости прыжка
        self.momentumY += self.momentum_change_rate
        if self.momentumY > 8:
            self.momentumY = 8

        if self.isGrounded:
            if self.movement[0] > 0:
                self.activityChange('run')
                self.flip = False
            elif self.movement[0] < 0:
                self.activityChange('run')
                self.flip = True
            elif self.movement[0] == 0:
                self.activityChange('idle')

        # теперь здесь начинается проверка коллизий
        collision_types = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}

        self.rect.x += self.movement[0]
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True

        self.rect.y += self.movement[1]
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True


        return collision_types


    def activityChange(self, new_activity_value):
        if self.activity != new_activity_value:
            self.activity = new_activity_value
            self.frame = 0



# tile size 32 x 32
TILE_SIZE = 32

grass = pygame.image.load('tiles/grass_block.png') # 1
ground = pygame.image.load('tiles/ground.png')  # 2
um = pygame.image.load('pix_umbrella.png')


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


animation_database = {}
animation_database['idle'] = load_animation('animation/idle', [70, 70])
animation_database['run'] = load_animation('animation/run', [10])
animation_database['fly'] = load_animation('animation/fly', [1])


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

#background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 70, 350]]]


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


rect = pygame.Rect(100, 100, animation_frames['idle_0'].get_width(), 
                                   animation_frames['idle_0'].get_height())
player = Player(rect)

while  True:
    display.fill((146, 244, 255)) # заполняем экран цветом
    
    #-расчёт расположения камеры----------------------------------------#
    true_scroll[0] += (player.rect.x - true_scroll[0] - 150) / 18
    true_scroll[1] += (player.rect.y - true_scroll[1] - 150) / 18
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

    #--рисуем тайлы и если эти тайлы должны иметь способность к столкновению, то добавляем-----#
    #--координаты тайла в список в форме pygame.rect
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
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    #------------------------------------------------------------------------------------------#



    collisions = player.move(tile_rects)

    if collisions['bottom']: # если мы столкнулись с тайлом снизу, то не надо увеличивать ускорения падения
        player.momentumY = 0
        player.air_timer = 0
        player.air_count = 0
        player.isGrounded = True
    else:
        player.air_timer += 1
    if collisions['top']:
        player.momentumY = 0


    player.frame += 1
    if player.frame >= len(animation_database[player.activity]):
        player.frame = 0
    player_img_id = animation_database[player.activity][player.frame]
    player_img = animation_frames[player_img_id]

    display.blit(pygame.transform.flip(player_img, player.flip, False), 
                                      (player.rect.x - scroll[0], player.rect.y - scroll[1]))
    #pygame.draw.rect(display, (255, 0 , 0), (player.rect.x - scroll[0], player.rect.y - scroll[1], 
      #                                       player.rect.width, player.rect.height), 2)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.isMovingRight = True
                was_left = False
            if event.key == K_LEFT:
                player.isMovingLeft = True
                was_left = True
            if event.key == K_UP or event.key ==  K_SPACE and not player.activity == 'fly' :
                #if air_timer < 20:
                    #player_y_momentum = -6
                if not collisions['bottom']:
                    if player.air_count < 2:
                        player.air_count +=1
                        player.momentumY = -7
                        player.isGrounded = False
                else:
                    player.momentumY = -7
            if event.key == K_x and not collisions['bottom']:
                player.momentumY = 2
                player.momentum_change_rate = 0
                player.activity = 'fly'
                




        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.isMovingRight = False
            if event.key == K_LEFT:
                player.isMovingLeft = False
            if event.key == K_x and not collisions['bottom']:
                player.momentum_change_rate = 0.4
                player.activity = 'run'

    text = str(clock.get_fps())
    #text = f'X: {player.rect.x} Y: {player.rect.y} momentum: {player.momentumY}'
    textsurface = myfont.render(text, False, (0, 0, 0))
    display.blit(textsurface,(0,0))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(50)