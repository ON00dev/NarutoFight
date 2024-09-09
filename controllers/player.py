import time
import pygame
from models.character import Character
from config.settings import KEYS

class Player(Character):
    def __init__(self, name, sprite_dir, position):
        super().__init__(name, sprite_dir, position)
        self.name = name
        self.position = position
        self.sprite_dir = sprite_dir
        self.animations = self.load_all_animations()

        if not self.animations or "idle" not in self.animations:
            raise ValueError("Falha ao carregar as animações, verifique o caminho do sprite.")

        self.current_animation = self.animations["idle"]
        self.current_frame = 0
        self.frame_duration = 50
        self.last_frame_update_time = pygame.time.get_ticks()
        self.action = "idle"
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=self.position)
        self.facing_left = False
        self.is_busy = False
        self.is_jumping = False  # Inicialmente o player não está pulando
        self.jump_velocity = -15  # Velocidade inicial do pulo
        self.gravity = 1.5  # Ajustando a gravidade para tornar a queda mais rápida
        self.jump_limit = 482  # Altura do chão (ajustar conforme a altura do chão no jogo)

    def load_all_animations(self):
        """Carrega todas as animações do jogador."""
        animation_list = ["idle", "walk", "run", "jump", "fall", "attack_1", "attack_2", "attack_3",
                          "block", "clones", "teleport", "reappear", "special_1", "special_2", "crouch"]  # Incluído crouch
        animations = {}
        for action in animation_list:
            try:
                animations[action] = self.load_images(action)
            except FileNotFoundError as e:
                print(f"Erro ao carregar animação {action}: {e}")
        return animations if animations else None

    def update(self, cpu_position):
        keys = pygame.key.get_pressed()

        # Se estiver ocupado com uma ação, não permite outras ações
        if self.is_busy:
            self.animate()
            return

        # Controle de ataques
        if keys[KEYS['attack_1']] and self.chakra > 15:
            self.set_action("attack_1")
            self.take_damage(15)

        elif keys[KEYS['attack_2']] and self.chakra > 15:
            self.set_action("attack_2")
            self.take_damage(15)

        elif keys[KEYS['attack_3']] and self.chakra > 15:
            self.set_action("attack_3")
            self.take_damage(15)

        # Controle de movimentos especiais
        elif keys[KEYS['clones']] and self.chakra > 20:
            self.set_action("clones")
            self.take_damage(20)

        elif keys[KEYS['teleport']] and self.chakra > 20:
            self.teleport_and_reappear(target_position=cpu_position)
            self.take_damage(20)

        elif keys[KEYS['special_1']] and self.chakra > 45:
            self.set_action("special_1")
            self.take_damage(45)

        elif keys[KEYS['special_2']] and self.chakra > 45:
            self.set_action("special_2")
            self.take_damage(45)

        # Movimento para direita e esquerda (andar e correr)
        elif keys[KEYS['right']] and keys[KEYS['run']]:
            self.set_action("run")
            self.rect.x += 10  # Aumentando a velocidade de corrida para torná-la mais fluida
            self.facing_left = False

        elif keys[KEYS['left']] and keys[KEYS['run']]:
            self.set_action("run")
            self.rect.x -= 10  # Aumentando a velocidade de corrida para torná-la mais fluida
            self.facing_left = True

        elif keys[KEYS['right']]:
            self.set_action("walk")
            self.rect.x += 6  # Ajuste da velocidade de andar para fluidez
            self.facing_left = False

        elif keys[KEYS['left']]:
            self.set_action("walk")
            self.rect.x -= 6  # Ajuste da velocidade de andar para fluidez
            self.facing_left = True

        # Controle de pulo
        elif keys[KEYS['jump']] and not self.is_jumping:  # Garante que o pulo só ocorra quando não estiver no ar
            self.jump()

        # Ação de agachar
        elif keys[KEYS['crouch']]:
            self.set_action("crouch")

        # Se nenhuma tecla foi pressionada, o player volta para idle e recarrega chakra
        else:
            self.set_action("idle")
            self.recharge_chakra()

        self.apply_gravity()  # Aplica a gravidade
        self.animate()
        self.apply_screen_limits()
        super().update(self.action)

    def set_action(self, action):
        """Muda a animação do personagem."""
        if action != self.action and not self.is_busy:
            if action in self.animations:
                self.action = action
                self.current_animation = self.animations[action]
                self.current_frame = 0  # Reinicia a animação desde o início
                self.last_frame_update_time = pygame.time.get_ticks()  # Reinicia o timer
                self.is_busy = True  # Player fica ocupado até a animação terminar
                print(f"Player action: {self.action}")
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
                self.is_busy = False  # Libera o player após a animação terminar
                self.set_action("idle")  # Volta para idle após terminar a ação

        # Atualiza a imagem com base no frame atual
        self.image = self.current_animation[self.current_frame]

        # Inverte o sprite horizontalmente se estiver virado para a esquerda
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        """Executa o pulo."""
        self.is_jumping = True
        self.jump_velocity = -15  # Velocidade inicial do pulo
        self.set_action("jump")

    def apply_gravity(self):
        """Aplica gravidade ao personagem se ele estiver pulando."""
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += self.gravity  # Aumenta a gravidade para a queda

            # Inicia a queda se a velocidade for positiva (descendo)
            if self.jump_velocity > 0:
                self.set_action("fall")

            # Quando atingir o chão, termina o pulo
            if self.rect.y >= self.jump_limit:
                self.rect.y = self.jump_limit
                self.is_jumping = False
                self.set_action("idle")

    def apply_screen_limits(self):
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
