import pygame
import json
import subprocess
import sys

python = sys.executable

def tela_de_controles(config_teclas, largura_tela, altura_tela):

    pygame.init()
    pygame.mouse.set_visible(False)
    padrao_config_teclas = {
        "Mover para cima": pygame.K_w,
        "Mover para baixo": pygame.K_s,
        "Mover para esquerda": pygame.K_a,
        "Mover para direita": pygame.K_d,
        "Teleporte": pygame.K_LSHIFT,
        "Comprar na loja": pygame.K_e,
    }

    # Garantir que todas as opções existam no dicionário carregado
    for chave, valor in padrao_config_teclas.items():
        if chave not in config_teclas:
            config_teclas[chave] = valor
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Configuração de Controles")

    # Carregar imagem de fundo
    fundo = pygame.image.load("Sprites/botao_menu.png").convert()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

    # Fonte e cores
    fonte = pygame.font.Font(None, 50)
    fonte_esc = pygame.font.Font(None, 40)
    cor_texto = (255, 255, 255)
    cor_contorno = (0, 0, 0)  # Preto para o contorno
    cor_selecionado = (50, 255, 50)  # Verde para o item selecionado

    # Lista de funções e teclas
    funcoes = list(config_teclas.keys())
    indice_selecionado = 0
    redefinindo_tecla = False
    mensagem = ""  # Mensagem temporária de feedback

    relogio = pygame.time.Clock()
    tempo_piscar = 0  # Para controlar o piscar do "__"
    mostrar_piscar = True

    rodando = True
    while rodando:
        centro_tela = (largura_tela // 2, altura_tela // 2)  # Define o centro da tela
        pygame.mouse.set_pos(centro_tela)
        tela.blit(fundo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if redefinindo_tecla:
                    nova_tecla = evento.key
                    funcao_atual = funcoes[indice_selecionado]

                    # Verificar duplicação de teclas
                    if nova_tecla in config_teclas.values():
                        mensagem = f"Tecla '{pygame.key.name(nova_tecla)}' já usada!"
                    else:
                        config_teclas[funcao_atual] = nova_tecla
                        redefinindo_tecla = False
                        salvar_config_teclas(config_teclas)
                        mensagem = f"Tecla para '{funcao_atual}' alterada!"

                else:
                    if evento.key == pygame.K_w:  # Mover para cima
                        indice_selecionado = (indice_selecionado - 1) % len(funcoes)
                    elif evento.key == pygame.K_s:  # Mover para baixo
                        indice_selecionado = (indice_selecionado + 1) % len(funcoes)
                    elif evento.key == pygame.K_SPACE:  # Selecionar para redefinir
                        redefinindo_tecla = True
                        mensagem = "Pressione uma nova tecla..."
                    elif evento.key == pygame.K_ESCAPE:  # Voltar ao menu principal
                        pygame.quit()
                        subprocess.run([python, "Ruptura_Temporal.py"])
                        sys.exit()

        # Piscar do "__"
        tempo_piscar += relogio.get_time()
        if tempo_piscar > 500:  # Alterna a cada 500ms
            mostrar_piscar = not mostrar_piscar
            tempo_piscar = 0

        # Renderizar as opções
        for i, funcao in enumerate(funcoes):
            texto = f"{funcao}: {pygame.key.name(config_teclas[funcao])}"
            if i == indice_selecionado:
                cor = cor_selecionado
                if redefinindo_tecla and mostrar_piscar:
                    texto += " __"
            else:
                cor = cor_texto

            # Renderizar texto com contorno
            render_com_contorno(tela, texto, fonte, largura_tela // 4, 100 + i * 60, cor, cor_contorno)

        # Exibir mensagem de feedback
        if mensagem:
            render_com_contorno(tela, mensagem, fonte, largura_tela // 6, altura_tela - 50, cor_selecionado, cor_contorno)

        # Adicionar instrução no canto superior direito
        texto_esc = "ESC <---"
        render_com_contorno(tela, texto_esc, fonte_esc, largura_tela - 150, 20, cor_texto, cor_contorno)

        # Atualizar a tela
        pygame.display.flip()
        relogio.tick(60)
    config_teclas = carregar_config_teclas()

    pygame.quit()

def render_com_contorno(tela, texto, fonte, x, y, cor_texto, cor_contorno):
    """Renderiza texto com contorno."""
    render = fonte.render(texto, True, cor_contorno)
    deslocamento = 2  # Tamanho do contorno

    # Renderiza o contorno ao redor do texto
    for dx, dy in [(-deslocamento, 0), (deslocamento, 0), (0, -deslocamento), (0, deslocamento),
                   (-deslocamento, -deslocamento), (-deslocamento, deslocamento),
                   (deslocamento, -deslocamento), (deslocamento, deslocamento)]:
        tela.blit(render, (x + dx, y + dy))

    # Renderiza o texto principal por cima
    render_principal = fonte.render(texto, True, cor_texto)
    tela.blit(render_principal, (x, y))

def salvar_config_teclas(config_teclas):
    with open("config_teclas.json", "w") as arquivo:
        json.dump(config_teclas, arquivo)

def carregar_config_teclas():
    try:
        with open("config_teclas.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {
            "Mover para cima": pygame.K_w,
            "Mover para baixo": pygame.K_s,
            "Mover para esquerda": pygame.K_a,
            "Mover para direita": pygame.K_d,
            "Teleporte": pygame.K_LSHIFT,
            "Comprar na loja": pygame.K_e,
        }

if __name__ == "__main__":
    config_teclas = carregar_config_teclas()
    largura_tela, altura_tela = 800, 600  # Ajuste conforme necessário
    tela_de_controles(config_teclas, largura_tela, altura_tela)
