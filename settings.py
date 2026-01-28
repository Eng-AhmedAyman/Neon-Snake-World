# settings.py
import pygame

# --- Screen Settings ---
CELL_SIZE = 25
CELL_NUMBER = 25
HEADER_HEIGHT = 60

SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = (CELL_SIZE * CELL_NUMBER) + HEADER_HEIGHT

# --- Colors (Comfortable themes) ---
THEMES = [
    (20, 25, 35),  # 0: Calm Navy
    (30, 20, 30),  # 1: Dark Purple
    (35, 20, 20),  # 2: Matte Red
    (15, 30, 25),  # 3: Night Green
    (30, 30, 30),  # 4: Charcoal Grey
    (40, 30, 15),  # 5: Chocolate Brown
    (10, 30, 40),  # 6: Petrol Blue
]

SNAKE_COLOR = (0, 255, 255)
SNAKE_HEAD_COLOR = (0, 255, 255)
SNAKE_BODY_MAIN = (0, 255, 255)
SNAKE_BODY_ACCENT = (0, 200, 200)

EYE_COLOR = (0, 0, 0)
TEXT_COLOR = (220, 220, 220)
SCORE_COLOR = (0, 255, 255)
HIGH_SCORE_COLOR = (255, 200, 50)
GAME_OVER_BG = (10, 10, 15, 230)
MENU_BG_COLOR = (15, 20, 30)
GOLD_COLOR = (255, 215, 0)
CREDIT_COLOR = (100, 100, 100)
PAUSE_OVERLAY = (0, 0, 0, 100)
PARTICLE_COLOR_APPLE = (200, 50, 50)

# --- New Effects Settings ---
GRID_COLOR = (40, 45, 55)  # Grid Color (Slightly lighter than background)
SHAKE_INTENSITY = 5  # Screen Shake Intensity
SHAKE_DURATION = 4  # Shake Duration (in frames)
