# elements.py
import pygame
import random
from pygame.math import Vector2
from settings import *  # Import all settings


# --- Particle Class ---
class Particle:
    """
    Represents a visual particle effect for game juice/feedback.
    """

    def __init__(self, pos, color):
        self.x = pos[0] + random.randint(0, CELL_SIZE)
        self.y = pos[1] + random.randint(0, CELL_SIZE)
        self.color = color
        self.x_vel = random.uniform(-2, 2)
        self.y_vel = random.uniform(-2, 2)
        self.timer = random.randint(15, 30)
        self.size = random.randint(3, 6)

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.timer -= 1
        self.size -= 0.2

    def draw(self, screen):
        if self.size > 0:
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), int(self.size)
            )


# --- Fruit Class ---
class Fruit:
    """
    Represents the main collectible item (Apple).
    """

    def __init__(self):
        try:
            self.image = pygame.image.load("apple.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        except:
            self.image = None
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, screen):
        x_pos = int(self.pos.x * CELL_SIZE)
        y_pos = int(self.pos.y * CELL_SIZE) + HEADER_HEIGHT
        fruit_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        if self.image:
            screen.blit(self.image, fruit_rect)
        else:
            pygame.draw.rect(screen, PARTICLE_COLOR_APPLE, fruit_rect)


# --- Golden Apple Class ---
class BonusFruit:
    """
    Represents a special bonus item with a timer.
    """

    def __init__(self):
        self.randomize()
        self.spawn_time = pygame.time.get_ticks()
        self.exists = True

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self, screen):
        if self.exists:
            x_pos = int(self.pos.x * CELL_SIZE)
            y_pos = int(self.pos.y * CELL_SIZE) + HEADER_HEIGHT
            center = (x_pos + CELL_SIZE // 2, y_pos + CELL_SIZE // 2)
            radius = CELL_SIZE // 2
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                radius -= 2
            pygame.draw.circle(screen, GOLD_COLOR, center, radius)
            pygame.draw.circle(screen, (255, 255, 200), center, radius - 4)


# --- Snake Class ---
class Snake:
    """
    Represents the player's character.
    """

    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_eyes(self, screen, head_rect):
        eye_radius = 3
        center_x, center_y = head_rect.centerx, head_rect.centery
        offset = 6
        if self.direction.x == 1:
            eye1, eye2 = (center_x + 4, center_y - offset + 3), (
                center_x + 4,
                center_y + offset - 3,
            )
        elif self.direction.x == -1:
            eye1, eye2 = (center_x - 4, center_y - offset + 3), (
                center_x - 4,
                center_y + offset - 3,
            )
        elif self.direction.y == -1:
            eye1, eye2 = (center_x - offset + 3, center_y - 4), (
                center_x + offset - 3,
                center_y - 4,
            )
        else:
            eye1, eye2 = (center_x - offset + 3, center_y + 4), (
                center_x + offset - 3,
                center_y + 4,
            )
        pygame.draw.circle(screen, EYE_COLOR, eye1, eye_radius)
        pygame.draw.circle(screen, EYE_COLOR, eye2, eye_radius)

    def draw_mouth(self, screen, head_rect):
        if self.direction.x == 1:
            pygame.draw.circle(
                screen, (0, 0, 0), (head_rect.right, head_rect.centery), 4
            )
        elif self.direction.x == -1:
            pygame.draw.circle(
                screen, (0, 0, 0), (head_rect.left, head_rect.centery), 4
            )
        elif self.direction.y == -1:
            pygame.draw.circle(screen, (0, 0, 0), (head_rect.centerx, head_rect.top), 4)
        else:
            pygame.draw.circle(
                screen, (0, 0, 0), (head_rect.centerx, head_rect.bottom), 4
            )

    def draw_snake(self, screen, fruit_pos, bonus_pos):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE) + HEADER_HEIGHT
            center = (x_pos + CELL_SIZE // 2, y_pos + CELL_SIZE // 2)
            pygame.draw.circle(screen, SNAKE_COLOR, center, CELL_SIZE // 2)

            if index < len(self.body) - 1:
                next_block = self.body[index + 1]
                if block.distance_to(next_block) <= 1.1:
                    next_x = int(next_block.x * CELL_SIZE)
                    next_y = int(next_block.y * CELL_SIZE) + HEADER_HEIGHT
                    next_center = (next_x + CELL_SIZE // 2, next_y + CELL_SIZE // 2)
                    pygame.draw.line(
                        screen, SNAKE_COLOR, center, next_center, CELL_SIZE
                    )

        head_rect = pygame.Rect(
            int(self.body[0].x * CELL_SIZE),
            int(self.body[0].y * CELL_SIZE) + HEADER_HEIGHT,
            CELL_SIZE,
            CELL_SIZE,
        )
        self.draw_eyes(screen, head_rect)

        head_vec = self.body[0]
        dist_fruit = head_vec.distance_to(fruit_pos)
        dist_bonus = head_vec.distance_to(bonus_pos) if bonus_pos else 100
        if dist_fruit < 2 or dist_bonus < 2:
            self.draw_mouth(screen, head_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
