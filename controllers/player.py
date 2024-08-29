# controllers/player.py
from models.character import Character
import pygame

class Player(Character):
    def __init__(self, name, position):
        sprite_dir = f"assets/sprites/{name}"
        super().__init__(name, sprite_dir, position)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.set_action("walk")
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.set_action("walk")
        elif keys[pygame.K_UP]:
            self.rect.y -= 5
            self.set_action("jump")
        elif keys[pygame.K_DOWN]:
            self.set_action("crouch")
        elif keys[pygame.K_SPACE]:
            self.set_action("attack")
        elif keys[pygame.K_a]:
            self.set_action("special")
        else:
            self.set_action("idle")

        super().update()