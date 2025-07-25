import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.on_ground = False

    def handle_input(self, keys):
        speed = 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -12
            self.on_ground = False

    def update(self, platforms):
        gravity = 0.6
        self.vel_y += gravity
        self.rect.y += int(self.vel_y)
        # Simple ground/platform collision
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

    def draw(self, surface):
        pygame.draw.rect(surface, (80, 200, 255), self.rect) 