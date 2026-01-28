# main.py
import pygame
import sys
import random
import math
import ctypes
from pygame.math import Vector2

# Importing local modules
from settings import *
from sounds import SoundManager
from elements import Snake, Fruit, BonusFruit, Particle

pygame.init()
pygame.mixer.init()

# 1. Fixing taskbar icon in Windows
try:
    app_id = "my_snake_game.unique.id.v1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except:
    pass

# 2. Load Icon
try:
    icon_surface = pygame.image.load("icon.png")
    pygame.display.set_icon(icon_surface)
except:
    pass

# 3. Background Music
try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except:
    pass

# Initialize Main Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Neon Snake World 🌍🐍")
clock = pygame.time.Clock()

# Fonts
game_font_big = pygame.font.Font(None, 60)
game_font_huge = pygame.font.Font(None, 80)
game_font_small = pygame.font.Font(None, 28)
game_font_tiny = pygame.font.Font(None, 24)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Create a sound manager
sounds = SoundManager()


def draw_text_with_glow(text, font, text_col, glow_col, center_pos, surface):
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    glow_surf = font.render(text, True, glow_col)
    for ox, oy in offsets:
        rect = glow_surf.get_rect(center=(center_pos[0] + ox, center_pos[1] + oy))
        surface.blit(glow_surf, rect)
    main_surf = font.render(text, True, text_col)
    main_rect = main_surf.get_rect(center=center_pos)
    surface.blit(main_surf, main_rect)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.bonus = None
        self.state = "MENU"
        self.is_paused = False
        self.music_muted = False
        self.particles = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1

        # New: Shake Timer and Virtual Surface
        self.shake_timer = 0
        # Create a virtual surface to draw everything on before rendering to the main screen
        self.display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        try:
            self.logo_img = pygame.image.load("logo.png").convert_alpha()
            self.logo_img = pygame.transform.scale(self.logo_img, (150, 150))
        except:
            self.logo_img = None

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as file:
                file.write(str(self.high_score))

    def create_particles(self, position, color, amount=8):
        x_pixel = position.x * CELL_SIZE
        y_pixel = position.y * CELL_SIZE + HEADER_HEIGHT
        for _ in range(amount):
            self.particles.append(Particle((x_pixel, y_pixel), color))

    def update(self):
        if self.state == "PLAYING" and not self.is_paused:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
            self.check_bonus_timer()

        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.timer > 0]

        # Decrease shake timer
        if self.shake_timer > 0:
            self.shake_timer -= 1

    def draw_grid(self):
        # Draw vertical lines
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(
                self.display_surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT)
            )
        # Draw horizontal lines
        for y in range(HEADER_HEIGHT, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(
                self.display_surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y)
            )

    def draw_elements(self):
        # 1. Draw on the virtual surface (display_surface) instead of the screen directly
        self.draw_solid_bg()

        # 2. Draw Grid (New)
        if self.state != "MENU":
            self.draw_grid()

        self.draw_ui_bg()

        if self.state != "MENU":
            self.fruit.draw_fruit(self.display_surface)
            if self.bonus:
                self.bonus.draw(self.display_surface)
            bonus_pos = self.bonus.pos if self.bonus else None
            self.snake.draw_snake(self.display_surface, self.fruit.pos, bonus_pos)
            for particle in self.particles:
                particle.draw(self.display_surface)
            self.draw_stats()
            if self.is_paused:
                self.draw_pause_screen()

        if self.state == "GAME_OVER":
            self.draw_game_over()
        if self.state == "MENU":
            self.draw_menu()

        # 3. Apply Shake Effect
        shake_offset = (0, 0)
        if self.shake_timer > 0:
            shake_offset = (
                random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY),
                random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY),
            )

        # 4. Blit the final surface to the main screen with offset
        screen.fill((0, 0, 0))  # Clear edges (black fill) during shake
        screen.blit(self.display_surface, shake_offset)

    def draw_solid_bg(self):
        theme_index = (self.score // 25) % len(THEMES)
        self.display_surface.fill(THEMES[theme_index])

    def draw_ui_bg(self):
        ui_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(self.display_surface, (15, 20, 30), ui_rect)
        pygame.draw.line(
            self.display_surface,
            (50, 60, 70),
            (0, HEADER_HEIGHT),
            (SCREEN_WIDTH, HEADER_HEIGHT),
            2,
        )

    def draw_stats(self):
        row1_y = 20
        score_surf = game_font_small.render(f"Score: {self.score}", True, SCORE_COLOR)
        level_surf = game_font_small.render(f"Level: {self.level}", True, TEXT_COLOR)
        high_surf = game_font_small.render(
            f"Best: {self.high_score}", True, HIGH_SCORE_COLOR
        )

        self.display_surface.blit(score_surf, score_surf.get_rect(midleft=(20, row1_y)))
        self.display_surface.blit(
            level_surf, level_surf.get_rect(center=(SCREEN_WIDTH / 2, row1_y))
        )
        self.display_surface.blit(
            high_surf, high_surf.get_rect(midright=(SCREEN_WIDTH - 20, row1_y))
        )

        row2_y = 45
        music_status = "OFF" if self.music_muted else "ON"
        music_col = (255, 100, 100) if self.music_muted else (100, 255, 100)
        prefix_surf = game_font_tiny.render(
            f"[P] Pause   [M] Sound: ", True, (150, 150, 150)
        )
        prefix_rect = prefix_surf.get_rect(midright=(SCREEN_WIDTH / 2 + 10, row2_y))
        status_surf = game_font_tiny.render(music_status, True, music_col)

        self.display_surface.blit(prefix_surf, prefix_rect)
        self.display_surface.blit(
            status_surf, status_surf.get_rect(midleft=(prefix_rect.right, row2_y))
        )

    def draw_menu(self):
        self.display_surface.fill(MENU_BG_COLOR)
        title_y = 100 if not self.logo_img else 80
        draw_text_with_glow(
            "Snake Game",
            game_font_huge,
            SNAKE_HEAD_COLOR,
            (0, 150, 150),
            (SCREEN_WIDTH // 2, title_y),
            self.display_surface,
        )

        if self.logo_img:
            float_y = math.sin(pygame.time.get_ticks() * 0.003) * 10
            logo_rect = self.logo_img.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20 + float_y)
            )
            self.display_surface.blit(self.logo_img, logo_rect)

        sub_title = game_font_small.render(
            "Welcome to the Neon Snake World", True, SNAKE_BODY_ACCENT
        )
        self.display_surface.blit(
            sub_title,
            sub_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)),
        )

        if pygame.time.get_ticks() % 1000 < 600:
            draw_text_with_glow(
                "Press SPACE to Start",
                game_font_big,
                SCORE_COLOR,
                (0, 100, 100),
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130),
                self.display_surface,
            )

        best_surf = game_font_small.render(
            f"Highest Score: {self.high_score}", True, HIGH_SCORE_COLOR
        )
        self.display_surface.blit(
            best_surf, best_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 70))
        )
        credit_surf = game_font_tiny.render("Made by Ahmed Ayman", True, CREDIT_COLOR)
        self.display_surface.blit(
            credit_surf,
            credit_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30)),
        )

    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(PAUSE_OVERLAY)
        self.display_surface.blit(overlay, (0, 0))
        draw_text_with_glow(
            "PAUSED",
            game_font_big,
            TEXT_COLOR,
            (50, 50, 50),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20),
            self.display_surface,
        )
        resume_text = game_font_small.render(
            "Press P to Resume", True, SNAKE_HEAD_COLOR
        )
        self.display_surface.blit(
            resume_text,
            resume_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30)),
        )

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            if not self.music_muted:
                pygame.mixer.music.pause()
        else:
            if not self.music_muted:
                pygame.mixer.music.unpause()

    def toggle_music(self):
        self.music_muted = not self.music_muted
        if self.music_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.create_particles(self.fruit.pos, PARTICLE_COLOR_APPLE)
            self.fruit.randomize()
            self.snake.add_block()
            sounds.play_eat()
            self.score += 1
            if self.score % 10 == 0:
                self.level_up()
            if not self.bonus and random.randint(0, 10) < 3:
                self.bonus = BonusFruit()

        if self.bonus:
            if self.bonus.pos == self.snake.body[0]:
                self.create_particles(self.bonus.pos, GOLD_COLOR, amount=15)
                self.snake.add_block()
                self.score += 5
                self.bonus = None
                sounds.play_bonus()

    def check_bonus_timer(self):
        if not self.is_paused and self.bonus:
            if pygame.time.get_ticks() - self.bonus.spawn_time > 5000:
                self.bonus = None

    def level_up(self):
        self.level += 1
        new_speed = max(40, 150 - (self.level * 5))
        pygame.time.set_timer(SCREEN_UPDATE, int(new_speed))

    def check_fail(self):
        if (
            not 0 <= self.snake.body[0].x < CELL_NUMBER
            or not 0 <= self.snake.body[0].y < CELL_NUMBER
        ):
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        if self.state == "PLAYING":
            sounds.play_crash()
            self.save_high_score()
            self.shake_timer = SHAKE_DURATION  # Trigger the shake
        self.state = "GAME_OVER"
        if not self.music_muted:
            pygame.mixer.music.unpause()

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(GAME_OVER_BG)
        self.display_surface.blit(overlay, (0, 0))
        draw_text_with_glow(
            "GAME OVER",
            game_font_big,
            (255, 50, 50),
            (100, 0, 0),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40),
            self.display_surface,
        )
        score_surf = game_font_small.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.display_surface.blit(
            score_surf,
            score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)),
        )
        restart_surf = game_font_small.render(
            "Press SPACE to Restart", True, TEXT_COLOR
        )
        self.display_surface.blit(
            restart_surf,
            restart_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80)),
        )
        menu_surf = game_font_small.render("Press ESC for Menu", True, (150, 150, 150))
        self.display_surface.blit(
            menu_surf,
            menu_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120)),
        )
        credit_surf = game_font_tiny.render(
            "Made by Ahmed Ayman", True, (100, 100, 100)
        )
        self.display_surface.blit(
            credit_surf,
            credit_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30)),
        )

    def start_game(self):
        self.snake.reset()
        self.fruit.randomize()
        self.bonus = None
        self.score = 0
        self.level = 1
        pygame.time.set_timer(SCREEN_UPDATE, 150)
        self.high_score = self.load_high_score()
        self.state = "PLAYING"
        self.is_paused = False
        self.particles = []
        self.shake_timer = 0
        if not self.music_muted:
            pygame.mixer.music.unpause()

    def go_to_menu(self):
        self.state = "MENU"


# --- Main Loop ---
main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                main_game.toggle_music()
            if main_game.state == "MENU":
                if event.key == pygame.K_SPACE:
                    main_game.start_game()
            elif main_game.state == "PLAYING":
                if event.key == pygame.K_p:
                    main_game.toggle_pause()
                if not main_game.is_paused:
                    if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                    if (
                        event.key == pygame.K_RIGHT
                        and main_game.snake.direction.x != -1
                    ):
                        main_game.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
            elif main_game.state == "GAME_OVER":
                if event.key == pygame.K_SPACE:
                    main_game.start_game()
                if event.key == pygame.K_ESCAPE:
                    main_game.go_to_menu()

    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
