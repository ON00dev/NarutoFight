# controllers/cpu.py
from models.character import Character
import random

class CPU(Character):
    def __init__(self, name, sprite_dir, position):
        # Ajuste na assinatura para aceitar 3 argumentos (nome, diretório dos sprites, posição)
        super().__init__(name, sprite_dir, position)

    def update(self):
        move = random.choice(["walk", "idle", "attack", "special"])
        self.set_action(move)

        if move == "walk":
            self.rect.x += random.choice([-5, 5])

        super().update()
