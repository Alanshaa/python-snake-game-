import pygame
import random
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
GRID_SIZE = 25
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE


GRASS_1 = (170, 215, 81)
GRASS_2 = (162, 209, 73)
SNAKE_HEAD_COLOR = (43, 110, 36)
SNAKE_BODY_COLOR = (60, 150, 50)
APPLE_COLOR = (230, 0, 0)
APPLE_LEAF = (0, 150, 0)
SHADOW_COLOR = (0, 0, 0, 60) # Semi-transparent black for depth
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        x, y = self.position
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
        
        # Shadow
        pygame.draw.circle(surface, (120, 160, 50), (center[0] + 3, center[1] + 3), GRID_SIZE // 2)
        # Apple Body
        pygame.draw.circle(surface, APPLE_COLOR, center, GRID_SIZE // 2 - 2)
        # Apple Leaf
        pygame.draw.ellipse(surface, APPLE_LEAF, (x + GRID_SIZE//2, y + 2, 8, 12))

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = RIGHT
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point

    def move(self, food):
        cur = self.get_head_position()
        x, y = self.direction
        
        # Wrap around the screen
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), ((cur[1] + (y * GRID_SIZE)) % HEIGHT))
        
        # Check collision with self
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return
            
        self.positions.insert(0, new)
        
        # Check collision with food
        if new == food.position:
            self.length += 1
            self.score += 10
            food.randomize_position(self.positions)
        else:
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw_eyes(self, surface, x, y):
        # Draw eyes based on direction
        radius = 4
        pupil = 2
        offset_x1, offset_y1 = 0, 0
        offset_x2, offset_y2 = 0, 0
        
        center_x = x + GRID_SIZE // 2
        center_y = y + GRID_SIZE // 2

        if self.direction == UP:
            offset_x1, offset_y1 = -5, -6
            offset_x2, offset_y2 = 5, -6
        elif self.direction == DOWN:
            offset_x1, offset_y1 = -5, 6
            offset_x2, offset_y2 = 5, 6
        elif self.direction == LEFT:
            offset_x1, offset_y1 = -6, -5
            offset_x2, offset_y2 = -6, 5
        elif self.direction == RIGHT:
            offset_x1, offset_y1 = 6, -5
            offset_x2, offset_y2 = 6, 5

        # Whites of the eyes
        pygame.draw.circle(surface, WHITE, (center_x + offset_x1, center_y + offset_y1), radius)
        pygame.draw.circle(surface, WHITE, (center_x + offset_x2, center_y + offset_y2), radius)
        
        # Pupils
        pygame.draw.circle(surface, BLACK, (center_x + offset_x1, center_y + offset_y1), pupil)
        pygame.draw.circle(surface, BLACK, (center_x + offset_x2, center_y + offset_y2), pupil)

    def draw(self, surface):
        # Draw shadows first for depth
        for p in self.positions:
            shadow_rect = pygame.Rect(p[0] + 4, p[1] + 4, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (120, 160, 50), shadow_rect, border_radius=10)

        # Draw the snake body and head
        for i, p in enumerate(self.positions):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            rect = pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE)
            
            # Use border_radius to make the snake look rounded and organic
            pygame.draw.rect(surface, color, rect, border_radius=10)
            
            # Add eyes to the head
            if i == 0:
                self.draw_eyes(surface, p[0], p[1])

def draw_grid(surface):
    # Creates a checkerboard grass pattern
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0:
                pygame.draw.rect(surface, GRASS_1, rect)
            else:
                pygame.draw.rect(surface, GRASS_2, rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Realistic 2D Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24, bold=True)

    snake = Snake()
    food = Food()

    while True:
        # Better event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        snake.move(food)

        # Drawing Phase
        draw_grid(screen)
        food.draw(screen)
        snake.draw(screen)
        
        # Draw Score
        score_surface = font.render(f"Score: {snake.score}", True, BLACK)
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        clock.tick(12) # Slightly faster frame rate for smoother feel

if __name__ == '__main__':
    main()