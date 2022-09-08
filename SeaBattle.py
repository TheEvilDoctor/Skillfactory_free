from random import randint

# Exceptions:


class BoardException:
    pass


class BoardOutException(BoardException):
    def __str__(self):
        raise f"Упс! Перелет за край света(((\nВ следующий раз постарайтесь попасть по игровой доске!"


class DotIsUsed(BoardException):
    def __str__(self):
        raise f"На этой клетке уже видны следы бомбардировки!\nПохоже, Вы уже атаковали эту зону..."


class TheShipAtWrongPlace(BoardException, Exception):
    pass


# General:
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.x, self.y}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Dot(self.x + other.x, self.y + other.y)


class Ship:
    ship_dots = []

    def __init__(self, dot_beg, size, direction):
        self.dot: Dot = dot_beg
        self.size: int = size
        self.direction = direction
        self.hp = size

    @property
    def dots(self):
        # вертикальный корабль
        if self.direction == 1:
            for n in range(self.size):
                next_dot = Dot(self.dot.x, self.dot.y + n)
                self.ship_dots.append(next_dot)
        # горизонтальный корабль
        if self.direction == 0:
            for n in range(self.size):
                next_dot = Dot(self.dot.x + n, self.dot.y)
                self.ship_dots.append(next_dot)
        return self.ship_dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.blank = [['0'] * size for _ in range(size)]
        self.done_dots = []
        self.ships = []
        self.ships_count = 7

    def __str__(self):
        the_board = "  1 2 3 4 5 6"
        for x, y in enumerate(self.blank):
            the_board += f"\n{x + 1} " + "|".join(y)
        if self.hid:
            the_board.replace("■", "0")
        return the_board

    def add_ship(self, ship):
        for dot in ship.dots:
            if not self.in_board(dot) or dot in self.done_dots:
                raise TheShipAtWrongPlace()

        self.contour(ship)

        for dot in ship.dots:
            self.blank[dot.x][dot.y] = "■"
            self.done_dots.append(dot)
        self.ships.append(ship)

    def contour(self, ship, verb=False):
        contour = (Dot(-1, -1), Dot(0, -1), Dot(1, -1), Dot(-1, 0), Dot(1, 0), Dot(-1, 1), Dot(0, 1), Dot(1, 1))
        for dot in ship.dots:
            for c_dot in contour:
                c_dot = c_dot + dot
                if self.in_board(c_dot) and not (c_dot in self.done_dots):
                    if verb:
                        self.blank[c_dot.x][c_dot.y] = "*"
                    self.done_dots.append(c_dot)

    def in_board(self, dot):
        return (0 <= dot.x < self.size) and (0 <= dot.y < self.size)

    def shot(self, dot):
        if dot in self.done_dots:
            raise DotIsUsed

        if not self.in_board(dot):
            raise BoardOutException

        self.done_dots.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.hp -= 1
                if ship.hp == 0:
                    self.contour(ship, verb=True)
                    self.ships_count -= 1
                    print(f'{ship.size}-х палубный корабль уничтожен!')

                    return True
                else:
                    print('Вражеский корабль поврежден!')
                    return True
            else:
                self.blank[dot.x][dot.y] = '*'
                print('Увы, вы промахнулись...')
                return False

    def new_start(self):
        self.done_dots = []


# Внешняя логика


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_bord = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                dot = self.ask()
                the_shot = self.enemy_bord.shot(dot)
                return the_shot
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f'Ваш противник выстрелил в точку {dot.x+1} - {dot.y+1}')
        return dot


class User(Player):
    def ask(self):
        while True:
            print('Ваш ход! Прицельтесь хорошенько!')
            x = input('Введите координаты точки по горизонтали: ')
            y = input('Введите координаты точки по вертикали: ')

            if not(x.isdigit()) or not(y.isdigit()):
                print('Координаты должны быть числами!')

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:
    def __init__(self, desk_size):
        self.size = desk_size
        self.board = Board(size=self.size)
        user_desk = self.gen_board()
        ai_desk = self.gen_board()
        self.user = User(user_desk, ai_desk)
        self.ai = AI(ai_desk, user_desk)
        user_desk.hid = False
        ai_desk.hid = True

    def greet(self):
        info = f"Капитан, мы могли бы предложить вам " \
               f"новейшее оружие большого радиуса действия..." \
               f"Но, зная о Ваши великих подвигах и завоеваниях" \
               f"просим Вас продемонстрировать доблесть и" \
               f"сокрушить вражеский флот с помощью лишь одной пушки!" \
               f"" \
               f"Пушка простенькая. " \
               f"Чтобы сделать выстрел необходимо лишь ввести две координаты:" \
               f"ШИРОТА и ДОЛГОТА - X и Y" \
               f"" \
               f"Место столкновения армад - поле {self.size} на {self.size} клеток" \
               f""

        print(f'Добро пожаловать в зону морских баталий, капитан!\n')
        ask_info = input(f'Желаете ознакомиться с местной навигацией?\n').lower().replace(' ', '')
        if ask_info == 'да' or ask_info == 'yes':
            print(info)
        print('Начнем же битву!\n')

    def gen_board(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        tries = 0
        for ship_size in ships:
            while True:
                tries += 1
                if tries > 5000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), ship_size, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except TheShipAtWrongPlace:
                    pass
        board.new_start()
        return board
    
    def new_board(self):
        self.board = None
        while self.board is None:
            self.board = self.gen_board()
        return self.board
    
    def structure(self):
        shoot = 0
        while True:
            print('Вот Ваш флот, капитан!')
            print(self.user.board)
            print(f'\nВражеский флот:')
            print(self.ai.board)
            print("_" * 20)
            if shoot % 2 == 0:
                print('Ваш ход, капитан!')
                success = self.user.move()
            else:
                print('Ход противника...')
                success = self.ai.move()
            shoot += 1
            if success:
                shoot -= 1
            if self.ai.board.ships_count == 0:
                print(f'Наше почтение, Капитан!'
                      f'Еще одна великолепная победа у Вас в кармане!')
                break
            if self.user.board.ships_count == 0:
                print(f'Сожалеем, Капитан, но, все ваши корабли потоплены.'
                      f'Это поражение...')
                break

    def start(self):
        self.greet()
        self.structure()

# Запуск


game = Game(6)
game.start()
