import pygame
import sys
from Variaveis import largura_tela, altura_tela

pygame.init()

tela_config = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
pygame.display.set_caption("Configurações")

fundo_config = pygame.image.load("Sprites/Config.png")
fundo_config = pygame.transform.scale(fundo_config, (largura_tela, altura_tela))

# Adicionando opção restante
opcoes = ["Dificuldade"]
opcao_selecionada = 0  # Índice da opção atual

running_config = True
while running_config:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_config = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
            elif event.key == pygame.K_SPACE:
                if opcoes[opcao_selecionada] == "Dificuldade":
                    
                    # Adicione a lógica para configurar a dificuldade

    tela_config.blit(fundo_config, (0, 0))

    # Desenhe um retângulo cinza transparente sobre os botões
    pygame.draw.rect(tela_config, (100, 100, 100, 100), (0, (altura_tela - len(opcoes) * 40) / 2, 200, len(opcoes) * 40))

    # Desenhe as opções na tela
    fonte = pygame.font.Font(None, 36)
    for i, opcao in enumerate(opcoes):
        cor = (255, 255, 255) if i == opcao_selecionada else (150, 150, 150)
        texto = fonte.render(opcao, True, cor)
        tela_config.blit(texto, (50, (altura_tela - len(opcoes) * 40) / 2 + i * 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
