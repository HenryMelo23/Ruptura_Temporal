import tkinter as tk
root = tk.Tk()
import pygame
import random
import sys
import time
import math
from Config_Teclas import  carregar_config_teclas
config_teclas = carregar_config_teclas()

# Crie uma janela tkinter (não será exibida)
pygame.font.init()
relogio = pygame.time.Clock()
# Configurações do mapa
mapa_path1 = "Sprites/Fase1.png"
mapa_path2 = "Sprites/Fase2.png"
mapa_path3 = "Sprites/Fase3.png"
mapa_path4 = "Sprites/Fase4.png"
python = sys.executable
cooldown_ativo_img = pygame.transform.scale(pygame.image.load("Sprites/cooldown2.png"), (50, 50))
cooldown_concluido_img = pygame.transform.scale(pygame.image.load("Sprites/cooldown.png"), (50, 50))
r_press=False
dispositivo_ativo = "teclado"



########################################## VARIAVEIS MAPA
cont=1
if cont ==1:
    largura_tela, altura_tela = int(1360*0.8), int(768*1)
    largura_mapa, altura_mapa = largura_tela, altura_tela
    cont+=1
centro_horizontal_tela = largura_mapa // 2
espacamento = 100
########################################## BOSS 1
chefe_largura, chefe_altura = largura_tela * 0.2, altura_tela * 0.2
pos_x_chefe, pos_y_chefe = largura_mapa // 2 - chefe_largura // 2, altura_mapa // 2 - chefe_altura // 2
tempo_animacao_chefe = 300  # Tempo em milissegundos entre cada quadro
tempo_passado_animacao_chefe = 0
frame_atual_chefe = 0
frames_chefe1_1 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss1.png"), (chefe_largura, chefe_altura)),
    pygame.transform.scale(pygame.image.load("Sprites/Boss2.png"), (chefe_largura, chefe_altura))
]
frames_chefe1_2 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss3.png"), (chefe_largura, chefe_altura)),
    pygame.transform.scale(pygame.image.load("Sprites/Boss4.png"), (chefe_largura, chefe_altura))
]
frames_chefe1_3 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss5.png"), (chefe_largura, chefe_altura)),
    pygame.transform.scale(pygame.image.load("Sprites/Boss6.png"), (chefe_largura, chefe_altura))
]
frames_chefe1_4 = [
    pygame.transform.scale(pygame.image.load("Sprites/peça.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load("Sprites/peça2.png"), (32, 32))
]

tempo_ultima_mudanca_direcao_boss = pygame.time.get_ticks()
# Defina uma variável de estado para controlar o comportamento do chefe
comportamento_boss = "aleatorio"  # Comece com movimento aleatório
ultima_direcao_boss = 'aleatorio'
Velocidade_boss=2
ultima_direcao_boss = random.choice(['up', 'down', 'left', 'right'])  # Inicialize a direção do boss   

####################### Variáveis para o ataque do boss
ataque_boss_paths = ["Sprites/Hit1.png", "Sprites/Hit2.png", "Sprites/Hit3.png"]
largura_ataque_boss, altura_ataque_boss = 60, 60
frames_ataque_boss = [pygame.transform.scale(pygame.image.load(path), (largura_ataque_boss, altura_ataque_boss)) for path in ataque_boss_paths]
ataques_boss = []
tempo_ultimo_ataque_boss = pygame.time.get_ticks()
intervalo_ataque_boss = 3500  # Intervalo entre ataques em milissegundos
tempo_ataque_boss = 0
duracao_frame_ataque_boss = 3500  # Duração de cada frame em milissegundos
tempo_ultimo_dano_atingido = pygame.time.get_ticks()
intervalo_dano_atingido = 1500  # 2 segundos

vida_boss = 85000
vida_maxima_boss1= vida_boss
largura_barra_boss = 20
altura_barra_boss = 200
pos_x_barra_boss = largura_mapa - 30
pos_y_barra_boss = altura_tela // 2 - altura_barra_boss // 2
Zona_quant=10

########################################## BOSS 2

chefe_largura2, chefe_altura2 = largura_tela * 0.2, altura_tela * 0.3
pos_x_chefe2, pos_y_chefe2 = largura_mapa // 1.1 - chefe_largura // 2, altura_mapa // 2 - chefe_altura // 1
tempo_animacao_chefe2 = 1000  # Tempo em milissegundos entre cada quadro
tempo_passado_animacao_chefe2 = 0
frame_atual_chefe = 0
frames_chefe2_1 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss2_1.png"), (chefe_largura2, chefe_altura2)),
    pygame.transform.scale(pygame.image.load("Sprites/Boss2_2.png"), (chefe_largura2, chefe_altura2))
]
frames_chefe2_2 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss2_1.png"), (chefe_largura2, chefe_altura2)),
    pygame.transform.scale(pygame.image.load("Sprites/Boss2_2.png"), (chefe_largura2, chefe_altura2))
]
frames_chefe2_3 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss2_1.png"), (chefe_largura2, chefe_altura2)),
    pygame.transform.scale(pygame.image.load("Sprites/Boss2_2.png"), (chefe_largura2, chefe_altura2))
]

