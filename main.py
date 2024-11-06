#!usr/bin/env
import pygame, sys

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt


def main():
    
    pygame.init()

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    BLACK = (0, 0, 0)

    # Налаштування частоти кадрів
    FPS = 30
    clock = pygame.time.Clock()

    # Основний ігровий цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Заповнення екрану кольором тла
        screen.fill(BLACK)
        # Оновлення екрану
        pygame.display.flip()
        # Затримка для управління FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()