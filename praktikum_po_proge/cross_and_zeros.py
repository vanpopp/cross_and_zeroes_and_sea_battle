spot = [['.'] * 3 for _ in range(3)]
check_field = 0


def show(field):
    for row in field:
        print(*row)


def check_win(symbol):
    for i in range(3):
        if all(spot[i][j] == symbol for j in range(3)):
            return True

    for j in range(3):
        if all(spot[i][j] == symbol for i in range(3)):
            return True

    if all(spot[i][i] == symbol for i in range(3)):
        return True

    if all(spot[i][2 - i] == symbol for i in range(3)):
        return True

    return False


show(spot)

while True:
    x = int(input('Введите столбец: ')) - 1
    y = int(input('Введите строку: ')) - 1

    if not (0 <= x < 3 and 0 <= y < 3):
        print('Выход за пределы поля. Сделайте другой ход')
        continue

    if spot[y][x] != '.':
        print('Клетка занята, выберите другую')
        continue

    symbol = 'X' if check_field % 2 == 0 else '0'
    spot[y][x] = symbol
    check_field += 1

    if check_win(symbol):
        show(spot)
        print(f'Победа {symbol}')
        break

    if check_field == 9:
        show(spot)
        print('Ничья. Конец игры')
        break

    show(spot)