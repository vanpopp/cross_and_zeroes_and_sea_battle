import pygame
from random import randint

# Инициализация pygame
pygame.init()

# Константы
CELL_SIZE = 50
GRID_SIZE = 10
MARGIN = 50
WIDTH = HEIGHT = MARGIN * 2 + CELL_SIZE * GRID_SIZE
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морской бой")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Игровое поле
spot = [['.'] * GRID_SIZE for _ in range(GRID_SIZE)]
ships = {'alive': [], 'original': []}


def check_ship(x, y, length, direction):
    """Проверка, можно ли разместить корабль в данной позиции"""
    for i in range(length):
        nx = x + (i if direction == 0 else 0)
        ny = y + (i if direction == 1 else 0)
        if nx < 0 or nx >= GRID_SIZE or ny < 0 or ny >= GRID_SIZE:
            return False

        for other_ship in ships['original']:
            for other_ship_x, other_ship_y in other_ship:
                if abs(nx - other_ship_x) <= 1 and abs(ny - other_ship_y) <= 1:
                    return False
    return True


def create_ship(length):
    """Создание корабля случайным образом"""
    while True:
        x = randint(0, GRID_SIZE - 1)
        y = randint(0, GRID_SIZE - 1)
        direction = randint(0, 1)
        ship = []

        if check_ship(x, y, length, direction):
            for i in range(length):
                nx = x + (i if direction == 0 else 0)
                ny = y + (i if direction == 1 else 0)
                ship.append((nx, ny))
            ships['alive'].append(ship)
            ships['original'].append(ship.copy())
            return


def dead_ship(ship):
    """Отметка потопленного корабля"""
    for x, y in ship:
        spot[y][x] = 'D'


# Размещение кораблей: 1×4, 2×3, 3×2, 4×1
ship_types = [(4, 1), (3, 2), (2, 3), (1, 4)]
for length, count in ship_types:
    for _ in range(count):
        create_ship(length)

game = True
ships_dead = 0
message = "Стреляй! Кликни по полю."


def draw_grid():
    """Отрисовка сетки поля"""
    for i in range(GRID_SIZE + 1):
        # Вертикальные линии
        pygame.draw.line(screen, BLACK,
                         (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, MARGIN + GRID_SIZE * CELL_SIZE))
        # Горизонтальные линии
        pygame.draw.line(screen, BLACK,
                         (MARGIN, MARGIN + i * CELL_SIZE),
                         (MARGIN + GRID_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE))


def draw_board():
    """Отрисовка состояния поля (попадания, промахи, потопленные)"""
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if spot[y][x] == 'X':
                # Попадание - красный крест
                pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 3)
                pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 3)
            elif spot[y][x] == '*':
                # Промах - белый круг
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 4)
            elif spot[y][x] == 'D':
                # Потопленный корабль: красный крестик на чёрном фоне.
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 3)
                pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 3)


def get_cell_from_pos(pos):
    """Преобразование координат мыши в координаты клетки поля"""
    mx, my = pos
    if MARGIN <= mx < MARGIN + GRID_SIZE * CELL_SIZE and MARGIN <= my < MARGIN + GRID_SIZE * CELL_SIZE:
        x = (mx - MARGIN) // CELL_SIZE
        y = (my - MARGIN) // CELL_SIZE
        return x, y
    return None


# Основной цикл игры
while game:
    screen.fill(BLUE)
    draw_grid()
    draw_board()

    # Отрисовка сообщения
    text_surf = font.render(message, True, WHITE)
    screen.blit(text_surf, (MARGIN, 10))

    # Отрисовка счётчика
    dead_text = font.render(f"Потоплено: {ships_dead}/{len(ships['alive'])}", True, WHITE)
    screen.blit(dead_text, (MARGIN, HEIGHT - 40))
    pygame.display.flip()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = get_cell_from_pos(event.pos)
            if cell:
                x, y = cell
                if spot[y][x] in 'XD*':
                    message = "Вы уже стреляли сюда!"
                    continue

                hit = False
                for i in range(len(ships['alive'])):
                    if (x, y) in ships['alive'][i]:
                        ships['alive'][i].remove((x, y))
                        hit = True
                        if len(ships['alive'][i]) == 0:
                            message = "Потоплен!"
                            dead_ship(ships['original'][i])
                            ships_dead += 1
                        else:
                            message = "Попадание!"
                            spot[y][x] = 'X'
                        break

                if not hit:
                    message = "Промах!"
                    spot[y][x] = '*'

                if ships_dead == len(ships['original']):
                    message = "Игра окончена! Все корабли потоплены!"
                    # Можно добавить задержку или экран победы

    clock.tick(FPS)

pygame.quit()
