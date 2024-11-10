#!usr/bin/env python3
import pygame, sys, random

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

# https://www.freetetris.org/game.php
# Подивись, як обертаються тетраміно у різних випадках!

pygame.init()

# https://www.color-blindness.com/color-name-hue/
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 166, 0)
DARK_VIOLET = (168, 0, 191)
LIME = (0, 255, 0)
GREY = (128, 128, 128)
HOWER_COLOR = (165, 165, 165) # DARK_GREY

# Налаштування частоти кадрів
FPS = 30
clock = pygame.time.Clock()

# Основні розміри екрану та комірок
CELL_SIZE = 30
GRID_WIDTH = 10 # комірок
GRID_HEIGHT = 20 # комірок

# Висота області для наступного тетраміно
NEXT_AREA_HEIGHT = 3 * CELL_SIZE

# Загальна висота екрану (ігрова зона + область для наступного тетраміно)
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + NEXT_AREA_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

TETROMINO_SHAPES = {
                    'I': [(0, 0), (1, 0), (2, 0), (3, 0)],  # AQUA
                    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],  # YELLOW
                    'L': [(0, 0), (0, 1), (0, 2), (1, 2)],  # ORANGE
                    'J': [(1, 0), (1, 1), (1, 2), (0, 2)],  # BLUE
                    'T': [(0, 0), (1, 0), (2, 0), (1, 1)],  # DARK_VIOLET
                    'S': [(1, 0), (2, 0), (0, 1), (1, 1)],  # LIME
                    'z': [(0, 0), (1, 0), (1, 1), (2, 1)]   # RED
}

TETROMINO_COLORS = {
                    'I': AQUA,
                    'O': YELLOW,
                    'L': ORANGE,
                    'J': BLUE,
                    'T': DARK_VIOLET,
                    'S': LIME,
                    'z': RED
}

def create_array_for_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect_obj = pygame.Rect(x * CELL_SIZE, NEXT_AREA_HEIGHT + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect_obj, 1)


# Відображає наступне тетраміно у верхній області
def draw_next_tetromino(shape, color):
    for cell in shape:
        cell_x = (3 + cell[0]) * CELL_SIZE   # Позиція у верхній частині екрану
        cell_y = (1 + cell[1]) * CELL_SIZE   # Позиція у верхній частині екрану
        pygame.draw.rect(screen, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))


# Випадковий вибір тетроміно
def get_tetromino():
    current_shape = random.choice(list(TETROMINO_SHAPES.keys()))
    shape = TETROMINO_SHAPES[current_shape]
    color = TETROMINO_COLORS[current_shape]
    # min_x = min(cell[0] for cell in current_shape)
    # max_x = max(cell[0] for cell in current_shape)
    # min_y = min(cell[1] for cell in current_shape)
    # max_y = max(cell[1] for cell in current_shape)
    # max_min_x_y = [min_x, max_x, min_y, max_y]
    return Tetromino(shape, color)


def list_coords_bottom_field(all_coords, tetromino_shape_coords):
    all_coords += tetromino_shape_coords
    return all_coords


