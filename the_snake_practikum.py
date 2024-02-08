from random import choice, randint
from typing import Any, Optional, Union
import pygame
import sys

# Initialisation of PyGame.
pygame.init()

# Constants for dimensions.
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Main colors for game
COLOR_RED: tuple[int, int, int] = (255, 0, 0)
COLOR_BLACK: tuple[int, int, int] = (0, 0, 0)
COLOR_GREEN: tuple[int, int, int] = (0, 255, 0)
COLOR_LIGHT_BLUE: tuple[int, int, int] = (93, 216, 228)
COLOR_BROWN: tuple[int, int, int] = (107, 78, 58)
COLOR_BLUE: tuple[int, int, int] = (66, 143, 220)

BOARD_BACKGROUND_COLOR: tuple = COLOR_BLACK

# Snake's speed
SPEED: int = 5

# Moving directions
UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)
MOVE_LIST: list = [UP, DOWN, LEFT, RIGHT]

# Game's settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Parent class for game's objects."""

    body_color: Optional[tuple] = None

    def __init__(self) -> None:
        self.position: Union[list, tuple] = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self) -> None:
        """Abstract method, which will be changed in next classes"""
        raise NotImplementedError(
            'Check "draw" method for GameObjects'
        )


class Portal(GameObject):
    """Portals on the game-field."""

    posp: list = []

    def __init__(self) -> None:
        super().__init__()
        self.body_color = COLOR_BLUE
        self.positions = self.pos_portal()

    def pos_portal(self) -> list:
        """Portal coordinates."""
        self.posp.append((80, 40))
        self.posp.append((540, 420))
        return self.posp

    def draw(self, surface):
        """Method to draw portals on the surface."""
        for position in self.positions:
            rect_portal = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect_portal)


class Wall(GameObject):
    """Borders."""

    post: list = []

    def __init__(self) -> None:
        super().__init__()
        self.body_color = COLOR_BROWN
        self.positions = self.pos_wall()

    def pos_wall(self) -> list:
        """Borders coordinates"""
        for i in range(24):
            self.post.append((0, i * GRID_SIZE))
            self.post.append((620, i * GRID_SIZE))
        self.post.remove((0, 60))
        self.post.remove((0, 80))
        self.post.remove((620, 60))
        self.post.remove((620, 80))
        self.post.remove((0, 380))
        self.post.remove((0, 400))
        self.post.remove((620, 380))
        self.post.remove((620, 400))

        for i in range(32):
            self.post.append((i * GRID_SIZE, 0))
            self.post.append((i * GRID_SIZE, 460))

        return self.post

    def draw(self, surface):
        """Method to draw borders on the surface."""
        for position in self.positions:
            rect_wall = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect_wall)


class Apple(GameObject):
    """This class describes apples. The snake must eat apples to grow."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = COLOR_RED
        self.randomize_position()

    def randomize_position(self) -> None:
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

    length: int = 1
    positions: Union[list[tuple[int, int]], Any] = None
    direction: Union[tuple, Any] = None
    next_direction: Optional[tuple[tuple, tuple]] = None
    last: Union[tuple, Any] = None

    def __init__(self) -> None:
        super().__init__()
        self.body_color = COLOR_GREEN
        self.direction = choice(MOVE_LIST)
        self.positions = [self.position]

    def update_direction(self) -> None:
        """This Method updates move direction after hitting the button."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
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

    def get_head_position(self) -> tuple[int, int]:
        """The method considering coordinates of the head of a snake."""
        return self.positions[0][0], self.positions[0][1]

    def reset(self, surface) -> None:
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


def handle_keys(game_object) -> None:
    """Function of processing of actions of the user.

    This method excludes the movement of a snake in itself.
    """
    key_builds: dict = {
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_UP, LEFT): UP,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_LEFT, DOWN): LEFT
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key, game_object.direction) in key_builds:
                game_object.next_direction = key_builds[
                    (event.key, game_object.direction)
                ]
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def new_apple(snake, wall, portal) -> Apple:
    """Function to create new apples."""
    while True:
        apple = Apple()
        if (apple.position not in snake.positions) and (
            apple.position not in wall.positions) and (
                apple.position not in portal.positions):
            break
    return apple


def infinite_way(snake, portal) -> Snake:
    """This function allows travel throw display's borders."""
    head_pos_x: int = snake.get_head_position()[0]
    head_pos_y: int = snake.get_head_position()[1]
    portal_1_pos_x: int = portal.positions[0][0]
    portal_1_pos_y: int = portal.positions[0][1]
    portal_2_pos_x: int = portal.positions[1][0]
    portal_2_pos_y: int = portal.positions[1][1]
    if head_pos_x == portal_1_pos_x and head_pos_y == portal_1_pos_y:
        head_pos_x = portal_2_pos_x
        head_pos_y = portal_2_pos_y
    elif head_pos_x == portal_2_pos_x and head_pos_y == portal_2_pos_y:
        head_pos_x = portal_1_pos_x
        head_pos_y = portal_1_pos_y

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
    wall = Wall()
    portal = Portal()
    apple = new_apple(snake, wall, portal)
    speed = SPEED
    while True:
        clock.tick(speed)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake = infinite_way(snake, portal)
        apple.draw(screen)
        snake.draw(screen)
        wall.draw(screen)
        portal.draw(screen)
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            snake.last = None
            apple = new_apple(snake, wall, portal)
            speed += 0.5

        if snake.positions[0] in snake.positions[1:]:
            snake.reset(screen)
            speed = SPEED

        if snake.positions[0] in wall.positions:
            snake.reset(screen)
            speed = SPEED

        pygame.display.update()


if __name__ == '__main__':

    main()
