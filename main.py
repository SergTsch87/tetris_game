#!usr/bin/env python3
import pygame, sys, random

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

# !!!
# Tetris: Rotate system SRS
# https://www.freetetris.org/game.php
# Подивись, як обертаються тетраміно у різних випадках!

# Для порівнянь двох комітів:
# https://github.com/SergTsch87/tetris_game/compare/9c806b4..531a140

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
# NEXT_AREA_HEIGHT = 0 * CELL_SIZE

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


def some_new_func():
    pass


# Not Using!
def create_array_for_grid():
    # Ігрове поле '10 x 20', початково усі чарунки порожні
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


# def list_coords_bottom_field(all_coords, tetromino_shape_coords, color):
# def list_coords_bottom_field(all_coords, cell_x, cell_y, tetromino_shape_coords):
def list_coords_bottom_field(all_coords, cell_x, cell_y):
    # Кожне x, y зі списку tetromino_shape_coords множимо на CELL_SIZE
    # Як визначити хоча б одну координату, в якій зупинилась фігура внизу поля?..
    
    # list_cells_x_y = list(zip(current_tetromino.cell_x, current_tetromino.cell_y))
    # print(f'new_list_x == {list(map(lambda x: x * CELL_SIZE, cell_x))}')
    # print(f'new_list_y == {list(map(lambda y: y * CELL_SIZE, cell_y))}')
    new_list_x = list(map(lambda x: x * CELL_SIZE, cell_x))
    new_list_y = list(map(lambda y: y * CELL_SIZE, cell_y))
    list_cells_x_y = list(zip(new_list_x, new_list_y))
    # list_cells_x_y = list(zip(cell_x, cell_y))
    # print(f'\ndef list_coords_bottom_field:  list_cells_x_y == {list_cells_x_y}\n')
    
    # all_coords.extend(tetromino_shape_coords)
    all_coords.extend(list_cells_x_y)
    # print(f'\ndef list_coords_bottom_field:  all_coords == {all_coords}\n')
    return all_coords
    # return all_coords, color

def draw_bottom_field(all_coords, color):
    # print(f'\ndraw_bottom_field:  all_coords == {all_coords}\n')
    for cell in all_coords:
        # абсолютні коорд-ти:
        # cell_x = cell[0] * CELL_SIZE
        # cell_y = cell[1] * CELL_SIZE
        cell_x = cell[0]
        cell_y = cell[1]
        # print(f'(cell_x, cell_y) == ({cell_x}, {cell_y})')
        # rect_obj = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
        # rect_obj = pygame.Rect(cell_x, NEXT_AREA_HEIGHT + cell_y, CELL_SIZE, CELL_SIZE)
        
        # !!! Це трохи допомогло!
        # Але, фігури дивно пересуваються наприкінці: за дві чарунки до низу поля, вони затримуються, а потім швидко "перестрибуються через дві чарунки".
        # А деякі фігури можуть ще й зависнути, не рухаючись вниз (тільки по горизонталі).
        # "Розвиснути" можуть, якщо почати їх крутити
        rect_obj = pygame.Rect(cell_x, 2 * CELL_SIZE + cell_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect_obj)
        # pygame.draw.rect(screen, BLUE, rect_obj)
        # print(f'\ndef draw_bottom_field:  screen == {screen}\n')


# Чи нема тут помилки?..
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
    return Tetromino(shape, color)


def print_test(var):
    print(f'{vars.__name__} == {var}')


def rotate_tetromino(coords_figure_x_y):
    return [(-y, x) for x, y in coords_figure_x_y]
    

