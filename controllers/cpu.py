# controllers/cpu.py
from models.character import Character
from models.projectile import Projectile
import random

class CPU(Character):
    def __init__(self, name, sprite_dir, position):
        super().__init__(name, sprite_dir, position)
        self.projectiles = []

    def launch_projectile(self):
        if self.action == "special" and self.current_frame == len(self.animations["special"]) - 1:
            projectile = Projectile(self.rect.right + 4, self.rect.centery, self.facing_left, self.sprite_dir)
            self.projectiles.append(projectile)

    def update(self, player_position):
        # Determina para onde a CPU deve olhar
        if player_position[0] < self.rect.x:
            self.facing_left = True  # Olha para a esquerda
        else:
            self.facing_left = False  # Olha para a direita

        # Chama o método de animação com base na direção
        super().update()
        self.launch_projectile()

        # Determina a ação da CPU
        move = random.choice(["idle"])#(["walk", "idle", "attack_1", "attack_2", "attack_3"])
        self.set_action(move)

        if move == "walk":
            self.rect.x += random.choice([-5, 5])
