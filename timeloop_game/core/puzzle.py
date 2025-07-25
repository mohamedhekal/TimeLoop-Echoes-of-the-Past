import pygame

class Button:
    def __init__(self, rect):
        self.rect = pygame.Rect(*rect)
        self.pressed = False

    def update(self, entities):
        self.pressed = any(self.rect.colliderect(e.rect) for e in entities)

    def draw(self, surface):
        color = (0, 200, 0) if self.pressed else (200, 0, 0)
        pygame.draw.rect(surface, color, self.rect)

class Door:
    def __init__(self, rect, button: Button):
        self.rect = pygame.Rect(*rect)
        self.button = button
        self.open = False

    def update(self):
        self.open = self.button.pressed

    def draw(self, surface):
        if not self.open:
            pygame.draw.rect(surface, (120, 120, 120), self.rect)

class MovingPlatform:
    def __init__(self, rect, x1, x2, speed):
        self.rect = pygame.Rect(*rect)
        self.x1 = x1
        self.x2 = x2
        self.speed = speed
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < self.x1:
            self.rect.x = self.x1
            self.direction = 1
        elif self.rect.x > self.x2:
            self.rect.x = self.x2
            self.direction = -1

    def draw(self, surface):
        pygame.draw.rect(surface, (180, 180, 40), self.rect) 