# Not Using!
def check_collision(coords_figure_x_y, grid_binary_coords):
    for x, y in coords_figure_x_y:
        if not(0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            return True
        if grid_binary_coords[y][x] == 1:
            return True
    return False


# Визначення тетріміно (лінійний блок)
class Tetromino:
    instances = []

    def __init__(self, shape, color) -> None:
        # поч-ві (відносні) коорд-ти тетріміно
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0      # Початкова позиція тетроміно на основній сітці
        # self.y = -3      # Початкова позиція тетроміно на основній сітці
        # self.y = NEXT_AREA_HEIGHT // CELL_SIZE     # Початкова позиція тетроміно на основній сітці
        self.shape = shape
        self.color = color
        Tetromino.instances.append(self)

    def draw(self):
        for cell in self.shape:
            # абсолютні коорд-ти:
            cell_x = (self.x + cell[0]) * CELL_SIZE
            
            # cell_y = NEXT_AREA_HEIGHT + (self.y + cell[1]) * CELL_SIZE  # Тут фігури падають з самого верха, і промальовуються за 3 чарунки перед низом
            cell_y = (self.y + cell[1]) * CELL_SIZE  # Тут фігури падають з 3-ї чарунки, пролітають до низу, і промальовуються за 3 чарунки перед низом
            
            # print(f'\ndef draw(self):  cell_y == {cell_y}\n')
            rect_obj = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, self.color, rect_obj)
        # print(f'\ndef draw(self): last in for:  cell_y == {cell_y}\n')
    
    # Переміщення тетроміно вниз
    def move_down(self):
        # print(f'\n def move_down:  self.y == {self.y}')
        # print(f'def move_down:  GRID_HEIGHT == {GRID_HEIGHT}\n')
        if self.y < GRID_HEIGHT - 1:
        # if self.y < 2 * GRID_HEIGHT - 1:  # Цей код не впливає на "540 пкс"...
        # if self.y < (NEXT_AREA_HEIGHT // CELL_SIZE + GRID_HEIGHT - 1):
            self.y += 1
        # print(self.y)
        # else:
        #     self.y = y


    @property
    def cell_x(self):
        # Повертає список X-координат для фігури із врахуванням поточного зміщення
        return [cell[0] + self.x for cell in self.shape]
    
    @property
    def cell_y(self):
        # print(f'\n@property: self.shape == {self.shape}')
        # print(f'@property: [cell[1] for cell in self.shape] == {[cell[1] for cell in self.shape]}')
        # print(f'@property: self.y == {self.y}')
        # print(f'@property: return  [cell[1] + self.y for cell in self.shape]  ==  {[cell[1] + self.y for cell in self.shape]}\n')
        # Повертає список Y-координат для фігури із врахуванням поточного зміщення
        
        return [cell[1] + self.y for cell in self.shape]
        # return [cell[1] + self.y for cell in self.shape]


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

    grid_binary = create_array_for_grid()
    
    # Випадковий вибір поточного тетроміно
    current_tetromino = get_tetromino()
    fix_tetromino = get_tetromino()
    
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
            
            # !!!
            # Саме після заміни першого коду на другий (current_tetromino.shape на current_tetromino.cell_y)
            # фігури й почали доходити тільки до 360-ти пкс
            # if current_tetromino.y + max(cell[1] for cell in current_tetromino.shape) >= GRID_HEIGHT + 2:  # фігури опускаються тільки на одну чарунку нижче, - більше не виходить...
            
            # if current_tetromino.y + max(cell[1] for cell in current_tetromino.shape) >= GRID_HEIGHT - 1:
            if current_tetromino.y + max(cell[1] for cell in current_tetromino.shape) >= GRID_HEIGHT:

            # if current_tetromino.y + max(current_tetromino.cell_y) >= GRID_HEIGHT - 1:
                # Тут буде зупинка фігури
                # print('if current_tetromino.y + max(current_tetromino.cell_y) >= GRID_HEIGHT - 1:')
                # print(f'all_coords == {all_coords}')
                # print(f'current_tetromino.cell_x == {current_tetromino.cell_x}')
                # print(f'current_tetromino.cell_y == {current_tetromino.cell_y}')
                # print(f'current_tetromino.shape == {current_tetromino.shape}')

                # all_coords = list_coords_bottom_field(all_coords, current_tetromino.shape, current_tetromino.color)
                # all_coords = list_coords_bottom_field(all_coords, current_tetromino.cell_x, current_tetromino.cell_y, current_tetromino.shape)
                all_coords = list_coords_bottom_field(all_coords, current_tetromino.cell_x, current_tetromino.cell_y)
                # list(TETROMINO_SHAPES.keys())
                # print(f'all_coords = list_coords_bottom_field  >>>  all_coords == {all_coords}')
                # print('The end\n')
                
                fix_tetromino = current_tetromino

                # draw_bottom_field(all_coords, current_tetromino.color)
                # draw_bottom_field(all_coords, fix_tetromino.color)
                # pygame.display.flip()

                # print(f'(cell_X, cell_Y) == ({fix_tetromino.cell_x}, {fix_tetromino.cell_y})')
                # приклад: (cell_X, cell_Y) == ([7, 6, 5, 5], [20, 20, 20, 19])
                # print(f'(X, Y) == ({fix_tetromino.x}, {fix_tetromino.y})')
                # # приклад: (X, Y) == (7, 19)

                list_cells_x_y = list(zip(fix_tetromino.cell_x, fix_tetromino.cell_y))
                # print(f'list_cells_x_y == {list_cells_x_y}')

                # print_test(list_cells_x_y)


                current_tetromino = next_tetromino
                next_tetromino = get_tetromino()  # Новий блок згори

                print(f'\nmain >> if current_time - last_drop_time > drop_speed: >>  all_coords == {all_coords}\n')
            else:
                current_tetromino.move_down()
            
            last_drop_time = current_time
        
        # Заповнення екрану кольором тла
        screen.fill(GREY)

        draw_grid()
        current_tetromino.draw()
        draw_next_tetromino(next_tetromino.shape, next_tetromino.color)
        
        print(f'\nmain >> before draw_bottom_field(all_coords): >>  all_coords == {all_coords}\n')
        draw_bottom_field(all_coords, fix_tetromino.color)

        # Оновлення екрану
        pygame.display.flip()
        # Затримка для управління FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()