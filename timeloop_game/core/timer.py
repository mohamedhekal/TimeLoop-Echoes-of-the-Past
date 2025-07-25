import pygame

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.time_left = duration
        self.last_tick = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = (now - self.last_tick) / 1000.0
        self.time_left -= elapsed
        self.last_tick = now
        if self.time_left < 0:
            self.time_left = 0

    def reset(self):
        self.time_left = self.duration
        self.last_tick = pygame.time.get_ticks()

    def is_time_up(self):
        return self.time_left <= 0

    def draw(self, surface):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Time: {int(self.time_left)}", True, (255, 255, 255))
        surface.blit(text, (10, 10)) 