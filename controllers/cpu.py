# controllers/cpu.py
import time
import random
import pygame
from models.character import Character

class CPU(Character):
    def __init__(self, name, sprite_dir, position):
        super().__init__(name, sprite_dir, position)
        self.name = name
        self.position = position
        self.sprite_dir = sprite_dir
        self.animations = self.load_all_animations()  # Carrega todas as animações corretamente
        if self.animations is None:
            raise ValueError("Falha ao carregar as animações")  # Proteção contra falhas de carregamento
        self.current_animation = self.animations["idle"]
        self.current_frame = 0
        self.frame_duration = 50  # Duração de cada frame em milissegundos
        self.last_frame_update_time = pygame.time.get_ticks()  # Marca o último momento em que o frame foi trocado
        self.action = "idle"
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=self.position)
        self.facing_left = False
        self.special_cooldown = 0
        self.is_teleporting = False

    def load_all_animations(self):
        """Carrega todas as animações da CPU."""
        animation_list = ["idle", "walk", "run", "jump", "fall", "attack_1", "attack_2", "attack_3",
                          "block", "clones", "teleport", "reappear", "special_1", "special_2"]
        animations = {}
        for action in animation_list:
            try:
                animations[action] = self.load_images(action)  # Carrega os frames de cada animação
            except FileNotFoundError as e:
                print(f"Erro ao carregar animação {action}: {e}")
        return animations if animations else None  # Retorna o dicionário de animações ou None se falhar

    def update(self, player_position):
        """Atualiza o estado da CPU com base na posição do player e em sua lógica de combate."""
        # Atualiza a direção da CPU para olhar para o player
        if player_position[0] < self.rect.x:
            self.facing_left = True  # Olha para a esquerda
        else:
            self.facing_left = False  # Olha para a direita

        # Continua com a lógica de comportamento da CPU
        distance_to_player = abs(player_position[0] - self.rect.x)

        if self.chakra < 20:  # Recarregar chakra
            self.recharge_chakra()
            self.set_action("block")
        elif self.health < 50:  # Recuar quando com pouca vida
            self.recover_or_flee(distance_to_player)
        else:
            if distance_to_player > 200:
                self.run_towards_player(player_position)
            else:
                self.decide_action(player_position)

        self.apply_screen_limits()
        self.animate()  # Atualiza a animação
        super().update(self.action)

    def decide_action(self, player_position):
        """Decide a próxima ação da CPU com base na situação atual."""
        current_time = time.time()

        # Ataques especiais e decisões com base no chakra e cooldown
        if self.chakra > 45 and current_time > self.special_cooldown:
            self.set_action("special_1")
            self.special_cooldown = current_time + 15  # Cooldown de 15 segundos para o próximo special
        elif self.chakra > 20:
            self.pick_offensive_or_defensive(player_position)
        else:
            self.set_action("block")

    def pick_offensive_or_defensive(self, player_position):
        """Escolhe se a CPU ataca ou defende com base em decisões randômicas."""
        if random.choice([True, False]):
            # Decide entre ataque normal ou clones
            if random.choice([True, False]):
                self.set_action("attack_1")
                self.take_damage(15)  # Gasta chakra
            else:
                self.set_action("clones")
                self.take_damage(20)
        else:
            self.set_action("reappear")
            self.teleport_and_reappear(target_position=player_position)

    def run_towards_player(self, player_position):
        """Corre em direção ao player quando longe."""
        self.set_action("run")
        if self.facing_left:
            self.rect.x -= 10  # Corre para a esquerda
        else:
            self.rect.x += 10  # Corre para a direita

    def recover_or_flee(self, distance_to_player):
        """Recupera chakra ou foge se estiver com pouca vida."""
        if distance_to_player < 150:
            self.set_action("run")
            if self.facing_left:
                self.rect.x += 10  # Corre para longe do jogador
            else:
                self.rect.x -= 10
        else:
            self.recharge_chakra()
            self.set_action("idle")

    def apply_screen_limits(self):
        """Impede que a CPU ultrapasse os limites da tela."""
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

    def set_action(self, action):
        """Muda a animação da CPU."""
        if action != self.action:
            if action in self.animations:
                self.action = action
                self.current_animation = self.animations[action]
                self.current_frame = 0  # Reinicia a animação desde o início
                self.last_frame_update_time = pygame.time.get_ticks()  # Reinicia o timer
                print(f"CPU action: {self.action}")
            else:
                print(f"A animação para '{action}' não foi encontrada.")

    def animate(self):
        """Atualiza o frame atual da animação com base no tempo."""
        current_time = pygame.time.get_ticks()

        # Verifica se já passou tempo suficiente para trocar de frame
        if current_time - self.last_frame_update_time >= self.frame_duration:
            self.current_frame += 1
            self.last_frame_update_time = current_time  # Atualiza o tempo do último frame

            # Reinicia a animação se todos os frames já foram exibidos
            if self.current_frame >= len(self.current_animation):
                self.current_frame = 0

        # Atualiza a imagem com base no frame atual
        self.image = self.current_animation[self.current_frame]

        # Inverte o sprite horizontalmente se estiver virado para a esquerda
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)