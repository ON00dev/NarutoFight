# controllers/cpu.py
import random
from models.character import Character

class CPU(Character):
    def __init__(self, name, position):
        sprite_dir = f"assets/sprites/{name}"
        super().__init__(name, sprite_dir, position)

    def update(self):
        move = random.choice(["walk", "idle", "attack", "special"])
        self.set_action(move)

        if move == "walk":
            self.rect.x += random.choice([-5, 5])

        super().update()