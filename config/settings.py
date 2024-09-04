# config/settings.py
import configparser
import pygame
import os
import sys

config = configparser.ConfigParser()

# Caminho absoluto para o arquivo settings.ini
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini')

try:
    config.read(config_path)

    if 'DISPLAY' not in config or 'CONTROLS' not in config:
        raise KeyError("Seção 'DISPLAY' ou 'CONTROLS' não encontrada no arquivo de configuração.")

    WIDTH = int(config['DISPLAY']['width'])
    HEIGHT = int(config['DISPLAY']['height'])
    FPS = int(config['DISPLAY']['fps'])

    KEYS = {
        'attack_1': getattr(pygame, config['CONTROLS']['attack_1']),
        'attack_2': getattr(pygame, config['CONTROLS']['attack_2']),
        'attack_3': getattr(pygame, config['CONTROLS']['attack_3']),
        'block': getattr(pygame, config['CONTROLS']['block']),
        'jump': getattr(pygame, config['CONTROLS']['jump']),
        'crouch': getattr(pygame, config['CONTROLS']['crouch']),
        'left': getattr(pygame, config['CONTROLS']['left']),
        'right': getattr(pygame, config['CONTROLS']['right']),
        'run': getattr(pygame, config['CONTROLS']['run']),
        'teleport': getattr(pygame, config['CONTROLS']['teleport']),
        'clones': getattr(pygame, config['CONTROLS']['clones']),
        'special_1': getattr(pygame, config['CONTROLS']['special_1']),
        'special_2': getattr(pygame, config['CONTROLS']['special_2'])
    }

except KeyError as e:
    print(f"Erro de configuração: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao carregar configurações: {e}")
    sys.exit(1)
