# models/fight.py
class Fight:
    def __init__(self, player, cpu, screen):
        self.player = player
        self.cpu = cpu
        self.screen = screen

    def update(self):
        # Atualiza o estado do player e da CPU
        self.player.update()
        self.cpu.update()

    def draw(self):
        # Desenha os personagens na tela
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.cpu.image, self.cpu.rect)
