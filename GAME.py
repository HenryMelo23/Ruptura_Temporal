
import pygame
import subprocess
import sys
import random
import math
import time
import os
import sys
import json
from Tela_Cartas import tela_de_pausa
from Variaveis import *
from utils import *


pygame.init()

dano_inimigo=80
estalos = pygame.mixer.Sound("Sounds/Estalo.mp3")
estalos.set_volume(0.07) 

som_ataque_boss = pygame.mixer.Sound("Sounds/Hit_Boss1.mp3")
som_ataque_boss.set_volume(0.04) 

Hit_inimigo1 = pygame.mixer.Sound("Sounds/Inimigo1_hit.wav")
Hit_inimigo1.set_volume(0.04) 

Disparo_Geo = pygame.mixer.Sound("Sounds/Disparo_Geo.wav")
Disparo_Geo.set_volume(0.04) 

Musica_tema_Boss1 = pygame.mixer.Sound("Sounds/Fase1_Boss.mp3")
Musica_tema_Boss1.set_volume(0.06) 

Musica_tema_fases = pygame.mixer.Sound("Sounds/Fase_boas.mp3")
Musica_tema_fases.set_volume(0.06) 

Som_tema_fases = pygame.mixer.Sound("Sounds/Praia.wav")
Som_tema_fases.set_volume(0.10) 

Som_portal = pygame.mixer.Sound("Sounds/Portal.mp3")
Som_portal.set_volume(0.06) 

Dano_person = pygame.mixer.Sound("Sounds/hit_person.mp3")
Dano_person.set_volume(0.1)  

toque=0
comando_direção_petro=True
musica_boss1= 1
tempo_ultimo_ataque = 0 
apertou_q=False

# Variáveis para rastrear o texto de dano
texto_dano = None
tempo_texto_dano = 0
centro_x_tela_pequena = largura_mapa // 2
centro_y_tela_pequena = altura_mapa // 2

mensagem_mostrada = True  # Variável para controlar se a mensagem já foi mostrada ou não
tempo_mostrando_mensagem = 0  
mensagem = "Tecla R PARA CHAMAR O REI"
imune_tempo_restante = 0  # Tempo restante de imunidade (em milissegundos)
teleportado = False  # Controle de teleporte

direcao_atual_petro="left_petro"
carregar_atributos_na_fase=True
nivel_ameaca = inimigos_eliminados // 10
fonte_mensagem = pygame.font.Font(None, 48)  # Tamanho da fonte
mensagens_exibidas = set()
mensagem_ativa = None
tempo_fim_mensagem = 0

mensagens_iniciais = [
    (3, "Use W, A, S e D para se mover"),
    (7, "Clique no botão esquerdo do mouse para atacar"),
    (11, "Use SHIFT para dar dash"),
    (15, "Aperte Q para abrir a loja"),
    (19, "Junte pontos e melhore o personagem"),
    (23, "Você está sozinho. Mas está preparado."),
    
]



def gerar_posicao_aleatoria(largura_mapa, altura_mapa, largura_personagem, altura_personagem):
    largura_mapa_int, altura_mapa_int, largura_personagem_int, altura_personagem_int=map(int,(largura_mapa, altura_mapa, largura_personagem, altura_personagem))
    x = random.randint(0, largura_mapa_int - largura_personagem_int)
    y = random.randint(0, altura_mapa_int - altura_personagem_int)
    return x, y


def limpar_salvamento():
    if os.path.exists('atributos.json'):
        os.remove('atributos.json')

def salvar_atributos():
    atributos = {
        "velocidade_personagem": velocidade_personagem,
        "intervalo_disparo": intervalo_disparo,
        "dano_person_hit": dano_person_hit,
        "chance_critico": chance_critico,
        "roubo_de_vida": roubo_de_vida,
        "quantidade_roubo_vida": quantidade_roubo_vida,
        "vida_petro": vida_petro,
        "vida_maxima_personagem":vida_maxima,
        "vida_maxima_petro":vida_maxima_petro,
        "vida_atual_personagem":vida,
        "nivel_Petro":xp_petro,
        "existencia_petro":Petro_active,
        "existencia_trembo":trembo,
        "dano_petro":dano_petro,
        "resistencia_personagem":Resistencia,
        "resistencia_petro":Resistencia_petro,
        "dano_inimigo_longe":dano_inimigo_longe,
        "dano_inimigo_perto":dano_inimigo_perto,
        "Poison_Active":Poison_Active,
        "Ultimo_Estalo":Ultimo_Estalo,
        "Executa_inimigo":Executa_inimigo,
        "Mercenaria_Active": Mercenaria_Active,
        "Valor_Bonus": Valor_Bonus,
        "tempo_cooldown_dash": tempo_cooldown_dash,
        "petro_evolucao":petro_evolucao,
        "Dano_Veneno_Acumulado":Dano_Veneno_Acumulado,
        "Tempo_cura":Tempo_cura,
        "porcentagem_cura":porcentagem_cura,
    }
    with open('atributos.json', 'w') as file:
        json.dump(atributos, file)

def carregar_atributos():
    global velocidade_personagem, intervalo_disparo, dano_person_hit, chance_critico, roubo_de_vida, quantidade_roubo_vida,vida_maxima,vida_maxima_petro,vida,xp_petro,Petro_active,trembo,dano_petro,Resistencia,Resistencia_petro,dano_inimigo_longe,dano_inimigo_perto,direcao_atual,Poison_Active,Ultimo_Estalo,Executa_inimigo,Valor_Bonus,Mercenaria_Active,tempo_cooldown_dash,vida_petro,petro_evolucao,Dano_Veneno_Acumulado, Tempo_cura,porcentagem_cura
    with open('atributos.json', 'r') as file:
        atributos = json.load(file)
        velocidade_personagem = atributos["velocidade_personagem"]
        intervalo_disparo = atributos["intervalo_disparo"]
        dano_person_hit = atributos["dano_person_hit"]
        chance_critico = atributos["chance_critico"]
        roubo_de_vida = atributos["roubo_de_vida"]
        quantidade_roubo_vida = atributos["quantidade_roubo_vida"]
        vida_petro= atributos["vida_petro"]
        vida_maxima=atributos["vida_maxima_personagem"]
        vida_maxima_petro=atributos["vida_maxima_petro"]
        vida=atributos["vida_atual_personagem"]
        xp_petro=atributos["nivel_Petro"]
        Petro_active=atributos["existencia_petro"]
        trembo=atributos["existencia_trembo"]
        dano_petro=atributos["dano_petro"]
        Resistencia=atributos["resistencia_personagem"]
        Resistencia_petro=atributos["resistencia_petro"]
        dano_inimigo_longe=atributos["dano_inimigo_longe"]
        dano_inimigo_perto=atributos["dano_inimigo_perto"]
        Poison_Active=atributos["Poison_Active"]
        Ultimo_Estalo=atributos["Ultimo_Estalo"]
        Executa_inimigo=atributos["Executa_inimigo"]
        Mercenaria_Active=atributos["Mercenaria_Active"]
        Valor_Bonus=atributos["Valor_Bonus"]
        tempo_cooldown_dash=atributos["tempo_cooldown_dash"]
        petro_evolucao= atributos["petro_evolucao"]
        Dano_Veneno_Acumulado= atributos["Dano_Veneno_Acumulado"]
        Tempo_cura= atributos["Tempo_cura"]
        porcentagem_cura= atributos["porcentagem_cura"]
        
with open("aurea_selecionada.json", "r") as file:
    aurea = json.load(file)["aurea"]

with open("tutorial_config.json", "r") as f:
    mostrar_tutorial = json.load(f).get("mostrar_tutorial", True)

upgrade_aureas = carregar_upgrade_aureas("aureas_upgrade.json")

        
tempo_inicial = time.time() 

tempo_anterior = pygame.time.get_ticks()
tempo_movimento = random.randint(2000, 7000)
tempo_parado = random.randint(500, 700) 
movendo = True 
boss_vivo1=False
relogio = pygame.time.Clock()
ultimo_tempo_reducao = time.time()
largura_disparo, altura_disparo = 40, 40
velocidade_disparo = 10
disparos = []

tela = pygame.display.set_mode((largura_mapa, altura_mapa))
pygame.display.set_caption("Renderizando Mapa com Personagem")

pontuacao_inimigos=0
maxima_pontuacao_magia = 750
piscar_magia = False





#INIMIGOS

tempo_ultimo_inimigo_apos_morte = pygame.time.get_ticks()
# Carregar a imagem do mapa
mapa = pygame.image.load(mapa_path1).convert()
mapa = pygame.transform.scale(mapa, (largura_mapa, altura_mapa))
# Carregar as sequências de imagens do personagem

# Configurações do loop principal
relogio = pygame.time.Clock()
tempo_passado = 0
frame_atual = 0
frame_atual_disparo = 0
# Atualizar a última direção da personagem
ultima_tecla_movimento = None
movimento_pressionado = False
#as seguintes variáveis para controle do tempo de hit do inimigo
tempo_ultimo_hit_inimigo = pygame.time.get_ticks()

piscando_vida = False
vida_inimigo_maxima=30
vida_inimigo= vida_inimigo_maxima





def determinar_frames_petro(posicao_petro, posicao_inimigo):
    if posicao_petro[0] < posicao_inimigo[0]:  # Petro está à esquerda do inimigo
        return 'right_petro'
    elif posicao_petro[0] > posicao_inimigo[0]:  # Petro está à direita do inimigo
        return 'left_petro'
    elif posicao_petro[1] < posicao_inimigo[1]:  # Petro está acima do inimigo
        return 'down_petro'
    elif posicao_petro[1] > posicao_inimigo[1]:  # Petro está abaixo do inimigo
        return 'up_petro'
    else:
        return 'stop_petro'  # Petro está na mesma posição do inimigo