frames_chefe2_4 = [
    pygame.transform.scale(pygame.image.load("Sprites/peça.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load("Sprites/peça2.png"), (32, 32))
]
frame_porcentagem=frames_chefe2_1
boss_vivo2=True
vida_boss2 = 100000
vida_maxima_boss2= vida_boss2
largura_barra_boss2 = 20
altura_barra_boss2 = 200
pos_x_barra_boss2 = largura_mapa - 30
pos_y_barra_boss2 = altura_tela // 4 - altura_barra_boss // 1.3

########################################## BOSS 4
boss_vivo4=True
zonas_nulas = []
contador_colisoes = 0
vida_planeta=150
# Organizando os frames do Boss em uma lista
chefe_largura4, chefe_altura4 = largura_tela * 0.2, altura_tela * 0.3
frames_chefe4_1 = [
    pygame.transform.scale(pygame.image.load("Sprites/Boss4_1.png"), (chefe_largura4, chefe_altura4)), 
    pygame.transform.scale(pygame.image.load("Sprites/Boss4_3.png"), (chefe_largura4, chefe_altura4))
]


frames_vortex = [
    pygame.image.load("Sprites/Vortex1_1.png"),
    pygame.image.load("Sprites/Vortex1_2.png")
]

sprite_disparo_boss = [
    pygame.transform.scale(pygame.image.load("Sprites/Planet1_1.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("Sprites/Planet1_2.png"), (100, 100))
]

# Índice do frame atual da galáxia
indice_frame_vortex = 0

# Tempo de troca de frame da galáxia
intervalo_frame_vortex = 500  # Troca a cada 500 ms


estado_boss_atacando = False
tempo_ataque = 0  
current_frame_index = 0

boss_rect = frames_chefe4_1[current_frame_index].get_rect()

boss_rect.center = (largura_tela - boss_rect.width // 2, altura_tela // 2)

last_frame_change = pygame.time.get_ticks()
frame_interval = 1000 



current_frame_disparo_boss = 0
tempo_frame_disparo_boss = 0  # Para controlar a troca de frames
intervalo_frame_disparo_boss = 200  # Intervalo em milissegundos

projetil_lista = []

ultimo_disparo = pygame.time.get_ticks()
intervalo_disparo_Boss_4 = 6000 



vida_boss4 = 130000
vida_maxima_boss4 = vida_boss4
largura_barra_boss4 = 20
altura_barra_boss4 = 200
pos_x_barra_boss4 = largura_mapa - 30
pos_y_barra_boss4 = altura_tela // 2 - altura_barra_boss4 // 2
def calcular_posicao_boss(boss_rect):
    # Posição central do Boss
    pos_x_boss = boss_rect.centerx
    pos_y_boss = boss_rect.centery
    return pos_x_boss, pos_y_boss

tempo_ultimo_dano_vortex = 0 


# Altura e quantidade de sprites
altura_sprite_disparo_boss2 = 10
quantidade_sprites_boss2 = 16
linha = pygame.image.load("Sprites/Onda_Boss2.png")
ataque_vertical_ativo = False
posicao_ataque_vertical = (0, 0)
velocidade_ataque_vertical = 2  
tempo_espera_ataque = 3000  # Tempo em milissegundos (1 segundo)
tempo_cooldown_dano_vertical = 1000  # Tempo de cooldown em milissegundos
tempo_ultimo_dano_vertical = pygame.time.get_ticks()  # Inicializa o tempo do último dano
largura_ataque_vertical = 20 
altura_ataque_vertical = 100 

tempo_inicio_dano_horizontal= pygame.time.get_ticks()  # Inicializa o tempo do último dano

tempo_ultimo_dano_horizontal = pygame.time.get_ticks()  # Inicializa o tempo do último dano
ataque_horizontal_ativo = False
tempo_cooldown_dano_horizontal = 1000  # Tempo de cooldown em milissegundos
posicao_ataque_horizontal = (0, 0)
velocidade_ataque_horizontal = 1
tempo_inicio_ataque_horizontal = 0
altura_ataque_horizontal=20
# Inicialize as variáveis relacionadas ao tempo antes do loop principal do jogo
tempo_inicio_ataque_vertical = 0
tempo_inicio_ataque_horizontal = 0

############################################ Boss 3
vida_boss3 = 200000
vida_maxima_boss3=vida_boss3
largura_barra_boss3 = 20
altura_barra_boss3 = 200
pos_x_barra_boss3 = largura_mapa - 30
pos_y_barra_boss3 = altura_tela // 4 - altura_barra_boss // 1.3
Boss_vivo3=True


#########################################  Condicionais
# Variável para armazenar a pontuação
pontuacao = 0
pontuacao_exib=700
pontuacao_magia=0
vida_maxima = 450
vida = vida_maxima  # Valor inicial da vida
largura_barra_vida = int(root.winfo_screenwidth()*0.095)
altura_barra_vida = 20
posicao_circulo = (20, altura_mapa * 0.09)  # mesma posição da barra de magia
raio_circulo = int(largura_mapa * 0.025)  # ajustando o tamanho do círculo
centro_circulo = (posicao_circulo[0] + raio_circulo, posicao_circulo[1] + raio_circulo)
imagem_relogio = pygame.image.load("Sprites/relogio.png")
imagem_relogio = pygame.transform.scale(imagem_relogio, (raio_circulo * 2.6, raio_circulo * 2.6))  
posicao_imagem_relogio = (13, altura_mapa * 0.074) 
Executa_inimigo=0.05
Ultimo_Estalo=False
imagem_vida=pygame.image.load("Sprites/vida.png")
imagem_vida = pygame.transform.scale(imagem_vida, (largura_mapa* 0.25, altura_mapa*0.20))
posicao_vida = (13, -40)  
Chance_Sorte=0
Poison_Active=False
boss_envenenado = False
dano_por_tick_veneno_boss = 0
tempo_inicio_veneno_boss = 0
ultimo_tick_veneno_boss = 0
duracao_veneno_boss = 4000 
fonte_hit= "Texto/breakaway.ttf"
#Fonte para tipos de dano
fonte_dano_normal = pygame.font.Font(fonte_hit, 26)
fonte_dano_critico = pygame.font.Font(fonte_hit, 43)
fonte_veneno = pygame.font.Font(fonte_hit, 26)
Dano_Veneno_Acumulado=0.05
tab_pressionado = False
#########################################  CORES_GERAIS

amarelo= (255, 255, 0)
vermelho=(255, 0, 0)
verde=(0, 255, 0)
azul = (0, 0, 255)

######################################### INIMIGOS_COMUNS
intervalo_hit_inimigo = 700  
inimigos_atingidos_por_onda = {}
if largura_tela == 1366:
    vel_inimig= 1  # Ajuste a velocidade conforme necessário
elif largura_tela == 1920:
    vel_inimig= 1
elif largura_tela <= 1360:
    vel_inimig= 1
Velocidade_Inimigos_1=1.3
max_inimigos=6
max_inimigos2=4
max_inimigos3=5
max_inimigos4=4
distancia_minima_inimigos = 50  # Ajuste conforme necessário
largura_inimigo, altura_inimigo = largura_tela*0.05, altura_tela*0.08
frames_inimigo = [pygame.transform.scale(pygame.image.load("Sprites/inimig1.png"), (largura_inimigo, altura_inimigo)),
                 pygame.transform.scale(pygame.image.load("Sprites/inimig2.png"), (largura_inimigo, altura_inimigo))]

frames_inimigo2=[pygame.transform.scale(pygame.image.load("Sprites/inimig3.png"), (100, 100)),
                 pygame.transform.scale(pygame.image.load("Sprites/inimig4.png"), (102, 102))]




frames_inimigo_esquerda2 = [pygame.transform.scale(pygame.image.load("Sprites/inimigo_direita2-1.png"), (largura_inimigo, altura_inimigo)),
                           pygame.transform.scale(pygame.image.load("Sprites/inimigo_direita2-2.png"), (largura_inimigo, altura_inimigo))]
frames_inimigo_direita2 = [pygame.transform.scale(pygame.image.load("Sprites/inimigo_esquerda2-1.png"), (largura_inimigo, altura_inimigo)),
                          pygame.transform.scale(pygame.image.load("Sprites/inimigo_esquerda2-2.png"), (largura_inimigo, altura_inimigo))]


######################################### PERSONAGEM
direcao_atual = 'stop'  # Direção inicial
largura_personagem, altura_personagem = largura_tela*0.05, altura_tela*0.08
pos_x_personagem, pos_y_personagem = 100, 100
Resistencia=35
xp_petro=1
dano_inimigo_perto=30
velocidade_personagem = 1.5
intervalo_disparo = 800
dano_person_hit=25
chance_critico=0.02
roubo_de_vida=0
quantidade_roubo_vida=0.10
queijo_geracao=1
dano_boss=90
dano_inimigo_longe=24
largura_onda, altura_onda = 70, 120  
velocidade_onda = 3
tempo_ultimo_uso_habilidade = 0
cooldown_habilidade = 10000  # Cooldown de 3 segundos
ondas = []
duracao_frame_onda = 100
eliminacoes_consecutivas = 0
bonus_pontuacao = 0
Mercenaria_Active = False
Valor_Bonus=25



frames_onda_cinetica = [
    pygame.image.load(f"Sprites/Habilit_{i}.png") for i in range(1, 8)
]
frames_onda_cinetica = [
    pygame.transform.scale(frame, (largura_onda, altura_onda)) for frame in frames_onda_cinetica
]

personagem_paths = {
    'up': ["Sprites/Geo1-up.png", "Sprites/Geo2-up.png"],
    'down': ["Sprites/Geo1-Down.png", "Sprites/Geo2-Down.png"],
    'left': ["Sprites/Geo1-Esq.png", "Sprites/Geo2-Esq.png"],
    'right': ["Sprites/Geo1-Dir.png", "Sprites/Geo2-Dir.png"],
    'stop': ["Sprites/Geo1-somb.png", "Sprites/Geo2-somb.png"],
    'disp' :["Sprites/Geo_Disp1.png", "Sprites/Geo_Disp2.png"]
}

trembo_paths = {
    'up': ["Sprites/trembo_costa1.png", "Sprites/trembo_costa1.png"],
    'down': ["Sprites/trembo_frente1.png", "Sprites/trembo_frente2.png"],
    'left': ["Sprites/trembo_esquerda1.png", "Sprites/trembo_esquerda2.png"],
    'right': ["Sprites/trembo_direita1.png", "Sprites/trembo_direita2.png"],
    'stop': ["Sprites/trembo_stop1.png", "Sprites/trembo_stop2.png"],
    'shift':["Sprites/inimig1.png", "Sprites/Geo2.png"],
    'disp':["Sprites/trembo_stop1.png", "Sprites/trembo_stop2.png"]
}

Petro_paths = {
    'up_petro': ["Sprites/Petro_nivel1_up1.png", "Sprites/Petro_nivel1_up2.png"],
    'down_petro': ["Sprites/Petro_nivel1_esq1.png", "Sprites/Petro_nivel1_esq2.png"],
    'left_petro': ["Sprites/Petro_nivel1_esq1.png", "Sprites/Petro_nivel1_esq2.png"],
    'right_petro': ["Sprites/Petro_nivel1_dir1.png", "Sprites/Petro_nivel1_dir2.png"],
    'stop_petro': ["Sprites/Petro_nivel1_stop1.png", "Sprites/Petro_nivel1_stop2.png", "Sprites/Petro_nivel1_stop3.png"],
    
}

Petro_paths2 = {
    'up_petro': ["Sprites/Petro_nivel1_up1.png", "Sprites/Petro_nivel1_up2.png"],
    'down_petro': ["Sprites/Petro_nivel1_esq1.png", "Sprites/Petro_nivel1_esq2.png"],
    'left_petro': ["Sprites/Petro_nivel2_esq1.png", "Sprites/Petro_nivel2_esq2.png"],
    'right_petro': ["Sprites/Petro_nivel2_dir1.png", "Sprites/Petro_nivel2_dir2.png"],
    'stop_petro': ["Sprites/Petro_nivel1_stop1.png", "Sprites/Petro_nivel1_stop2.png", "Sprites/Petro_nivel1_stop3.png"],
    
}

Petro_paths3 = {
    'up_petro': ["Sprites/Petro_nivel1_up1.png", "Sprites/Petro_nivel1_up2.png"],
    'down_petro': ["Sprites/Petro_nivel1_esq1.png", "Sprites/Petro_nivel1_esq2.png"],
    'left_petro': ["Sprites/Petro_nivel3_esq1.png", "Sprites/Petro_nivel3_esq2.png"],
    'right_petro': ["Sprites/Petro_nivel3_dir1.png", "Sprites/Petro_nivel3_dir2.png"],
    'stop_petro': ["Sprites/Petro_nivel1_stop1.png", "Sprites/Petro_nivel1_stop2.png", "Sprites/Petro_nivel1_stop3.png"],
    
}


Petro_active=False

tempo_animacao_stop = 700
tempo_animacao_no_stop = 300   # Tempo em milissegundos entre cada quadro
cooldown_dash = False
tempo_ultimo_dash = 0
tempo_cooldown_dash = 2800  #  segundos de cooldown
distancia_dash = 300

# Carregamento das imagens da animação de teletransporte
teleporte_sprites_original = [pygame.image.load('sprites/tele1.png'),
                     pygame.image.load('sprites/tele2.png'),
                     pygame.image.load('sprites/tele3.png')]
# Defina o tamanho desejado para a animação de teletransporte
teleporte_size = (largura_tela*0.05, altura_tela*0.08)
teleporte_sprites = [pygame.transform.scale(img, teleporte_size) for img in teleporte_sprites_original]

teleporte_index = 0
teleporte_duration = 500  # Duração de cada quadro da animação (em milissegundos)
teleporte_timer = 0
# ... Código existente ...


# Configurações do disparo
disparo_paths = ["Sprites/Fogo1.png", "Sprites/Fogo2.png"]
largura_disparo, altura_disparo = 40, 40

velocidade_disparo = 10
disparos = []


###Configuração personagens secundarios

largura_trembo,altura_trembo= largura_tela*0.08, altura_tela*0.11


# Carregar as sequências de imagens do personagem
frames_animacao = {direcao: [pygame.image.load(path) for path in paths] for direcao, paths in personagem_paths.items()}
frames_animacao = {direcao: [pygame.transform.scale(frame, (largura_personagem, altura_personagem)) for frame in frames] for direcao, frames in frames_animacao.items()}

# Adicionar uma entrada para 'stop' no dicionário
frames_animacao['stop'] = [pygame.image.load(path) for path in personagem_paths['stop']]
frames_animacao['stop'] = [pygame.transform.scale(frame, (largura_personagem, altura_personagem)) for frame in frames_animacao['stop']]


###############################################

# Carregar as sequências de imagens do trembo
frames_animacao_trembo = {direcao: [pygame.image.load(path) for path in paths] for direcao, paths in trembo_paths.items()}
frames_animacao_trembo = {direcao: [pygame.transform.scale(frame, (largura_trembo, altura_trembo)) for frame in frames] for direcao, frames in frames_animacao_trembo.items()}

# Adicionar uma entrada para 'stop' no dicionário
frames_animacao_trembo['stop'] = [pygame.image.load(path) for path in trembo_paths['stop']]
frames_animacao_trembo['stop'] = [pygame.transform.scale(frame, (largura_trembo, altura_trembo)) for frame in frames_animacao_trembo['stop']]


###############################################

############################################### PETRO
Resistencia_petro=50
petro_evolucao=1
vida_maxima_petro = 620
dano_petro=8
recuperacao_petro=15
pos_x_petro= pos_x_personagem + largura_personagem + 4
pos_y_petro = pos_y_personagem
tempo_anterior_petro = pygame.time.get_ticks()
tempo_ultima_atualizacao_direcao = pygame.time.get_ticks()
intervalo_dano_petro = 1000  # Intervalo de 1 segundo
vida_petro=vida_maxima_petro
largura_Petro,altura_Petro= largura_tela*0.03, altura_tela*0.05

comando_direção_petro=True


# Carregar as sequências de imagens do Petro
frames_animacao_Petro = {direcao: [pygame.image.load(path) for path in paths] for direcao, paths in Petro_paths.items()}
frames_animacao_Petro = {direcao: [pygame.transform.scale(frame, (largura_Petro, altura_Petro)) for frame in frames] for direcao, frames in frames_animacao_Petro.items()}

frames_animacao_Petro2 = {direcao: [pygame.image.load(path) for path in paths] for direcao, paths in Petro_paths2.items()}
frames_animacao_Petro2 = {direcao: [pygame.transform.scale(frame, (largura_tela*0.06, altura_tela*0.08)) for frame in frames] for direcao, frames in frames_animacao_Petro2.items()}

frames_animacao_Petro3 = {direcao: [pygame.image.load(path) for path in paths] for direcao, paths in Petro_paths3.items()}
frames_animacao_Petro3 = {direcao: [pygame.transform.scale(frame, (largura_tela*0.1, altura_tela*0.12)) for frame in frames] for direcao, frames in frames_animacao_Petro3.items()}

# Adicionar uma entrada para 'stop' no dicionário
frames_animacao_Petro['stop_petro'] = [pygame.image.load(path) for path in Petro_paths['stop_petro']]
frames_animacao_Petro['stop_petro'] = [pygame.transform.scale(frame, (largura_Petro, altura_Petro)) for frame in frames_animacao_Petro['stop_petro']]




###############################################



# Carregar as sequências de imagens do disparo
frames_disparo = [pygame.image.load(path) for path in disparo_paths]
frames_disparo = [pygame.transform.scale(frame, (largura_disparo, altura_disparo)) for frame in frames_disparo]

##FASE2
# Carregar a imagem da personagem quando está congelada
imagem_personagem_congelada = pygame.image.load("Sprites/congelada1.png")
imagem_personagem_congelada = pygame.transform.scale(imagem_personagem_congelada, (largura_personagem, altura_personagem))
cor_vida=verde



##############################      FUNÇÔES


def criar_ataque_boss():
    return {
        "rect": pygame.Rect(random.randint(0, largura_mapa - largura_ataque_boss), random.randint(0, altura_mapa - altura_ataque_boss), largura_ataque_boss, altura_ataque_boss),
        "image_index": 0,
        "tempo_inicio": pygame.time.get_ticks()
    }



#######################################################FASE 3


# Carregar a imagem da sprite do disparo do boss
sprite_disparo_boss3 = pygame.image.load('Sprites/disparo_boss3.png')  # Substitua 'sprite_disparo_boss.png' pelo caminho do seu arquivo de imagem
sprite_disparo_boss3 = pygame.transform.scale(sprite_disparo_boss3, (50, 50))  # Ajuste as dimensões conforme necessário




cegueira_1="Sprites/cego.png"
disparo_paths_inimigo3 = ["Sprites/Disp_inimigo3_1.png", "Sprites/Disp_inimigo3_2.png"]
frames_disparo3 = [pygame.image.load(path) for path in disparo_paths_inimigo3]
frames_disparo3 = [pygame.transform.scale(frame, (largura_disparo, altura_disparo)) for frame in frames_disparo3]

largura_inimigo3, altura_inimigo3 = largura_tela*0.05, altura_tela*0.08
frames_inimigo_esquerda3 = [pygame.transform.scale(pygame.image.load("Sprites/inimigo_direita3-1.png"), (largura_inimigo, altura_inimigo)),
                           pygame.transform.scale(pygame.image.load("Sprites/inimigo_direita3-2.png"), (largura_inimigo, altura_inimigo))]
frames_inimigo_direita3 = [pygame.transform.scale(pygame.image.load("Sprites/inimigo_esquerda3-1.png"), (largura_inimigo, altura_inimigo)),
                          pygame.transform.scale(pygame.image.load("Sprites/inimigo_esquerda3-2.png"), (largura_inimigo, altura_inimigo))]
imagem_personagem_doente = pygame.image.load("Sprites/Doente.png")
imagem_personagem_doente = pygame.transform.scale(imagem_personagem_doente, (largura_personagem, altura_personagem))


#FASE 4
disparo_paths_inimigo4 = ["Sprites/Magia_inimigo1.png", "Sprites/Magia_inimigo2.png"]
frames_disparo4 = [pygame.image.load(path) for path in disparo_paths_inimigo4]
frames_disparo4 = [pygame.transform.scale(frame, (largura_disparo, altura_disparo)) for frame in frames_disparo4]

#FRAME DO INIMIGO NO GAME 4





frames_inimigo_esquerda4 = [pygame.transform.scale(pygame.image.load("Sprites/inimigo_direita4-1.png"), (largura_inimigo, altura_inimigo)),
                           pygame.transform.scale(pygame.image.load("Sprites/inimigo_direita4-2.png"), (largura_inimigo, altura_inimigo))]
frames_inimigo_direita4 = [pygame.transform.scale(pygame.image.load("Sprites/inimigo_esquerda4-1.png"), (largura_inimigo, altura_inimigo)),
                          pygame.transform.scale(pygame.image.load("Sprites/inimigo_esquerda4-2.png"), (largura_inimigo, altura_inimigo))]


##############################   SOBRE o DECK 3############################################################


# Defina as variáveis de posição do quadrado e texto
posicao_info_x = 0  # Deslocamento horizontal
posicao_info_y = -220  # Deslocamento vertical (levanta o quadrado)
icone_w=pygame.transform.scale(pygame.image.load("Sprites/W.png"), (largura_inimigo, altura_inimigo))
icone_x=pygame.transform.scale(pygame.image.load("Sprites/X.png"), (largura_inimigo, altura_inimigo))
trembo=False
mostrar_info = False
# Dicionário para armazenar as cartas compradas e suas quantidades
cartas_compradas = {
    "Speed Boost": 0,
    "Disparo crescente": 0,
    "Tempestade": 0,
    "Cura": 0,
    "Speed Atack": 0,
    "Teleporte": 0,
    "Petro": 0,
    "Defesa": 0,
    "Sorte": 0,
    "Poison":0,
    "Coletora":0,
}
cartas_imagens = {
    "Speed Boost": pygame.image.load('Sprites/Deck/Speed_boost1.png'),
    "Disparo crescente": pygame.image.load('Sprites/Deck/carta_odio1.png'),
    "Tempestade": pygame.image.load('Sprites/Deck/Carta_tempestade_crescente1.png'),
    "Cura": pygame.image.load('Sprites/Deck/Carta_roubo_vida1.png'),
    "Speed Atack": pygame.image.load('Sprites/Deck/carta_onda.png'),
    "Teleporte": pygame.image.load('Sprites/Deck/carta_teleporte1.png'),
    "Petro": pygame.image.load('Sprites/Deck/carta_petro1.png'),
    "Defesa": pygame.image.load('Sprites/Deck/carta_defesa1.png'),
    "Sorte": pygame.image.load('Sprites/Deck/carta_sorte1.png'),
    "Poison": pygame.image.load('Sprites/Deck/carta_poison1.png'),
    "Coletora": pygame.image.load('Sprites/Deck/carta_estalo1.png'),
}
cartas_disponiveis_nomes = [
    "Speed Boost", 
    "Disparo crescente", 
    "Tempestade", 
    "Cura", 
    "Speed Atack", 
    "Teleporte", 
    "Petro", 
    "Defesa",
    "Sorte",
    "Poison",
    "Coletora",
]
area_cartas = pygame.Rect(largura_tela // 4 - (len(cartas_compradas) * 100) // 2, altura_tela - 150, len(cartas_compradas) * 100, 100)
cartas_visiveis = True

#########################################################     Cronometro       ##################################################################
tempo_acumulado = 0      
tempo_inicial = time.time()  
cronometro_pausado = False   

# Função para formatar o tempo
def formatar_tempo(tempo_total):
    horas = int(tempo_total // 3600)
    minutos = int((tempo_total % 3600) // 60)
    segundos = int(tempo_total % 60)
    if horas > 0:
        return f"{horas:02}:{minutos:02}:{segundos:02}"
    else:
        return f"{minutos:02}:{segundos:02}"

# Função para atualizar o cronômetro
def atualizar_cronometro():
    if not cronometro_pausado:
        tempo_decorrido = time.time() - tempo_inicial + tempo_acumulado
        return formatar_tempo(tempo_decorrido)
    else:
        return formatar_tempo(tempo_acumulado)

# Função para pausar o cronômetro
def pausar_cronometro():
    global cronometro_pausado, tempo_acumulado
    if not cronometro_pausado:
        cronometro_pausado = True
        tempo_acumulado += time.time() - tempo_inicial

# Função para retomar o cronômetro em um novo script ou fase
def retomar_cronometro():
    global cronometro_pausado, tempo_inicial
    if cronometro_pausado:
        cronometro_pausado = False
        tempo_inicial = time.time()

# Função para exibir o cronômetro na tela
def exibir_cronometro(tela):
    tempo_exibido = atualizar_cronometro()
    fonte = pygame.font.Font(None, 36)
    
    # Renderizar o texto do cronômetro com contorno preto para contraste
    texto_contorno = fonte.render(tempo_exibido, True, (0, 0, 0))  
    texto_cronometro = fonte.render(tempo_exibido, True, (255, 255, 255)) 
    
    # Coordenadas do canto superior direito com uma margem de 10 pixels
    pos_x = largura_mapa - 100
    pos_y = 10
    
    # Desenhar o contorno em posições levemente deslocadas ao redor do texto principal
    tela.blit(texto_contorno, (pos_x - 1, pos_y))     # Esquerda
    tela.blit(texto_contorno, (pos_x + 1, pos_y))     # Direita
    tela.blit(texto_contorno, (pos_x, pos_y - 1))     # Cima
    tela.blit(texto_contorno, (pos_x, pos_y + 1))     # Baixo
    
    # Desenhar o texto principal no centro
    tela.blit(texto_cronometro, (pos_x, pos_y))

def criar_onda(posicao,ultima_tecla_movimento):
    return {
        "rect": pygame.Rect(posicao[0], posicao[1], largura_onda, altura_onda),  # Define a hitbox
        "direcao": ultima_tecla_movimento,  # Direção do movimento
        "frame_atual": 0,  # Frame inicial da animação
        "tempo_inicio": pygame.time.get_ticks()  # Para controlar os frames e o tempo de vida
    }
def rotacionar_frames(frames, angulo):
    return [pygame.transform.rotate(frame, angulo) for frame in frames]

def desenhar_habilidades(tela, cooldowns,dispositivo_ativo):
   
    if dispositivo_ativo == "teclado":
        tecla_disparo=  pygame.key.name(config_teclas["Disparar"])
        tecla_teleporte= pygame.key.name(config_teclas["Teleporte"])
        tecla_onda=  pygame.key.name(config_teclas["Onda"])
        tecla_loja=  pygame.key.name(config_teclas["Comprar na loja"])
    else:
        tecla_disparo=  "A"
        tecla_teleporte= "X"
        tecla_onda=  "B"
        tecla_loja=  "Y"

    habilidades = [
    ("disparo", tecla_disparo, icone_disparo_pronto, icone_disparo_recarga, cooldowns['disparo']),
    ("teleporte", tecla_teleporte, icone_teleporte_pronto, icone_teleporte_recarga, cooldowns['teleporte']),
    ("onda",tecla_onda, icone_onda_pronto, icone_onda_recarga, cooldowns['onda']),
    ("loja", tecla_loja, icone_loja, icone_loja_pronto, cooldowns['loja']),
    ]
    
    for i, (nome, tecla, icone_pronto, icone_recarga, cooldown) in enumerate(habilidades):
        x, y = posicoes_icones[i]
        
        # Escolher o ícone baseado no cooldown
        if cooldown is not None and cooldown > 0:
            icone = icone_recarga
        else:
            icone = icone_pronto
        
        # Desenhar o ícone
        tela.blit(icone, (x, y))
        
        cor_texto = (255, 255, 255)  # Branco para o texto principal
        cor_contorno = (0, 0, 0)    # Preto para o contorno
        
        # Desenhar a tecla acima do ícone com contorno
        fonte = pygame.font.Font(None, 20)
        render_texto_com_contorno(fonte, tecla.upper(), cor_texto, cor_contorno, x + icone_tamanho[0] // 10, y - 10, tela)

def render_texto_com_contorno(fonte, texto, cor_texto, cor_contorno, x, y, tela, deslocamento=2): #texto da interface
    """Renderiza texto com contorno."""
    texto_render = fonte.render(texto, True, cor_contorno)
    
    # Desenhar o contorno ao redor
    for dx, dy in [(-deslocamento, 0), (deslocamento, 0), (0, -deslocamento), (0, deslocamento),
                   (-deslocamento, -deslocamento), (-deslocamento, deslocamento),
                   (deslocamento, -deslocamento), (deslocamento, deslocamento)]:
        tela.blit(texto_render, (x + dx, y + dy))
    
    # Desenhar o texto principal
    texto_principal = fonte.render(texto, True, cor_texto)
    tela.blit(texto_principal, (x, y))

def desenhar_texto_com_contorno(surface, texto, fonte, cor_texto, cor_contorno, posicao): #TEXTO DE PONTOAÇÂO
    # Renderizar o texto duas vezes, uma para o contorno e outra para o texto em si
    texto_surface = fonte.render(texto, True, (255,0,0))
    texto_contorno = fonte.render(texto, True, cor_contorno)
    
    # Desenhar o contorno
    x, y = posicao
    surface.blit(texto_contorno, (x - 1, y))  # Esquerda
    surface.blit(texto_contorno, (x + 1, y))  # Direita
    surface.blit(texto_contorno, (x, y - 1))  # Acima
    surface.blit(texto_contorno, (x, y + 1))  # Abaixo

    # Desenhar o texto
    surface.blit(texto_surface, posicao)

def calcular_posicao_prevista(pos_x, pos_y, direcao, velocidade, tempo_previsao):
    if direcao == 'up':
        pos_y -= velocidade * tempo_previsao
    elif direcao == 'down':
        pos_y += velocidade * tempo_previsao
    elif direcao == 'left':
        pos_x -= velocidade * tempo_previsao
    elif direcao == 'right':
        pos_x += velocidade * tempo_previsao
    return pos_x, pos_y

def atualizar_movimento_inimigos(inimigos, pos_x_personagem, pos_y_personagem, direcao_jogador, velocidade_personagem, tempo_previsao):
    for inimigo in inimigos:
        # Calcular a posição prevista do jogador
        pos_prevista_x, pos_prevista_y = calcular_posicao_prevista(
            pos_x_personagem, pos_y_personagem, direcao_jogador, velocidade_personagem, tempo_previsao
        )
        
        # Calcular a direção para a posição prevista
        dx = pos_prevista_x - inimigo["rect"].x
        dy = pos_prevista_y - inimigo["rect"].y
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia > 0:  # Evitar divisão por zero
            inimigo["rect"].x += (dx / distancia) * Velocidade_Inimigos_1
            inimigo["rect"].y += (dy / distancia) * Velocidade_Inimigos_1

###################################################  SONS UNIVERSAIS ################################################

####################################################  CONFIG     ######################################################
tap_image = pygame.image.load("Sprites/Tab.png")
tap_image = pygame.transform.scale(tap_image, (64 ,64))
pos_x_tab = 20
pos_y_tab = 120
cor_contorno = (0, 0, 0)  # Preto para o contorno
config_teclas = carregar_config_teclas()
####################################################  Habilidades     ######################################################
icone_disparo_pronto = pygame.transform.scale(pygame.image.load("Sprites/icon_disp2.png"), (80, 80))
icone_teleporte_pronto = pygame.transform.scale( pygame.image.load("Sprites/icon_teleport2.png"), (80, 80))
icone_onda_pronto =  pygame.transform.scale(pygame.image.load("Sprites/icon_onda2.png"), (80, 80))
icone_loja =  pygame.transform.scale(pygame.image.load("Sprites/icon_loja.png"), (80, 80))
icone_abobora_pronto =  pygame.transform.scale(pygame.image.load("Sprites/icon_teste.png"), (80, 80))

# Ícones indisponíveis
icone_disparo_recarga = pygame.transform.scale(pygame.image.load("Sprites/icon_disp.png"), (80, 80))
icone_teleporte_recarga = pygame.transform.scale( pygame.image.load("Sprites/icon_teleport.png"), (80, 80))
icone_onda_recarga = pygame.transform.scale(pygame.image.load("Sprites/icon_onda.png"), (80, 80))
icone_loja_pronto = pygame.transform.scale(pygame.image.load("Sprites/icon_loja2.png"), (80, 80))
icone_abobora_recarga =  pygame.transform.scale(pygame.image.load("Sprites/icon_teste.png"), (80, 80))

# Redimensionar ícones (opcional)
icone_tamanho = (80, 80)
todos_icones = [
    icone_disparo_pronto, icone_teleporte_pronto, icone_onda_pronto, icone_loja, icone_abobora_pronto,
    icone_disparo_recarga, icone_teleporte_recarga, icone_onda_recarga, icone_abobora_recarga,
]
# Coordenadas dos ícones na parte inferior central
centro_tela = largura_mapa // 2.15
espacamento = 100  # Espaço entre os ícones
altura_base = altura_mapa - 100  # Margem inferior

posicoes_icones = [
    (centro_tela - 2 * espacamento, altura_base),
    (centro_tela - espacamento, altura_base),
    (centro_tela, altura_base),
    (centro_tela + espacamento, altura_base),
    (centro_tela + 2 * espacamento, altura_base),
]
area_icones = pygame.Rect(0, altura_tela - 100, largura_tela, 100)  # Exemplo: região inferior de 100px
