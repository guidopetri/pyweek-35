#! /usr/bin/env python3

import pygame
import config
import sys

from character import MainCharacter
from background import Background
from background import Foreground
from background import Boundaries
from background import Shadows
from dialog import Dialog
from gui import Gui
from map import Map


def handle_events(state):
    keys_map = {pygame.K_UP: {'movement': (0, -config.character_speed),
                              'direction': 'back',
                              },
                pygame.K_DOWN: {'movement': (0, config.character_speed),
                                'direction': 'forward',
                                },
                pygame.K_LEFT: {'movement': (-config.character_speed, 0),
                                'direction': 'left',
                                },
                pygame.K_RIGHT: {'movement': (config.character_speed, 0),
                                 'direction': 'right',
                                 },
                }

    any_key = False
    mode = state['current_game_mode']
    state['walking'] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            any_key = True

    keys = pygame.key.get_pressed()

    if mode == config.Modes.MAIN_MENU:
        if any_key:
            state['current_game_mode'] = config.Modes.INTRO
    elif mode == config.Modes.INTRO:
        if any_key:
            state['active_message'] += 1
            if state['active_message'] >= len(config.intro_messages):
                state['current_game_mode'] = config.Modes.GAME
                state['active_message'] = 0
    elif mode == config.Modes.GAME:
        for key, actions in keys_map.items():
            if keys[key]:
                state['position'] = tuple(map(sum, zip(state['position'],
                                                       actions['movement'])))
                state['walking'] = True
                state['direction'] = actions['direction']

        if config.debug_mode:
            if keys[pygame.K_a]:
                state['hp'] = min(state['hp'] + 1, 100)
            if keys[pygame.K_s]:
                state['hp'] = max(state['hp'] - 1, 0)
            if keys[pygame.K_d]:
                state['status'] = 'unsafe'
            if keys[pygame.K_f]:
                state['status'] = 'safe'
            if keys[pygame.K_g]:
                state['status'] = 'dead'
            if keys[pygame.K_e]:
                state['inventory']['candle'] += 1
            if keys[pygame.K_r]:
                state['inventory']['candle'] -= 1
            if keys[pygame.K_t]:
                state['action'] = 'firefly'
            if keys[pygame.K_y]:
                state['action'] = 'walking'

    return state


if __name__ == '__main__':
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode(config.screen_size)

    game_state = {'current_game_mode': config.Modes.GAME,
                  'active_message': 0,
                  'hp': 100,
                  'status': 'safe',
                  'action': 'walking',
                  'inventory': {'candle': 5, 'firefly': 1, 'snail': 3},
                  'direction': 'forward',
                  'walking': False,
                  'position': (0, 0),
                  }

    character = MainCharacter(surface)
    bg = Background(surface)
    dialog = Dialog(surface)
    shadows = Shadows(surface, area=720, variance=48000)
    fg = Foreground(surface)
    gui = Gui(surface)
    boundaries = Boundaries(surface)
    game_map = Map()
    game_map.generate_map()
    game_state['map'] = game_map.map
    game_map.pretty_print()

    while True:
        game_state = handle_events(game_state)

        surface.fill('black')

        bg.render(game_state)
        character.render(game_state)
        fg.render(game_state)
        shadows.render(game_state)
        gui.render(game_state)
        dialog.render(game_state)

        pygame.display.flip()

        clock.tick(config.framerate)