def atualizar_posicao_personagem(keys, joystick):
    global pos_x_personagem, pos_y_personagem, direcao_atual, ultima_tecla_movimento
    global movimento_pressionado, cooldown_dash, distancia_dash, tempo_ultimo_dash, teleporte_timer, teleporte_duration, teleporte_index

    direcao_atual = 'stop'  # Por padrão, definimos a direção como 'stop'

    if  keys[config_teclas["Teleporte"]] and not cooldown_dash:
        # Animação de teletransporte
        Som_portal.play()
        teleporte_timer += velocidade_personagem
        if teleporte_timer >= teleporte_duration:
            teleporte_index = (teleporte_index + 1) % len(teleporte_sprites)
            teleporte_timer = 0

        # Desenhe a sprite de teletransporte
        tela.blit(teleporte_sprites[teleporte_index], (pos_x_personagem, pos_y_personagem))

        # Atualize a tela
        pygame.display.flip()
        pygame.time.delay(teleporte_duration // 2)  # Tempo de espera entre cada quadro (metade da duração)

        # Continue com o código do dash como antes
        if ultima_tecla_movimento == 'up':
            pos_y_personagem = max(0, pos_y_personagem - distancia_dash)
        elif ultima_tecla_movimento == 'down':
            pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + distancia_dash)
        elif ultima_tecla_movimento == 'left':
            pos_x_personagem = max(0, pos_x_personagem - distancia_dash)
        elif ultima_tecla_movimento == 'right':
            pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + distancia_dash)

        # Inicie o cooldown do dash
        cooldown_dash = True
        tempo_ultimo_dash = pygame.time.get_ticks()

    elif keys[config_teclas["Mover para direita"]]:
        pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + velocidade_personagem)
        direcao_atual = 'right'
        ultima_tecla_movimento = 'right'
        movimento_pressionado = True
    elif keys[config_teclas["Mover para cima"]]:
        pos_y_personagem = max(0, pos_y_personagem - velocidade_personagem)
        direcao_atual = 'up'
        ultima_tecla_movimento = 'up'
        movimento_pressionado = True
    elif keys[config_teclas["Mover para baixo"]]:
        pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + velocidade_personagem)
        direcao_atual = 'down'
        ultima_tecla_movimento = 'down'
        movimento_pressionado = True
    elif keys[config_teclas["Mover para esquerda"]]:
        pos_x_personagem = max(0, pos_x_personagem - velocidade_personagem)
        direcao_atual = 'left'
        ultima_tecla_movimento = 'left'
        movimento_pressionado = True

    elif botao_mouse[0]:
        
        direcao_atual = 'disp'


    else:
        direcao_atual = 'stop'

    # Atualização do cooldown do dash
    if cooldown_dash and pygame.time.get_ticks() - tempo_ultimo_dash > tempo_cooldown_dash:
        cooldown_dash = False
    

    # Verificar movimento do joystick
    if joystick:
        joystick_x = joystick.get_axis(0)  # Eixo horizontal
        joystick_y = joystick.get_axis(1)  # Eixo vertical

        # Calcular magnitude do analógico
        magnitude = math.sqrt(joystick_x**2 + joystick_y**2)
        if magnitude > 0.2:  # Deadzone para ignorar pequenos desvios
            # Calcular ângulo em graus
            angle = math.degrees(math.atan2(-joystick_y, joystick_x)) % 360

            # Determinar direção baseada no ângulo
            if 45 <= angle < 135:  # Cima
                pos_y_personagem = max(0, pos_y_personagem - velocidade_personagem)
                direcao_atual = 'up'
                ultima_tecla_movimento = 'up'
                movimento_pressionado = True
            elif 135 <= angle < 225:  # Esquerda
                pos_x_personagem = max(0, pos_x_personagem - velocidade_personagem)
                direcao_atual = 'left'
                ultima_tecla_movimento = 'left'
                movimento_pressionado = True
            elif 225 <= angle < 315:  # Baixo
                pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + velocidade_personagem)
                direcao_atual = 'down'
                ultima_tecla_movimento = 'down'
                movimento_pressionado = True
            else:  # Direita
                pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + velocidade_personagem)
                direcao_atual = 'right'
                ultima_tecla_movimento = 'right'
                movimento_pressionado = True

    # Verificar botões do joystick para teletransporte
    if joystick and joystick.get_button(2) and not cooldown_dash:
        # Animação de teletransporte
        Som_portal.play()
        teleporte_timer += velocidade_personagem
        if teleporte_timer >= teleporte_duration:
            teleporte_index = (teleporte_index + 1) % len(teleporte_sprites)
            teleporte_timer = 0

        # Desenhar a sprite de teletransporte
        tela.blit(teleporte_sprites[teleporte_index], (pos_x_personagem, pos_y_personagem))

        # Atualizar a tela
        pygame.display.flip()
        pygame.time.delay(teleporte_duration // 2)  # Tempo de espera entre cada quadro (metade da duração)

        # Continuar com o código do dash como antes
        if ultima_tecla_movimento == 'up':
            pos_y_personagem = max(0, pos_y_personagem - distancia_dash)
        elif ultima_tecla_movimento == 'down':
            pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + distancia_dash)
        elif ultima_tecla_movimento == 'left':
            pos_x_personagem = max(0, pos_x_personagem - distancia_dash)
        elif ultima_tecla_movimento == 'right':
            pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + distancia_dash)

        # Iniciar o cooldown do dash
        cooldown_dash = True
        tempo_ultimo_dash = pygame.time.get_ticks()

    # Atualizar o cooldown do dash
    if cooldown_dash and pygame.time.get_ticks() - tempo_ultimo_dash > tempo_cooldown_dash:
        cooldown_dash = False
    
    return direcao_atual

inimigos_comum = []



def criar_inimigo(x, y, tipo=1):
    if tipo == 1:
        image = pygame.transform.scale(pygame.image.load("Sprites/inimig1.png"), (largura_inimigo, altura_inimigo))
    # Ajustar a hitbox para ser menor que a imagem original
    largura_hitbox = int(largura_inimigo * 0.8)  # Reduz a largura da hitbox
    altura_hitbox = int(altura_inimigo * 0.5)    # Reduz a altura da hitbox
    offset_x = (largura_inimigo - largura_hitbox) // 2  # Centraliza a hitbox horizontalmente
    offset_y = (altura_inimigo - altura_hitbox) // 2    # Centraliza a hitbox verticalmente

    rect = pygame.Rect(x + offset_x, y + offset_y, largura_hitbox, altura_hitbox)
    
    return {"rect": rect, "image": image, "tipo": tipo, "vida": vida_inimigo_maxima, "vida_maxima": vida_inimigo_maxima}


def gerar_inimigo():
    global inimigos_comum
    
    if len(inimigos_comum) < max_inimigos:
        # Escolhe aleatoriamente uma borda para gerar o inimigo
        
        borda = random.choice(['esquerda', 'direita', 'superior', 'inferior'])
        if borda == 'esquerda':
            novo_inimigo = criar_inimigo(0, random.randint(0, int(altura_mapa) - int(altura_inimigo)))
        elif borda == 'direita':
            novo_inimigo = criar_inimigo(int(largura_mapa) - int(largura_inimigo), random.randint(0, int(altura_mapa) - int(altura_inimigo)))
        elif borda == 'superior':
            novo_inimigo = criar_inimigo(random.randint(0, int(largura_mapa) - int(largura_inimigo)), 0)
        elif borda == 'inferior':
            novo_inimigo = criar_inimigo(random.randint(0, int(largura_mapa) - int(largura_inimigo)), int(altura_mapa) - int(altura_inimigo))

        # Verifica se o novo inimigo está muito próximo de algum inimigo existente
        distancia_minima_alcancada = any(
            math.sqrt((novo_inimigo["rect"].x - inimigo["rect"].x) ** 2 + (novo_inimigo["rect"].y - inimigo["rect"].y) ** 2) < distancia_minima_inimigos
            for inimigo in inimigos_comum
        )

        # Ajusta a posição do novo inimigo se estiver muito próximo
        while distancia_minima_alcancada:
            borda = random.choice(['esquerda', 'direita', 'superior', 'inferior'])
            if borda == 'esquerda':
                novo_inimigo = criar_inimigo(0, random.randint(0, int(altura_mapa) - int(altura_inimigo)))
            elif borda == 'direita':
                novo_inimigo = criar_inimigo(int(largura_mapa) - int(largura_inimigo), random.randint(0, int(altura_mapa) - int(altura_inimigo)))
            elif borda == 'superior':
                novo_inimigo = criar_inimigo(random.randint(0, int(largura_mapa) - int(largura_inimigo)), 0)
            elif borda == 'inferior':
                novo_inimigo = criar_inimigo(random.randint(0, int(largura_mapa) - int(largura_inimigo)), int(altura_mapa) - int(altura_inimigo))

            distancia_minima_alcancada = any(
                math.sqrt((novo_inimigo["rect"].x - inimigo["rect"].x) ** 2 + (novo_inimigo["rect"].y - inimigo["rect"].y) ** 2) < distancia_minima_inimigos
                for inimigo in inimigos_comum
            )

        inimigos_comum.append(novo_inimigo)
        

def calcular_direcao_para_inimigo(personagem, inimigos):
    # Inicialize a distância mínima como infinito e o inimigo mais próximo como None
    distancia_minima = float('inf')
    inimigo_mais_proximo = None

    # Calcule a distância para cada inimigo e encontre o inimigo mais próximo
    for inimigo in inimigos:
        distancia = math.sqrt((inimigo["rect"].x - personagem["rect"].x) ** 2 + (inimigo["rect"].y - personagem["rect"].y) ** 2)
        if distancia < distancia_minima:
            distancia_minima = distancia
            inimigo_mais_proximo = inimigo

    # Se encontrou um inimigo próximo, calcule a direção para ele
    if inimigo_mais_proximo:
        dx = inimigo_mais_proximo["rect"].x - personagem["rect"].x
        dy = inimigo_mais_proximo["rect"].y - personagem["rect"].y
        direcao_x = 1 if dx > 0 else -1
        direcao_y = 1 if dy > 0 else -1
        return (direcao_x, direcao_y)
    else:
        return (0, 0)  # Se não houver inimigos, retorne a direção neutra




