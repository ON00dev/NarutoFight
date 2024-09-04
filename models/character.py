# models/character.py
import pygame
import os

class Character(pygame.sprite.Sprite):
    def __init__(self, name, sprite_dir, position):
        super().__init__()
        self.name = name
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sprite_dir = os.path.normpath(os.path.join(project_root, sprite_dir.lstrip("./")))
        self.position = position
        self.animations = self.load_animations()
        self.current_animation = self.animations.get("idle", [])
        self.current_frame = 0
        self.animation_speed = 0.2
        self.action = "idle"
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=self.position)
        self.health = 100
        self.chakra = 110
        self.facing_left = False
        self.is_jumping = False
        self.jump_velocity = 0
        self.is_teleporting = False

    def load_animations(self):
        """Carrega todas as animações do personagem a partir do diretório de sprites."""
        animations = {
            "idle": self.load_images("idle"),
            "walk": self.load_images("walk"),
            "jump": self.load_images("jump"),
            "fall": self.load_images("fall"),
            "crouch": self.load_images("crouch"),
            "attack_1": self.load_images("attack_1"),
            "attack_2": self.load_images("attack_2"),
            "attack_3": self.load_images("attack_3"),
            "block": self.load_images("block"),
            "teleport": self.load_images("teleport"),
            "reappear": self.load_images("reappear"),
            "run": self.load_images("run"),
            "clones": self.load_images("clones"),
            "special_1": self.load_images("special1"),
            "scpecial_2": self.load_images("special2")
        }
        return animations

    def load_images(self, action):
        frames = []
        path = os.path.join(self.sprite_dir, action)

        if not os.path.exists(path):
            raise FileNotFoundError(f"O caminho {path} não foi encontrado.")

        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):
                img_path = os.path.join(path, filename)
                frame = pygame.image.load(img_path).convert_alpha()
                frames.append(frame)

        if not frames:
            raise FileNotFoundError(f"Nenhuma imagem PNG encontrada no diretório {path}.")

        return frames

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.current_animation):
            self.current_frame = 0  # Reinicia a animação

        self.image = self.current_animation[int(self.current_frame)]

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.apply_gravity()
        self.animate()
        self.recharge_chakra()
        super().update()

    def set_action(self, action):
        if action != self.action:
            if action in self.animations:
                self.action = action
                self.current_animation = self.animations[action]
                self.current_frame = 0  # Reinicia a animação desde o início
                self.consume_chakra(action)
                if action == "jump" and not self.is_jumping:
                    self.is_jumping = True
                    self.jump_velocity = -15  # Inicia o pulo com uma velocidade negativa
            else:
                print(f"A animação para '{action}' não foi encontrada.")

    def apply_gravity(self):
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += 1  # Simula a gravidade (aumentando a velocidade Y)
            if self.rect.y >= self.position[1]:  # Retorna ao chão
                self.rect.y = self.position[1]
                self.is_jumping = False
                self.set_action("idle")
            elif self.jump_velocity > 0:
                self.set_action("fall")

    def consume_chakra(self, action):
        if self.chakra <= 0:
            return  # Não executa a ação se o chakra estiver zerado

        if action in ["attack_1", "attack_2", "attack_3"]:
            self.chakra -= 15
        elif action in ["clones", "reappear"]:
            self.chakra -= 20
        elif action == "special":
            self.chakra -= 45
        self.chakra = max(self.chakra, 0)  # Garante que não seja menor que 0%

    def recharge_chakra(self):
        if self.action == "idle":
            self.chakra = min(self.chakra + 20 / (3 * 60), 110)  # 20% a cada 3 segundos
