# sounds.py
import pygame


class SoundManager:
    """
    Handles loading and playing sound effects safely.
    Prevents crashes if sound files are missing.
    """

    def __init__(self):
        self.eat_sound = None
        self.bonus_sound = None
        self.crash_sound = None
        try:
            self.eat_sound = pygame.mixer.Sound("eat.wav")
        except:
            pass
        try:
            self.bonus_sound = pygame.mixer.Sound("bonus.wav")
        except:
            pass
        try:
            self.crash_sound = pygame.mixer.Sound("crash.wav")
        except:
            pass

    def play_eat(self):
        if self.eat_sound:
            self.eat_sound.play()

    def play_bonus(self):
        if self.bonus_sound:
            self.bonus_sound.play()

    def play_crash(self):
        if self.crash_sound:
            self.crash_sound.play()
