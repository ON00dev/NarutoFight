# app/narutofight.py
import pygame
import sys, os
from config.settings import WIDTH, HEIGHT, FPS, KEYS  # Certifique-se de importar KEYS corretamente
from models.fight import Fight
from controllers.player import Player
from controllers.cpu import CPU

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naruto Fight")
clock = pygame.time.Clock()

# Carregando o fundo e o chão
background = pygame.image.load('../assets/backgrounds/background_standart.jpg').convert()
floor = pygame.image.load('../assets/sprites/s_floor/floor.png').convert_alpha()

def draw_chakra_bar(screen, x, y, percentage, color):
    """Desenha uma barra de chakra na tela."""
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    fill = (percentage / 110) * BAR_WIDTH
    border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, color, fill_rect)
    pygame.draw.rect(screen, (255, 225, 150), border_rect, 2)

def draw_hp_bar(screen, x, y, percentage, color):
    """Desenha uma barra de HP (vida) na tela."""
    BAR_WIDTH = 300
    BAR_HEIGHT = 25
    fill = (percentage / 100) * BAR_WIDTH
    border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, color, fill_rect)
    pygame.draw.rect(screen, (255, 125, 0), border_rect, 3)

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

        # Desenhar as barras de chakra e HP
        draw_hp_bar(screen, 20, 10, player.health, (255, 200, 0))  # Barra de vida do player
        draw_chakra_bar(screen, 20, 40, player.chakra, (0, 175, 255))  # Barra de chakra do player

        draw_hp_bar(screen, WIDTH - 320, 10, cpu.health, (255, 200, 0))  # Barra de vida da CPU
        draw_chakra_bar(screen, WIDTH - 220, 40, cpu.chakra, (0, 175, 255))  # Barra de chakra da CPU

        fight.update()
        fight.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
