# app/narutofight.py
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import sys
from config.settings import WIDTH, HEIGHT, FPS
from models.fight import Fight
from controllers.player import Player
from controllers.cpu import CPU

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naruto Fight")
clock = pygame.time.Clock()

def main():
    # Caminhos relativos a partir do diretório raiz do projeto
    player = Player("s_naruto", "./assets/sprites/s_naruto", (100, 400))
    cpu = CPU("s_sasuke", "./assets/sprites/s_sasuke", (600, 400))
    fight = Fight(player, cpu, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fight.update()

        screen.fill((0, 0, 0))
        fight.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
