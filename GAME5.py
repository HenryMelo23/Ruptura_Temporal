
import pygame
import sys
import random
import math
import subprocess
import json
import os
from Tela_Cartas import tela_de_pausa
from Variaveis import *

# Inicializar o Pygame
pygame.init()


Boss_andando=False
texto_dano = None
tempo_texto_dano = 0



som_ataque_boss = pygame.mixer.Sound("Sounds/Hit_Boss1.mp3")
som_ataque_boss.set_volume(0.04)  # Defina o volume do som do ataque do boss

Hit_inimigo3 = pygame.mixer.Sound("Sounds/Inimigo3_hit.mp3")
Hit_inimigo3.set_volume(0.04)  # Defina o volume do som do ataque do boss

Disparo_Geo = pygame.mixer.Sound("Sounds/Disparo_Geo.wav")
Disparo_Geo.set_volume(0.04)  # Defina o volume do som do ataque do boss

Musica_tema_Boss3 = pygame.mixer.Sound("Sounds/Fase3_Boss.mp3")
Musica_tema_Boss3.set_volume(0.07)  # Defina o volume do som do ataque do boss

Musica_tema_fases = pygame.mixer.Sound("Sounds/Fase_boas.mp3")
Musica_tema_fases.set_volume(0.07)  # Defina o volume do som do ataque do boss

Som_tema_fases = pygame.mixer.Sound("Sounds/Esgoto.mp3")
Som_tema_fases.set_volume(0.10)  # Defina o volume do som do ataque do boss

Som_portal = pygame.mixer.Sound("Sounds/Portal.mp3")
Som_portal.set_volume(0.06)  # Defina o volume do som do ataque do boss

Boss_Queijo= pygame.mixer.Sound("Sounds/Queijo.mp3")
Boss_Queijo.set_volume(0.11)  # Defina o volume do som do ataque do boss

Boss3_andando= pygame.mixer.Sound("Sounds/Boss3_andando.mp3")
Boss3_andando.set_volume(0.7)  # Defina o volume do som do ataque do boss

Frascos= pygame.mixer.Sound("Sounds/Frasco.mp3")
Frascos.set_volume(0.02)  # Defina o volume do som do ataque do boss

toque=0

musica_boss3= 1



# Defina os limites da área onde o queijo pode aparecer (exemplo)
area_x_min = 10
area_x_max = 800
area_y_min = 10
area_y_max = 800
# Carregue e exiba a sprite de queijo no meio da tela
sprite_queijo = pygame.image.load('Sprites/queijo.png')
largura_queijo, altura_queijo = sprite_queijo.get_size()

queijo_spawn=False
vida_queijo = 25
tempo_ultimo_grupo_disparo_boss3 = 0
tempo_espera_grupo_disparo_boss3 = 5000  # Tempo de espera entre cada grupo de disparo (em milissegundos)

# Defina as dimensões da hitbox do queijo (largura e altura)
largura_hitbox_queijo = largura_queijo + 50  # Adicione 20 pixels à largura
altura_hitbox_queijo = altura_queijo + 50  # Adicione 20 pixels à altura
pos_x_chefe3 = largura_tela /1.3  # Posição inicial do boss na tela (à direita)
pos_y_chefe3 = altura_tela / 3   # Centralizado verticalmente
chefe_largura3,chefe_altura3= largura_tela * 0.2, altura_tela * 0.3
disparos_boss3=[]
tempo_espera_ataque_boss3=5000
carregar_atributos_na_fase=True


# Carregar os frames do boss
boss_frame1 = pygame.image.load("Sprites/Boss3_1.png")
boss_frame1 = pygame.transform.scale(boss_frame1, (largura_tela * 0.2, altura_tela * 0.3))

boss_frame2 = pygame.image.load("Sprites/Boss3_2.png")
boss_frame2 = pygame.transform.scale(boss_frame2, (largura_tela * 0.2, altura_tela * 0.3))

# Carregar os frames do boss
boss_frame_andando1 = pygame.image.load("Sprites/Bossandando3_1.png")
boss_frame_andando1 = pygame.transform.scale(boss_frame_andando1, (largura_tela * 0.2, altura_tela * 0.3))

boss_frame_andando2 = pygame.image.load("Sprites/Bossandando3_2.png")
boss_frame_andando2 = pygame.transform.scale(boss_frame_andando2, (largura_tela * 0.2, altura_tela * 0.3))
boss_frame_andando = boss_frame_andando1  # Inicialize com o primeiro frame

boss_frame_peca1 = pygame.image.load("Sprites/peça.png")
boss_frame_peca1 = pygame.transform.scale(boss_frame_peca1, (64, 64))
boss_frame_peca2 = pygame.image.load("Sprites/peça.png")
boss_frame_peca2 = pygame.transform.scale(boss_frame_peca2, (64, 64))
boss_frame_peca = boss_frame_peca1  # Inicialize com o primeiro frame


boss_frame_atual = boss_frame1  # Inicialize com o primeiro frame
tempo_ultimo_frame_boss = pygame.time.get_ticks()  # Inicialize o tempo do último frame do boss

# Configurações da tela
 
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Renderizando Mapa com Personagem")

# Variáveis para a barra de magia
pontuacao_inimigos=0
maxima_pontuacao_magia = 750
piscar_magia = False
comando_direção_petro=True

# Variáveis para controlar a imobilização da personagem
personagem_doente = False
tempo_ultimo_atingido = pygame.time.get_ticks()
tempo_doente = 800  # Tempo em milissegundos de imobilização após ser atingido

spawn_inimigo=True



intervalo_disparo_inimigo = 1500  # Intervalo de 2 segundos entre os disparos dos inimigos (ajuste conforme necessário)
tempo_ultimo_disparo_inimigo = pygame.time.get_ticks()  # Adicione esta variável global para controlar o tempo do último disparo de cada inimigo





#INIMIGOS
inimigos_eliminados = 0
tempo_ultimo_inimigo_apos_morte = pygame.time.get_ticks()
# Adicione esta variável global para controlar o tempo do último disparo de cada inimigo
tempo_ultimo_disparo_inimigo = pygame.time.get_ticks()

# Carregar a imagem do mapa
mapa = pygame.image.load(mapa_path3).convert()
mapa = pygame.transform.scale(mapa, (largura_tela, altura_tela))


disparos_inimigos = []


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


# esta variável global para controlar o piscar da barra de vida
piscando_vida = False

# Adicione esses frames aos frames_inimigo existentes
frames_inimigo = frames_inimigo_esquerda3 + frames_inimigo_direita3


vida_inimigo_maxima=30
vida_inimigo= vida_inimigo_maxima
carregar_atributos_na_fase=True
imune_tempo_restante = 0  # Tempo restante de imunidade (em milissegundos)
teleportado = False  # Controle de teleporte

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
        
    }
    with open('atributos.json', 'w') as file:
        json.dump(atributos, file)

