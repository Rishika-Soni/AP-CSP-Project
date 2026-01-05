import pygame
import random
import sys
import os
import tkinter as tk
from tkinter import simpledialog


# popup window to enter player name before game starts
root = tk.Tk()
root.withdraw()
player_name = ""
while player_name.strip() == "":
    player_name = simpledialog.askstring("Player Name", "Enter your name")
root.destroy()


CELL = 20
COLS, ROWS = 20, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FPS = 8


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
GRAY = (200, 200, 200)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
direction = (1, 0)
food = None
score = 0
game_over = False


# load leaderboard file if exists
if os.path.exists("leaderboard.txt"):
    with open("leaderboard.txt", "r") as f:
        leaderboard = [line.strip().split(",") for line in f.readlines()]
else:
    leaderboard = []


# save score and keep only top 5
def save_score(name, score):
    leaderboard.append([name, str(score)])
    leaderboard.sort(key=lambda x: int(x[1]), reverse=True)
    leaderboard[:] = leaderboard[:5]
    with open("leaderboard.txt", "w") as f:
        for n, s in leaderboard:
            f.write(f"{n},{s}\n")


# place food at random grid cell not on snake
def place_food():
    while True:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in snake:
            return pos


food = place_food()


# movement and collision logic
def update_snake(dir_vector, grow=False):
    global snake
    dx, dy = dir_vector
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)
    if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
        return True
    if new_head in snake:
        return True
    snake.insert(0, new_head)
    if not grow:
        snake.pop()
    return False


# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # movement + restart control
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if direction != (0, 1):
                    direction = (0, -1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if direction != (0, -1):
                    direction = (0, 1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if direction != (1, 0):
                    direction = (-1, 0)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if direction != (-1, 0):
                    direction = (1, 0)
            if event.key == pygame.K_r and game_over:
                snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
                direction = (1, 0)
                food = place_food()
                score = 0
                game_over = False


    # snake movement and scoring
    if not game_over:
        head_x, head_y = snake[0]
        next_head = (head_x + direction[0], head_y + direction[1])
        will_grow = (next_head == food)
        collided = update_snake(direction, grow=will_grow)
        if will_grow:
            score += 1
            food = place_food()
        if collided:
            game_over = True
            save_score(player_name, score)


    screen.fill(BLACK)


    # grid draw
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


    # snake draw
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
        if i == 0:
            pygame.draw.rect(screen, GREEN, rect)
        else:
            pygame.draw.rect(screen, (0, max(0, 150 - 5*i), 0), rect)


    # food draw
    fx, fy = food
    food_rect = pygame.Rect(fx * CELL, fy * CELL, CELL, CELL)
    pygame.draw.rect(screen, RED, food_rect)


    # score display
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (5, 5))


    # leaderboard on game over
    if game_over:
        go_surf = font.render("GAME OVER", True, WHITE)
        screen.blit(go_surf, (WIDTH // 2 - 60, HEIGHT // 2 - 10))
        y_offset = HEIGHT // 2 + 30
        for i, (n, s) in enumerate(leaderboard):
            lb = font.render(f"{i+1}. {n}: {s}", True, WHITE)
            screen.blit(lb, (WIDTH // 2 - 70, y_offset))
            y_offset += 20


    pygame.display.flip()
    clock.tick(FPS)
    