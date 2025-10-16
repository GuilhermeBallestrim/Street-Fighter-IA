# Funcoes.py
def carregar_chao(caminho, WIDTH, GROUND_HEIGHT, pygame):
    chao = pygame.image.load(caminho).convert_alpha()
    chao = pygame.transform.scale(chao, (WIDTH, GROUND_HEIGHT))
    return chao
