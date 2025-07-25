import os
import pygame
try:
    import cairosvg
except ImportError:
    cairosvg = None

class Ghost:
    def __init__(self, recorded_moves, start_pos, color='green'):
        self.moves = recorded_moves
        self.index = 0
        self.rect = pygame.Rect(*start_pos, 40, 60)
        self.state = 'idle'
        self.walk_frame = 0
        self.walk_timer = 0
        self.color = color
        self.sprites = {'idle': None, 'walk': [None, None], 'jump': None}
        self.positions = []  # for motion trail
        # Load sprites
        self.sprites['idle'] = self.load_sprite(f'character_{self.color}_idle')
        self.sprites['walk'][0] = self.load_sprite(f'character_{self.color}_walk_a')
        self.sprites['walk'][1] = self.load_sprite(f'character_{self.color}_walk_b')
        self.sprites['jump'] = self.load_sprite(f'character_{self.color}_jump')

    def load_sprite(self, name):
        svg_path = f'timeloop_game/assets/Characters/{name}.svg'
        png_path = f'timeloop_game/assets/Characters/{name}.png'
        if os.path.exists(png_path):
            return pygame.image.load(png_path).convert_alpha()
        elif os.path.exists(svg_path) and cairosvg:
            cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=40, output_height=60)
            return pygame.image.load(png_path).convert_alpha()
        return None

    def update(self):
        if self.index < len(self.moves):
            move = self.moves[self.index]
            self.rect.x += move['x']
            self.rect.y += move['y']
            self.index += 1
            # Determine state
            if move['y'] < 0:
                self.state = 'jump'
            elif move['x'] != 0:
                self.state = 'walk'
            else:
                self.state = 'idle'
            # Animate walk
            if self.state == 'walk':
                self.walk_timer += 1
                if self.walk_timer > 8:
                    self.walk_frame = 1 - self.walk_frame
                    self.walk_timer = 0
            else:
                self.walk_frame = 0
                self.walk_timer = 0
            # Save position for trail
            self.positions.append(self.rect.topleft)
            if len(self.positions) > 8:
                self.positions.pop(0)

    def draw(self, surface):
        # Draw motion trail
        sprite = None
        if self.state == 'walk':
            sprite = self.sprites['walk'][self.walk_frame]
        else:
            sprite = self.sprites[self.state]
        for i, pos in enumerate(self.positions):
            alpha = int(40 + 20 * i)
            if sprite:
                img = sprite.copy()
                img.set_alpha(alpha)
                surface.blit(img, (pos[0], pos[1]))
            else:
                s2 = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                center = (self.rect.width//2, self.rect.height//2)
                pygame.draw.circle(s2, (100, 200, 255, alpha), center, 20)
                pygame.draw.circle(s2, (255, 255, 255, min(180, alpha+80)), center, 20, 3)
                surface.blit(s2, (pos[0], pos[1]))
        # Draw main ghost
        if sprite:
            img = sprite.copy()
            img.set_alpha(100)
            surface.blit(img, self.rect)
        else:
            s2 = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            center = (self.rect.width//2, self.rect.height//2)
            pygame.draw.circle(s2, (100, 200, 255, 90), center, 20)
            pygame.draw.circle(s2, (255, 255, 255, 180), center, 20, 3)
            surface.blit(s2, (self.rect.x, self.rect.y)) 