def carregar_atributos():
    global velocidade_personagem, intervalo_disparo, dano_person_hit, chance_critico, roubo_de_vida, quantidade_roubo_vida,vida_maxima,vida_maxima_petro,vida,xp_petro,Petro_active,trembo,dano_petro,Resistencia,Resistencia_petro,dano_inimigo_longe,dano_inimigo_perto
    with open('atributos.json', 'r') as file:
        atributos = json.load(file)
        velocidade_personagem = atributos["velocidade_personagem"]
        intervalo_disparo = atributos["intervalo_disparo"]
        dano_person_hit = atributos["dano_person_hit"]
        chance_critico = atributos["chance_critico"]
        roubo_de_vida = atributos["roubo_de_vida"]
        quantidade_roubo_vida = atributos["quantidade_roubo_vida"]
        
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



def calcular_cor_barra_de_vida(porcentagem_vida):
    if porcentagem_vida > 80:
        return (0, 255, 0)  # Verde
    elif porcentagem_vida > 55:
        return (173, 255, 47)  # Verde amarelado
    elif porcentagem_vida > 40:
        return (255, 165, 0)  # Laranja
    elif porcentagem_vida > 30:
        return (255, 69, 0)  # Laranja avermelhado
    else:
        return (255, 0, 0)  # Vermelho


def desenhar_barra_de_vida(surface, x, y, largura_total, altura, vida_atual, vida_maxima):
    porcentagem_vida = (vida_atual / vida_maxima) * 100
    cor_barra = calcular_cor_barra_de_vida(porcentagem_vida)
    largura_vida = int(largura_total * (vida_atual / vida_maxima))
    borda = pygame.Rect(x, y, largura_total, altura)
    barra = pygame.Rect(x, y, largura_vida, altura)
    pygame.draw.rect(surface, (0, 0,0), borda, 2)  # Borda branca
    pygame.draw.rect(surface, cor_barra, barra)  # Cor variável

    
    
def renderizar_cartas_compradas(tela):
    pos_x = largura_tela // 2 - (len(cartas_compradas) * 100) // 2  # centraliza as cartas
    pos_y = altura_tela - 90  # ajuste a altura conforme necessário

    for nome, quantidade in cartas_compradas.items():
        if quantidade > 0:  # Apenas renderiza cartas compradas
            # Renderiza a imagem da carta
            imagem_carta = cartas_imagens[nome]
            tela.blit(imagem_carta, (pos_x, pos_y))
            
            # Renderiza a quantidade de cartas compradas
            fonte = pygame.font.SysFont('Texto/Doctor Glitch.otf', 20)
            texto = fonte.render(str(quantidade), True, (0, 0, 0))  # Cor do texto em branco
            tela.blit(texto, (pos_x + 30, pos_y + 70))  # Ajuste a posição do texto conforme necessário
            
            # Atualiza a posição X para a próxima carta
            pos_x += 50  # Espaço entre as cartas   
    
    
    
def desenhar_barra_de_vida_petro(surface, vida_petro, pos_x, pos_y,vida_maxima_petro):
    # Calculando a largura da barra de vida
    largura_barra_petro = 30 # Ajuste conforme necessário
    altura_barra_petro = 10     # Ajuste conforme necessário
    
    # Calculando a porcentagem de vida restante
    porcentagem_vida_petro = vida_petro / vida_maxima_petro
    
    
    # Desenhando a parte preenchida da barra de vida (marrom)
    barra_preenchida = pygame.Rect(pos_x, pos_y, largura_barra_petro * porcentagem_vida_petro, altura_barra_petro)
    pygame.draw.rect(surface, (139, 69, 19), barra_preenchida)
    
    # Desenhando a borda da barra de vida (preta)
    pygame.draw.rect(surface, (0, 0, 0), (pos_x, pos_y, largura_barra_petro, altura_barra_petro), 2)    
    

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
    
    
    global personagem_doente, tempo_ultimo_atingido

    # Se o personagem estiver imóvel, não atualize a posição
    if personagem_doente:
        if keys[pygame.K_a]:
            pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + velocidade_personagem)
            direcao_atual = 'right'
            ultima_tecla_movimento = 'right'
            movimento_pressionado = True
        elif keys[pygame.K_d]:
            pos_x_personagem = max(0, pos_x_personagem - velocidade_personagem)
            direcao_atual = 'left'
            ultima_tecla_movimento = 'left'
            movimento_pressionado = True
        elif keys[pygame.K_w]:
            pos_y_personagem =min(altura_mapa - altura_personagem, pos_y_personagem + velocidade_personagem)
            direcao_atual = 'down'
            ultima_tecla_movimento = 'down'
            movimento_pressionado = True
        elif keys[pygame.K_s]:
            pos_y_personagem = max(0, pos_y_personagem - velocidade_personagem)
            direcao_atual = 'up'
            ultima_tecla_movimento = 'up'
            movimento_pressionado = True
        if personagem_doente:
            return

        elif keys[pygame.K_LSHIFT] and not cooldown_dash:
         # Animação de teletransporte
            teleporte_timer += velocidade_personagem
            if teleporte_timer >= teleporte_duration:
                teleporte_index = (teleporte_index + 1) % len(teleporte_sprites)
                teleporte_timer = 0

    # Verificar movimento do teclado
    if keys[pygame.K_a]:
        pos_x_personagem = max(0, pos_x_personagem - velocidade_personagem)
        direcao_atual = 'left'
        ultima_tecla_movimento = 'left'
        movimento_pressionado = True
    elif keys[pygame.K_d]:
        pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + velocidade_personagem)
        direcao_atual = 'right'
        ultima_tecla_movimento = 'right'
        movimento_pressionado = True
    elif keys[pygame.K_w]:
        pos_y_personagem = max(0, pos_y_personagem - velocidade_personagem)
        direcao_atual = 'up'
        ultima_tecla_movimento = 'up'
        movimento_pressionado = True
    elif keys[pygame.K_s]:
        pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + velocidade_personagem)
        direcao_atual = 'down'
        ultima_tecla_movimento = 'down'
        movimento_pressionado = True
    elif keys[pygame.K_LSHIFT] and not cooldown_dash:
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
        
    elif keys[pygame.K_SPACE]:
        
        direcao_atual = 'disp'
        
        
        

    else:
        direcao_atual = 'stop'

    # Atualização do cooldown do dash
    if cooldown_dash and pygame.time.get_ticks() - tempo_ultimo_dash > tempo_cooldown_dash:
        cooldown_dash = False
    

    # Verificar movimento do joystick
    if joystick:
        joystick_x = joystick.get_axis(0)
        joystick_y = joystick.get_axis(1)

        if joystick_x > 0.5:
            pos_x_personagem = min(largura_mapa - largura_personagem, pos_x_personagem + velocidade_personagem)
            direcao_atual = 'right'
            ultima_tecla_movimento = 'right'
            movimento_pressionado = True
        elif joystick_x < -0.5:
            pos_x_personagem = max(0, pos_x_personagem - velocidade_personagem)
            direcao_atual = 'left'
            ultima_tecla_movimento = 'left'
            movimento_pressionado = True

        if joystick_y > 0.5:
            pos_y_personagem = min(altura_mapa - altura_personagem, pos_y_personagem + velocidade_personagem)
            direcao_atual = 'down'
            ultima_tecla_movimento = 'down'
            movimento_pressionado = True
        elif joystick_y < -0.5:
            pos_y_personagem = max(0, pos_y_personagem - velocidade_personagem)
            direcao_atual = 'up'
            ultima_tecla_movimento = 'up'
            movimento_pressionado = True

    # Verificar botões do joystick para teletransporte
    if joystick and joystick.get_button(0) and not cooldown_dash:
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



