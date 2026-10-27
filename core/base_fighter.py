import pygame
import pymunk
import os

# Tipos de colisão
COL_DANO_CHEIO = 1
COL_DANO_REDUZIDO = 2
COL_ATAQUE = 3

class BaseFighter:
    def __init__(self, space, x, y, nome_pasta):
        self.nome_pasta = nome_pasta
        self.caminho_base = os.path.join("Personagens", nome_pasta)
        
        # Corpo físico do personagem
        self.body = pymunk.Body(10, float('inf')) # 10 de massa, inércia infinita usando Python nativo
        
        # 1. Hitbox (Recebe dano cheio - Corpo/Cabeça)
        self.shape_dano_cheio = pymunk.Poly.create_box(self.body, (50, 100))
        self.shape_dano_cheio.collision_type = COL_DANO_CHEIO
        # self.shape_dano_cheio.sensor = True  <-- APAGUE OU COMENTE ESTA LINHA
        
        # 2. Hitbox (Dano reduzido - Braços/Defesa)
        # Vértices de uma caixa 20x100 centralizada
        vertices_reduzido = [(-10, -50), (10, -50), (10, 50), (-10, 50)] 
        self.shape_dano_reduzido = pymunk.Poly(self.body, vertices_reduzido, transform=pymunk.Transform(tx=25))
        self.shape_dano_reduzido.collision_type = COL_DANO_REDUZIDO
        self.shape_dano_reduzido.sensor = True
        
        # 3. Hurtbox (Dá dano - Soco/Chute) - Iniciada desativada
        # Vértices de uma caixa 40x20 centralizada
        vertices_ataque = [(-20, -10), (20, -10), (20, 10), (-20, 10)]
        self.shape_ataque = pymunk.Poly(self.body, vertices_ataque, transform=pymunk.Transform(tx=45, ty=20))
        self.shape_ataque.collision_type = COL_ATAQUE
        self.shape_ataque.sensor = True
        # Adiciona ao espaço físico
        space.add(self.body, self.shape_dano_cheio, self.shape_dano_reduzido)
        
        # Atributos de Jogo
        self.hp = 100
        self.carregar_assets()

    def carregar_assets(self):
        # Exemplo de carregamento modular baseado na pasta do personagem
        caminho_tex = os.path.join(self.caminho_base, "texturas")
        caminho_som = os.path.join(self.caminho_base, "efeitos_sonoros")
        # self.sprite_idle = pygame.image.load(os.path.join(caminho_tex, "idle.png"))
        # self.som_soco = pygame.mixer.Sound(os.path.join(caminho_som, "soco.wav"))
        pass

    def atacar(self, space):
        # Adiciona a caixa de dano ao space temporariamente durante o frame de ataque
        if self.shape_ataque not in space.shapes:
            space.add(self.shape_ataque)

    def atualizar(self, dt):
        # Lógica de atualização (animação, timers de ataque, IA)
        pass

    def desenhar(self, tela):
        # Desenho temporário para debug das hitboxes
        x, y = self.body.position
        pygame.draw.rect(tela, (255, 0, 0), (x-25, y-50, 50, 100), 2) # Dano cheio