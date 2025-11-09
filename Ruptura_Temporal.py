
#Este projeto está licenciado sob a Creative Commons Attribution-NonCommercial-ShareAlike 4.0.
#Uso comercial é estritamente proibido. Modificações e redistribuições são permitidas sob as mesmas condições.


import pygame
import sys
import importlib
import subprocess
import os
import json
import uuid
import pyperclip
from Config_Teclas import tela_de_controles,carregar_config_teclas
from Variaveis import largura_tela, altura_tela, python
from rede import descobrir_host_udp, conectar_ao_host


pygame.init()
pygame.mouse.set_visible(False)
centro_tela = (largura_tela // 2, altura_tela // 2)  # Define o centro da tela
pygame.mouse.set_pos(centro_tela)
caminho_fonte_letras = "Texto/Broken.otf"
tamanho_fonte_letras = 20
caminho_fonte_letra1 = "Texto/World.otf"

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Menu do Jogo")

fundo_menu1 = pygame.image.load("Sprites/Melhoria_1.png")
fundo_menu2 = pygame.image.load("Sprites/Melhoria_2.png")
fundo_menu3 = pygame.image.load("Sprites/Melhoria_3.png")
fundo_menu4 = pygame.image.load("Sprites/Melhoria_4.png")
fundo_menu5 = pygame.image.load("Sprites/Melhoria_5.png")

fundo_menu1 = pygame.transform.scale(fundo_menu1, (largura_tela, altura_tela))
fundo_menu2 = pygame.transform.scale(fundo_menu2, (largura_tela, altura_tela))
fundo_menu3 = pygame.transform.scale(fundo_menu3, (largura_tela, altura_tela))
fundo_menu4 = pygame.transform.scale(fundo_menu4, (largura_tela, altura_tela))
fundo_menu5 = pygame.transform.scale(fundo_menu5, (largura_tela, altura_tela))

imagens_fundo = [fundo_menu1, fundo_menu4, fundo_menu2, fundo_menu4, fundo_menu5, fundo_menu3, fundo_menu2, fundo_menu3,
                 fundo_menu4, fundo_menu5, fundo_menu3, fundo_menu2, fundo_menu5]




# Configuração de troca de fundo
tempo_exibicao_fundo1 = 5000  # 5 segundos para exibir fundo_menu1
tempo_troca_fundo = 150      # 1 segundo para cada imagem na sequência
indice_fundo = 0
exibindo_fundo1 = True        # Controla se estamos no fundo_menu1
ultima_troca = pygame.time.get_ticks()

cor_letra = (40, 10, 88)
branco = (255, 255, 255)
cor_fundo_botao = (255, 255, 255, 100)
# --- Adicionar contorno ao título ---
contorno_rosa = (255, 105, 180)  # Rosa não muito vibrante

Letras_Of = caminho_fonte_letras

caminho_fonte_titulo = "Texto/Top_Menu.otf"
tamanho_fonte_titulo = 72
fonte_titulo = pygame.font.Font(caminho_fonte_titulo, tamanho_fonte_titulo)
# --- Ajustar o tamanho da fonte de "COOP" ---
ajuste_tamanho_fonte = int(tamanho_fonte_titulo * 0.80)   # 80% menor, pode ajustar o fator
porcentagem_vertical = 0.12  # Ajuste de 5% da altura da tela, pode modificar o valor
ajuste_vertical = int(altura_tela * porcentagem_vertical)  # Posição vertical com base na altura
fonte_coop = pygame.font.Font(caminho_fonte_titulo, ajuste_tamanho_fonte)
titulo_jogo = "Ruptura Temporal"
posicao_titulo = (largura_tela // 2, altura_tela // 8)

# Adicionando a nova opção de Configuração
opcoes = ["Iniciar Jornada", "Configuração", "Sair"]
indice_selecionado = 0

DELAY_ENTRE_OPCOES = 100
ultima_mudanca_de_opcao = pygame.time.get_ticks()

pygame.mixer.init()
pygame.mixer.music.load("Sounds/Menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    controle = pygame.joystick.Joystick(0)
    controle.init()
else:
    controle = None

if pygame.joystick.get_count() > 0:
    controle = pygame.joystick.Joystick(0)
    controle.init()
else:
    controle = None

# Variável para controlar movimento do analógico
analogo_movido = False


def tela_escolha_modo():
    import socket, pyperclip
    from rede import descobrir_host_udp
    pygame.init()
    largura, altura = largura_tela, altura_tela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Escolher Modo de Jogo")
    fonte = pygame.font.Font("Texto/World.otf", 36)
    clock = pygame.time.Clock()

    opcoes = ["Host Game", "Join Game", "Offline"]
    selecionado = 0
    
    while True:
        tela.fill((15, 15, 15))
        titulo = fonte.render("Selecione o modo de jogo", True, (255, 255, 255))
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 6))

        for i, texto in enumerate(opcoes):
            cor = (255, 255, 255) if i == selecionado else (120, 120, 120)
            render = fonte.render(texto, True, cor)
            tela.blit(render, (largura // 2 - render.get_width() // 2, altura // 3 + i * 70))

        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    escolha = opcoes[selecionado]
                    # -----------------------------
                    # MODO HOST
                    # -----------------------------
                    if escolha == "Host Game":
                        return "host", None

                    # -----------------------------
                    # MODO JOIN
                    # -----------------------------
                    elif escolha == "Join Game":
                        ip_encontrado = descobrir_host_udp(timeout=5)
                        if ip_encontrado:
                            return "join", ip_encontrado
                        else:
                            tela.fill((15, 15, 15))
                            msg = fonte.render("Nenhum host LAN encontrado.", True, (255, 80, 80))
                            tela.blit(msg, (largura // 2 - msg.get_width() // 2, altura // 2))
                            pygame.display.flip()
                            pygame.time.delay(3000)

                    # -----------------------------
                    # MODO OFFLINE
                    # -----------------------------
                    elif escolha == "Offline":
                        pygame.mixer.music.stop()

                        import GAME



def tela_selecao_aurea(tela, fonte):
    aureas = [
        {"nome": "Racional", "imagem": "Sprites/aurea_cientista.png", "ativa": True},
        {"nome": "Impulsiva", "imagem": "Sprites/aurea_impulsiva.png", "ativa": True},
        {"nome": "Devota", "imagem": "Sprites/aurea_devota.png", "ativa": True},
        {"nome": "Vanguarda", "imagem": "Sprites/aurea_vanguarda.png", "ativa": True},
        {"nome": "?", "imagem": "Sprites/aurea_misteriosa.png", "ativa": False}
    ]

    # 🔹 Carrega os níveis salvos (ou usa 0 se o arquivo não existir)
    try:
        with open("aureas_upgrade.json", "r") as f:
            data = json.load(f)
            upgrades = data.get("upgrades", {})
    except:
        upgrades = {}

    selecionado = 0
    clock = pygame.time.Clock()
    largura, altura = tela.get_size()

    largura_quadro = 120
    altura_quadro = 140
    espacamento = 50
    colunas = 3
    # --- Adicionar mensagem de instrução no canto inferior direito ---
    fonte_instrucao = pygame.font.Font(caminho_fonte_letras, 18)  # Use o mesmo estilo de fonte
    texto_instrucao = "A para esquerda e D para direita, espaço ou enter para selecionar"
    render_instrucao = fonte_instrucao.render(texto_instrucao, True, (0, 0, 0))  # Texto preto
    while True:
        tela.fill((15, 15, 15))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    selecionado = (selecionado + 1) % len(aureas)
                    while not aureas[selecionado]["ativa"]:
                        selecionado = (selecionado + 1) % len(aureas)
                elif evento.key in [pygame.K_LEFT, pygame.K_a]:
                    selecionado = (selecionado - 1) % len(aureas)
                    while not aureas[selecionado]["ativa"]:
                        selecionado = (selecionado - 1) % len(aureas)
                elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if aureas[selecionado]["ativa"]:
                        with open("aurea_selecionada.json", "w") as file:
                            json.dump({"aurea": aureas[selecionado]["nome"]}, file)
                        return

        for i, aurea in enumerate(aureas):
            linha = i // colunas
            coluna = i % colunas

            x = largura // 2 - ((colunas * largura_quadro + (colunas - 1) * espacamento) // 2) + coluna * (largura_quadro + espacamento)
            y = altura // 4 + linha * (altura_quadro + 30)

            cor_borda = (255, 255, 255) if i == selecionado else (80, 80, 80)
            pygame.draw.rect(tela, cor_borda, (x, y, largura_quadro, altura_quadro), 3)

            cor_texto = cor_borda

            # 🔹 Nome com nível, se aplicável
            nome = aurea["nome"]
            if nome != "?" and aurea["ativa"]:
                nivel = upgrades.get(nome, 0)
                nome_display = f"{nome} (Nv. {nivel})" if nivel > 0 else nome
            else:
                nome_display = nome

            texto = fonte.render(nome_display, True, cor_texto)
            tela.blit(texto, (x + largura_quadro // 2 - texto.get_width() // 2, y - 25))

            try:
                imagem = pygame.image.load(aurea["imagem"]).convert_alpha()
                imagem = pygame.transform.scale(imagem, (largura_quadro, altura_quadro))
                tela.blit(imagem, (x, y))
            except:
                pass
        # Cria contorno branco desenhando o texto levemente deslocado em várias direções
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            contorno = fonte_instrucao.render(texto_instrucao, True, (255, 255, 255))  # Contorno branco
            tela.blit(contorno, (largura - render_instrucao.get_width() - 20 + dx,
                                altura - render_instrucao.get_height() - 20 + dy))

        # Renderiza o texto principal (preto)
        tela.blit(render_instrucao, (largura - render_instrucao.get_width() - 20,
                                    altura - render_instrucao.get_height() - 20))        
        pygame.display.flip()
        clock.tick(60)

def tela_decisao_tutorial(tela, fonte):
    opcoes = ["Sim", "Não"]
    selecionado = 0
    clock = pygame.time.Clock()

    while True:
        tela.fill((10, 10, 10))
        texto_titulo = fonte.render("Deseja jogar o tutorial?", True, (255, 255, 255))
        tela.blit(texto_titulo, (largura_tela // 2 - texto_titulo.get_width() // 2, altura_tela // 4))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_LEFT, pygame.K_a]:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key in [pygame.K_RIGHT, pygame.K_d]:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    with open("tutorial_config.json", "w") as file:
                        json.dump({"mostrar_tutorial": opcoes[selecionado] == "Sim"}, file)
                    return opcoes[selecionado] == "Sim"

        for i, texto in enumerate(opcoes):
            cor = (255, 255, 255) if i == selecionado else (120, 120, 120)
            render = fonte.render(texto, True, cor)
            tela.blit(render, (largura_tela // 2 - 100 + i * 150, altura_tela // 2))

        pygame.display.flip()
        clock.tick(60)


while True:  # Loop principal do menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and pygame.time.get_ticks() - ultima_mudanca_de_opcao >= DELAY_ENTRE_OPCOES:
                indice_selecionado = (indice_selecionado - 1) % len(opcoes)
                ultima_mudanca_de_opcao = pygame.time.get_ticks()
            elif event.key == pygame.K_s and pygame.time.get_ticks() - ultima_mudanca_de_opcao >= DELAY_ENTRE_OPCOES:
                indice_selecionado = (indice_selecionado + 1) % len(opcoes)
                ultima_mudanca_de_opcao = pygame.time.get_ticks()
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if indice_selecionado == 0:
                    if not os.path.exists("tutorial_config.json"):
                        mostrar_tutorial = tela_decisao_tutorial(tela, fonte)
                        with open("tutorial_config.json", "w") as f:
                            json.dump({"mostrar_tutorial": mostrar_tutorial}, f)
                    else:
                        with open("tutorial_config.json", "r") as f:
                            mostrar_tutorial = json.load(f)["mostrar_tutorial"]

                    tela_selecao_aurea(tela, fonte)
                    modo, ip = tela_escolha_modo()  # Chama a função de escolha do modo local
                    

                    pygame.mixer.music.stop()

                    # Salvar o modo e IP escolhidos para o GAME-rede usar
                    with open("modo_jogo.json", "w") as f:
                        json.dump({"modo": modo, "ip": ip}, f)

                    import GAMERE




                elif indice_selecionado == 1:  # Configuração de Controles
                    config_teclas = carregar_config_teclas()
                    tela_de_controles(config_teclas, largura_tela, altura_tela)
                elif indice_selecionado == 2:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        elif event.type == pygame.JOYAXISMOTION:
            # Verifica o eixo Y do analógico esquerdo e garante que o eixo X não tenha desvio significativo
            if event.axis == 1 and abs(controle.get_axis(0)) < 0.2:  # Garante que o eixo X está parado
                if not analogo_movido:
                    if event.value > 0.5:
                        indice_selecionado = (indice_selecionado + 1) % len(opcoes)
                        analogo_movido = True
                    elif event.value < -0.5:
                        indice_selecionado = (indice_selecionado - 1) % len(opcoes)
                        analogo_movido = True
            elif event.axis == 1 and abs(event.value) < 0.5:
                analogo_movido = False

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # Botão A no controle Xbox
                if indice_selecionado == 0:
                    pygame.mixer.music.stop()
                    import GAMERE
                elif indice_selecionado == 1:  # Configuração de Controles
                    tela_de_controles()
                elif indice_selecionado == 2:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

    # Lógica de troca de imagem de fundo
    agora = pygame.time.get_ticks()
    
    if exibindo_fundo1:
        # Exibe fundo_menu1 por 5 segundos
        tela.blit(fundo_menu1, (0, 0))
        if agora - ultima_troca > tempo_exibicao_fundo1:
            exibindo_fundo1 = False
            ultima_troca = agora
            indice_fundo = 0  # Reinicia o índice para a sequência
    else:
        # Exibe a sequência de imagens
        tela.blit(imagens_fundo[indice_fundo], (0, 0))
        if agora - ultima_troca > tempo_troca_fundo:
            indice_fundo += 1
            ultima_troca = agora
            
            # Verifica se terminou a sequência para voltar ao fundo_menu1
            if indice_fundo >= len(imagens_fundo):
                exibindo_fundo1 = True
                indice_fundo = 0

    # Código restante para renderizar opções, título e atualizar a tela
    for i, opcao in enumerate(opcoes):
        Letras_Of = caminho_fonte_letra1 if i == indice_selecionado else caminho_fonte_letras

        fonte = pygame.font.Font(Letras_Of, tamanho_fonte_letras)

        retangulo_botao = pygame.Rect(largura_tela // 10 - 100, altura_tela // 2 + i * 60, 300, 20)

        superficie_transparente = pygame.Surface((300, 25), pygame.SRCALPHA)
        superficie_transparente.fill(cor_fundo_botao)
        tela.blit(superficie_transparente, (retangulo_botao.left, retangulo_botao.top))

        if i == indice_selecionado:
            posicao_x_botao = largura_tela // 10 - 100
            posicao_y_botao = altura_tela // 2 + i * 60
            altura_botao = 40

            seta_esquerda_inicio = (posicao_x_botao - 30, posicao_y_botao + altura_botao // 2)
            seta_esquerda_fim = (posicao_x_botao - 10, posicao_y_botao + altura_botao // 2)
            seta_direita_inicio = (posicao_x_botao + 330, posicao_y_botao + altura_botao // 2)
            seta_direita_fim = (posicao_x_botao + 310, posicao_y_botao + altura_botao // 2)

            pygame.draw.line(tela, branco, seta_esquerda_inicio, seta_esquerda_fim, 5)
            pygame.draw.line(tela, branco, seta_direita_inicio, seta_direita_fim, 5)

        texto_botao = fonte.render(opcao, True, cor_letra)
        retangulo_texto = texto_botao.get_rect(center=retangulo_botao.center)
        tela.blit(texto_botao, retangulo_texto)
    
    # --- Texto de instrução ---
    fonte_instrucao = pygame.font.Font(caminho_fonte_letras, 18)
    texto_instrucao = "Use W ou S para alternar e Espaço ou Enter para selecionar"
    render_instrucao = fonte_instrucao.render(texto_instrucao, True, (0, 0, 0))  # texto preto
    # --- Adicionar "COOP" no canto inferior direito ---
    # Carregar a fonte com o tamanho ajustado
    texto_coop = "COOP"
    cor_texto_coop = (0, 255, 255)  # Azul esverdeado
    cor_borda_coop = (255, 255, 0)  # Borda amarela

    # Renderizar o texto e o contorno
    render_coop = fonte_coop.render(texto_coop, True, cor_texto_coop)
    render_coop_borda = fonte_coop.render(texto_coop, True, cor_borda_coop)

    # Posição
    posicao_coop = (largura_tela - render_coop.get_width() - 10, ajuste_vertical)
    texto_titulo = fonte_titulo.render(titulo_jogo, True, cor_letra)
    retangulo_titulo = texto_titulo.get_rect(center=posicao_titulo)
    # Desenho da borda (contorno)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        tela.blit(render_coop_borda, (posicao_coop[0] + dx, posicao_coop[1] + dy))

    
    # Cria contorno branco desenhando o texto levemente deslocado em várias direções
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        contorno = fonte_instrucao.render(texto_instrucao, True, (255, 255, 255))
        tela.blit(contorno, (largura_tela - render_instrucao.get_width() - 20 + dx,
                            altura_tela - render_instrucao.get_height() - 20 + dy))
    # Desenhar o contorno (rosa) ao redor do título
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        texto_titulo_contorno = fonte_titulo.render(titulo_jogo, True, contorno_rosa)
        tela.blit(texto_titulo_contorno, (retangulo_titulo.left + dx, retangulo_titulo.top + dy))
    # Renderiza o texto principal (preto)
    tela.blit(render_instrucao, (largura_tela - render_instrucao.get_width() - 20,
                                altura_tela - render_instrucao.get_height() - 20))

    # Desenho do texto
    
    
    tela.blit(texto_titulo, retangulo_titulo)
    tela.blit(render_coop, posicao_coop)

    pygame.display.flip()