# Antes do loop principal, crie uma lista para armazenar os inimigos
inimigos_comum = []

tempo_ultima_criacao_gelo = pygame.time.get_ticks()



def criar_disparo_inimigo(pos_inimigo, pos_personagem):
    dx = pos_personagem[0] - pos_inimigo[0]
    dy = pos_personagem[1] - pos_inimigo[1]
    dist = max(1, math.sqrt(dx ** 2 + dy ** 2))

    # Ajuste a velocidade do projétil dos inimigos conforme necessário
    velocidade_disparo_inimigo = 1.6  # Ajuste conforme necessário
    direcao_disparo_inimigo = (dx / dist * velocidade_disparo_inimigo, dy / dist * velocidade_disparo_inimigo)

    return {"rect": pygame.Rect(pos_inimigo[0], pos_inimigo[1], largura_disparo, altura_disparo), "velocidade": direcao_disparo_inimigo}
dobro_pontuacao = 15  # Quantidade de pontos necessários para dobrar a pontuação e adicionar mais inimigos
pontuacao_dobro = dobro_pontuacao  # Inicializa a pontuação necessária para dobrar a pontuação

def verificar_colisao_disparo_inimigo(pos_disparo, pos_inimigo, largura_disparo, altura_disparo, largura_inimigo, altura_inimigo,inimigos_eliminados):
    rect_disparo = pygame.Rect(pos_disparo[0], pos_disparo[1], largura_disparo, altura_disparo)
    rect_inimigo = pygame.Rect(pos_inimigo[0], pos_inimigo[1], largura_inimigo, altura_inimigo)
    
    return rect_disparo.colliderect(rect_inimigo)


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


tempo_ultimo_disparo = pygame.time.get_ticks()


Som_tema_fases.play(loops=-1)
Musica_tema_fases.play(loops=-1)

