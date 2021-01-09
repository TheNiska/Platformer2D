import pygame
import sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
WINDOW_SIZE = (400, 400)
pygame.display.set_caption('Platformer')
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (player_image.get_width()//3, player_image.get_height()//3))
grass = pygame.image.load('tile2.png') # 1
lava = pygame.image.load('tile3.png')  # 2

game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], # game_map[y][x]
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['1', '1', '1', '1', '1', '1', '1', '2', '2', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

# задаём булевские переменные движется ли объект вправо или влево
moving_left = False
moving_right = False

# расположение игрока на оси x и y, и его ускорение по оси y
player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

while  True:
    screen.fill((146, 244, 255)) # заполняем экран цветом
    screen.blit(player_image, player_location) # рисуем player_image в позиции player_location

    # если спрайт игрока выходит за нижнюю границу окна, то меняет направление движения игрока 
    # на противоположное, иначе просто увеличивает ускорение движения. Если игрок движется вверх,
    # то его ускорение отрицательно и она постепенно станет положительным и игрок будет двигаться вниз
    if player_location[1] > WINDOW_SIZE[1] - player_image.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    # обработка движения по оси x
    if moving_right:
        player_location[0] += 4
    if moving_left:
        player_location[0] -= 4

    # обновляем координаты прямоугольника коллизий игрока
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)

    # если одни прямоугольник столкнулся с другим
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255, 0 ,0), test_rect)
    else:
        pygame.draw.rect(screen, (0, 0 ,0), test_rect)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False        

    pygame.display.update()
    clock.tick(60)
