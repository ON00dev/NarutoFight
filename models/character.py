# models/character.py
import pygame
import os


class Character(pygame.sprite.Sprite):
    def __init__(self, name, sprite_dir, position):
        super().__init__()
        self.name = name
        # Construa o caminho relativo ao diretório base do projeto
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Use os.path.normpath para normalizar o caminho e remover './'
        self.sprite_dir = os.path.normpath(os.path.join(self.base_dir, sprite_dir))
        self.position = position
        self.animations = self.load_animations()
        self.current_animation = self.animations["idle"]
        self.current_frame = 0
        self.animation_speed = 0.2
        self.action = "idle"
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=self.position)
        self.health = 100

    def load_images(self, action):
        """Carrega todos os frames para uma determinada ação."""
        frames = []
        # Construa o caminho completo para a ação específica
        path = os.path.join(self.sprite_dir, action)

        print(f"Tentando carregar imagens de: {path}")  # Verificação de debug

        if not os.path.exists(path):
            raise FileNotFoundError(f"O caminho {path} não foi encontrado.")

        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):
                img_path = os.path.join(path, filename)
                try:
                    frames.append(pygame.image.load(img_path).convert_alpha())
                except pygame.error as e:
                    raise FileNotFoundError(f"Erro ao carregar imagem {img_path}: {e}")

        if not frames:
            raise FileNotFoundError(f"Nenhuma imagem PNG encontrada no diretório {path}.")

        return frames

    def load_animations(self):
        """Carrega todas as animações para o personagem."""
        animations = {
            "idle": self.load_images("idle"),
            "walk": self.load_images("walk"),
            "jump": self.load_images("jump"),
            "crouch": self.load_images("crouch"),
            "attack_1": self.load_images("attack_1")
            "attack_2": self.load_images("attack_2")
            "attack_3": self.load_images("attack_3"),
            "special": self.load_images("special"),
            "block": self.load_images("block"),
            "run": self.load_images("run"),
            "clones": self.load_images("clones"),
            "damage": self.load_images("damage"),
            "teleport": self.load_images("teleport")

        }
        return animations

    def animate(self):
        """Atualiza o frame atual da animação."""
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.current_animation):
            self.current_frame = 0
        self.image = self.current_animation[int(self.current_frame)]

    def update(self):
        """Atualiza o estado do personagem."""
        self.animate()

    def set_action(self, action):
        """Muda a animação do personagem."""
        if action != self.action:
            self.action = action
            self.current_animation = self.animations[action]
            self.current_frame = 0
