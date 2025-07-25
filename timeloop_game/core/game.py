import os
import pygame
try:
    import cairosvg
except ImportError:
    cairosvg = None
from core.player import Player
from core.ghost import Ghost
from core.level_loader import LevelLoader
from core.timer import Timer
from utils.recorder import Recorder
from core.puzzle import Button, Door, MovingPlatform

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        pygame.mixer.init()
        self.snd_win = pygame.mixer.Sound('timeloop_game/assets/sounds/win.wav')
        self.snd_lose = pygame.mixer.Sound('timeloop_game/assets/sounds/lose.wav')
        self.snd_button = pygame.mixer.Sound('timeloop_game/assets/sounds/button.wav')
        # Parallax backgrounds
        self.bg_layers = []
        self.bg_offsets = [0, 0]
        self.bg_speeds = [0.2, 0.5]
        bg_files = [
            ('timeloop_game/assets/Backgrounds/background_color_hills.svg', 'timeloop_game/assets/Backgrounds/background_color_hills.png'),
            ('timeloop_game/assets/Backgrounds/background_color_trees.svg', 'timeloop_game/assets/Backgrounds/background_color_trees.png')
        ]
        for i, (svg_path, png_path) in enumerate(bg_files):
            if os.path.exists(png_path):
                img = pygame.image.load(png_path).convert()
                img = pygame.transform.scale(img, (800, 600))
                self.bg_layers.append(img)
            elif os.path.exists(svg_path) and cairosvg:
                cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=800, output_height=600)
                img = pygame.image.load(png_path).convert()
                img = pygame.transform.scale(img, (800, 600))
                self.bg_layers.append(img)
            else:
                self.bg_layers.append(None)
        # Platform tile
        self.tile_img = None
        tile_svg = 'timeloop_game/assets/Tiles/terrain_stone_horizontal_middle.svg'
        tile_png = 'timeloop_game/assets/Tiles/terrain_stone_horizontal_middle.png'
        if os.path.exists(tile_png):
            self.tile_img = pygame.image.load(tile_png).convert_alpha()
        elif os.path.exists(tile_svg) and cairosvg:
            cairosvg.svg2png(url=tile_svg, write_to=tile_png, output_width=40, output_height=20)
            self.tile_img = pygame.image.load(tile_png).convert_alpha()
        self.reset_game()
        self.show_menu = True
        self.button_was_pressed = False

    def draw_parallax_background(self):
        for i, img in enumerate(self.bg_layers):
            if img:
                x = int(self.bg_offsets[i]) % 800
                self.screen.blit(img, (-x, 0))
                self.screen.blit(img, (800-x, 0))

    def draw_platforms(self):
        for plat in self.platforms:
            if self.tile_img:
                tiles = plat.width // 40
                for i in range(tiles):
                    self.screen.blit(self.tile_img, (plat.x + i*40, plat.y))
            else:
                pygame.draw.rect(self.screen, (120, 90, 60), plat, border_radius=8)
                pygame.draw.rect(self.screen, (80, 60, 40), plat, 3, border_radius=8)

    def reset_game(self):
        (self.platforms, self.player_start, self.exit_rect,
         button_rect, door_rect, moving_platform_data) = LevelLoader.load_level('timeloop_game/levels/level_1.json')
        self.player = Player(*self.player_start)
        self.timer = Timer(20)  # 20 seconds for demo
        self.recorder = Recorder()
        self.ghosts = []
        self.ghost_replays = []
        self.won = False
        self.win_time = None
        self.lost = False
        self.lose_time = None
        self.max_loops = 3
        self.loop_count = 0
        self.button = Button(button_rect) if button_rect else None
        self.door = Door(door_rect, self.button) if door_rect and self.button else None
        self.moving_platform = None
        if moving_platform_data:
            self.moving_platform = MovingPlatform(
                moving_platform_data['rect'],
                moving_platform_data['x1'],
                moving_platform_data['x2'],
                moving_platform_data['speed']
            )
        self.button_was_pressed = False

    def run(self):
        while True:
            if self.show_menu:
                self.menu_loop()
                self.reset_game()
                self.show_menu = False
            self.running = True
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                if not self.won and not self.lost:
                    keys = pygame.key.get_pressed()
                    if self.moving_platform:
                        self.moving_platform.update()
                    platforms = self.platforms[:]
                    if self.moving_platform:
                        platforms.append(self.moving_platform.rect)
                    self.player.handle_input(keys)
                    self.player.update(platforms)
                    self.recorder.record((self.player.rect.x, self.player.rect.y))
                    self.timer.update()
                    for ghost in self.ghosts:
                        ghost.update()
                    entities = [self.player] + self.ghosts
                    if self.button:
                        self.button.update(entities)
                        if self.button.pressed and not self.button_was_pressed:
                            self.snd_button.play()
                        self.button_was_pressed = self.button.pressed
                    if self.door:
                        self.door.update()
                    if self.timer.is_time_up():
                        self.ghost_replays.append(self.recorder.get_moves())
                        self.ghosts = [Ghost(moves, self.player_start) for moves in self.ghost_replays]
                        self.player = Player(*self.player_start)
                        self.recorder = Recorder()
                        self.timer.reset()
                        self.loop_count += 1
                        if self.loop_count >= self.max_loops:
                            self.lost = True
                            self.lose_time = pygame.time.get_ticks()
                            self.snd_lose.play()
                    can_exit = (not self.door or self.door.open)
                    if can_exit and self.player.rect.colliderect(self.exit_rect):
                        self.won = True
                        self.win_time = pygame.time.get_ticks()
                        self.snd_win.play()
                # Animate parallax
                for i in range(len(self.bg_layers)):
                    self.bg_offsets[i] += self.bg_speeds[i]
                self.draw_parallax_background()
                self.draw_platforms()
                if self.moving_platform:
                    self.moving_platform.draw(self.screen)
                if self.button:
                    self.button.draw(self.screen)
                if self.door:
                    self.door.draw(self.screen)
                pygame.draw.rect(self.screen, (0, 255, 100), self.exit_rect, border_radius=8)
                for ghost in self.ghosts:
                    ghost.draw(self.screen)
                self.player.draw(self.screen)
                self.timer.draw(self.screen)
                font = pygame.font.SysFont('comicsansms', 48, bold=True)
                loop_text = font.render(f"Loops: {self.loop_count}/{self.max_loops}", True, (255, 255, 255))
                self.screen.blit(loop_text, (10, 50))
                if self.won:
                    font = pygame.font.SysFont('comicsansms', 72, bold=True)
                    text = font.render("You Escaped!", True, (255, 255, 0))
                    self.screen.blit(text, (220, 250))
                    if pygame.time.get_ticks() - self.win_time > 2000:
                        self.running = False
                        self.show_menu = True
                if self.lost:
                    font = pygame.font.SysFont('comicsansms', 72, bold=True)
                    text = font.render("Loop Limit! You Lose!", True, (255, 80, 80))
                    self.screen.blit(text, (100, 250))
                    if pygame.time.get_ticks() - self.lose_time > 2000:
                        self.running = False
                        self.show_menu = True
                pygame.display.flip()
                self.clock.tick(60)

    def menu_loop(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        menu_running = False
                    if event.key == pygame.K_q:
                        exit()
            self.screen.fill((20, 20, 30))
            font = pygame.font.SysFont(None, 72)
            title = font.render("TimeLoop", True, (0, 255, 255))
            self.screen.blit(title, (250, 120))
            font2 = pygame.font.SysFont(None, 48)
            msg = font2.render("Press R to Start or Q to Quit", True, (255, 255, 255))
            self.screen.blit(msg, (140, 300))
            pygame.display.flip()
            self.clock.tick(60) 