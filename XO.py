there_is_the_winner = False
ch_turn = 1


def new_area():
    global game_area
    game_area = (['*', '1', '2', '3'],
                 ['1', ' ', ' ', ' '],
                 ['2', ' ', ' ', ' '],
                 ['3', ' ', ' ', ' '])


def info():
    print(f'''В вашем распоряжении игровое поле 3 х 3 клетки''')
    show_the_area()
    print(f'''Чтобы выиграть, вам необходимо заполнить выбранным вами значком (Х или 0) линию из 3 клеток.
Линия может быть вертикальной, горизонтальной или диагональной.

Для обозначения хода используется система координат: СТРОКА - СТОЛБЕЦ.
Пример хода: 1, 1

Удачи!''')


def show_the_area():
    print(f'''{game_area[0]}\n{game_area[1]}\n{game_area[2]}\n{game_area[3]}''')


def your_turn():
    if ch_turn % 2 == 1:
        print('Ходят крестики!')
    else:
        print('Ходят нолики!')
    show_the_area()
    while True:
        coords = list(map(int, input('Введите координаты клетки (№ строки, № столбца)\n').replace(' ', '').split(',')))
        y, x = coords
        if y not in range(1, 4) or x not in range(1, 4) or game_area[y][x] != ' ':
            print('Некорректные координаты. Попробуйте еще раз')
            continue
        if ch_turn % 2 == 1:
            game_area[y][x] = 'X'
            break
        elif ch_turn % 2 == 0:
            game_area[y][x] = 'O'
            break


def the_victory():
    xs = ['X', 'X', 'X']
    os = ['O', 'O', 'O']
    global there_is_the_winner
    win = (((1, 1), (1, 2), (1, 3)), ((2, 1), (2, 2), (2, 3)), ((3, 1), (3, 2), (3, 3)),
           ((1, 1), (2, 1), (3, 1)), ((1, 2), (2, 2), (3, 2)), ((1, 3), (2, 3), (3, 3)),
           ((1, 1), (2, 2), (3, 3)), ((3, 1), (2, 2), (1, 3)))
    for line in win:
        check_line = []
        for point in line:
            check_line.append(game_area[point[0]][point[1]])
        if check_line == xs:
            print('Победили КРЕСТИКИ!')
            there_is_the_winner = True
        elif check_line == os:
            print('Победили НОЛИКИ!')
            there_is_the_winner = True


print(f'''                Привет, игроки!\n
Мы рады приветствовать вас в игре "КРЕСТИКИ-НОЛИКИ!"\n''')

need_help = input('Желаете ознакомиться с правилами?(да/нет)\n').lower().replace(' ', '')

if need_help == 'да':
    info()

print('\nНачнем игру!')
new_area()
while True:
    your_turn()
    ch_turn += 1
    the_victory()
    if ch_turn == 10:
        print('Ничья...'
              'Сыграем снова!')
        new_area()
    if there_is_the_winner:
        new_game = input(f'Хотите начать новую игру?(да/нет)\n').lower()
        if new_game == 'да':
            new_area()

