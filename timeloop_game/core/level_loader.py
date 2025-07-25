import json
import pygame

class LevelLoader:
    @staticmethod
    def load_level(path):
        with open(path, 'r') as f:
            data = json.load(f)
        platforms = [pygame.Rect(*plat) for plat in data.get('platforms', [])]
        player_start = tuple(data.get('player_start', [100, 500]))
        exit_rect = pygame.Rect(*data.get('exit', [700, 500, 40, 60]))
        button_rect = data.get('button')
        door_rect = data.get('door')
        moving_platform = data.get('moving_platform')
        return platforms, player_start, exit_rect, button_rect, door_rect, moving_platform 