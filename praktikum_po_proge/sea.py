from random import *

spot = [['.'] * 10 for _ in range(10)]
ships = {'alive': [], 'original': []}


def check_ship(x, y, length, direction): # проверка на наличие корабля рядом
    for i in range(length):
        nx = x + (i if direction == 0 else 0)
        ny = y + (i if direction == 1 else 0)
        if nx < 0 or nx > 9 or ny < 0 or ny > 9: return False

        for other_ship in ships['original']:
            for other_ship_x, other_ship_y in other_ship:
                if abs(nx - other_ship_x) <= 1 and abs(ny - other_ship_y) <= 1:
                    return False

    return True


def create_ship(length): #создание корабля, создание поля кораблей для проверки кораблей рядом
    while True:
        x = randint(0, 9)
        y = 10 - randint(1, 10)
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


def show(spt): # вывод корабля
    for row in spt:
        print(*row)


def dead_ship(ship):    # вызывается в строке 92, для того чтобы в выводе корабль был отображен как потопленный весь, а не отдельная точка
    for x, y in ship:
        spot[y][x] = '☠'

ship_types = [(4, 1), (3, 2), (2, 3), (1, 4)]

for length, count in ship_types: # вызов функции для создания кораблей
    for i in range(count):
        create_ship(length)


game = True
ships_dead = 0 # счетчик потопленных кораблей
print(ships)


while game:
    show(spot)
    x = int(input("Введите столбец: ")) - 1
    y = 10 - int(input('Введите строку: '))
    if x < 0 or x > 9 or y < 0 or y > 9:
        print('Координаты от 1 до 10, попробуйте еще раз')
        continue
    if spot[y][x] in 'X☠*':
        print('Вы уже стреляли сюда, Выберите другую клетку')
        continue
    for i in range(len(ships['alive'])):
        if (x, y) in ships['alive'][i]:
            ships['alive'][i].remove((x, y))
            if len(ships['alive'][i]) == 0:
                print('Потоплен')
                dead_ship(ships['original'][i])
                ships_dead += 1
            else:
                print('Попадание')
                spot[y][x] = 'X'

            break
    else:
        print('Промах')
        spot[y][x] = '*'
    if ships_dead == len(ships['alive']):
        game = False
        show(spot)
        print('Игра окончена')
