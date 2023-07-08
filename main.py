import pygame
import time
import random


# Game settings
DEBUG = True

GOING_THROUGH_WALLS = True

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 400, 400

SNAKE_STEP = 10
GAME_SPEED = 10

# Initializing game 
pygame.init()
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Oleg\' Snake Game')
pygame.display.update()

# Object to set up display flip freequency
clock = pygame.time.Clock()

# Helpers
font = pygame.font.SysFont(None, size=50)

def raise_msg(text, color):
    msg = font.render(text, True, color)
    dis.blit(msg, [WIDTH // 3, HEIGHT // 3])

def get_food_coords():
    food_x = round(random.randint(0, WIDTH-SNAKE_STEP) / SNAKE_STEP) * SNAKE_STEP
    food_y = round(random.randint(0, HEIGHT-SNAKE_STEP) / SNAKE_STEP) * SNAKE_STEP

    return food_x, food_y

def draw_snake(dis, snake_list):
    for coords in snake_list:
        pygame.draw.rect(dis, BLACK, [coords[0], coords[1], SNAKE_STEP, SNAKE_STEP])

def display_score(dis, score):
    msg = font.render(f"Score: {str(score)}", True, GREEN)
    dis.blit(msg, [0, 0])

terminate_window = False
game_over = False
hit_wall = False

snake_len = 1
snake_list = []

x, y = WIDTH // 2, HEIGHT // 2
food_x, food_y = get_food_coords()

dx, dy = 0, SNAKE_STEP

while not terminate_window:
    # hanging on in menu
    while game_over:
        raise_msg('Game Over!', RED)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:

                    # init game again
                    game_over = False
                    x, y = WIDTH // 2, HEIGHT // 2
                    food_x, food_y = get_food_coords()
                    dx, dy = 0, SNAKE_STEP
                    dis.fill(WHITE)
                    pygame.display.update()
                    snake_list = []
                    snake_len = 1
                elif event.key == pygame.K_q:
                    terminate_window = True
                    game_over = False
            
            elif event.type == pygame.QUIT:
                terminate_window = True
                game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate_window = True
        
        # TODO break is necessary because otherwise multiple actions are taken and overlaps (very fast UP->LEFT ends up in moving through the snake)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not dx > 0:
                dx = -SNAKE_STEP
                dy = 0
                break
            elif event.key == pygame.K_RIGHT and not dx < 0:
                dx = SNAKE_STEP
                dy = 0
                break
            elif event.key == pygame.K_UP and not dy > 0:
                dx = 0
                dy = -SNAKE_STEP
                break
            elif event.key == pygame.K_DOWN and not dy < 0:
                dx = 0
                dy = SNAKE_STEP
                break

    if not hit_wall:
        x += dx
        y += dy
    elif 0 <= x + dx <= WIDTH - 10 and 0 <= y + dy <= HEIGHT - 10:
        hit_wall = False
        x += dx
        y += dy

    if x < 0 or WIDTH < x + 10 or HEIGHT < y + 10 or y < 0:
        if not DEBUG and not GOING_THROUGH_WALLS:
            game_over = True
        elif DEBUG and not GOING_THROUGH_WALLS:
            hit_wall = True
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + 10 > WIDTH:
                x = WIDTH - 10
            if y + 10 > HEIGHT:
                y = HEIGHT - 10
        else:
            if x < 0:
                x = WIDTH - 10
            elif y < 0:
                y = HEIGHT - 10
            elif x + 10 > WIDTH:
                x = 0
            elif y + 10 > HEIGHT:
                y = 0

    if not hit_wall:
        head = (x, y)
        # check snake doesn't eat itself
        for t in snake_list:
            if head == t:
                game_over = True

        # shifting the head each stroke ->
        snake_list.append(head)

        # taking care of the tail
        if len(snake_list) > snake_len:
            del snake_list[0]

    if x == food_x and y == food_y:
        food_x, food_y = get_food_coords()
        while (food_x, food_y) in snake_list:
            food_x, food_y = get_food_coords()
        snake_len += 1

    # drawing part
    dis.fill(WHITE)

    pygame.draw.rect(dis, RED, [food_x, food_y, SNAKE_STEP, SNAKE_STEP])
    draw_snake(dis, snake_list)
    display_score(dis, snake_len-1)
    pygame.display.update()

    # Screen upd frequency
    clock.tick(GAME_SPEED)


pygame.quit()
quit()