# models/fight.py
class Fight:
    def __init__(self, player, cpu, screen):
        self.player = player
        self.cpu = cpu
        self.screen = screen

    def update(self):
        # Passa a posição da CPU para o player
        self.player.update(self.cpu.rect.topleft)

        # Passa a posição do player para a CPU
        self.cpu.update(self.player.rect.topleft)

    def draw(self):
        # Desenha os personagens na tela
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.cpu.image, self.cpu.rect)
