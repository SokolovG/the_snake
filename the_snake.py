"""Данный модуль представляет собой механику игры змейка."""
from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
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
        self.body_color = None  # Цвет переопределям уже в других методах.

    def draw(self):
        """Метод отрисовки, который в будущем будет переопределяться."""
        pass

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
        self.position = self.randomize_position()
        # Ставим яблоко в рандомную позицию.

    def randomize_position(self):
        """
        Функция, которая возвращает рандомную
        позицию яблока в координатах.
        """
        # Случайным образом выбираем координаты х и у для яблока.
        position_x = randint(0, (GRID_WIDTH - 1)) * GRID_SIZE
        position_y = randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        return (position_x, position_y)

    def draw(self):
        """Данный метод отрисовывает яблоко через библиотеку pygame."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

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
        head = self.get_head_position()
        # Получаем актуальные координаты нашей головы.
        x, y = head
        # Записываем их в переменные как координаты Х и У

        self.update_direction()
        # Вызываем обновления направления перед его проверкой.

        def direction_x(name):
            if name == 'RIGHT':
                new_position_x = (x + GRID_SIZE) % SCREEN_WIDTH
            elif name == 'LEFT':
                new_position_x = (x - GRID_SIZE) % SCREEN_WIDTH

            self.position = (new_position_x, y)
            self.positions.insert(0, self.position)

        def direction_y(name):

            if name == 'DOWN':
                new_position_y = (y + GRID_SIZE) % SCREEN_HEIGHT
            elif name == 'UP':
                new_position_y = (y - GRID_SIZE) % SCREEN_HEIGHT

            self.position = (x, new_position_y)
            self.positions.insert(0, self.position)

        if self.direction == RIGHT:
            direction_x('RIGHT')

        elif self.direction == LEFT:
            direction_x('LEFT')

        elif self.direction == DOWN:
            direction_y('DOWN')

        elif self.direction == UP:
            direction_y('UP')

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)

    def grow(self):
        """
        Данный метод увеличивает нашу змейку с помощью
        добавления новых координат в наш список.
        """
        self.length += 1
        self.positions.append(self.positions[-1])

    def draw(self):
        """Данный метод отрисовывает змейку на графике."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        С помощью данного метода мы получаем координаты
        нашей головы змейки в данный момент.
        """
        result = self.positions[0]
        return result

    def reset(self):
        """Данный метод нужен для сброса змейки в изначальное положение."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice(DIRECTIONS)

def handle_keys(game_object):
    """Функция отвечающая за реагирование на пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

def main():
    """
    Главная функция, в которой прописано запуск всей игры змейка.
    Тут идет инициализация pygame, а также вечный цикл,
    в котором вызываются методы наших классов.
    """
    pygame.init()  # Инициализация PyGame:
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.grow()
            apple.position = apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()


if __name__ == '__main__':
    main()
