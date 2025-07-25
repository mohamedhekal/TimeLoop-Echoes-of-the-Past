import pygame

class Button:
    def __init__(self, rect):
        self.rect = pygame.Rect(*rect)
        self.pressed = False

    def update(self, entities):
        self.pressed = any(self.rect.colliderect(e.rect) for e in entities)

    def draw(self, surface):
        # Draw shadow
        shadow = self.rect.copy()
        shadow.y += 4
        pygame.draw.rect(surface, (40, 40, 60, 80), shadow, border_radius=8)
        # Draw button
        color = (0, 220, 100) if self.pressed else (220, 60, 60)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=8)
        if self.pressed:
            glow = pygame.Surface((self.rect.width+8, self.rect.height+8), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (0,255,100,80), glow.get_rect())
            surface.blit(glow, (self.rect.x-4, self.rect.y-4), special_flags=pygame.BLEND_RGBA_ADD)

class Door:
    def __init__(self, rect, button: Button):
        self.rect = pygame.Rect(*rect)
        self.button = button
        self.open = False

    def update(self):
        self.open = self.button.pressed

    def draw(self, surface):
        # Draw shadow
        shadow = self.rect.copy()
        shadow.y += 6
        pygame.draw.rect(surface, (40, 40, 60, 80), shadow, border_radius=8)
        # Draw door
        if not self.open:
            pygame.draw.rect(surface, (120, 120, 120), self.rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=8)
        else:
            # Draw open door as a faint outline
            pygame.draw.rect(surface, (120, 255, 120, 80), self.rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255, 120), self.rect, 2, border_radius=8)

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
        # Draw shadow
        shadow = self.rect.copy()
        shadow.y += 6
        pygame.draw.rect(surface, (40, 40, 60, 80), shadow, border_radius=8)
        # Draw platform
        pygame.draw.rect(surface, (180, 180, 40), self.rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=8) 