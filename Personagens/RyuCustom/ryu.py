from core.base_fighter import BaseFighter

# O loader procurará por uma classe chamada "Personagem"
class Personagem(BaseFighter):
    def __init__(self, space, x, y):
        # Passa "RyuCustom" como referência para carregar as pastas certas
        super().__init__(space, x, y, "RyuCustom")
        self.hp = 120
        self.velocidade = 5
        
    def ataque_especial_fogo(self):
        # Lógica para instanciar um projétil (Pymunk Body independente)
        print("Lançando magia de fogo com arquivos da própria pasta!")