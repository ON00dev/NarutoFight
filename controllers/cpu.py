# controllers/cpu.py
from models.character import Character
import random
import time
import pygame

class CPU(Character):
    def __init__(self, name, sprite_dir, position):
        super().__init__(name, sprite_dir, position)
        self.projectiles = []
        self.special_cooldown = 0

    def update(self, player_position):
        # Atualiza a direção da CPU para olhar para o player
        if player_position[0] < self.rect.x:
            self.facing_left = True  # Olha para a esquerda
        else:
            self.facing_left = False  # Olha para a direita

        # Calcula a distância até o jogador
        distance_to_player = abs(player_position[0] - self.rect.x)

        # Decide se a CPU deve correr ou andar em direção ao jogador
        if distance_to_player > random.randint(200,270):  # Distância maior, corre
            self.set_action("run")
            if self.facing_left:
                self.rect.x -= 10
            else:
                self.rect.x += 10
        elif distance_to_player > 50:  # Distância média, anda
            self.set_action("walk")
            if self.facing_left:
                self.rect.x -= 5
            else:
                self.rect.x += 5
        else:
            self.decide_action(player_position)

        self.apply_screen_limits()
        super().update()

    def decide_action(self, player_position):
        """Decide a próxima ação da CPU com base na situação atual."""
        current_time = time.time()

        # Diversifica as ações perto do jogador
        if self.chakra > 45 and current_time > self.special_cooldown:
            self.set_action("special_1")
            self.special_cooldown = current_time + 15  # Cooldown de 15 segundos para o próximo special
        elif self.chakra > 20:
            if random.random() > 0.5:
                self.set_action("clones")
            else:
                self.set_action("reappear")
                self.teleport_and_reappear(player_position)
        elif self.chakra > 15:
            attack_type = random.choice(["attack_1", "attack_2", "attack_3"])
            self.set_action(attack_type)
        else:
            # Aleatoriamente escolher entre bloquear ou agachar quando não pode atacar
            if random.random() > 0.5:
                self.set_action("block")
            else:
                self.set_action("crouch")

    def teleport_and_reappear(self, player_position):
        """Realiza o teleporte e reaparece do lado oposto do jogador."""
        self.set_action("teleport")
        self.is_teleporting = True
        time.sleep(0.75)  # Aguarda 0,75 segundos para simular o desaparecimento

        # Reaparece do lado oposto do jogador
        self.rect.x = player_position[0] - 100 if self.facing_left else player_position[0] + 100
        self.set_action("reappear")
        self.is_teleporting = False

    def apply_screen_limits(self):
        """Impede que o personagem ultrapasse os limites da tela."""
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
