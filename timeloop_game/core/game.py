import pygame
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
        self.reset_game()
        self.show_menu = True

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
                    can_exit = (not self.door or self.door.open)
                    if can_exit and self.player.rect.colliderect(self.exit_rect):
                        self.won = True
                        self.win_time = pygame.time.get_ticks()
                self.screen.fill((30, 30, 40))
                for plat in self.platforms:
                    pygame.draw.rect(self.screen, (100, 80, 60), plat)
                if self.moving_platform:
                    self.moving_platform.draw(self.screen)
                if self.button:
                    self.button.draw(self.screen)
                if self.door:
                    self.door.draw(self.screen)
                pygame.draw.rect(self.screen, (0, 255, 100), self.exit_rect)
                for ghost in self.ghosts:
                    ghost.draw(self.screen)
                self.player.draw(self.screen)
                self.timer.draw(self.screen)
                font = pygame.font.SysFont(None, 48)
                loop_text = font.render(f"Loops: {self.loop_count}/{self.max_loops}", True, (255, 255, 255))
                self.screen.blit(loop_text, (10, 50))
                if self.won:
                    font = pygame.font.SysFont(None, 72)
                    text = font.render("You Escaped!", True, (255, 255, 0))
                    self.screen.blit(text, (220, 250))
                    if pygame.time.get_ticks() - self.win_time > 2000:
                        self.running = False
                        self.show_menu = True
                if self.lost:
                    font = pygame.font.SysFont(None, 72)
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