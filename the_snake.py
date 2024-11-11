from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 15
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Cловарь TURNS
TURNS = {
    (pygame.K_UP, DOWN): UP,
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, UP): DOWN,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, RIGHT): LEFT,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, LEFT): RIGHT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Начальная позиция игры и змеи
POSITION_Game = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
POSITION_Snake = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
POSITION_Initial = (SCREEN_WIDTH // 2 // GRID_SIZE, SCREEN_HEIGHT
                    // 2 // GRID_SIZE)


class GameObject:
    """Базовый класс игры."""

    def __init__(self):
        self.position = POSITION_Game
        self.body_color = None

    def draw_cell(self, screen, position, color):
        """Рисует одну ячейку на экране."""
        rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self, screen):
        """Реализует отрисовку объекта на экране."""


class Apple(GameObject):
    """Класс описывающий яблоко."""

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None
        if occupied_positions is None:
            occupied_positions = []
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Отвечает за установку случайной позиции яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1)
            )
            if self.position not in occupied_positions:
                break

    def draw(self, screen):
        """Предназначен для отображения яблока на игровом экране."""
        self.draw_cell(screen, self.position, self.body_color)


class Snake(GameObject):
    """Класс описывающий объект змейка."""

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        """Используется для сброса состояния змейки."""
        initial_position = POSITION_Initial
        self.position = initial_position
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [initial_position]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.growing = False  # Без этого арбибута код выдает ошибку
        self.last = None

    def get_head_position(self):
        """Предназначена для получения текущей позиции головы змейки."""
        return self.positions[0]

    def update_direction(self, event):
        """Обновляет направление движения змейки на основе нажатой клавиши."""
        if (event.key, self.direction) in TURNS:
            self.next_direction = TURNS[(event.key, self.direction)]

    def move(self):
        """Отвечает за движение змейки."""
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        return new_head

    def grow(self):  # Без этого метода код не работает
        """Позволяет змейке увеличиваться в длину."""
        self.growing = True

    def draw(self, screen):
        """Отвечает за визуализацию змейки на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1]
                               * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0][0] * GRID_SIZE,
                                self.positions[0][1] * GRID_SIZE, GRID_SIZE,
                                GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last[0] * GRID_SIZE, self.last[1]
                                    * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Позволяя управлять змейкой."""
    TURN_KEYS = set(event_key for event_key, _ in TURNS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN and event.key in TURN_KEYS:
            new_direction = TURNS.get((event.key, game_object.direction),
                                      game_object.direction)
            if new_direction != game_object.direction:
                game_object.next_direction = new_direction


def main():
    """Запускает игровой процесс."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    occupied_positions = set(snake.positions)
    apple = Apple(occupied_positions)  # Передаем занятые позиции

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обрабатываем ввод пользователя:
        handle_keys(snake)  # Передаем объект змейки в функцию

        # Двигаем змейку:
        new_head = snake.move()

        # Проверка на столкновение с собой в главной функции
        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()
        else:
            if not snake.growing:
                snake.last = snake.positions.pop()
            snake.positions.insert(0, new_head)
            snake.growing = False

        # Проверяем, съели ли яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(occupied_positions)

        # Отрисовываем объекты:
        apple.draw(screen)
        snake.draw(screen)

        # Обновляем экран:
        pygame.display.update()


if __name__ == '__main__':
    main()
