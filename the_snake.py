"""Данный модуль представляет собой механику игры змейка."""
from random import choice, randint
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
NUMBER_GRID_X = GRID_WIDTH - 1
NUMBER_GRID_Y = GRID_HEIGHT - 1
ALL_GRIDS = NUMBER_GRID_X * NUMBER_GRID_Y
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Родительский класс, представляющий игровой объект,
    и от которого идет наследие.
    Атрибуты:
    body_color (tuple or None): Цвет объекта,
    который будет переопределен в другом классе.
    position (tuple): Позиция яблока на экране.
    Изначально только одна позиция - CENTER.
    """

    def __init__(self):
        """Инициализатор, который создает позицию и цвет."""
        self.position = CENTER  # Начальная позиция объекта - центр.
        self.positions = []
        self.body_color = None  # Цвет переопределям уже в других методах.
        self.last = None

    def draw(self):
        """Метод отрисовки, который в будущем будет переопределяться."""

    def draw_rect(self, position, color=None):
        """
        Создаёт объект прямоугольника (Rect)
        и отрисовывает его на экране.
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color or self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, width=1)

        return rect

    def clear_rect(self, position):
        """
        Данный метод затирает последний объект,
        чтобы змейка двигалась
        """
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.
    Атрибуты:
        body_color (tuple): Цвет тела яблока.
        Изначально задается значением APPLE_COLOR.
        position (tuple): Позиция яблока на экране.
        В ней мы вызываем функцию для случайного места генерации яблока.
    """

    def __init__(self):
        """Наследуем все от родительского класса и переопределяем."""
        super().__init__()
        self.body_color = APPLE_COLOR
        # Ставим яблоко в рандомную позицию.
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Функция, которая возвращает рандомную
        позицию яблока в координатах.
        """
        # Случайным образом выбираем координаты х и у для яблока.
        all_grids = set()
        # Количество клеток по оси X и по оси Y.
        for i in range(ALL_GRIDS):
            position_x = randint(0, NUMBER_GRID_X) * GRID_SIZE
            position_y = randint(0, NUMBER_GRID_Y) * GRID_SIZE
            all_grids.add((position_x, position_y))

        free_grids = all_grids - set(self.positions)
        choice_position = choice(list(free_grids))
        return choice_position

    def draw(self):
        """Данный метод отрисовывает яблоко через библиотеку pygame."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """
    Класс, представляющий змейку в игре.
    Атрибуты:
        length (int): Длина змейки в кубиках. По умолчанию равна 1.
        positions (list): Список позиций змейки на экране.
        Изначально - центр экрана.
        direction (str): Текущее направление движения змейки.
        По умолчанию 'RIGHT'.
        next_direction (str): Следующее направление движения змейки,
        которое будет применено
        после текущего обновления. По умолчанию None.
        body_color (tuple): Цвет тела змейки.
        Изначально задается значением SNAKE_COLOR.
        last (tuple or None): Позиция последнего элемента змейки для отрисовки.
        Изначально None.
    """

    def __init__(self):
        """Инициализация начальных значений атрибутов змейки."""
        super().__init__()
        self.length = 1  # По умолчанию змейка равна одному кубику.
        self.positions = [CENTER]  # Изначальная позиция змейки - центр.
        self.direction = RIGHT  # Изначальное направление змейки - вправо.
        self.next_direction = None
        # По умолчанию другое направление змейки None.
        self.body_color = SNAKE_COLOR
        self.last = None  # По умолчанию последний элемент змейки None.

    def update_direction(self):
        """Обновление направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            # Если next_direction не равен None, то переопределяем.
        self.next_direction = None

    def move(self):
        """
        Данный метод занимается движением нашей змейки,
        и проверками на направление.
        """
        self.update_direction()
        # Получаем актуальные координаты нашей головы.
        head_x, head_y = self.get_head_position()

        direction_x, direction_y = self.direction

        new_position = ((head_x + GRID_SIZE * direction_x) % SCREEN_WIDTH,
                        (head_y + GRID_SIZE * direction_y) % SCREEN_WIDTH)
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.remove_last_segment()

        self.next_direction = None

    def remove_last_segment(self):
        """Удаляет последний элемент, имитируя движение"""
        self.last = self.positions.pop()

    def grow(self):
        """
        Данный метод увеличивает нашу змейку с помощью
        добавления новых координат в наш список.
        """
        self.length += 1
        self.positions.append(self.positions[-1])

    def draw(self):
        """Данный метод отрисовывает змейку на графике."""
        self.draw_rect(self.positions[0])  # Отрисовка головы змейки

        # Затирание последнего сегмента
        if self.last:
            self.clear_rect(self.last)

    def get_head_position(self):
        """
        С помощью данного метода мы получаем координаты
        нашей головы змейки в данный момент.
        """
        return self.positions[0]

    def reset(self):
        """Данный метод нужен для сброса змейки в изначальное положение."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice(DIRECTIONS)


def handle_keys(game_object):
    """Функция отвечающая за реагирование на пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Главная функция, в которой прописано запуск всей игры змейка.
    Тут идет инициализация pygame, а также вечный цикл,
    в котором вызываются методы наших классов.
    """
    pg.init()  # Инициализация PyGame:
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if apple.position == snake.get_head_position():
            snake.grow()
            apple.position = apple.randomize_position()

        head = snake.get_head_position()
        body = snake.positions[1:]
        len_of_body = len(snake.positions)
        if len_of_body > 2 and head in body:
            # Голова змейки столкнулась с её телом.
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        snake.move()
        pg.display.update()


if __name__ == '__main__':
    main()
