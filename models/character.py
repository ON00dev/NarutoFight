# models/character.py
import pygame
import os
import threading

class Character(pygame.sprite.Sprite):
    def __init__(self, name, sprite_dir, position):
        super().__init__()
        self.name = name
        self.position = position
        self.sprite_dir = sprite_dir
        self.animations = {}  # Mantém todas as animações carregadas
        self.animation_cache = {}  # Cache para armazenar animações já carregadas
        self.current_animation = []  # Inicialmente vazio
        self.current_frame = 0
        self.frame_duration = 50  # Duração de cada frame
        self.last_frame_update_time = pygame.time.get_ticks()
        self.image = pygame.Surface((64, 64))  # Animação temporária até carregar a real
        self.rect = self.image.get_rect(topleft=self.position)
        self.facing_left = False
        self.animations_loaded = False
        self.is_teleporting = False
        self.is_jumping = True
        self.jump_velocity = 15
        self.chakra = 110
        self.health = 100
        self.action = "idle"  # Inicializa com "idle"

        # Inicia o carregamento da animação inicial (idle)
        self.load_animations_threaded("idle")
        self.set_action("idle")  # Define a animação inicial como idle

    def is_on_screen(self):
        """Verifica se o personagem está dentro dos limites visíveis da tela."""
        screen_width, screen_height = pygame.display.get_surface().get_size()
        return self.rect.right > 0 and self.rect.left < screen_width and self.rect.bottom > 0 and self.rect.top < screen_height

    def load_images(self, action):
        """Carrega os sprites de uma ação específica."""
        if action not in self.animation_cache:
            frames = []
            path = os.path.join(self.sprite_dir, action)

            if not os.path.exists(path):
                raise FileNotFoundError(f"O caminho {path} não foi encontrado.")

            for filename in sorted(os.listdir(path)):
                if filename.endswith(".png"):
                    img_path = os.path.join(path, filename)
                    surface = pygame.image.load(img_path).convert_alpha()  # Usa Surface
                    frames.append(surface)

            if not frames:
                raise FileNotFoundError(f"Nenhuma imagem PNG encontrada no diretório {path}.")

            self.animation_cache[action] = frames

        return self.animation_cache[action]

    def load_animations_threaded(self, action):
        """Carrega uma animação em uma thread separada."""
        thread = threading.Thread(target=self.load_images, args=(action,))
        thread.start()  # Inicia o carregamento da animação em segundo plano
        return []  # Retorna uma lista vazia até que a animação seja carregada

    def load_all_animations(self):
        """Inicia o carregamento de todas as animações em threads separadas."""
        animation_list = ["idle", "walk", "run", "jump", "fall", "attack_1", "attack_2", "attack_3", "block",
                          "clones", "teleport", "reappear", "special_1", "special_2"]

        for action in animation_list:
            self.load_animations_threaded(action)

    def check_if_loaded(self):
        """Verifica se todas as animações foram carregadas."""
        for action in ["idle", "walk", "run", "jump", "fall", "attack_1", "attack_2", "attack_3",
                       "block", "clones", "teleport", "reappear", "special_1", "special_2"]:
            if action not in self.animation_cache:
                return False  # Ainda não carregou completamente

        self.animations_loaded = True
        return True

    def animate(self):
        """Atualiza o frame atual da animação com base no tempo."""
        # Verifica se a animação foi carregada e se não está vazia
        if not self.animations_loaded and not self.check_if_loaded():
            return  # Animações ainda não estão carregadas ou a lista está vazia

        if len(self.current_animation) == 0:
            return  # Proteção para garantir que não haja uma lista vazia

        current_time = pygame.time.get_ticks()
        animation_speed = self.frame_duration

        if current_time - self.last_frame_update_time >= animation_speed:
            self.current_frame += 1
            self.last_frame_update_time = current_time

            if self.current_frame >= len(self.current_animation):
                self.current_frame = 0

        # Atualiza a imagem com base no frame atual
        if len(self.current_animation) > 0:
            self.image = self.current_animation[self.current_frame]

        # Inverte o sprite se estiver virado para a esquerda
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, action):
        """Atualiza o estado do personagem."""
        if not self.is_on_screen():
            return  # Suspende a atualização se o personagem estiver fora da tela

        self.animate()

        # Atualiza a posição vertical se o personagem estiver pulando
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += 1  # Simula a gravidade

            # Limite de altura do pulo e inicia a queda
            if self.jump_velocity > 0:
                self.set_action("fall")

            # Quando atingir o chão
            if self.rect.y >= 482:  # Volta para a posição inicial (ajustar para seu jogo)
                self.rect.y = 482
                self.is_jumping = False
                self.set_action("idle")

    def set_action(self, action):
        """Muda a animação do personagem."""
        if action != self.action:
            # Garante que a animação foi carregada antes de definir a ação
            if action in self.animation_cache and len(self.animation_cache[action]) > 0:
                self.action = action  # Atualiza a ação atual
                self.current_animation = self.animation_cache[action]
                self.current_frame = 0
                self.last_frame_update_time = pygame.time.get_ticks()
            else:
                print(f"A animação para '{action}' não foi encontrada ou ainda está carregando.")

    def apply_screen_limits(self):
        """Mantém o personagem dentro dos limites da tela."""
        screen_width = pygame.display.get_surface().get_width()
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

    def jump(self):
        """Executa o pulo."""
        if not self.is_jumping:  # Permite pular apenas se não estiver pulando
            self.is_jumping = True
            self.jump_velocity = -15  # Velocidade inicial do pulo
            self.set_action("jump")

    def apply_gravity(self):
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += 3  # Simula a gravidade (aumentando a velocidade Y)
            if self.rect.y >= self.position[1]:  # Retorna ao chão
                self.rect.y = self.position[1]
                self.is_jumping = False
                self.set_action("fall")
            elif self.jump_velocity > 0:
                self.set_action("fall")

    def consume_chakra(self, action):
        if self.chakra <= 0:
            return  # Não executa a ação se o chakra estiver zerado

        if action in ["attack_1", "attack_2", "attack_3"]:
            self.chakra -= 15
        elif action in ["clones", "reappear"]:
            self.chakra -= 20
        elif action == "special_1" or  action == "special_2":
            self.chakra -= 45
        self.chakra = max(self.chakra, 0)  # Garante que não seja menor que 0%

    def recharge_chakra(self):
        if self.action == "idle":
            self.chakra = min(self.chakra + 20 / (3 * 60), 110)  # 20% a cada 3 segundos

    def teleport_and_reappear(self, target_position):
        """Teleporta e reaparece em uma posição oposta ao player."""
        self.set_action("teleport")
        self.is_teleporting = True
        pygame.time.delay(750)  # Aguarda 0,75 segundos para simular o desaparecimento

        # Move o personagem para o lado oposto do player
        if self.facing_left:
            self.rect.x = target_position[0] + 100
        else:
            self.rect.x = target_position[0] - 100

        self.set_action("reappear")
        self.is_teleporting = False

    def take_damage(self, amount):
        """Reduz a vida."""
        self.chakra = max(self.health - amount, 0)  # Gasta vida, sem deixar negativo