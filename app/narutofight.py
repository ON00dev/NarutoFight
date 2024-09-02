# app/narutofight.py
import pygame
import sys
from config.settings import WIDTH, HEIGHT, FPS
from models.fight import Fight
from controllers.player import Player
from controllers.cpu import CPU
import os

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naruto Fight")
clock = pygame.time.Clock()

# Carregando o fundo e o chão
background = pygame.image.load('../assets/backgrounds/background_standart.jpg').convert()
floor = pygame.image.load('../assets/sprites/s_floor/floor.png').convert_alpha()

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    player = Player("s_naruto", os.path.join(project_root, "assets/sprites/s_naruto"), (100, 482))
    cpu = CPU("s_naruto", os.path.join(project_root, "assets/sprites/s_naruto"), (600, 482))
    fight = Fight(player, cpu, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()
        cpu.update(player.rect.topleft)

        screen.blit(background, (0, 0))
        screen.blit(floor, (0, HEIGHT - floor.get_height()))

        fight.update()
        fight.draw()

        # Desenhar os projéteis
        for projectile in player.projectiles:
            projectile.draw(screen)
        for projectile in cpu.projectiles:
            projectile.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
