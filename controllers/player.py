# controllers/player.py
from models.character import Character
from models.projectile import Projectile

class Player(Character):
    def __init__(self, name, sprite_dir, position):
        super().__init__(name, sprite_dir, position)
        self.projectiles = []

    def launch_projectile(self):
        # Lança o projétil após a conclusão da animação "special1"
        if self.action == "special" and self.current_frame == len(self.animations["special"]) - 1:
            projectile = Projectile(self.rect.right + 4, self.rect.centery, self.facing_left, self.sprite_dir)
            self.projectiles.append(projectile)

    def update(self):
        super().update()
        self.launch_projectile()

        # Atualiza e remove projéteis inativos
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.active:
                self.projectiles.remove(projectile)
