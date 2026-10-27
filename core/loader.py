import os
import importlib.util

def carregar_entidades(pasta_raiz, classe_alvo="Personagem"):
    entidades_carregadas = {}
    
    if not os.path.exists(pasta_raiz):
        os.makedirs(pasta_raiz)
        
    for nome_pasta in os.listdir(pasta_raiz):
        caminho_pasta = os.path.join(pasta_raiz, nome_pasta)
        
        if os.path.isdir(caminho_pasta):
            arquivos_py = [f for f in os.listdir(caminho_pasta) if f.endswith('.py')]
            
            for arquivo in arquivos_py:
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                try:
                    # Carrega o módulo dinamicamente
                    nome_modulo = f"{nome_pasta}_{arquivo[:-3]}"
                    spec = importlib.util.spec_from_file_location(nome_modulo, caminho_arquivo)
                    modulo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(modulo)
                    
                    # Extrai a classe desejada (espera-se que o usuário crie a classe 'Personagem' ou 'Mapa')
                    if hasattr(modulo, classe_alvo):
                        entidades_carregadas[nome_pasta] = getattr(modulo, classe_alvo)
                    else:
                        print(f"[ERRO] A classe '{classe_alvo}' não foi encontrada em {caminho_arquivo}")
                        
                except Exception as e:
                    print(f"[ERRO FATAL] Falha ao compilar/carregar {nome_pasta}: {e}")
                    
    return entidades_carregadas