FPS=pygame.time.Clock()
###################################################################################################PRINCIPAL#################################################################################################################
#LOOP PRINCIPAL
running = True
while running:
    
    if carregar_atributos_na_fase:
        
        carregar_atributos_na_fase=False
    
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    
    atualizar_posicao_personagem(keys,joystick)

    

    novos_inimigos = []
    novos_disparos = []
    inimig_atin=[]

    for inimigo in inimigos_comum:
        inimigo_rect = inimigo["rect"]
        inimigo_image = inimigo["image"]

        inimigo_atingido = False

        for disparo in disparos:
            
            if verificar_colisao_disparo_inimigo(disparo, (inimigo["rect"].x, inimigo["rect"].y), largura_disparo, altura_disparo, largura_inimigo3, altura_inimigo3,inimigos_eliminados):
                if random.random() <= chance_critico:  # 10% de chance de dano crítico
                    dano = dano_person_hit * 3  # Valor do dano crítico é 3 vezes o dano normal
                    cor = (255, 255, 0)  # Amarelo (RGB)
                    fonte_dano=fonte_dano_critico
                else:
                    dano = dano_person_hit
                    cor = (255, 0, 0)  # Vermelho (RGB)
                    fonte_dano=fonte_dano_normal
                    
                # Renderize o texto do dano
                texto_dano = fonte_dano.render("-" + str(int(dano)), True, cor)
                    
                # Desenhe o texto na tela perto do chefe
                pos_texto = (inimigo["rect"].x + largura_inimigo3 // 2 - texto_dano.get_width() // 2,  inimigo["rect"].y - 20)
                            
                # Rastreie o tempo de exibição do texto
                tempo_texto_dano = pygame.time.get_ticks()
                inimigo["vida"] -= dano
                disparos.remove(disparo)  # Remover o disparo após colisão
                if Poison_Active:
                    inimigo["veneno"] = {
                        "dano_por_tick": inimigo["vida_maxima"] * Dano_Veneno_Acumulado,  # 0.5% da vida máxima
                        "tempo_inicio": pygame.time.get_ticks(),
                        "duracao": 4000,  # 4 segundos
                        "ultimo_tick": pygame.time.get_ticks(),  # Tempo do último tick
                        "posicao_texto": (inimigo["rect"].x, inimigo["rect"].y - 20),  # Posição inicial do texto
                        "tempo_texto_dano": pygame.time.get_ticks()  # Tempo de exibição do texto
                        }


                if random.random() < roubo_de_vida:
                    vida += (vida_maxima-vida)*quantidade_roubo_vida+50

                if inimigo["vida"] <= 0:
                    # Se a vida do inimigo é menor ou igual a zero, remover o inimigo
                    inimigos_comum.remove(inimigo)
                    vida_inimigo_maxima+=23
                    Resistencia_petro+=24.5
                    dano_inimigo_perto+=15
                    dano_person_hit+=5
                    vida_maxima_petro+=35
                    dano_petro+=0.015
                    dano_inimigo_longe+=7
                   
                    inimigos_eliminados += 1
                    pontuacao += 100
                    pontuacao_exib+=100
                    if vida_petro < (vida_maxima_petro*0.6):
                            vida_petro+=(vida_maxima_petro*0.4)
                    if not boss_vivo4:
                        if vida_boss4>0:
                            vida_boss4+=800
                            vida_maxima_boss4= vida_boss4   
                    break  # Sai do loop interno para evitar problemas ao modificar a lista enquanto iteramos sobre ela
                

        if inimigo_atingido:
            break  # Sair do loop externo se um inimigo foi atingido
    

    
        if pontuacao_exib > pontuacao_magia:
            pontuacao_magia = min(pontuacao_exib, maxima_pontuacao_magia)

        

    def criar_disparo():
        return {"rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_disparo, altura_disparo),"direcao": ultima_tecla_movimento }

    # Adicionar um novo disparo quando a tecla de espaço é pressionada
    tempo_atual = pygame.time.get_ticks()
    if (keys[pygame.K_SPACE] or (joystick and joystick.get_button(2))) and movimento_pressionado and tempo_atual - tempo_ultimo_disparo >= intervalo_disparo:
        Disparo_Geo.play()
        if ultima_tecla_movimento is not None:
            pos_x_disparo = pos_x_personagem + largura_personagem // 1 - largura_disparo // 1
            pos_y_disparo = pos_y_personagem + altura_personagem // 1 - altura_disparo // 1
            disparos.append((pos_x_disparo, pos_y_disparo, ultima_tecla_movimento))
            tempo_ultimo_disparo = tempo_atual  # Atualizar o tempo do último disparo
   

    tempo_passado += relogio.get_rawtime()
    relogio.tick()

     # Adicionar inimigos a cada 10 segundos
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_ultimo_inimigo >= 1000 and len(inimigos_comum) < max_inimigos2 :
        
        tempo_ultimo_inimigo = tempo_atual  # Atualizar o tempo do último inimigo adicionado
        
        

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
    

    # Desenha a personagem
    if not personagem_doente:
        tela.blit(frames_animacao[direcao_atual][frame_atual], (pos_x_personagem, pos_y_personagem))
    else:
        tela.blit(imagem_personagem_doente, (pos_x_personagem, pos_y_personagem))


    if trembo:
        # Desenhar o segundo personagem ao lado do personagem original
        pos_x_segundo_personagem = pos_x_personagem + largura_personagem + 4
        pos_y_segundo_personagem = pos_y_personagem
        tela.blit(frames_animacao_trembo[direcao_atual][frame_atual], (pos_x_segundo_personagem, pos_y_segundo_personagem))
    


    if Petro_active:
                        
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
                        
                    
                    
        if Boss_vivo3:
            # Define a direção de Petro em relação ao boss
            dx = pos_x_chefe3 - pos_x_petro
            dy = pos_y_chefe3 - pos_y_petro

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
            distancia_petro_boss = math.sqrt((pos_x_petro - pos_x_chefe3) ** 2 + (pos_y_petro - pos_y_chefe3) ** 2)
            if distancia_petro_boss <= 50:
                # Verifica se passou tempo suficiente desde o último dano
                tempo_atual_petro = pygame.time.get_ticks()
                if tempo_atual_petro - tempo_anterior_petro >= intervalo_dano_petro:
                    # Aplica dano ao "boss"
                    vida_petro -= int(dano_inimigo_perto)
                    vida_boss3-= int(dano_person_hit*0.25)+300
                    # Aqui você pode adicionar outras ações relacionadas ao dano ao "boss"
                    tempo_anterior_petro = tempo_atual_petro
  
         
        if comando_direção_petro:
            direcao_atual_petro="left_petro"
            comando_direção_petro=False
         
            
        desenhar_barra_de_vida_petro(tela, vida_petro, pos_x_petro, pos_y_petro - 20,vida_maxima_petro)  # Ajuste a posição conforme necessário
        tela.blit(petro_nivel[direcao_atual_petro][frame_atual], (pos_x_petro, pos_y_petro)) 




    
    # Desenhar os disparos normais
    novos_disparos = []
    for disparo in disparos:
        pos_x_disparo, pos_y_disparo, direcao_disparo = disparo
        tela.blit(frames_disparo[frame_atual_disparo], (pos_x_disparo, pos_y_disparo))

        # Atualizar a posição do disparo
        if direcao_disparo == 'up':
            pos_y_disparo -= velocidade_disparo
        elif direcao_disparo == 'down':
            pos_y_disparo += velocidade_disparo
        elif direcao_disparo == 'left':
            pos_x_disparo -= velocidade_disparo
        elif direcao_disparo == 'right':
            pos_x_disparo += velocidade_disparo

        # Adicionar o disparo à lista se não atingir o final do mapa
        if (
            0 <= pos_x_disparo < largura_mapa and
            0 <= pos_y_disparo < altura_mapa
        ):
            novos_disparos.append((pos_x_disparo, pos_y_disparo, direcao_disparo))

    disparos = novos_disparos

    frame_atual_disparo = (frame_atual_disparo + 1) % len(frames_disparo3)

    

    # loop principal, onde o inimigo é desenhado:
    for inimigo in inimigos_comum:
        dx = pos_x_personagem - inimigo["rect"].x
        dy = pos_y_personagem - inimigo["rect"].y
        dist = max(40, abs(dx) + abs(dy))
        inimigo["rect"].x += (dx / dist) * 0.85
        inimigo["rect"].y += (dy / dist) * 0.75 

        # Atualize os frames do inimigo com base na direção
        if dx > 0:  # Mova para a direita
            inimigo["image"] = frames_inimigo_direita3[frame_atual % len(frames_inimigo_direita3)]
        else:  # Mova para a esquerda
            inimigo["image"] = frames_inimigo_esquerda3[frame_atual % len(frames_inimigo_esquerda3)]

        tela.blit(inimigo["image"], inimigo["rect"])
        desenhar_barra_de_vida(tela, inimigo["rect"].x, inimigo["rect"].y - 10, largura_inimigo3, 5, inimigo["vida"], inimigo["vida_maxima"])
    
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_disparo_inimigo >= intervalo_disparo_inimigo and random.random() <= 0.01:  #frequencia do disparo do sinimigos
            disparos_inimigos.append(criar_disparo_inimigo((inimigo["rect"].x, inimigo["rect"].y), (pos_x_personagem, pos_y_personagem)))
            tempo_ultimo_disparo_inimigo = tempo_atual  # Atualize o tempo do último disparo


    personagem_rect = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
    inimigos_rects = [inimigo["rect"] for inimigo in inimigos_comum]

    if imune_tempo_restante > 0:
        imune_tempo_restante -= relogio.get_time()  # Reduz o tempo de imunidade com base no tempo de quadro
    else:
        imune_tempo_restante = 0  # Redefine a imunidade

    
    if verificar_colisao_personagem_inimigo(personagem_rect, inimigos_rects) and imune_tempo_restante <= 0:
        
        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            Dano_pos_resistencia_person = int((vida_maxima * 0.25) - Resistencia)
            if Dano_pos_resistencia_person > 0:
                vida -= Dano_pos_resistencia_person
            tempo_ultimo_hit_inimigo = tempo_atual
            
            piscando_vida = True




    # Verifica colisão entre disparos dos inimigos e personagem
    novos_disparos_inimigos = []
    for disparo_inimigo in disparos_inimigos:
        pos_x_disparo_inimigo, pos_y_disparo_inimigo = disparo_inimigo["rect"].x, disparo_inimigo["rect"].y
        tela.blit(frames_disparo3[frame_atual_disparo], (pos_x_disparo_inimigo, pos_y_disparo_inimigo))

        # Atualize a posição do disparo do inimigo
        disparo_inimigo["rect"].x += disparo_inimigo["velocidade"][0]
        disparo_inimigo["rect"].y += disparo_inimigo["velocidade"][1]



        if (
            pos_x_personagem < pos_x_disparo_inimigo < pos_x_personagem + largura_personagem and
            pos_y_personagem < pos_y_disparo_inimigo < pos_y_personagem + altura_personagem
        ):
            # O disparo do inimigo atingiu o personagem
            
            if not personagem_doente:
                Dano_pos_resistencia_person_longe=int((vida_maxima*0.35+dano_inimigo_longe)-Resistencia)
                        
                if Dano_pos_resistencia_person_longe < 0:
                    pass
                else:  
                    vida -=Dano_pos_resistencia_person_longe
                tempo_ultimo_hit_inimigo = tempo_atual  # Atualize o tempo do último hit do inimigo
                # esta parte para iniciar o piscar da barra de vida
                tempo_ultimo_atingido = pygame.time.get_ticks()
                
                
                personagem_doente = True  # O personagem está imóvel após ser atingido
                disparos_inimigos.remove(disparo_inimigo)
            continue
            # Lógica para controle da imobilização
        tempo_atual = pygame.time.get_ticks()
        if personagem_doente and tempo_atual - tempo_ultimo_atingido >= tempo_doente:
            personagem_doente = False  # A personagem volta a poder se mexer
            
        # Adicione o disparo à lista se não atingir o final do mapa
        if (
            0 <= pos_x_disparo_inimigo < largura_mapa and
            0 <= pos_y_disparo_inimigo < altura_mapa
        ):
            novos_disparos_inimigos.append(disparo_inimigo)

    # Atualiza a lista de disparos dos inimigos
    disparos_inimigos = novos_disparos_inimigos



    if vida <= 0:
        if trembo:
            vida = vida_maxima  # Recupera a vida total
            trembo = False  # Consome o "trembo"
            imune_tempo_restante = 10000
            teleportado = True  # Ativa o teleporte aleatório

           
            pos_x_personagem, pos_y_personagem = gerar_posicao_aleatoria(largura_mapa, altura_mapa, largura_personagem, altura_personagem)
        else:
       
            pygame.time.delay(2000)
            Musica_tema_fases.stop()
            Som_tema_fases.stop()
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

        # verificação para parar o piscar depois de um tempo
        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            piscando_vida = False

    tempo_atual = pygame.time.get_ticks()

    if vida_boss3 <=0:
        Boss_vivo3=False


    if Boss_vivo3:

        if pontuacao >= 100500 or (keys[pygame.K_r]) or r_press:
            r_press=True
            Musica_tema_fases.stop()
            max_inimigos2=9
            if musica_boss3 == 1:
                # Defina o volume da música (opcional)
                Musica_tema_Boss3.play(loops=-1)
                musica_boss3+=1

            spawn_inimigo=False
            personagem_doente = False
       
            pygame.draw.rect(tela, vermelho, (pos_x_barra_boss3, pos_y_barra_boss3, largura_barra_boss3, altura_barra_boss3))
            pygame.draw.rect(tela, (224,190,1), (pos_x_barra_boss3, pos_y_barra_boss3, largura_barra_boss3, (vida_boss3 /  vida_base3) * altura_barra_boss3))
            pygame.draw.rect(tela, (255, 255, 255), (pos_x_barra_boss3, pos_y_barra_boss3, largura_barra_boss3, altura_barra_boss3), 2)
            if not Boss_andando:

                # Verificar se é hora de alternar os frames do boss
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_frame_boss >= 500:
                    if boss_frame_atual == boss_frame1:
                        boss_frame_atual = boss_frame2
                    else:
                        boss_frame_atual = boss_frame1
                    tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_atual, (pos_x_chefe3, pos_y_chefe3))




            for disparo in disparos:
                pos_x_disparo, pos_y_disparo, direcao_disparo = disparo
                rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                rect_boss = pygame.Rect(pos_x_chefe3, pos_y_chefe3, chefe_largura3, chefe_altura3)

                if rect_disparo.colliderect(rect_boss):
                    if vida_boss3 > 0:  # Verifica se o chefe está vivo antes de aplicar dano
                        if random.random() <= chance_critico:  # 10% de chance de dano crítico
                            dano = dano_person_hit * 3  # Valor do dano crítico é 3 vezes o dano normal
                            cor = (255, 255, 0)  # Amarelo (RGB)
                        else:
                            dano = dano_person_hit
                            cor = (255, 0, 0)  # Vermelho (RGB)
                    
                        # Renderize o texto do dano
                        texto_dano = fonte_dano_critico.render("-" + str(int(dano)), True, cor)
                        
                        # Desenhe o texto na tela perto do chefe
                        pos_texto = (pos_x_chefe3 + chefe_largura3 // 2 - texto_dano.get_width() // 2, pos_y_chefe3 - 20)
                                
                        # Rastreie o tempo de exibição do texto
                        tempo_texto_dano = pygame.time.get_ticks()
                        vida_boss3-=dano
                        disparos.remove(disparo)  # Remover o disparo após colisão
                        # Adicionar uma chance de 50% de aumentar a vida em 20 pontos
                        if random.random() < roubo_de_vida:

                            vida += int((vida_maxima-vida)*quantidade_roubo_vida)

            






            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_grupo_disparo_boss3 >= tempo_espera_grupo_disparo_boss3 and not queijo_spawn:  # Verifique se passou 1 segundo
                # Reinicie o contador de disparos
                contador_disparos_boss3 = 0
                disparos_boss3.clear()  # Limpe a lista de disparos anteriores

            # Gere um grupo de 4 disparos
                for _ in range(4):
                    # Gere uma posição aleatória no canto direito da tela
                    pos_y_disparo_boss3 = random.randint(0, altura_tela - altura_disparo)
                    pos_x_disparo_boss3 = largura_tela  # Inicie o disparo no canto direito da tela
                    disparos_boss3.append((pos_x_disparo_boss3, pos_y_disparo_boss3, 'left'))  # 'left' indica que o disparo vai para a esquerda

                # Atualize o tempo do último grupo de disparos do boss
                tempo_ultimo_grupo_disparo_boss3 = tempo_atual  # Atualize o tempo do último grupo de disparos do boss

            # Atualize a posição dos disparos do boss3 antes de desenhá-los
            novos_disparos_boss3 = []
            for disparo in disparos_boss3:
                pos_x_disparo, pos_y_disparo, direcao_disparo = disparo

                # Atualize a posição do disparo
                if direcao_disparo == 'right':
                    pos_x_disparo += 3
                elif direcao_disparo == 'left':
                    pos_x_disparo -= 3

                # Adicione o disparo à lista se não atingir o final do mapa
                if 0 <= pos_x_disparo < largura_mapa:
                    novos_disparos_boss3.append((pos_x_disparo, pos_y_disparo, direcao_disparo))

                # Limpe a lista de disparos anteriores e atualize para os novos disparos
            disparos_boss3 = novos_disparos_boss3

            # Desenhe os disparos atualizados na tela
            for disparo in disparos_boss3:
                pos_x_disparo, pos_y_disparo, _ = disparo
                tela.blit(sprite_disparo_boss3, (pos_x_disparo, pos_y_disparo))


            for disparo in disparos_boss3:
                pos_x_disparo, pos_y_disparo, _ = disparo
                rect_disparo_boss = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                rect_personagem = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)

                if rect_disparo_boss.colliderect(rect_personagem):
                    Frascos.play()
                    vida -= int(vida_maxima*0.25)+450
                    disparos_boss3.remove(disparo)  # Remova o disparo após colisão
        
        
    #PRIMEIRA GERAÇÂO QUEIJO MESTRE
        if vida_boss3 <= 0.9 * vida_base3 and queijo_geracao==1:
            if  not queijo_spawn:
                
                pos_x_queijo = random.randint(area_x_min, area_x_max)
                pos_y_queijo = random.randint(area_y_min, area_y_max)

            queijo_spawn = True
            tela.blit(sprite_queijo, (pos_x_queijo, pos_y_queijo))

            
            if queijo_spawn:
                # Calcule o vetor de direção do chefe para o queijo
                vetor_direcao = (pos_x_queijo - pos_x_chefe3, pos_y_queijo - pos_y_chefe3)
                # Normalize o vetor de direção para manter uma velocidade constante
                comprimento_vetor = max(1, math.sqrt(vetor_direcao[0] ** 2 + vetor_direcao[1] ** 2))
                vetor_direcao_normalizado = (vetor_direcao[0] / comprimento_vetor, vetor_direcao[1] / comprimento_vetor)
                # Defina a velocidade do chefe
                velocidade_chefe = 0.8
                #   Atualize a posição do chefe em direção ao queijo
                pos_x_chefe3 += vetor_direcao_normalizado[0] * velocidade_chefe
                pos_y_chefe3 += vetor_direcao_normalizado[1] * velocidade_chefe
                # Verifique se o boss chegou ao queijo
                distancia_para_queijo = math.sqrt((pos_x_queijo - pos_x_chefe3) ** 2 + (pos_y_queijo - pos_y_chefe3) ** 2)
                # Alternar entre os frames da animação de locomoção do inimigo
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_frame_boss >= 300:
                    
                    if boss_frame_andando == boss_frame_andando1:
                        boss_frame_andando= boss_frame_andando2
                    else:
                        boss_frame_andando = boss_frame_andando1
                    tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_andando, (pos_x_chefe3, pos_y_chefe3))

                # Defina uma distância de tolerância para considerar que o chefe alcançou o queijo
                distancia_tolerancia = 10
                if distancia_para_queijo < distancia_tolerancia:
                    # O chefe chegou ao queijo, volte para a posição inicial
                    pos_x_chefe3 = largura_tela / 1.3
                    pos_y_chefe3 = altura_tela / 3
                    vida_boss3 += int(vida_base3-vida_boss3)*0.3
                    if vida_boss3 > vida_base3:
                        vida_base3=vida_boss3
                    # Resetar a variável que indica se o queijo está presente
                    queijo_spawn = False

                for disparo in disparos:
                    # Verifique a colisão entre o disparo e o queijo
                    rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                    rect_queijo_hitbox = pygame.Rect(pos_x_queijo - 10, pos_y_queijo - 10, largura_hitbox_queijo, altura_hitbox_queijo)
                    if rect_disparo.colliderect(rect_queijo_hitbox):
                        # Reduza a vida do queijo com base no dano do disparo
                        vida_queijo -= 5
                        # Remova o disparo
                        disparos.remove(disparo)
                        # Verifique se a vida do queijo chegou a zero
                        if vida_queijo <= 5:
                            queijo_geracao+=1
                            queijo_spawn=False
                            pos_x_chefe3 = largura_tela / 1.3
                            pos_y_chefe3 = altura_tela / 3
                            vida_queijo=50

    #SEGUNDA GERAÇÂO QUEIJO MESTRE
        if vida_boss3 <= 0.6 * vida_base3 and queijo_geracao==2:
            if not queijo_spawn:
                
                pos_x_queijo = random.randint(area_x_min, area_x_max)
                pos_y_queijo = random.randint(area_y_min, area_y_max)
            queijo_spawn = True
            tela.blit(sprite_queijo, (pos_x_queijo, pos_y_queijo))

            
            if queijo_spawn:
                # Calcule o vetor de direção do chefe para o queijo
                vetor_direcao = (pos_x_queijo - pos_x_chefe3, pos_y_queijo - pos_y_chefe3)
                # Normalize o vetor de direção para manter uma velocidade constante
                comprimento_vetor = max(1, math.sqrt(vetor_direcao[0] ** 2 + vetor_direcao[1] ** 2))
                vetor_direcao_normalizado = (vetor_direcao[0] / comprimento_vetor, vetor_direcao[1] / comprimento_vetor)
                # Defina a velocidade do chefe
                velocidade_chefe = 1
                #   Atualize a posição do chefe em direção ao queijo
                pos_x_chefe3 += vetor_direcao_normalizado[0] * velocidade_chefe
                pos_y_chefe3 += vetor_direcao_normalizado[1] * velocidade_chefe
                # Verifique se o boss chegou ao queijo
                distancia_para_queijo = math.sqrt((pos_x_queijo - pos_x_chefe3) ** 2 + (pos_y_queijo - pos_y_chefe3) ** 2)
                # Alternar entre os frames da animação de locomoção do inimigo
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_frame_boss >= 300:
                    
                    if boss_frame_andando == boss_frame_andando1:
                        boss_frame_andando= boss_frame_andando2
                    else:
                        boss_frame_andando = boss_frame_andando1
                    tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_andando, (pos_x_chefe3, pos_y_chefe3))

                # Defina uma distância de tolerância para considerar que o chefe alcançou o queijo
                distancia_tolerancia = 10
                if distancia_para_queijo < distancia_tolerancia:
                    # O chefe chegou ao queijo, volte para a posição inicial
                    pos_x_chefe3 = largura_tela / 1.3
                    pos_y_chefe3 = altura_tela / 3
                    vida_boss3 += int(vida_base3-vida_boss3)*0.5
                    if vida_boss3 > vida_base3:
                        vida_base3=vida_boss3
                    # Resetar a variável que indica se o queijo está presente
                    queijo_spawn = False

                for disparo in disparos:
                    # Verifique a colisão entre o disparo e o queijo
                    rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                    rect_queijo_hitbox = pygame.Rect(pos_x_queijo - 10, pos_y_queijo - 10, largura_hitbox_queijo, altura_hitbox_queijo)
                    if rect_disparo.colliderect(rect_queijo_hitbox):
                        # Reduza a vida do queijo com base no dano do disparo
                        vida_queijo -= 5
                        # Remova o disparo
                        disparos.remove(disparo)
                        # Verifique se a vida do queijo chegou a zero
                        if vida_queijo <= 5:
                            queijo_geracao+=1
                            queijo_spawn=False
                            pos_x_chefe3 = largura_tela / 1.3
                            pos_y_chefe3 = altura_tela / 3
                            vida_queijo=40

    #Terceira GERAÇÂO QUEIJO MESTRE
        if vida_boss3 <= 0.4 * vida_base3 and queijo_geracao==3:
            if not queijo_spawn:
                
                pos_x_queijo = random.randint(area_x_min, area_x_max)
                pos_y_queijo = random.randint(area_y_min, area_y_max)
            queijo_spawn = True
            tela.blit(sprite_queijo, (pos_x_queijo, pos_y_queijo))

            
            if queijo_spawn:
                # Calcule o vetor de direção do chefe para o queijo
                vetor_direcao = (pos_x_queijo - pos_x_chefe3, pos_y_queijo - pos_y_chefe3)
                # Normalize o vetor de direção para manter uma velocidade constante
                comprimento_vetor = max(1, math.sqrt(vetor_direcao[0] ** 2 + vetor_direcao[1] ** 2))
                vetor_direcao_normalizado = (vetor_direcao[0] / comprimento_vetor, vetor_direcao[1] / comprimento_vetor)
                # Defina a velocidade do chefe
                velocidade_chefe = 1.2
                #   Atualize a posição do chefe em direção ao queijo
                pos_x_chefe3 += vetor_direcao_normalizado[0] * velocidade_chefe
                pos_y_chefe3 += vetor_direcao_normalizado[1] * velocidade_chefe
                # Verifique se o boss chegou ao queijo
                distancia_para_queijo = math.sqrt((pos_x_queijo - pos_x_chefe3) ** 2 + (pos_y_queijo - pos_y_chefe3) ** 2)
                # Alternar entre os frames da animação de locomoção do inimigo
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_frame_boss >= 300:
                    
                    if boss_frame_andando == boss_frame_andando1:
                        boss_frame_andando= boss_frame_andando2
                    else:
                        boss_frame_andando = boss_frame_andando1
                    tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_andando, (pos_x_chefe3, pos_y_chefe3))

                # Defina uma distância de tolerância para considerar que o chefe alcançou o queijo
                distancia_tolerancia = 10
                if distancia_para_queijo < distancia_tolerancia:
                    # O chefe chegou ao queijo, volte para a posição inicial
                    pos_x_chefe3 = largura_tela / 1.3
                    pos_y_chefe3 = altura_tela / 3
                    vida_boss3 += int(vida_base3-vida_boss3)*0.6
                    if vida_boss3 > vida_base3:
                        vida_base3=vida_boss3
                    # Resetar a variável que indica se o queijo está presente
                    queijo_spawn = False

                for disparo in disparos:
                    # Verifique a colisão entre o disparo e o queijo
                    rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                    rect_queijo_hitbox = pygame.Rect(pos_x_queijo - 10, pos_y_queijo - 10, largura_hitbox_queijo, altura_hitbox_queijo)
                    if rect_disparo.colliderect(rect_queijo_hitbox):
                        # Reduza a vida do queijo com base no dano do disparo
                        vida_queijo -= 5
                        # Remova o disparo
                        disparos.remove(disparo)
                        # Verifique se a vida do queijo chegou a zero
                        if vida_queijo <= 5:
                            queijo_geracao+=1
                            queijo_spawn=False
                            pos_x_chefe3 = largura_tela / 1.3
                            pos_y_chefe3 = altura_tela / 3
                            vida_queijo=40
    #Quarta GERAÇÂO QUEIJO MESTRE
        if vida_boss3 <= 0.4 * vida_base3 and queijo_geracao==3:
            if not queijo_spawn:
                
                pos_x_queijo = random.randint(area_x_min, area_x_max)
                pos_y_queijo = random.randint(area_y_min, area_y_max)
            queijo_spawn = True
            tela.blit(sprite_queijo, (pos_x_queijo, pos_y_queijo))

            
            if queijo_spawn:
                # Calcule o vetor de direção do chefe para o queijo
                vetor_direcao = (pos_x_queijo - pos_x_chefe3, pos_y_queijo - pos_y_chefe3)
                # Normalize o vetor de direção para manter uma velocidade constante
                comprimento_vetor = max(1, math.sqrt(vetor_direcao[0] ** 2 + vetor_direcao[1] ** 2))
                vetor_direcao_normalizado = (vetor_direcao[0] / comprimento_vetor, vetor_direcao[1] / comprimento_vetor)
                # Defina a velocidade do chefe
                velocidade_chefe = 1.4
                #   Atualize a posição do chefe em direção ao queijo
                pos_x_chefe3 += vetor_direcao_normalizado[0] * velocidade_chefe
                pos_y_chefe3 += vetor_direcao_normalizado[1] * velocidade_chefe
                # Verifique se o boss chegou ao queijo
                distancia_para_queijo = math.sqrt((pos_x_queijo - pos_x_chefe3) ** 2 + (pos_y_queijo - pos_y_chefe3) ** 2)
                # Alternar entre os frames da animação de locomoção do inimigo
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_frame_boss >= 300:
                    
                    if boss_frame_andando == boss_frame_andando1:
                        boss_frame_andando= boss_frame_andando2
                    else:
                        boss_frame_andando = boss_frame_andando1
                    tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_andando, (pos_x_chefe3, pos_y_chefe3))

                # Defina uma distância de tolerância para considerar que o chefe alcançou o queijo
                distancia_tolerancia = 10
                if distancia_para_queijo < distancia_tolerancia:
                    # O chefe chegou ao queijo, volte para a posição inicial
                    pos_x_chefe3 = largura_tela / 1.3
                    pos_y_chefe3 = altura_tela / 3
                    vida_boss3 += int(vida_base3-vida_boss3)*0.7
                    if vida_boss3 > vida_base3:
                        vida_base3=vida_boss3
                    # Resetar a variável que indica se o queijo está presente
                    queijo_spawn = False

                for disparo in disparos:
                    # Verifique a colisão entre o disparo e o queijo
                    rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                    rect_queijo_hitbox = pygame.Rect(pos_x_queijo - 10, pos_y_queijo - 10, largura_hitbox_queijo, altura_hitbox_queijo)
                    if rect_disparo.colliderect(rect_queijo_hitbox):
                        # Reduza a vida do queijo com base no dano do disparo
                        vida_queijo -= 5
                        # Remova o disparo
                        disparos.remove(disparo)
                        # Verifique se a vida do queijo chegou a zero
                        if vida_queijo <= 5:
                            queijo_geracao+=1
                            queijo_spawn=False
                            pos_x_chefe3 = largura_tela / 1.3
                            pos_y_chefe3 = altura_tela / 3
                            vida_queijo=40
    #Quinta GERAÇÂO QUEIJO MESTRE
        if vida_boss3 <= 0.4 * vida_base3 and queijo_geracao==3:
            if not queijo_spawn:
                
                pos_x_queijo = random.randint(area_x_min, area_x_max)
                pos_y_queijo = random.randint(area_y_min, area_y_max)
            queijo_spawn = True
            tela.blit(sprite_queijo, (pos_x_queijo, pos_y_queijo))

            
            if queijo_spawn:
                # Calcule o vetor de direção do chefe para o queijo
                vetor_direcao = (pos_x_queijo - pos_x_chefe3, pos_y_queijo - pos_y_chefe3)
                # Normalize o vetor de direção para manter uma velocidade constante
                comprimento_vetor = max(1, math.sqrt(vetor_direcao[0] ** 2 + vetor_direcao[1] ** 2))
                vetor_direcao_normalizado = (vetor_direcao[0] / comprimento_vetor, vetor_direcao[1] / comprimento_vetor)
                # Defina a velocidade do chefe
                velocidade_chefe = 1.3
                #   Atualize a posição do chefe em direção ao queijo
                pos_x_chefe3 += vetor_direcao_normalizado[0] * velocidade_chefe
                pos_y_chefe3 += vetor_direcao_normalizado[1] * velocidade_chefe
                # Verifique se o boss chegou ao queijo
                distancia_para_queijo = math.sqrt((pos_x_queijo - pos_x_chefe3) ** 2 + (pos_y_queijo - pos_y_chefe3) ** 2)
                # Alternar entre os frames da animação de locomoção do inimigo
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - tempo_ultimo_frame_boss >= 300:
                    
                    if boss_frame_andando == boss_frame_andando1:
                        boss_frame_andando= boss_frame_andando2
                    else:
                        boss_frame_andando = boss_frame_andando1
                    tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_andando, (pos_x_chefe3, pos_y_chefe3))

                # Defina uma distância de tolerância para considerar que o chefe alcançou o queijo
                distancia_tolerancia = 10
                if distancia_para_queijo < distancia_tolerancia:
                    # O chefe chegou ao queijo, volte para a posição inicial
                    pos_x_chefe3 = largura_tela / 1.3
                    pos_y_chefe3 = altura_tela / 3
                    vida_boss3 += int(vida_base3-vida_boss3)*1
                    if vida_boss3 > vida_base3:
                        vida_base3=vida_boss3
                    # Resetar a variável que indica se o queijo está presente
                    queijo_spawn = False

                for disparo in disparos:
                    # Verifique a colisão entre o disparo e o queijo
                    rect_disparo = pygame.Rect(pos_x_disparo, pos_y_disparo, largura_disparo, altura_disparo)
                    rect_queijo_hitbox = pygame.Rect(pos_x_queijo - 10, pos_y_queijo - 10, largura_hitbox_queijo, altura_hitbox_queijo)
                    if rect_disparo.colliderect(rect_queijo_hitbox):
                        # Reduza a vida do queijo com base no dano do disparo
                        vida_queijo -= 10
                        # Remova o disparo
                        disparos.remove(disparo)
                        # Verifique se a vida do queijo chegou a zero
                        if vida_queijo <= 5:
                            queijo_geracao+=1
                            queijo_spawn=False
                            pos_x_chefe3 = largura_tela / 1.3
                            pos_y_chefe3 = altura_tela / 3
                            vida_queijo=30



    if not Boss_vivo3:
        
            rect_boss = pygame.Rect(pos_x_chefe3, pos_y_chefe3, 64, 64)
            rect_personagem = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
            if tempo_atual - tempo_ultimo_frame_boss >= 300:
                if boss_frame_peca == boss_frame_peca1:
                    boss_frame_peca= boss_frame_peca2
                else:
                    boss_frame_peca = boss_frame_peca1
                tempo_ultimo_frame_boss = tempo_atual
                tela.blit(boss_frame_peca, (pos_x_chefe3, pos_y_chefe3))
            
            if rect_boss.colliderect(rect_personagem):
                if toque == 0:
                    salvar_atributos()
                    Musica_tema_Boss3.stop()
                    import GAME4
                    toque+=1

    # Verifica se a pontuação atingiu 1500 e se o jogador pressionou 'Q'
    if pontuacao_exib >= 700 and (keys[config_teclas["Comprar na loja"]] or (joystick and joystick.get_button(3))):
        pontuacao_exib-=700
        pontuacao_magia-=700
        
        
        ret = tela_de_pausa(velocidade_personagem, intervalo_disparo,vida,largura_disparo, altura_disparo,trembo,dano_person_hit,chance_critico,roubo_de_vida,
                            quantidade_roubo_vida,tempo_cooldown_dash,vida_maxima,Petro_active,Resistencia,vida_petro,vida_maxima_petro,dano_petro,xp_petro,petro_evolucao,Resistencia_petro,
                            Chance_Sorte,Poison_Active,Dano_Veneno_Acumulado,Executa_inimigo,Ultimo_Estalo,mostrar_info,Mercenaria_Active,Valor_Bonus,dispositivo_ativo)
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
    
    
        


    

    posicao_barra_vida = (80, altura_mapa - (altura_mapa - 34))
    fonte = pygame.font.Font(None, int(altura_barra_vida*1))
    texto_pontuacao = fonte.render(f'{pontuacao_exib}', True, (250, 255,255))
    fonte_vida = pygame.font.Font(None, int(altura_barra_vida*0.9))
    texto_vida = fonte_vida.render(f'{int(vida)}/{int(vida_maxima)}', True, (255, 255, 255))

    # Renderiza o texto de pontuação com uma borda
    texto_pontuacao_borda = fonte.render(f'{pontuacao_exib}', True, (0, 0, 0))  # Cor preta para a borda
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
    for inimigo in inimigos_comum:
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
    if area_cartas.collidepoint(pos_x_personagem, pos_y_personagem):  # Supondo que você tenha as posições x e y do personagem
        cartas_visiveis = False  # Se o personagem está na área, esconda as cartas
    else:
        cartas_visiveis = True  # Se o personagem não está na área, mostre as cartas
    if cartas_visiveis:
        renderizar_cartas_compradas(tela)
    # Se o cooldown estiver ativo, mostre-o na tela

    # Remova o texto após 2 segundos
    if texto_dano is not None and pygame.time.get_ticks() - tempo_texto_dano >= 250:
        texto_dano = None

    # Desenhe o texto na tela
    if texto_dano is not None:
        tela.blit(texto_dano, pos_texto)


    pygame.display.flip()
    FPS.tick(100)  # Limita a 60 FPS


# Encerrar o Pygame
pygame.quit()
sys.exit()