# Визначення тетріміно (лінійний блок)
class Tetromino:
    instances = []

    def __init__(self, shape, color) -> None:
        # поч-ві (відносні) коорд-ти тетріміно
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0      # Початкова позиція тетроміно на основній сітці
        self.shape = shape
        self.color = color
        Tetromino.instances.append(self)

    def draw(self):
        for cell in self.shape:
            # абсолютні коорд-ти:
            cell_x = (self.x + cell[0]) * CELL_SIZE
            cell_y = NEXT_AREA_HEIGHT + (self.y + cell[1]) * CELL_SIZE
            rect_obj = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, self.color, rect_obj)
    
    # Переміщення тетроміно вниз
    def move_down(self):
        if self.y < GRID_HEIGHT - 1:
            self.y += 1
        print(self.y)
        # else:
        #     self.y = y


    @property
    def cell_x(self):
        # Повертає список X-координат для фігури із врахуванням поточного зміщення
        return [cell[0] + self.x for cell in self.shape]
    
    @property
    def cell_y(self):
        # Повертає список Y-координат для фігури із врахуванням поточного зміщення
        return [cell[1] + self.y for cell in self.shape]


    def move_left(self):
        # # if self.x > 0:
        # min_x = min(cell[0] for cell in self.shape)
        if min(self.cell_x) > 0:
            self.x -= 1


    def move_right(self):
        # # Мій варіант: - такий код не враховує різноманітність форм тетраміно!..
        # # if self.x < GRID_WIDTH - len(self.shape):

        # # Варіант від ChatGPT: - а такий код варто оптимізувати, - щоб був без циклів
        # max_x = max(cell[0] for cell in self.shape)
        # if self.x + max_x < GRID_WIDTH - 1:
        if max(self.cell_x) < GRID_WIDTH - 1:
            self.x += 1


    def rotate(self):
        # Обертаємо фігуру на 90 градусів за годинниковою стрілкою
        rotated_shape = [(-y, x) for x, y in self.shape]

        # Отримуємо координати обмеженої фігури
        rotated_cell_x = [cell[0] + self.x for cell in rotated_shape]
        rotated_cell_y = [cell[1] + self.y for cell in rotated_shape]

        # Перевіряємо, чи виходить фігура за межі екрану після обертання
        min_x, max_x = min(rotated_cell_x), max(rotated_cell_x)
        min_y, max_y = min(rotated_cell_y), max(rotated_cell_y)

        # Корекція положення по X
        if min_x < 0:
            self.x -= min_x  # Зсуваємо праворуч
        elif max_x >= SCREEN_WIDTH // CELL_SIZE:
            self.x -= max_x - (SCREEN_WIDTH // CELL_SIZE - 1)  # Зсуваємо ліворуч

        # Корекція положення по Y
        if max_y >= SCREEN_HEIGHT // CELL_SIZE:
            return   # скасовуємо обертання, якщо не вдається вирівняти по Y
        
        # # if (0 <= min_x <= max_x <= SCREEN_WIDTH) and (max_y <= SCREEN_HEIGHT):
        # if (0 <= min_x <= max_x <= SCREEN_WIDTH):
        # # if (self.x + min_x < 0) or (self.x + max_x >= SCREEN_WIDTH // CELL_SIZE) or (self.y + max_y <= SCREEN_HEIGHT // CELL_SIZE):
        #     return
        #     # Якщо виходить за межі, тоді обертання не буде

        # Якщо колізії немає, оновлюємо форму
        self.shape = rotated_shape


# Основний ігровий цикл
def main():
    # grid = create_array_for_grid()
    all_coords = []
    
    # Випадковий вибір поточного тетроміно
    current_tetromino = get_tetromino()
    
    drop_speed = 500  # Швидкість падіння (мс)
    last_drop_time = pygame.time.get_ticks()  # Час останнього падіння
    
    # Випадковий вибір наступного тетроміно
    next_tetromino = get_tetromino()
    
    running = True    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move_left()
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_right()
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move_down()
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()

        # Оновлення положення тетріміно
        current_time = pygame.time.get_ticks()
        if current_time - last_drop_time > drop_speed:
            # Якщо блок знаходиться на нижній межі, тоді створити новий
            if current_tetromino.y + max(cell[1] for cell in current_tetromino.shape) >= GRID_HEIGHT - 1:
                # Тут буде зупинка фігури
                all_coords = list_coords_bottom_field(all_coords, current_tetromino.shape)
                # list(TETROMINO_SHAPES.keys())

                current_tetromino = next_tetromino
                next_tetromino = get_tetromino()  # Новий блок згори
            else:
                current_tetromino.move_down()
            
            last_drop_time = current_time
        
        # Заповнення екрану кольором тла
        screen.fill(GREY)

        draw_grid()
        current_tetromino.draw()
                
        draw_next_tetromino(next_tetromino.shape, next_tetromino.color)

        # Оновлення екрану
        pygame.display.flip()
        # Затримка для управління FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()