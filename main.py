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
# BLUE = (0, 0, 255)
BLUE = (0, 255, 255)
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
            pygame.draw.rect(screen, BLACK, rect_obj, 1)


# Визначення тетріміно (лінійний блок)
class Tetromino:
    def __init__(self) -> None:
        # поч-ві коорд-ти тетріміно
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        self.shape = [(0, 0), (1, 0), (2, 0), (3, 0)]
        self.color = BLUE

    def draw(self):
        for cell in self.shape:
            rect_obj = pygame.Rect((self.x + cell[0]) * CELL_SIZE, (self.y + cell[1]) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, self.color, rect_obj)
    
    # Переміщення тетроміно вниз
    def move_down(self):
        if self.y < GRID_HEIGHT - 1:
            self.y += 1

    def move_left(self):
        if self.x > 0 and self.y < GRID_HEIGHT - 1:
            self.x -= 1

    def move_right(self):
        # Мій варіант:
        # if self.x < GRID_WIDTH - len(self.shape):
        # Варіант від ChatGPT:
        if self.x + max(cell[0] for cell in self.shape) < GRID_WIDTH - 1 and self.y < GRID_HEIGHT - 1:
            self.x += 1


# Основний ігровий цикл
def main():
    grid = create_array_for_grid()
    tetromino = Tetromino()
    drop_speed = 500  # Швидкість падіння (мс)
    last_drop_time = pygame.time.get_ticks()  # Час останнього падіння

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino.move_left()
                elif event.key == pygame.K_RIGHT:
                    tetromino.move_right()
                elif event.key == pygame.K_DOWN:
                    tetromino.move_down()

        # Оновлення положення тетріміно
        current_time = pygame.time.get_ticks()
        if current_time - last_drop_time > drop_speed:
            tetromino.move_down()
            last_drop_time = current_time
        
        # Заповнення екрану кольором тла
        # screen.fill(BLACK)
        screen.fill(GREY)

        draw_grid()
        tetromino.draw()

        # Оновлення екрану
        pygame.display.flip()
        # Затримка для управління FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()