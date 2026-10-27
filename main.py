import pygame
import pymunk
from core.loader import carregar_entidades

def resolver_colisao(arbiter, space, data):
    shape_ataque, shape_vitima = arbiter.shapes
    # Lógica de redução de dano baseada no tipo de colisão
    if shape_vitima.collision_type == 1: # Dano Cheio
        print("Dano Máximo Aplicado!")
    elif shape_vitima.collision_type == 2: # Dano Reduzido
        print("Dano Reduzido (Defesa) Aplicado!")
        
    # No Pymunk 7+, rejeitamos o processamento físico usando esta propriedade:
    arbiter.process_collision = False
def menu_principal():
    print("=== MENU PRINCIPAL ===")
    print("1. Modo Carreira (vs IA Primitiva)")
    print("2. Luta Livre (vs IA Primitiva)")
    print("3. Multiplayer (WASD vs Setinhas)")
    # Implementar interface pygame guiada por eventos aqui
    return "multiplayer" # Simulação de escolha

def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Carregamento Dinâmico
    print("Carregando personagens...")
    personagens_disponiveis = carregar_entidades("Personagens", "Personagem")
    print(f"Personagens carregados: {list(personagens_disponiveis.keys())}")
    
    mapas_disponiveis = carregar_entidades("Mapas", "Mapa")

    modo_jogo = menu_principal()
    
# Configuração do Motor de Física
    space = pymunk.Space()
    space.gravity = (0, 900)
    
    # Criando o Chão Estático
    chao_shape = pymunk.Segment(space.static_body, (0, 550), (800, 550), 5)
    chao_shape.friction = 1.0
    space.add(chao_shape)
    
    # Nova API Pymunk 7+ para Handlers de Colisão
    # ... (restante do seu código)
    
    # Nova API Pymunk 7+ para Handlers de Colisão
    space.on_collision(3, 1, begin=resolver_colisao) # 3 = Ataque, 1 = Dano Cheio
    space.on_collision(3, 2, begin=resolver_colisao) # 3 = Ataque, 2 = Dano Reduzido

    # Instanciando lutadores se existirem
    if personagens_disponiveis:
        nome_p1 = list(personagens_disponiveis.keys())[0]
        jogador1 = personagens_disponiveis[nome_p1](space, 200, 400)
        jogador2 = personagens_disponiveis[nome_p1](space, 600, 400)
    else:
        print("Nenhum personagem encontrado. Crie um na pasta Personagens.")
        return

    rodando = True
    while rodando:
        dt = clock.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                
        # Captura de input (Multiplayer)
        teclas = pygame.key.get_pressed()
        if modo_jogo == "multiplayer":
            # Jogador 1 (WASD)
            if teclas[pygame.K_a]: jogador1.body.position = (jogador1.body.position.x - 5, jogador1.body.position.y)
            if teclas[pygame.K_d]: jogador1.body.position = (jogador1.body.position.x + 5, jogador1.body.position.y)
            if teclas[pygame.K_f]: jogador1.atacar(space)
            
            # Jogador 2 (Setas)
            if teclas[pygame.K_LEFT]: jogador2.body.position = (jogador2.body.position.x - 5, jogador2.body.position.y)
            if teclas[pygame.K_RIGHT]: jogador2.body.position = (jogador2.body.position.x + 5, jogador2.body.position.y)
            
        elif modo_jogo in ["carreira", "luta_livre"]:
            # IA Primitiva
            if jogador2.body.position.x > jogador1.body.position.x:
                jogador2.body.position = (jogador2.body.position.x - 1, jogador2.body.position.y)
            else:
                jogador2.atacar(space)
        # Renderização
        tela.fill((0, 0, 0))
        
        # Desenha o chão
        pygame.draw.line(tela, (255, 255, 255), (0, 550), (800, 550), 5)
        
        jogador1.desenhar(tela)
        jogador2.desenhar(tela)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()