import pygame

class Ghost:
    def __init__(self, recorded_moves, start_pos):
        self.moves = recorded_moves
        self.index = 0
        self.rect = pygame.Rect(*start_pos, 40, 60)

    def update(self):
        if self.index < len(self.moves):
            move = self.moves[self.index]
            self.rect.x += move['x']
            self.rect.y += move['y']
            self.index += 1

    def draw(self, surface):
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 100))
        surface.blit(s, (self.rect.x, self.rect.y)) 