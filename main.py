#!usr/bin/env
import pygame, sys

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt


pygame.init()

SCREEN_WIDTH = 300   #  10 чарунок по 30 пкс кожна
SCREEN_HEIGHT = 600  #  20 чарунок по 30 пкс кожна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOWER_COLOR = (150, 150, 150)
GREY = (128, 128, 128)

# Налаштування частоти кадрів
FPS = 30
clock = pygame.time.Clock()

# Налаштування сітки
CELL_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE   # 10 комірок
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE   # 20 комірок


def create_array_for_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect_obj = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREY, rect_obj, 1)


def main():
    
    # Основний ігровий цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Заповнення екрану кольором тла
        # screen.fill(BLACK)
        screen.fill(BLACK)

        draw_grid()

        # Оновлення екрану
        pygame.display.flip()
        # Затримка для управління FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()