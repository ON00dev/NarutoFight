# models/character.py
import pygame
import os

class Character(pygame.sprite.Sprite):
    def __init__(self, name, sprite_dir, position):
        super().__init__()
        self.name = name
        # Corrigindo o caminho para garantir que seja relativo ao diretório raiz do projeto
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
        self.facing_left = True  # Por padrão, os sprites estão virados para a esquerda

    def load_images(self, action):
        frames = []
        path = os.path.join(self.sprite_dir, action)

        print(f"Tentando carregar imagens de: {path}")  # Verificação de debug

        if not os.path.exists(path):
            raise FileNotFoundError(f"O caminho {path} não foi encontrado.")

        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):
                img_path = os.path.join(path, filename)
                try:
                    frame = pygame.image.load(img_path).convert_alpha()
                    frames.append(frame)
                except pygame.error as e:
                    raise FileNotFoundError(f"Erro ao carregar imagem {img_path}: {e}")

        if not frames:
            raise FileNotFoundError(f"Nenhuma imagem PNG encontrada no diretório {path}.")

        return frames

    def load_animations(self):
        animations = {
            "idle": self.load_images("idle"),
            "walk": self.load_images("walk"),
            "jump": self.load_images("jump"),
            "crouch": self.load_images("crouch"),
            "attack_1": self.load_images("attack_1"),
            "attack_2": self.load_images("attack_2"),
            "attack_3": self.load_images("attack_3"),
            "special_1": self.load_images("special1"),
            "block": self.load_images("block"),
            "run": self.load_images("run"),
            "clones": self.load_images("clones"),
            "damage": self.load_images("damage"),
            "teleport": self.load_images("teleport"),
            "fall": self.load_images("fall"),
            "reappear": self.load_images("reappear"),
            "projectil_1": self.load_images("projectil1")

        }

        return animations

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.current_animation):
            self.current_frame = 0
        self.image = self.current_animation[int(self.current_frame)]
        if not self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.animate()

    def set_action(self, action):
        if action != self.action:
            if action in self.animations:
                self.action = action
                self.current_animation = self.animations[action]
                self.current_frame = 0
            else:
                print(f"A animação para '{action}' não foi encontrada.")
