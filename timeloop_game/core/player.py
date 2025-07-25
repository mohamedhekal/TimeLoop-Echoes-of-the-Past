import os
import pygame
try:
    import cairosvg
except ImportError:
    cairosvg = None

class Player:
    def __init__(self, x, y, color='green'):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.on_ground = False
        self.state = 'idle'  # idle, walk, jump
        self.walk_frame = 0
        self.walk_timer = 0
        self.color = color
        self.sprites = {'idle': None, 'walk': [None, None], 'jump': None}
        # Load idle
        self.sprites['idle'] = self.load_sprite(f'character_{self.color}_idle')
        # Load walk frames
        self.sprites['walk'][0] = self.load_sprite(f'character_{self.color}_walk_a')
        self.sprites['walk'][1] = self.load_sprite(f'character_{self.color}_walk_b')
        # Load jump
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

    def handle_input(self, keys):
        speed = 5
        moving = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
            moving = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -12
            self.on_ground = False
        # Set state
        if not self.on_ground:
            self.state = 'jump'
        elif moving:
            self.state = 'walk'
        else:
            self.state = 'idle'

    def update(self, platforms):
        gravity = 0.6
        self.vel_y += gravity
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True
        # Animate walk
        if self.state == 'walk':
            self.walk_timer += 1
            if self.walk_timer > 8:
                self.walk_frame = 1 - self.walk_frame
                self.walk_timer = 0
        else:
            self.walk_frame = 0
            self.walk_timer = 0

    def draw(self, surface):
        sprite = None
        if self.state == 'walk':
            sprite = self.sprites['walk'][self.walk_frame]
        else:
            sprite = self.sprites[self.state]
        if sprite:
            surface.blit(sprite, self.rect)
        else:
            center = self.rect.centerx, self.rect.centery
            pygame.draw.circle(surface, (80, 200, 255), center, 20)
            pygame.draw.circle(surface, (255, 255, 255), center, 20, 3) 