def criar_disparo():
        return {"rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_disparo, altura_disparo),"direcao": ultima_tecla_movimento }

# Variável para armazenar o tempo do último inimigo adicionado
tempo_ultimo_inimigo = pygame.time.get_ticks()
quantidade_inimigos = 1

# Função para verificar a colisão entre o personagem e os projéteis inimigos
def verificar_colisao_personagem(projeteis):
    global pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem

    for proj in projeteis:
        pos_x_proj, pos_y_proj = proj["rect"].x, proj["rect"].y

        if (
            pos_x_personagem < pos_x_proj < pos_x_personagem + largura_personagem and
            pos_y_personagem < pos_y_proj < pos_y_personagem + altura_personagem
        ):
            return True  # Colisão detectada

    return False  # Sem colisão

def verificar_colisao_personagem_inimigo(personagem_rect, inimigos_rects):
    tempo_atual = pygame.time.get_ticks()
    for inimigo_rect in inimigos_rects:
        if personagem_rect.colliderect(inimigo_rect):
            return True  # Colisão detectada

    return False  # Sem colisão

def soltar_moeda(posicao):
    chance = 1  # 25%
    if random.random() < chance:
        tamanho_moeda = (36, 36)  # Novo tamanho desejado
        sprite_redimensionada = pygame.transform.scale(sprite_moeda, tamanho_moeda)
        rect = sprite_redimensionada.get_rect(center=posicao)
        moedas_soltadas.append({
            "rect": rect,
            "image": sprite_redimensionada
        })
        print(f"[🪙] Moeda criada em {rect.topleft}, tamanho: {tamanho_moeda}")

def tela_upgrade_aureas(tela, fonte, moedas_disponiveis):
    
    with open("aureas_upgrade.json", "r") as f:
        upgrades = json.load(f)
    aureas = [
        {"nome": "Racional", "imagem": "Sprites/aurea_cientista.png", "ativa": True},
        {"nome": "Impulsiva", "imagem": "Sprites/aurea_impulsiva.png", "ativa": True},
        {"nome": "Devota", "imagem": "Sprites/aurea_devota.png", "ativa": True},
        {"nome": "Vanguarda", "imagem": "Sprites/aurea_vanguarda.png", "ativa": True},
        {"nome": "?", "imagem": "Sprites/aurea_misteriosa.png", "ativa": False}
    ]
    for nome in ["Racional", "Impulsiva", "Devota", "Vanguarda"]:
        if nome not in upgrades:
            upgrades[nome] = 0

    upgrades = carregar_upgrade_aureas("aureas_upgrade.json")

    selecionado = 0
    clock = pygame.time.Clock()
    largura, altura = tela.get_size()

    largura_quadro = 120
    altura_quadro = 140
    espacamento = 50
    colunas = 3

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
                    nome = aureas[selecionado]["nome"]
                    if aureas[selecionado]["ativa"] and nome != "?":
                        if moedas_disponiveis > 0:
                            upgrades[nome] += 1
                            moedas_disponiveis -= 1
                            salvar_upgrade_aureas("aureas_upgrade.json", upgrades)
                            print(f"[⚙️] {nome} melhorada para nível {upgrades[nome]}")
                        else:
                            print("[⛔] Sem moedas suficientes.")
                elif evento.key == pygame.K_ESCAPE:
                    return

        for i, aurea in enumerate(aureas):
            linha = i // colunas
            coluna = i % colunas

            x = largura // 2 - ((colunas * largura_quadro + (colunas - 1) * espacamento) // 2) + coluna * (largura_quadro + espacamento)
            y = altura // 4 + linha * (altura_quadro + 30)

            cor_borda = (255, 255, 255) if i == selecionado else (80, 80, 80)
            pygame.draw.rect(tela, cor_borda, (x, y, largura_quadro, altura_quadro), 3)

            # Texto com nome
            cor_texto = cor_borda
            nome_display = aurea["nome"]
            if nome_display != "?" and upgrades.get(nome_display, 0) > 0:
                nome_display += f" (Nv. {upgrades[nome_display]})"

            texto = fonte.render(nome_display, True, cor_texto)
            tela.blit(texto, (x + largura_quadro // 2 - texto.get_width() // 2, y - 25))

            

            # Texto com nível
            if aurea["ativa"] and aurea["nome"] != "?":
                nivel = upgrades.get(aurea["nome"], 0)
                texto_nivel = fonte.render(f"Nível {nivel}", True, (200, 200, 100))
                tela.blit(texto_nivel, (x + largura_quadro // 2 - texto_nivel.get_width() // 2, y + altura_quadro + 5))

            # Imagem
            try:
                imagem = pygame.image.load(aurea["imagem"]).convert_alpha()
                imagem = pygame.transform.scale(imagem, (largura_quadro, altura_quadro))
                tela.blit(imagem, (x, y))
            except:
                pass

        # Mostrar moedas
        texto_moedas = fonte.render(f"Moedas: {moedas_disponiveis}", True, (255, 255, 100))
        tela.blit(texto_moedas, (50, 40))

        instrucoes = fonte.render("← → para navegar | ENTER para melhorar | ESC para sair", True, (150, 150, 150))
        tela.blit(instrucoes, (largura // 2 - instrucoes.get_width() // 2, altura - 60))

        pygame.display.flip()
        clock.tick(60)



tempo_parado_person = pygame.time.get_ticks()  
boss_atingido_por_onda = pygame.time.get_ticks()
tempo_ultimo_disparo = pygame.time.get_ticks()
tempo_ultimo_escudo = pygame.time.get_ticks()

Som_tema_fases.play(loops=-1)
Musica_tema_fases.play(loops=-1)

upgrades = carregar_upgrade_aureas("aureas_upgrade.json")

FPS=pygame.time.Clock()
pygame.mouse.set_visible(False)
cursor_imagem = pygame.image.load("Sprites/Ponteiro.png").convert_alpha()  # Ajuste o caminho
cursor_tamanho = cursor_imagem.get_size()

sprite_moeda = pygame.image.load("Sprites/moeda.png").convert_alpha()
moedas_soltadas = []

###################################################################################################PRINCIPAL#################################################################################################################
#LOOP PRINCIPAL
running = True
while running:
    if impulsiva_ativa:
        disparo_paths = ["Sprites/Fogo_impulso1.png", "Sprites/Fogo_impulso2.png"]
    else:
        disparo_paths = ["Sprites/Fogo1.png", "Sprites/Fogo2.png"]
    frames_disparo = [pygame.image.load(path) for path in disparo_paths]
    frames_disparo = [pygame.transform.scale(frame, (largura_disparo, altura_disparo)) for frame in frames_disparo]
    
    nivel_impulsiva = upgrades.get("Impulsiva", 0)
    if impulsiva_ativa:
        duracao_buff = 3000 + nivel_impulsiva * 500  # 3s base + 0.5s por nível
        if pygame.time.get_ticks() - tempo_inicio_buff_impulsiva >= duracao_buff:
            impulsiva_ativa = False
            tipo_buff_impulsiva = None
        else:
            if tipo_buff_impulsiva == "dano":
                multiplicador_dano = 1.3 + (0.05 * nivel_impulsiva)
            elif tipo_buff_impulsiva == "velocidade":
                multiplicador_velocidade = 1.2 + (0.05 * nivel_impulsiva)
        mensagem = "+ Buff: Dano ↑" if tipo_buff_impulsiva == "dano" else "+ Buff: Velocidade ↑"

        efeitos_texto.append({
            "texto": mensagem,
            "x": pos_x_personagem,
            "y": pos_y_personagem - 20,
            "tempo_inicio": pygame.time.get_ticks(),
            "cor": (255, 100, 100) if tipo_buff_impulsiva == "dano" else (100, 100, 255)
        })


    pos_mouse = pygame.mouse.get_pos()
    botao_mouse = pygame.mouse.get_pressed()
    mouse_x = max(0, min(pos_mouse[0], largura_mapa - cursor_tamanho[0]))
    mouse_y = max(0, min(pos_mouse[1], altura_mapa - cursor_tamanho[1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif botao_mouse[0] and tempo_atual - tempo_ultimo_disparo >= intervalo_disparo:  # Botão esquerdo do mouse
            pos_mouse = pygame.mouse.get_pos()
            angulo = calcular_angulo_disparo((pos_x_personagem, pos_y_personagem), pos_mouse)
            Disparo_Geo.play()
            # Crie o disparo com direção baseada no ângulo
            novo_disparo = {
                "rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_disparo, altura_disparo),
                "angulo": angulo
            }
            disparos.append(novo_disparo)
            tempo_ultimo_disparo = tempo_atual  # Atualizar o tempo do último disparo
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and tempo_atual - tempo_ultimo_uso_habilidade >= cooldown_habilidade:  # Botão direito do mouse
            pos_mouse = pygame.mouse.get_pos()
            angulo = calcular_angulo_disparo((pos_x_personagem, pos_y_personagem), pos_mouse)
            
            # Criar uma onda cinética com as novas propriedades
            nova_onda = {
                "rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_onda, altura_onda),
                "angulo": angulo,
                "tempo_inicio": pygame.time.get_ticks(),
                "frame_atual": 0,
                "frames": frames_onda_cinetica  # Certifique-se de ter os frames para animação da onda
            }
            ondas.append(nova_onda)
            tempo_ultimo_uso_habilidade = tempo_atual
        
    # Verificar eventos de teclado
    keys = pygame.key.get_pressed()
    
    # Verificar eventos de joystick
    joystick_count = pygame.joystick.get_count()
    if joystick_count > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None

    # Chamar a função para atualizar a posição do personagem
    ultimo_x = pos_x_personagem
    ultimo_y = pos_y_personagem
    atualizar_posicao_personagem(keys,joystick)
    

    novos_inimigos = []
    novos_disparos = []
    inimig_atin=[]

    tempo_passado += relogio.get_rawtime()
    relogio.tick()

     # Adicionar inimigos a cada 10 segundos
    tempo_atual = pygame.time.get_ticks()
    if mostrar_tutorial:
        if tempo_atual > 23000 and apertou_q and tempo_atual - tempo_ultimo_inimigo >= 1000 and len(inimigos_comum) < max_inimigos and not boss_vivo1:
            gerar_inimigo()
            tempo_ultimo_inimigo = tempo_atual  # Atualizar o tempo do último inimigo adicionado
    else:
        if tempo_atual - tempo_ultimo_inimigo >= 1000 and len(inimigos_comum) < max_inimigos and not boss_vivo1:
            gerar_inimigo()
            tempo_ultimo_inimigo = tempo_atual  # Atualizar o tempo do último inimigo adicionado
    
    nivel_racional = upgrades.get("Racional", 0)
    #LUGAR AONDE COLOCAMOS AS AUREAS
    if aurea == "Racional":
        if pos_x_personagem == ultimo_x and pos_y_personagem == ultimo_y:
            if tempo_atual - tempo_parado_person >= 5000:
                ganho = 3 + nivel_racional  # ganho aumenta com o nível
                pontuacao += ganho
                pontuacao_exib += ganho
                tempo_parado_person = tempo_atual

                # Determina posição flutuante aleatória à direita ou esquerda do personagem
                lado = random.choice(["esquerda", "direita"])
                if lado == "esquerda":
                    x = pos_x_personagem - 20
                else:
                    x = pos_x_personagem + largura_personagem + 5

                y = pos_y_personagem - 10  # ligeiramente acima

                # Adiciona efeito à lista
                efeitos_texto.append({
                    "texto": f"+{ganho}",
                    "x": x,
                    "y": y,
                    "tempo_inicio": tempo_atual,
                    "cor": (50, 255, 50)  # verde
                })
    if aurea == "Impulsiva":
        
        if eliminacoes_consecutivas_impulsiva >= 5 and not impulsiva_ativa:
            impulsiva_ativa = True
            tipo_buff_impulsiva = random.choice(["dano", "velocidade"])
            tempo_inicio_buff_impulsiva = pygame.time.get_ticks()
            eliminacoes_consecutivas_impulsiva = 0  # Zera para forçar novo ciclo
    


                
    if direcao_atual == 'stop':
        if tempo_passado >= tempo_animacao_stop:
            tempo_passado = 0
            frame_atual = (frame_atual + 1) % len(frames_animacao[direcao_atual])
    if direcao_atual != 'stop':
        if tempo_passado >= tempo_animacao_no_stop:
            tempo_passado = 0
            frame_atual = (frame_atual + 1) % len(frames_animacao[direcao_atual])


    tela.fill((255, 255, 255))
    tela.blit(mapa, (0, 0))

    

    
    # Desenhar os disparos normais
    novos_disparos = []
    for disparo in disparos:
        disparo["rect"].x += velocidade_disparo * math.cos(disparo["angulo"])
        disparo["rect"].y += velocidade_disparo * math.sin(disparo["angulo"])
        
        # Verificar se o disparo está dentro do mapa
        if 0 <= disparo["rect"].x < largura_mapa and 0 <= disparo["rect"].y < altura_mapa:
            novos_disparos.append(disparo)

    disparos = novos_disparos

    # Renderizar os disparos
    for disparo in disparos:
        tela.blit(frames_disparo[frame_atual_disparo], disparo["rect"].topleft)



    novas_ondas = []
    for onda in ondas:
        onda["rect"].x += velocidade_onda * math.cos(onda["angulo"])
        onda["rect"].y += velocidade_onda * math.sin(onda["angulo"])

        # Atualizar o frame atual da animação da onda
        tempo_decorrido_onda = pygame.time.get_ticks() - onda["tempo_inicio"]
        onda["frame_atual"] = (tempo_decorrido_onda // duracao_frame_onda) % len(onda["frames"])

        # Renderizar a onda
        tela.blit(onda["frames"][onda["frame_atual"]], onda["rect"])

        # Verificar se a onda ainda está dentro do mapa
        if (
            0 <= onda["rect"].x < largura_mapa and
            0 <= onda["rect"].y < altura_mapa
        ):
            novas_ondas.append(onda)
        
    ondas = novas_ondas

    for onda in ondas:
        for inimigo in inimigos_comum:
            inimigo_id = id(inimigo["rect"])  # Use o id do rect como identificador único
            if onda["rect"].colliderect(inimigo["rect"]) and \
            (inimigo_id not in inimigos_atingidos_por_onda or tempo_atual - inimigos_atingidos_por_onda[inimigo_id] >= 500):
                # Aplica o dano ao inimigo
                inimigo["vida"] -= dano_person_hit*2  
                inimigos_atingidos_por_onda[inimigo_id] = tempo_atual  # Atualiza o tempo do último dano

                # Verifica se o inimigo foi derrotado
                if inimigo["vida"] <= 0:
                    inimigos_comum.remove(inimigo)
                    # Progressão escalonada
                    vida_inimigo_maxima += 1.2 + nivel_ameaca * 0.8
                    Resistencia_petro += 0.2 + nivel_ameaca * 0.1
                    dano_inimigo_perto += 0.2 + nivel_ameaca * 0.1
                    dano_person_hit += 0.15 + nivel_ameaca * 0.05
                    vida_maxima_petro += 0.5 + nivel_ameaca * 0.3
                    dano_petro += 0.015 + nivel_ameaca * 0.01
                    dano_inimigo_longe += 0.04 + nivel_ameaca * 0.02
                    dano_boss += 0.025 + nivel_ameaca * 0.02
                    Dano_Boss_Habilit += 0.05 + nivel_ameaca * 0.03
                    Velocidade_Inimigos_1 += 0.0015 + nivel_ameaca * 0.0005

                    inimigos_eliminados += 1

                    # Pontuação escalada
                    ganho = int(75 + math.log2(inimigos_eliminados + 1) * 4)
                    pontuacao += ganho
                    pontuacao_exib += ganho

                    # Cura da Petro se estiver muito ferida
                    if vida_petro < (vida_maxima_petro * 0.6):
                        vida_petro += (vida_maxima_petro * 0.4)
                        if vida_petro > vida_maxima_petro:
                            vida_petro = vida_maxima_petro

                    # Boss: progressão escalada
                    if not boss_vivo1:
                        if vida_boss > 0:
                            vida_boss += 15 + nivel_ameaca * 10
                            vida_maxima_boss1 = vida_boss
                            vida_boss2 += 20 + nivel_ameaca * 12
                            vida_maxima_boss2 = vida_boss2
                            vida_boss3 += 25 + nivel_ameaca * 15
                            vida_maxima_boss3 = vida_boss3
                            vida_boss4 += 30 + nivel_ameaca * 18
                            vida_maxima_boss4 = vida_boss4
        


        # Controle de dano para o boss
        if boss_vivo1 and onda["rect"].colliderect(pygame.Rect(pos_x_chefe, pos_y_chefe, chefe_largura, chefe_altura)):
            boss_id = "boss"  # Identificador único para o boss no dicionário
            tempo_atual = pygame.time.get_ticks()

            if tempo_atual - boss_atingido_por_onda >= 500: 
                vida_boss -= dano_person_hit * 5  
                
                boss_atingido_por_onda = tempo_atual  # Atualiza o tempo do último dano

                # Verifica se o boss foi derrotado
                if vida_boss <= 0:
                    boss_vivo1 = False
                    vida_maxima_boss1 = 0
                    # Aplique os efeitos ou recompensas ao derrotar o boss aqui

    tempo_atual = pygame.time.get_ticks()
    if movendo:
        if tempo_atual - tempo_anterior >= tempo_movimento:
            # Atualize o tempo anterior para o tempo atual
            tempo_anterior = tempo_atual
            movendo = False
            tempo_movimento = random.randint(3000, 7000)
        # Atualizar movimento dos inimigos com previsão
        tempo_previsao = 5  # Tempo em quadros para prever o movimento
        atualizar_movimento_inimigos(
        inimigos_comum, pos_x_personagem, pos_y_personagem, ultima_tecla_movimento, velocidade_personagem, tempo_previsao
        )
    else:
        if tempo_atual - tempo_anterior >= tempo_parado:
            # Atualize o tempo anterior para o tempo atual
            tempo_anterior = tempo_atual
            movendo = True
            tempo_parado = random.randint(10, 3000)
            

    


    # Desenhe os inimigos na tela
    for inimigo in inimigos_comum:
        inimigo["image"] = frames_inimigo[frame_atual % len(frames_inimigo)]

        tela.blit(inimigo["image"], inimigo["rect"])
        desenhar_barra_de_vida(tela, inimigo["rect"].x, inimigo["rect"].y - 10, largura_inimigo, 5, inimigo["vida"], inimigo["vida_maxima"])
    
    personagem_rect = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem*0.5, altura_personagem*0.8)
    inimigos_rects = [inimigo["rect"] for inimigo in inimigos_comum]

    
    if imune_tempo_restante > 0:
        imune_tempo_restante -= relogio.get_time()  
    else:
        imune_tempo_restante = 0 

    
    if verificar_colisao_personagem_inimigo(personagem_rect, inimigos_rects) and imune_tempo_restante <= 0:

        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            Dano_pos_resistencia_person = int(((vida_maxima * 0.06)+dano_inimigo_perto) - Resistencia)
            if aurea == "Vanguarda":
                for inimigo in inimigos_comum:
                    if personagem_rect.colliderect(inimigo["rect"]):
                        id_inimigo = id(inimigo)
                        tempo_queimadura = pygame.time.get_ticks()
                        inimigos_em_chamas[id_inimigo] = tempo_queimadura
                       

            if escudo_devota_ativo:
                escudo_devota_ativo= False
                pass
            
            elif Dano_pos_resistencia_person > 0:
                vida -= Dano_pos_resistencia_person
                if aurea == "Impulsiva":
                    eliminacoes_consecutivas_impulsiva = 0  # Perde streak se levar dano

                eliminacoes_consecutivas = 0
                bonus_pontuacao = 0
            
            tempo_ultimo_hit_inimigo = tempo_atual
            Dano_person.play()
            piscando_vida = True
            
    if not escudo_devota_ativo and tempo_atual - tempo_ultimo_escudo >= intervalo_escudo:
        escudo_devota_ativo = True
        tempo_ultimo_escudo = tempo_atual
        # adicionar um efeito visual de "escudo ativado"

    
        
    if vida <= 0:
        if trembo:
            vida = vida_maxima  # Recupera a vida total
            trembo = False  # Consome o "trembo"
            imune_tempo_restante = 10000
            teleportado = True  # Ativa o teleporte aleatório
            porcentagem_cura= 0.02
            Tempo_cura=2500
            pos_x_personagem, pos_y_personagem = gerar_posicao_aleatoria(largura_mapa, altura_mapa, largura_personagem, altura_personagem)
        else:
            mostrar_tutorial=False
            pygame.time.delay(2000)
            Musica_tema_fases.stop()
            Som_tema_fases.stop()
            tela_upgrade_aureas(tela, fonte, moedas_coletadas)

            pygame.quit()
            limpar_salvamento()
            subprocess.run([python, "Game_Over.py"])
            sys.exit()

    # Adicione esta verificação para controlar o piscar da barra de vida
    if piscando_vida:
        if tempo_atual % 500 < 250:  # Altere o valor 500 e 250 conforme necessário
            # Desenha a barra de vida piscando em vermelho
            pygame.draw.rect(tela, (255, 0, 0), (posicao_barra_vida[0], posicao_barra_vida[1], largura_barra_vida, altura_barra_vida))
        else:
            # Desenha a barra de vida normalmente
            pygame.draw.rect(tela, verde, (posicao_barra_vida[0], posicao_barra_vida[1], (vida / vida_maxima) * largura_barra_vida, altura_barra_vida))

        # Adicione esta verificação para parar o piscar depois de um tempo
        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            piscando_vida = False

    tempo_atual = pygame.time.get_ticks()

    if boss_vivo1:
        if not em_ataque_especial and pygame.time.get_ticks() - tempo_ultimo_ataque >= 5000:  # Intervalo entre ataques
            # Inicia o ataque especial
            em_ataque_especial = True
            jogador_posicoes = []  # Reiniciar lista de posições
            tempo_ataque_especial = pygame.time.get_ticks()

        if em_ataque_especial:
            tempo_atual = pygame.time.get_ticks()
            indice_imagem = (tempo_atual - tempo_ataque_especial) // intervalo_troca
            
            # Atualizar a posição somente no início de cada intervalo, exceto no quinto frame
            if len(jogador_posicoes) <= indice_imagem < len(imagens_ataque) - 2:
                jogador_posicoes.append((pos_x_personagem, pos_y_personagem))

            ataque_concluido = ataque_especial_boss(jogador_posicoes, imagens_ataque, tempo_ataque_especial, intervalo_troca, tela)
            if ataque_concluido:
                em_ataque_especial = False
                tempo_ultimo_ataque = pygame.time.get_ticks()

    # Verificar colisões com as bolhas e aplicar dano no loop principal
    if em_ataque_especial:
        personagem_rect = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
        for i, posicao in enumerate(jogador_posicoes[-1:]):
            if i < len(imagens_ataque):
                bolha_rect = pygame.Rect(posicao[0], posicao[1], 100, 100)  # Ajuste o tamanho da bolha aqui
                hitboxes[i] = bolha_rect
                # Verificar colisão com o personagem
                if len(jogador_posicoes) == indice_imagem  and personagem_rect.colliderect(bolha_rect):
                    if escudo_devota_ativo:
                        escudo_devota_ativo= False
                        pass
                    elif pygame.time.get_ticks() - tempo_ultimo_dano_ataque >= 5000:  # Dano a cada 4 segundos
                        vida -= (vida_maxima * 0.10) + Dano_Boss_Habilit
                        tempo_ultimo_dano_ataque= pygame.time.get_ticks()
    

    ###############################################   DESENHA O PERSONAGEM NA TELA ################################
    tela.blit(frames_animacao[direcao_atual][frame_atual], (pos_x_personagem, pos_y_personagem))
    for moeda in moedas_soltadas[:]:  # cópia da lista para evitar erro ao remover
        if personagem_rect.colliderect(moeda["rect"]):
            moedas_coletadas+=1
            moedas_soltadas.remove(moeda)
            print("[💰] Moeda coletada!")
    nova_lista = []
    for efeito in efeitos_texto:
        tempo_passado = tempo_atual - efeito["tempo_inicio"]
        if tempo_passado <= 800:  # mostra por 2 segundos
            fonte_efeito = pygame.font.Font(None, 28)
            x = efeito["x"]
            y = efeito["y"] - (tempo_passado // 25)
            texto_principal = fonte_efeito.render(efeito["texto"], True, efeito["cor"])

            # Contorno preto em 8 direções
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        contorno = fonte_efeito.render(efeito["texto"], True, (0, 0, 0))
                        tela.blit(contorno, (x + dx, y + dy))

            # Texto principal
            tela.blit(texto_principal, (x, y))
            nova_lista.append(efeito)
    efeitos_texto = nova_lista
    if trembo:
        # Desenhar o segundo personagem ao lado do personagem original
        pos_x_segundo_personagem = pos_x_personagem + largura_personagem + 4
        pos_y_segundo_personagem = pos_y_personagem
        tela.blit(frames_animacao_trembo[direcao_atual][frame_atual], (pos_x_segundo_personagem, pos_y_segundo_personagem))
    if trembo and tempo_atual- tempo_ultima_regeneracao >= Tempo_cura and vida < vida_maxima :
        if vida_maxima < vida:
            vida=vida_maxima
        vida+= (vida_maxima*porcentagem_cura)
        tempo_ultima_regeneracao = tempo_atual
    
    
    
    if Petro_active:
        # Calcula a direção para o inimigo mais próximo
        
        direcao_petro = calcular_direcao_para_inimigo({"rect": pygame.Rect(pos_x_petro, pos_y_petro, largura_personagem, altura_personagem)}, inimigos_comum)
        
        
        # Se houver inimigos, atualize a posição de "Petro"
        if inimigos_comum:
            # Calcula as coordenadas do inimigo mais próximo
            inimigo_mais_proximo = min(inimigos_comum, key=lambda inimigo: math.sqrt((inimigo["rect"].x - pos_x_petro) ** 2 + (inimigo["rect"].y - pos_y_petro) ** 2))
            pos_x_inimigo_mais_proximo = inimigo_mais_proximo["rect"].x
            pos_y_inimigo_mais_proximo = inimigo_mais_proximo["rect"].y
            
            posicao_petro = (pos_x_petro, pos_y_petro)
            posicao_inimigo = (pos_x_inimigo_mais_proximo, pos_y_inimigo_mais_proximo)
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultima_atualizacao_direcao >= 1000:  # 1000 milissegundos = 1 segundo
                # Atualiza a direção de Petro
                direcao_atual_petro = determinar_frames_petro(posicao_petro, posicao_inimigo)
                # Atualiza o tempo da última atualização da direção
                tempo_ultima_atualizacao_direcao = tempo_atual
            
            
            # Se "Petro" ainda não está na posição do inimigo, mova-o na direção calculada
            if pos_x_petro != pos_x_inimigo_mais_proximo or pos_y_petro != pos_y_inimigo_mais_proximo:
                pos_x_petro += 1 * direcao_petro[0]
                pos_y_petro += 1 * direcao_petro[1]
                

            # Calcula a distância entre "Petro" e o inimigo mais próximo
            distancia_petro_inimigo = math.sqrt((pos_x_petro - pos_x_inimigo_mais_proximo) ** 2 + (pos_y_petro - pos_y_inimigo_mais_proximo) ** 2)
            
            # Verifica se "Petro" está próximo o suficiente para aplicar dano
            if distancia_petro_inimigo <= 50:
                # Verifica se passou tempo suficiente desde o último dano
                tempo_atual_petro = pygame.time.get_ticks()
                if tempo_atual_petro - tempo_anterior_petro >= intervalo_dano_petro:
                    # Aplica dano ao inimigo mais próximo
                    Dano_pos_resistencia_petro=dano_inimigo-Resistencia_petro
                    if Dano_pos_resistencia_petro < 0:
                        pass
                    
                    else:
                        vida_petro-=int(Dano_pos_resistencia_petro)#Dano em petro
                    
                    
                    inimigo_mais_proximo["vida"] -= int(dano_person_hit * 0.005)+ dano_petro
                    tempo_anterior_petro = tempo_atual_petro
                    
                    # Verifica se o inimigo foi derrotado
                    if inimigo_mais_proximo["vida"] <= 0:
                        vida_inimigo_maxima+=23
                        pontuacao += int(75 + inimigos_eliminados * 0.5)
                        pontuacao_exib += int(75 + inimigos_eliminados * 0.5)
                        Resistencia_petro+=24.5
                        vida_maxima_petro+=35
                        dano_person_hit+=8
                        inimigos_eliminados += 1
                        dano_petro+=0.035 
                        dano_inimigo_longe+=2
                        dano_inimigo_perto+=0.35
                        # Remove o inimigo da lista de inimigos comuns
                        inimigos_comum.remove(inimigo_mais_proximo) 
                        
                    if not boss_vivo1:
                        if vida_boss>0:
                            vida_boss+=55
                            vida_maxima_boss1= vida_boss
                            vida_boss2+=66
                            vida_maxima_boss2= vida_boss2
                            vida_boss3+=72
                            vida_maxima_boss3= vida_boss3   
                            vida_boss4+=82
                            vida_maxima_boss4= vida_boss4
                        
        if vida_petro<=0:
            Petro_active= False
            vida_petro+= vida_maxima_petro
            vida_maxima_petro= vida_petro                     
                        
        
        if xp_petro == "nivel_1":
            petro_nivel=frames_animacao_Petro
            
        elif xp_petro == "nivel_2":
            petro_nivel=frames_animacao_Petro2
            
        elif xp_petro == "nivel_3":
            petro_nivel=frames_animacao_Petro3                
                      
                    
                    
        if boss_vivo1:
            # Define a direção de Petro em relação ao boss
            dx = pos_x_chefe - pos_x_petro
            dy = pos_y_chefe - pos_y_petro

            # Normaliza a direção para manter a mesma velocidade em todas as direções
            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            if magnitude != 0:
                direcao_x = dx / magnitude
                direcao_y = dy / magnitude
            else:
                direcao_x = 0
                direcao_y = 0

            # Move Petro na direção do boss
            pos_x_petro += 1 * direcao_x
            pos_y_petro += 1 * direcao_y

            # Verifica se Petro está próximo o suficiente para aplicar dano ao boss
            distancia_petro_boss = math.sqrt((pos_x_petro - pos_x_chefe) ** 2 + (pos_y_petro - pos_y_chefe) ** 2)
            if distancia_petro_boss <= 50:
                # Verifica se passou tempo suficiente desde o último dano
                tempo_atual_petro = pygame.time.get_ticks()
                if tempo_atual_petro - tempo_anterior_petro >= intervalo_dano_petro:
                    # Aplica dano ao "boss"
                    vida_petro -= int(dano_boss)
                    vida_petro+= int(vida_maxima_petro-vida_petro)*quantidade_roubo_vida
                    vida_boss-= int(dano_person_hit*0.15)+15
                    0
                    # Aqui você pode adicionar outras ações relacionadas ao dano ao "boss"
                    tempo_anterior_petro = tempo_atual_petro

        if comando_direção_petro:
            direcao_atual_petro="left_petro"
            comando_direção_petro=False
            
        desenhar_barra_de_vida_petro(tela, vida_petro, pos_x_petro, pos_y_petro - 20,vida_maxima_petro)  
        tela.blit(petro_nivel[direcao_atual_petro][frame_atual], (pos_x_petro, pos_y_petro))


#AQUI GERAMOS O BOSS:
    if pontuacao >= 3000500 or (keys[pygame.K_r]) or r_press:
        r_press=True
        # Verificar se é hora de realizar um ataque do boss
        Musica_tema_fases.stop()
        tempo_atual = pygame.time.get_ticks()
        

        if musica_boss1 == 1:
            boss_vivo1=True
            # Defina o volume da música (opcional)
            Musica_tema_Boss1.play(loops=-1)
            musica_boss1+=1

        
        

        # Lógica para animar o chefe
        tempo_passado_animacao_chefe += relogio.get_rawtime()
        if tempo_passado_animacao_chefe >= tempo_animacao_chefe:
            tempo_passado_animacao_chefe = 0
            frame_atual_chefe = (frame_atual_chefe + 1) % 2

        # Mude a direção do boss a cada 3 segundos
        tempo_atual = pygame.time.get_ticks()
        intervalo_mudanca_direcao_boss = random.randint(1000, 3000) # Tempo em milissegundos para mudar de direção do boss
        if tempo_atual - tempo_ultima_mudanca_direcao_boss >= intervalo_mudanca_direcao_boss:
        
            direcoes_possiveis = ['up', 'down', 'left', 'right']
            direcoes_possiveis.remove(ultima_direcao_boss)  # Remova a direção anterior
            ultima_direcao_boss = random.choice(direcoes_possiveis)
            tempo_ultima_mudanca_direcao_boss = tempo_atual  # Atualize o tempo da última mudança de direção
            

        if boss_vivo1:
            inimigos_comum = []  # Limpe a lista de inimigos comuns
            # Movimentação do boss
            
            
            if ultima_direcao_boss == 'up':
                pos_y_chefe = max(0, pos_y_chefe - Velocidade_boss   )  # Garanta que o boss não ultrapasse o topo
            elif ultima_direcao_boss == 'down':
                pos_y_chefe = min(altura_mapa - chefe_altura, pos_y_chefe + Velocidade_boss   )  # Garanta que o boss não ultrapasse a base
            elif ultima_direcao_boss == 'left':
                pos_x_chefe = max(0, pos_x_chefe - Velocidade_boss   )  # Garanta que o boss não ultrapasse a borda esquerda
            elif ultima_direcao_boss == 'right':
                pos_x_chefe = min(largura_mapa - chefe_largura, pos_x_chefe + Velocidade_boss   )  # Garanta que o boss não ultrapasse a borda direita

            # Verifica se o boss chegou à borda da tela
            if pos_x_chefe <= 0 or pos_x_chefe >= largura_mapa - chefe_largura or pos_y_chefe <= 0 or pos_y_chefe >= altura_mapa - chefe_altura:
                # Se sim, mude para a direção oposta (você pode definir as direções conforme necessário)
                if ultima_direcao_boss == 'up':
                    ultima_direcao_boss = 'down'
                elif ultima_direcao_boss == 'down':
                    ultima_direcao_boss = 'up'
                elif ultima_direcao_boss == 'left':
                    ultima_direcao_boss = 'right'
                elif ultima_direcao_boss == 'right':
                    ultima_direcao_boss = 'left'
                    
            






        if not boss_vivo1:
            rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, 64, 64)
            rect_personagem = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)

            if rect_boss.colliderect(rect_personagem):
                if toque == 0:
                    Musica_tema_Boss1.stop()
                    salvar_atributos()
                    pausar_cronometro()
                    import GAME2
                    
                    
                    toque+=1

        # Dentro do loop principal
        if vida_boss > 0:
            pygame.draw.rect(tela, vermelho, (pos_x_barra_boss, pos_y_barra_boss, largura_barra_boss, altura_barra_boss))
            pygame.draw.rect(tela, (143,33,252), (pos_x_barra_boss, pos_y_barra_boss, largura_barra_boss, (vida_boss / vida_maxima_boss1) * altura_barra_boss))
            pygame.draw.rect(tela, (255, 255, 255), (pos_x_barra_boss, pos_y_barra_boss, largura_barra_boss, altura_barra_boss), 2)
        if Ultimo_Estalo and vida_boss <= Executa_inimigo * vida_maxima_boss1:
            boss_vivo1=False

        if vida_boss <= 0:
            frame_porcentagem=frames_chefe1_4
            boss_vivo1=False




        for disparo in disparos:
            pos_x_disparo=disparo["rect"].x 
            pos_y_disparo=disparo["rect"].y 
            rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
            rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, chefe_largura, chefe_altura)
            
            if rect_disparo.colliderect(rect_boss):
                if vida_boss > 0:  # Verifica se o chefe está vivo antes de aplicar dano
                    if random.random() <= chance_critico:  # 10% de chance de dano crítico
                        dano = dano_person_hit * 3  # Valor do dano crítico é 3 vezes o dano normal
                        cor = (255, 255, 0)  # Amarelo (RGB)
                        fonte_dano = fonte_dano_critico
                    else:
                        dano = dano_person_hit
                        cor = (255, 0, 0)  # Vermelho (RGB)
                        fonte_dano = fonte_dano_normal

                # Ativar veneno no Boss com 50% de chance, se ainda não estiver envenenado
                if not boss_envenenado and Poison_Active:
                    boss_envenenado = True
                    dano_por_tick_veneno_boss = vida_boss * (Dano_Veneno_Acumulado / 100)  # Exemplo: 0.05% da vida máxima
                    tempo_inicio_veneno_boss = pygame.time.get_ticks()
                    ultimo_tick_veneno_boss = pygame.time.get_ticks()

                # Renderizar texto do dano
                texto_dano = fonte_dano.render("-" + str(int(dano)), True, cor)
                pos_texto = (pos_x_chefe + chefe_largura // 2 - texto_dano.get_width() // 2, pos_y_chefe - 20)
                tempo_texto_dano = pygame.time.get_ticks()
                vida_boss -= dano
                disparos.remove(disparo)

                # Roubo de vida
                if random.random() < roubo_de_vida:
                    vida += (vida_maxima - vida) * quantidade_roubo_vida

        # Aplicar dano de veneno no Boss se ele estiver envenenado
        if boss_envenenado:
            tempo_atual = pygame.time.get_ticks()

            # Aplicar dano a cada 500 ms
            if tempo_atual - ultimo_tick_veneno_boss >= 500:
                vida_boss -= dano_por_tick_veneno_boss
                ultimo_tick_veneno_boss = tempo_atual

            # Exibir texto do dano de veneno (1.5 segundos)
            if tempo_atual - ultimo_tick_veneno_boss <= 250:
                dano_veneno_texto = "-" + str(int(dano_por_tick_veneno_boss))
                texto_dano_veneno = fonte_veneno.render(dano_veneno_texto, True, (0, 255, 0))
                texto_dano_veneno_borda = fonte_veneno.render(dano_veneno_texto, True, (0, 0, 0))
                pos_texto = (pos_x_chefe + chefe_largura // 2 - texto_dano_veneno.get_width() // 2, pos_y_chefe - 30)
                tela.blit(texto_dano_veneno_borda, (pos_texto[0] - 1, pos_texto[1]))
                tela.blit(texto_dano_veneno_borda, (pos_texto[0] + 1, pos_texto[1]))
                tela.blit(texto_dano_veneno_borda, (pos_texto[0], pos_texto[1] - 1))
                tela.blit(texto_dano_veneno_borda, (pos_texto[0], pos_texto[1] + 1))
                tela.blit(texto_dano_veneno, pos_texto)

            # Desativar o veneno após o tempo de duração
            if tempo_atual - tempo_inicio_veneno_boss >= duracao_veneno_boss:
                boss_envenenado = False
        if boss_vivo1:
            rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, 200, 100)
            
            rect_personagem = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)

            if rect_boss.colliderect(rect_personagem):
                # Verifique se tempo suficiente passou desde o último ataque
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_ataque >= 2500:  # Tempo em milissegundos (2 segundos = 2000 milissegundos)
                    dano_boss_total=int((vida_maxima*0.10)+150+dano_boss)
                    if escudo_devota_ativo:
                        escudo_devota_ativo= False
                        pass
                    elif Resistencia < dano_boss_total:
                        vida -= int(dano_boss_total-Resistencia)
                    else:
                        pass
                    Dano_person.play()
                    piscando_vida = True
                    # Atualize o tempo do último ataque
                    tempo_ultimo_ataque = tempo_atual

            porcentagem_vida_boss = (vida_boss / vida_maxima_boss1) * 100

        if porcentagem_vida_boss >=90 :
            frame_porcentagem=frames_chefe1_1
                

        elif porcentagem_vida_boss <= 60 and porcentagem_vida_boss >=40:
            frame_porcentagem=frames_chefe1_2

        elif porcentagem_vida_boss <= 40 and porcentagem_vida_boss>0 :
            
            frame_porcentagem=frames_chefe1_3
            intervalo_mudanca_direcao_boss-=500
        

        tela.blit(frame_porcentagem[frame_atual_chefe], (pos_x_chefe, pos_y_chefe))

    for inimigo in inimigos_comum:
        inimigo_rect = inimigo["rect"]
        inimigo_image = inimigo["image"]

        inimigo_atingido = False

        for disparo in disparos:
            
            if verificar_colisao_disparo_inimigo(disparo, (inimigo["rect"].x, inimigo["rect"].y), largura_disparo, altura_disparo, largura_inimigo, altura_inimigo, inimigos_eliminados):

                if random.random() <= chance_critico:  # chance de dano crítico
                    dano = dano_person_hit * 3  # Valor do dano crítico é 3 vezes o dano normal
                    cor = (255, 255, 0)  # Amarelo (RGB)
                    fonte_dano=fonte_dano_critico
                else:
                    dano = dano_person_hit
                    cor = (255, 0, 0)  # Vermelho (RGB)
                    fonte_dano=fonte_dano_normal
                if Petro_active:
                    if vida_petro > vida_maxima_petro :
                        vida_petro+= (vida_maxima_petro-vida_petro) *0.25
                # Renderize o texto do dano
                texto_dano = fonte_dano.render("-" + str(int(dano)), True, cor)
                    
                # Desenhe o texto na tela perto do chefe
                pos_texto = (inimigo["rect"].x + largura_inimigo // 2 - texto_dano.get_width() // 2,  inimigo["rect"].y - 20)
                            
                # Rastreie o tempo de exibição do texto
                tempo_texto_dano = pygame.time.get_ticks()
                inimigo["vida"] -= dano
                disparos.remove(disparo)  # Remover o disparo após colisão
                # Adicionar uma chance de 50% de aumentar a vida em 20 pontos

                if random.random() < roubo_de_vida:
                    vida += (vida_maxima-vida)*quantidade_roubo_vida

                if Poison_Active:
                    inimigo["veneno"] = {
                        "dano_por_tick": inimigo["vida_maxima"] * Dano_Veneno_Acumulado,  # 0.5% da vida máxima
                        "tempo_inicio": pygame.time.get_ticks(),
                        "duracao": 4000,  # 4 segundos
                        "ultimo_tick": pygame.time.get_ticks(),  # Tempo do último tick
                        "posicao_texto": (inimigo["rect"].x, inimigo["rect"].y - 20),  # Posição inicial do texto
                        "tempo_texto_dano": pygame.time.get_ticks()  # Tempo de exibição do texto
                        }

                    # Dentro do loop principal, fora do loop de verificação de disparo
                    
                    
                if Ultimo_Estalo and inimigo["vida"] <= Executa_inimigo * inimigo["vida_maxima"]:
                    
                    estalos.play()
                    posicao_inimigo = inimigo["rect"].center
                    soltar_moeda(posicao_inimigo)
                    inimigos_comum.remove(inimigo)
                    inimigos_comum.remove(inimigo)

                    # Crescimento escalonado dos atributos
                    vida_inimigo_maxima += 1.5 + nivel_ameaca * 0.75
                    Resistencia_petro += 0.25 + nivel_ameaca * 0.1
                    dano_inimigo_perto += 0.2 + nivel_ameaca * 0.1
                    vida_maxima_petro += 0.6 + nivel_ameaca * 0.3
                    dano_petro += 0.015 + nivel_ameaca * 0.01
                    dano_inimigo_longe += 0.04 + nivel_ameaca * 0.02
                    dano_boss += 0.03 + nivel_ameaca * 0.02
                    Dano_Boss_Habilit += 0.05 + nivel_ameaca * 0.03
                    Velocidade_Inimigos_1 += 0.0015 + nivel_ameaca * 0.0005

                    inimigos_eliminados += 1

                    # Pontuação escalada com progressão suave
                    ganho_pontos = int(75 + math.log2(inimigos_eliminados + 1) * 5)
                    pontuacao += ganho_pontos
                    eliminacoes_consecutivas_impulsiva += 1
                    # Pontuação com carta Mercenária
                    if Mercenaria_Active:
                        eliminacoes_consecutivas += 1
                        pontuacao_exib += ganho_pontos + bonus_pontuacao
                        if eliminacoes_consecutivas % 5 == 0:
                            bonus_pontuacao += Valor_Bonus
                    else:
                        pontuacao_exib += ganho_pontos

                    # Escalonamento de vida dos bosses (somente se não estiver ativo no momento)
                    if not boss_vivo1:
                        if vida_boss > 0:
                            vida_boss += 15 + nivel_ameaca * 10
                            vida_maxima_boss1 = vida_boss
                            vida_boss2 += 20 + nivel_ameaca * 12
                            vida_maxima_boss2 = vida_boss2
                            vida_boss3 += 25 + nivel_ameaca * 15
                            vida_maxima_boss3 = vida_boss3
                            vida_boss4 += 30 + nivel_ameaca * 18
                            vida_maxima_boss4 = vida_boss4
                elif inimigo["vida"] <= 0:
                    posicao_inimigo = inimigo["rect"].center
                    soltar_moeda(posicao_inimigo)
                    inimigos_comum.remove(inimigo)
                    
                    # Crescimento proporcional por nível de ameaça
                    vida_inimigo_maxima += 1.2 + nivel_ameaca * 0.8
                    Resistencia_petro += 0.2 + nivel_ameaca * 0.1
                    dano_inimigo_perto += 0.2 + nivel_ameaca * 0.1
                    dano_person_hit += 0.15 + nivel_ameaca * 0.05
                    vida_maxima_petro += 0.5 + nivel_ameaca * 0.3
                    dano_petro += 0.02 + nivel_ameaca * 0.01
                    dano_inimigo_longe += 0.03 + nivel_ameaca * 0.02
                    dano_boss += 0.04 + nivel_ameaca * 0.02
                    Dano_Boss_Habilit += 0.05 + nivel_ameaca * 0.03
                    Velocidade_Inimigos_1 += 0.0015 + nivel_ameaca * 0.0005

                    inimigos_eliminados += 1

                    # Pontuação com escala suave
                    ganho = int(75 + math.log2(inimigos_eliminados + 1) * 4)
                    pontuacao += ganho
                    eliminacoes_consecutivas_impulsiva += 1
                    if Mercenaria_Active:
                        eliminacoes_consecutivas += 1
                        pontuacao_exib += ganho + bonus_pontuacao
                        if eliminacoes_consecutivas % 5 == 0:
                            bonus_pontuacao += Valor_Bonus
                    else:
                        pontuacao_exib += ganho

                    # Boss: aumento escalonado
                    if not boss_vivo1:
                        if vida_boss > 0:
                            vida_boss += 15 + nivel_ameaca * 10
                            vida_maxima_boss1 = vida_boss
                            vida_boss2 += 20 + nivel_ameaca * 12
                            vida_maxima_boss2 = vida_boss2
                            vida_boss3 += 25 + nivel_ameaca * 15
                            vida_maxima_boss3 = vida_boss3
                            vida_boss4 += 30 + nivel_ameaca * 18
                            vida_maxima_boss4 = vida_boss4

                    
                       
                    
                    break  # Sai do loop interno para evitar problemas ao modificar a lista enquanto iteramos sobre ela

        if "veneno" in inimigo:
            # Verifique se é hora de aplicar dano
            if tempo_atual - inimigo["veneno"]["ultimo_tick"] >= 500:
                inimigo["vida"] -= inimigo["veneno"]["dano_por_tick"]
                inimigo["veneno"]["ultimo_tick"] = tempo_atual  # Atualiza o tempo do último tick
                inimigo["veneno"]["tempo_texto_dano"] = tempo_atual  # Atualiza o tempo de exibição do texto

            # Exibe o texto apenas por 1.5 segundos após o dano
            if tempo_atual - inimigo["veneno"]["tempo_texto_dano"] <= 250:
                dano_veneno_texto = "-" + str(int(inimigo["veneno"]["dano_por_tick"]))

                # Renderize o texto do dano com borda preta
                texto_dano_veneno = fonte_veneno.render(dano_veneno_texto, True, (0, 255, 0))
                texto_dano_veneno_borda = fonte_veneno.render(dano_veneno_texto, True, (0, 0, 0))

                # Posicione o texto
                pos_texto = (inimigo["rect"].x + largura_inimigo // 2 - texto_dano_veneno.get_width() // 2,
                         inimigo["rect"].y - 30)

                # Exibe o texto com borda preta e o texto em verde
                tela.blit(texto_dano_veneno_borda, (pos_texto[0] - 1, pos_texto[1]))
                tela.blit(texto_dano_veneno_borda, (pos_texto[0] + 1, pos_texto[1]))
                tela.blit(texto_dano_veneno_borda, (pos_texto[0], pos_texto[1] - 1))
                tela.blit(texto_dano_veneno_borda, (pos_texto[0], pos_texto[1] + 1))
                tela.blit(texto_dano_veneno, pos_texto)  # Texto principal em verde

            # Verifica se o efeito de veneno expirou
            if tempo_atual - inimigo["veneno"]["tempo_inicio"] >= inimigo["veneno"]["duracao"]:
                del inimigo["veneno"]  # Remove o efeito de veneno ao expirar        

        if inimigo_atingido:
            break  # Sair do loop externo se um inimigo foi atingido
    

    
        if pontuacao_exib > pontuacao_magia:
            pontuacao_magia = min(pontuacao_exib, maxima_pontuacao_magia)

                    
    

        
    total_cartas_compradas = sum(cartas_compradas.values())
    custo_carta_atual = custo_base_carta + (total_cartas_compradas * custo_por_carta)
    # Verifica se a pontuação atingiu 1500 e se o jogador pressionou 'Q'
    if pontuacao_exib >= custo_carta_atual and keys[config_teclas["Comprar na loja"]] or (joystick and joystick.get_button(3)):
        pontuacao_exib -= custo_carta_atual
        pontuacao_magia -= custo_carta_atual
        apertou_q= True
        
        
        ret = tela_de_pausa(velocidade_personagem, intervalo_disparo,vida,largura_disparo, altura_disparo,trembo,dano_person_hit,chance_critico,roubo_de_vida,
                            quantidade_roubo_vida,tempo_cooldown_dash,vida_maxima,Petro_active,Resistencia,vida_petro,vida_maxima_petro,dano_petro,xp_petro,petro_evolucao,Resistencia_petro,
                            Chance_Sorte,Poison_Active,Dano_Veneno_Acumulado,Executa_inimigo,Ultimo_Estalo,mostrar_info,Mercenaria_Active,Valor_Bonus,dispositivo_ativo,Tempo_cura,porcentagem_cura,cartas_compradas,pontuacao_exib)
        velocidade_personagem = ret[0]
        intervalo_disparo = ret[1]
        vida = ret[2]
        largura_disparo =ret[3]
        altura_disparo =ret[4]
        trembo= ret[5]
        dano_person_hit= ret[6]
        chance_critico= ret[7]
        roubo_de_vida= ret[8]
        quantidade_roubo_vida= ret[9]
        tempo_cooldown_dash= ret[10]
        vida_maxima= ret[11]
        Petro_active= ret[12]
        Resistencia=  ret[13]
        vida_petro= ret[14]
        vida_maxima_petro= ret[15]
        dano_petro= ret[16]
        xp_petro= ret[17]
        petro_evolucao= ret[18]
        Resistencia_petro= ret[19]
        Chance_Sorte= ret[20]
        Poison_Active= ret[21]
        Dano_Veneno_Acumulado= ret[22]
        Executa_inimigo= ret[23]
        Ultimo_Estalo= ret[24]
        Mercenaria_Active= ret[25]
        Valor_Bonus= ret[26]
        dispositivo_ativo=ret[27]
        Tempo_cura=ret[28]
        porcentagem_cura=ret[29]
        cartas_compradas= ret[30]
        pontuacao_exib= ret[31]
        

    posicao_barra_vida = (80, altura_mapa - (altura_mapa - 34))
    fonte = pygame.font.Font(None, int(altura_barra_vida*1))
    texto_pontuacao = fonte.render(f'{pontuacao_exib}/{custo_carta_atual}', True, (250, 255,255))
    fonte_vida = pygame.font.Font(None, int(altura_barra_vida*0.9))
    texto_vida = fonte_vida.render(f'{int(vida)}/{int(vida_maxima)}', True, (255, 255, 255))

    # Renderiza o texto de pontuação com uma borda
    texto_pontuacao_borda = fonte.render(f'{pontuacao_exib}/{custo_carta_atual}', True, (0, 0, 0))  # Cor preta para a borda
    # Desenha o texto da borda um pouco deslocado para criar o efeito de contorno
    tela.blit(texto_pontuacao_borda, (largura_mapa*0.075 - 1, altura_mapa*0.118 - 1))
    tela.blit(texto_pontuacao_borda, (largura_mapa*0.075 + 1, altura_mapa*0.118 - 1))
    tela.blit(texto_pontuacao_borda, (largura_mapa*0.075 - 1, altura_mapa*0.118 + 1))
    tela.blit(texto_pontuacao_borda, (largura_mapa*0.075 + 1, altura_mapa*0.118 + 1))

    # Desenha o texto da pontuação por cima da borda
    tela.blit(texto_pontuacao, (largura_mapa*0.075, altura_mapa*0.118))

    

    

    # Calculando o ângulo do preenchimento em graus
    angulo_preenchimento = (pontuacao_magia / 735) * 360  # ângulo em graus
    # Preenchendo a parte do círculo
    if angulo_preenchimento > 0:
        pontos = []
        for i in range(int(angulo_preenchimento) + 1):
            radianos = math.radians(i - 90) 
            x = centro_circulo[0] + raio_circulo * math.cos(radianos)
            y = centro_circulo[1] + raio_circulo * math.sin(radianos)
            pontos.append((x, y))
        pygame.draw.polygon(tela, (53, 239, 252), [centro_circulo] + pontos) 
    
    tela.blit(imagem_relogio, posicao_imagem_relogio)
    
        

    if vida > vida_maxima:
        vida_maxima=vida

    porcentagem_vida_personagem = (vida / vida_maxima) * 100
    if aurea == "Devota" and escudo_devota_ativo:
        cor_barra = (0, 150, 255)  # Azul para indicar o escudo ativo
    else:
        cor_barra = calcular_cor_barra_de_vida(porcentagem_vida_personagem)

    pygame.draw.rect(tela, cor_barra, (posicao_barra_vida[0], posicao_barra_vida[1], (vida / vida_maxima) * largura_barra_vida, altura_barra_vida))
    pygame.draw.rect(tela, (0, 0, 0), (posicao_barra_vida[0], posicao_barra_vida[1], largura_barra_vida, altura_barra_vida), 2)

    
    # Renderiza o texto de vida com uma borda
    texto_vida_borda = fonte_vida.render(f'{int(vida)}/{int(vida_maxima)}', True, (0, 0, 0))  # Cor preta para a borda
    # Desenha o texto da borda um pouco deslocado para criar o efeito de contorno
    tela.blit(texto_vida_borda, (posicao_barra_vida[0]*2 - 1, posicao_barra_vida[1] + 5 - 1))
    tela.blit(texto_vida_borda, (posicao_barra_vida[0]*2 + 1, posicao_barra_vida[1] + 5 - 1))
    tela.blit(texto_vida_borda, (posicao_barra_vida[0]*2 - 1, posicao_barra_vida[1] + 5 + 1))
    tela.blit(texto_vida_borda, (posicao_barra_vida[0]*2 + 1, posicao_barra_vida[1] + 5 + 1))

    # Desenha o texto da vida por cima da borda
    tela.blit(texto_vida, (posicao_barra_vida[0]*2, posicao_barra_vida[1] + 5))
    
    
    tela.blit(imagem_vida, posicao_vida)
        # Verifica se o personagem está passando pelo centro da tela e se a mensagem ainda não foi mostrada
    if (pos_x_personagem >= centro_x_tela_pequena - 400 and
        pos_x_personagem <= centro_x_tela_pequena + 400 and
        pos_y_personagem >= centro_y_tela_pequena - 400 and
        pos_y_personagem <= centro_y_tela_pequena + 400 and mensagem_mostrada):
        
        
        # Renderiza o texto
        texto_renderizado = fonte.render(mensagem, True, (0,0,0))
        # Obtém o retângulo do texto
        texto_rect = texto_renderizado.get_rect()
        # Define a posição do texto para que ele fique no centro da tela
        texto_rect.center = (centro_x_tela_pequena, centro_y_tela_pequena)

        # Calcula as dimensões do retângulo de fundo da mensagem
        largura_fundo = texto_rect.width + 20  # Adiciona um espaço de 10 pixels de cada lado
        altura_fundo = texto_rect.height + 20  # Adiciona um espaço de 10 pixels em cima e embaixo
        # Cria um retângulo branco para o fundo da mensagem
        fundo_rect = pygame.Rect((centro_x_tela_pequena - largura_fundo // 2, centro_y_tela_pequena - altura_fundo // 2), (largura_fundo, altura_fundo))
        # Desenha o retângulo branco na tela
        pygame.draw.rect(tela, (225, 255, 255), fundo_rect)
        # Desenha o texto na tela
        tela.blit(texto_renderizado, texto_rect) 

        # Incrementa o tempo que a mensagem está sendo mostrada
        tempo_mostrando_mensagem += 1
        
        # Se a mensagem estiver sendo mostrada por mais de 3 segundos
        if tempo_mostrando_mensagem > 420:  # 60 frames por segundo * 3 segundos = 180
            mensagem_mostrada = False  # Define que a mensagem foi mostrada
            tempo_mostrando_mensagem = 0  # Reinicia o contador de tempo
    
    # Remova o texto após 2 segundos
    if texto_dano is not None and pygame.time.get_ticks() - tempo_texto_dano >= 250:
        texto_dano = None

    cooldowns = {
        "disparo": max(0, tempo_atual - tempo_ultimo_disparo >= intervalo_disparo),
        "teleporte": max(0, pygame.time.get_ticks() - tempo_ultimo_dash > tempo_cooldown_dash),
        "onda": max(0, tempo_atual - tempo_ultimo_uso_habilidade >= cooldown_habilidade),
        "loja": 1 if pontuacao_exib >= custo_carta_atual else 0, 
    }
    if not area_icones.colliderect(
    (pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
    ):
        # Desenhar habilidades na tela
        desenhar_habilidades(tela, cooldowns,dispositivo_ativo)
    if eliminacoes_consecutivas > 0:
        fonte_combo = pygame.font.Font(None, 36)  # Tamanho maior para o combo
        fonte_bonus = pygame.font.Font(None, 28)  # Tamanho menor para o bônus

        # Texto do combo
        texto_combo = f"Combo: {eliminacoes_consecutivas}"
        posicao_combo = (largura_mapa - 170, 50)  
        desenhar_texto_com_contorno(tela, texto_combo, fonte_combo, (255, 255, 255), (0, 0, 0), posicao_combo)

        # Texto do bônus
        texto_bonus = f"Bônus: +{bonus_pontuacao}"
        posicao_bonus = (largura_mapa - 200, 90)  
        desenhar_texto_com_contorno(tela, texto_bonus, fonte_bonus, (255, 255, 255), (0, 0, 0), posicao_bonus)
    
    # Desenhe o texto na tela
    if texto_dano is not None:
        tela.blit(texto_dano, pos_texto)
    # Controle de exibição
    if mostrar_tutorial:
        tempo_decorrido = time.time() - tempo_inicial
        if 'mensagens_exibidas' not in globals():
            mensagens_exibidas = set()
            mensagem_ativa = None
            tempo_fim_mensagem = 0

        # Ativando nova mensagem, se for o tempo certo
        for tempo_msg, texto_msg in mensagens_iniciais:
            if int(tempo_decorrido) == tempo_msg and tempo_msg not in mensagens_exibidas:
                mensagem_ativa = texto_msg
                tempo_fim_mensagem = tempo_decorrido + 10  # visível por 10 segundos
                mensagens_exibidas.add(tempo_msg)

        # Exibindo mensagem ativa com contorno
        if mensagem_ativa and tempo_decorrido < tempo_fim_mensagem:
            fonte_mensagem = pygame.font.Font(None, 48)
            texto = mensagem_ativa
            texto_renderizado = fonte_mensagem.render(texto, True, (255, 255, 255))
            texto_borda = fonte_mensagem.render(texto, True, (0, 0, 0))

            x = largura_mapa // 2 - texto_renderizado.get_width() // 2
            y = int(altura_mapa * 0.15)

            tela.blit(texto_borda, (x - 1, y))
            tela.blit(texto_borda, (x + 1, y))
            tela.blit(texto_borda, (x, y - 1))
            tela.blit(texto_borda, (x, y + 1))
            tela.blit(texto_renderizado, (x, y))
        else:
            mensagem_ativa = None
    tempo_atual = pygame.time.get_ticks()
    for inimigo in inimigos_comum:
        i_id = id(inimigo)
        if i_id in inimigos_em_chamas:
            tempo_inicio = inimigos_em_chamas[i_id]
            if tempo_atual - tempo_inicio <= duracao_incendio_vanguarda:
                if tempo_atual - inimigo.get("ultimo_tick_queimando", 0) >= 1000:
                    inimigo["ultimo_tick_queimando"] = tempo_atual
                    proporcao_inicial = 0.01  # 1% da vida máxima por segundo no início
                    proporcao_escalada = min(0.03, proporcao_inicial + (eliminacoes_consecutivas * 0.0015))  # escala até 3%
                    dano_fogo = int(vida_maxima * proporcao_escalada)

                    inimigo["vida"] -= dano_fogo
                   

                    efeitos_texto.append({
                        "texto": f"-{dano_fogo}",
                        "x": inimigo["rect"].x,
                        "y": inimigo["rect"].y - 20,
                        "tempo_inicio": tempo_atual,
                        "cor": (255, 120, 0)
                    })

                    if inimigo["vida"] <= 0:
                        inimigos_em_chamas.pop(i_id, None)
            else:
                inimigos_em_chamas.pop(i_id, None)
    for moeda in moedas_soltadas:
        tela.blit(moeda["image"], moeda["rect"])



    tela.blit(cursor_imagem, (mouse_x, mouse_y))
    exibir_cronometro(tela)
    pygame.display.flip()
    FPS.tick(100)  # Limita a 60 FPS


# Encerrar o Pygame
pygame.quit()
sys.exit()