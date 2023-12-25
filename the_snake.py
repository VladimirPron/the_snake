from random import choice, randint
import pygame

# Initialisation of PyGame.
pygame.init()

# Constants for dimensions.
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Main colors for game
COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_LIGHT_BLUE = (93, 216, 228)
# COLOR_RAND = (randint(0, 255), randint(0, 255), randint(0, 255))

BOARD_BACKGROUND_COLOR = COLOR_BLACK

# Snake's speed
SPEED: int = 2

# Moving directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
MOVE_LIST = (UP, DOWN, LEFT, RIGHT)

# Game's settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Parent class for game's objects."""

    body_color = None

    def __init__(self) -> None:
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self):
        """Abstract method, which will be changed in next classes"""
        raise NotImplementedError(
            'Check "draw" method for GameObjects'
        )


class Apple(GameObject):
    """This class describes apples. The snake must eat apples to grow."""

    def __init__(self):
        super().__init__()
        self.body_color = COLOR_RED
        self.randomize_position()

    def randomize_position(self):
        """Method to generate Apple's position on the surface."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Method to draw apples on the surface."""
        rectangle = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rectangle)
        pygame.draw.rect(surface, COLOR_LIGHT_BLUE, rectangle, 1)


class Snake(GameObject):
    """Class Snake describes snake."""

    length = 1
    positions = None
    direction = None
    next_direction = None
    last = None

    def __init__(self):
        super().__init__()
        self.body_color = COLOR_GREEN
        self.direction = choice(MOVE_LIST)
        self.positions = [self.position]

    def update_direction(self):
        """This Method updates move direction after hitting the button."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Method to move a snake."""
        new_position = (
            self.positions[0][0] + self.direction[0] * GRID_SIZE,
            self.positions[0][1] + self.direction[1] * GRID_SIZE
        )
        list.insert(self.positions, 0, new_position)
        self.last = self.positions[-1]
        self.positions = self.positions[: -1]

    def draw(self, surface):
        """Method to draw a snake."""
        for position in self.positions[: -1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, COLOR_LIGHT_BLUE, rect, 1)

        # Drawing of snake's head.
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, COLOR_LIGHT_BLUE, head_rect, 1)

        # Erasing of the last segment.
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """The method considering coordinates of the head of a snake."""
        return self.positions[0][0], self.positions[0][1]

    def reset(self, surface):
        """Method to reset game to default."""
        for each in self.positions:
            rect = pygame.Rect(
                (each[0], each[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        self.positions = [(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )]
        self.direction = choice(MOVE_LIST)
        self.last = None


def handle_keys(game_object):
    """Function of processing of actions of the user.

    This method excludes the movement of a snake in itself.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def new_apple(snake):
    """Function to create new apples."""
    while True:
        apple = Apple()
        if apple.position not in snake.position:
            break
    return apple


def infinite_way(snake):
    """This function allows travel throw display's borders."""
    head_pos_x, head_pos_y = snake.get_head_position()
    if head_pos_x >= SCREEN_WIDTH:
        head_pos_x = 0
    elif head_pos_x < 0:
        head_pos_x = SCREEN_WIDTH - GRID_SIZE

    if head_pos_y >= SCREEN_HEIGHT:
        head_pos_y = 0
    elif head_pos_y < 0:
        head_pos_y = SCREEN_HEIGHT - GRID_SIZE

    snake.positions[0] = (head_pos_x, head_pos_y)
    return snake


def main():
    """Main function of game."""
    snake = Snake()
    apple = new_apple(snake)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake = infinite_way(snake)
        apple.draw(screen)
        snake.draw(screen)
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            snake.last = None
            apple = new_apple(snake)

        if snake.positions[0] in snake.positions[1:]:
            snake.reset(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
