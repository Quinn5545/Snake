import pygame, sys, random
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)


GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
RED = (255, 0, 0)

OFFSET = 75

cell_size = 30
number_of_cells = 25


class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(
            OFFSET + self.position.x * cell_size,
            OFFSET + self.position.y * cell_size,
            cell_size,
            cell_size,
        )
        pygame.draw.rect(screen, RED, food_rect)
        # screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()

        while position in snake_body:
            position = self.generate_random_cell()

        return position


class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.eat_sound = pygame.mixer.Sound("sounds/eat.mp3")
        self.fail_sound = pygame.mixer.Sound("sounds/fail.mp3")

    def draw(self):
        for segment in self.body:
            segment_rect = (
                OFFSET + segment.x * cell_size,
                OFFSET + segment.y * cell_size,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        # self.high_score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_body()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.snake.eat_sound.play()
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        # if self.score > self.high_score:
        #     self.high_score = self.score
        self.snake.fail_sound.play()
        self.score = 0
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"

    def check_collision_with_body(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()


screen = pygame.display.set_mode(
    (2 * OFFSET + cell_size * number_of_cells, 2 * OFFSET + cell_size * number_of_cells)
)

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()
# food_surface = pygame.image.load("graphics/apple.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 150)

while True:
    for event in pygame.event.get():

        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)

    # Drawing
    screen.fill(GREEN)
    pygame.draw.rect(
        screen,
        DARK_GREEN,
        (
            OFFSET - 5,
            OFFSET - 5,
            cell_size * number_of_cells + 10,
            cell_size * number_of_cells + 10,
        ),
        5,
    )
    game.draw()
    title_surface = title_font.render("Quinn's Snake Game", True, DARK_GREEN)
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    # high_score_surface = score_font.render(str(game.high_score), True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET - 5, 20))
    screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 10))
    # screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 30))

    pygame.display.update()
    clock.tick(60)
