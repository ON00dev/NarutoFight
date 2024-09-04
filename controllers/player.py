# controllers/player.py
from models.character import Character
from config.settings import KEYS
import pygame
import time

class Player(Character):
    def __init__(self, name, sprite_dir, position):
        super().__init__(name, sprite_dir, position)
        self.projectiles = []
        self.last_action = None
        self.special_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if self.chakra > 0:
            if keys[KEYS['jump']] and self.last_action != "jump":
                self.set_action("jump")
                self.last_action = "jump"
            elif keys[KEYS['crouch']] and self.last_action != "crouch":
                self.set_action("crouch")
                self.last_action = "crouch"
            elif keys[KEYS['right']] and keys[KEYS['run']]:
                self.set_action("run")
                self.rect.x += 10
                self.facing_left = False
            elif keys[KEYS['left']] and keys[KEYS['run']]:
                self.set_action("run")
                self.rect.x -= 10
                self.facing_left = True
            elif keys[KEYS['right']]:
                self.set_action("walk")
                self.rect.x += 5
                self.facing_left = False
            elif keys[KEYS['left']]:
                self.set_action("walk")
                self.rect.x -= 5
                self.facing_left = True
            elif keys[KEYS['attack_1']] and self.chakra > 15 and self.last_action != "attack_1":
                self.set_action("attack_1")
                self.last_action = "attack_1"
            elif keys[KEYS['attack_2']] and self.chakra > 15 and self.last_action != "attack_2":
                self.set_action("attack_2")
                self.last_action = "attack_2"
            elif keys[KEYS['attack_3']] and self.chakra > 15 and self.last_action != "attack_3":
                self.set_action("attack_3")
                self.last_action = "attack_3"
            elif keys[KEYS['block']] and self.last_action != "block":
                self.set_action("block")
                self.last_action = "block"
            elif keys[KEYS['teleport']] and self.chakra > 20 and not self.is_teleporting:
                self.set_action("teleport")
                self.is_teleporting = True
                self.teleport_start_time = time.time()
            elif self.is_teleporting:
                if time.time() - self.teleport_start_time >= 0.75:  # Espera 0,75 segundo
                    self.is_teleporting = False
                    self.rect.x = self.rect.x + 100 if self.facing_left else self.rect.x - 100
                    self.set_action("reappear")
            elif keys[KEYS['clones']] and self.chakra > 20 and self.last_action != "clones":
                self.set_action("clones")
                self.last_action = "clones"
            else:
                self.set_action("idle")
                self.last_action = None


        self.apply_screen_limits()
        super().update()

    def apply_screen_limits(self):
        """Impede que o personagem ultrapasse os limites da tela."""
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
