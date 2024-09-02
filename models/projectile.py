# models/projectile.py
import pygame
import os


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_left, sprite_dir, speed=10):
        super().__init__()
        self.facing_left = facing_left
        self.sprite_dir = sprite_dir
        self.sprites = self.load_sprites()
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect(midleft=(x, y))
        self.speed = -speed if facing_left else speed
        self.active = True

    def load_sprites(self):
        """Carrega os sprites do projétil."""
        sprites = []
        path = os.path.join(self.sprite_dir, "projectile")

        if not os.path.exists(path):
            raise FileNotFoundError(f"O caminho {path} não foi encontrado.")

        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):
                img_path = os.path.join(path, filename)
                try:
                    frame = pygame.image.load(img_path).convert_alpha()
                    sprites.append(frame)
                except pygame.error as e:
                    raise FileNotFoundError(f"Erro ao carregar imagem {img_path}: {e}")

        if not sprites:
            raise FileNotFoundError(f"Nenhuma imagem PNG encontrada no diretório {path}.")

        return sprites

    def update(self):
        self.current_frame += 0.2  # Ajuste a velocidade de animação conforme necessário
        if self.current_frame >= len(self.sprites):
            self.current_frame = 0
        self.image = self.sprites[int(self.current_frame)]
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
