import pygame
import time
import random


DEBUG = True

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 900, 600

pygame.init()
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()
pygame.display.set_caption('Oleg\' Snake Game')

clock = pygame.time.Clock()

SNAKE_STEP = 10
GAME_SPEED = 10

x, y = WIDTH // 2, HEIGHT // 2
dx, dy = 0, 0

font = pygame.font.SysFont(None, size=50)
def raise_msg(text, color):
    msg = font.render(text, True, color)
    dis.blit(msg, [WIDTH // 3, HEIGHT // 3])

def get_food_coords():
    food_x = round(random.randint(0, WIDTH-SNAKE_STEP) / SNAKE_STEP, 1) * SNAKE_STEP
    food_y = round(random.randint(0, HEIGHT-SNAKE_STEP) / SNAKE_STEP, 1) * SNAKE_STEP

    return food_x, food_y

food_x, food_y = get_food_coords()

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -SNAKE_STEP
                dy = 0
            elif event.key == pygame.K_RIGHT:
                dx = SNAKE_STEP
                dy = 0
            elif event.key == pygame.K_UP:
                dx = 0
                dy = -SNAKE_STEP
            elif event.key == pygame.K_DOWN:
                dx = 0
                dy = SNAKE_STEP

    x += dx
    y += dy

    # TODO DEBUG! it's game over cases
    if DEBUG:
        if x < 0:
            x = 0
            dx = 0
        if y < 0:
            y = 0
            dy = 0
        if x + 10 > WIDTH:
            x = WIDTH - 10
            dx = 0
        if y + 10 > HEIGHT:
            y = HEIGHT - 10
            dy = 0
    
    elif x < 0 or WIDTH < x + 10 or HEIGHT < y + 10 or y < 0:
        game_over = True
    
    dis.fill(WHITE)

    pygame.draw.rect(dis, BLACK, [x, y, SNAKE_STEP, SNAKE_STEP])
    pygame.draw.rect(dis, RED, [food_x, food_y, SNAKE_STEP, SNAKE_STEP])
    pygame.display.update()

    # Screen upd frequency
    clock.tick(GAME_SPEED)

raise_msg('Game Over', RED)
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()