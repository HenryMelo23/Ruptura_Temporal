import pygame
import subprocess
import sys
import random
import math
import time
import os
import sys
import json
import threading
import queue
from Tela_Cartas_Coop import tela_de_pausa
from rede import iniciar_host, conectar_ao_host,fila_envio,fila_recebimento,thread_envio,thread_recebimento, anunciar_host_udp, descobrir_host_udp
from Variaveis import *
from utils import *
lock_inimigos = threading.Lock()


with open("modo_jogo.json", "r") as f:
    dados = json.load(f)
modo = dados["modo"]
ip = dados["ip"]


if modo == "host":
    anunciar_host_udp()  # LAN broadcast
    conn = iniciar_host()

elif modo == "join":
    ip_detectado = descobrir_host_udp()
    if ip_detectado:
        conn = conectar_ao_host(ip_detectado)
    else:
        pygame.quit()
        sys.exit()

# se não conectou, encerra

if conn is None:
    pygame.quit()
    sys.exit()

# inicia as threads de rede
threading.Thread(target=thread_envio, args=(conn,), daemon=True).start()
threading.Thread(target=thread_recebimento, args=(conn,), daemon=True).start()


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

def thread_atualizar_inimigos():
    global inimigos_comum, alvo_x, alvo_y, direcao_alvo, velocidade_personagem
    global movendo, tempo_anterior, tempo_movimento, tempo_parado
    ultimo_tempo = time.time()
    while True:
        agora = time.time()
        dt = agora - ultimo_tempo
        ultimo_tempo = agora
        if inimigos_comum:
            with lock_inimigos:
                try:
                    if movendo:
                        if tempo_atual - tempo_anterior >= tempo_movimento:
                            tempo_anterior = tempo_atual
                            movendo = False
                            tempo_movimento = random.randint(3000, 7000)
                        tempo_previsao = 5
                        atualizar_movimento_inimigos(
                            inimigos_comum, alvo_x, alvo_y, direcao_alvo, velocidade_personagem, tempo_previsao
                        )
                    else:
                        if tempo_atual - tempo_anterior >= tempo_parado:
                            tempo_anterior = tempo_atual
                            movendo = True
                            tempo_parado = random.randint(10, 3000)
                except Exception as e:
                    print("Erro na thread de inimigos:", e)
        time.sleep(0.01)

#Com o aumento de inimigos, o client apresentou lentidão já que com o aumento o envio de pacotes com a localização de inimigos aumenta e ficam pesados.
def thread_processar_pacotes():
    global inimigos_comum,frame_porcentagem
    global pos_x_player2, pos_y_player2, direcao_player2
    global jogador_remoto_morto, host_ativo, loja_aberta, esperando_client, boss_vivo1
    global quantidade_cartas, cor_ping, pontuacao_exib, convite_boss_aceitou, convite_boss_ativo, convite_boss_recebido, convite_boss_tempo, iniciar_boss, pos_x_chefe, pos_y_chefe
    while True:
        try:
            dados = fila_recebimento.get()
            if modo == "join" and "host_ready" in dados and dados["host_ready"]:
                esperando_client = False

            if modo == "host"  and "join_ready" in dados and dados["join_ready"]:
                esperando_host = False
            if "abrir_loja" in dados:
                if dados["abrir_loja"]:
                    quantidade_cartas = dados.get("quantidade_cartas", 1)  # Define a quantidade de cartas disponíveis
                    loja_aberta = True  # Define que a loja deve ser aberta no cliente
            if "pong" in dados:
                ping_atual = pygame.time.get_ticks() - dados["pong"]
                # Define a cor conforme o ping
                if ping_atual < 80:
                    cor_ping = (0, 255, 0)
                elif ping_atual < 160:
                    cor_ping = (255, 255, 0)
                else:
                    cor_ping = (255, 0, 0)

            if "pontuacao_atual" in dados:
                pontuacao_exib = dados["pontuacao_atual"]
                
            
            # --- Host convidou o boss ---
            if "convite_boss" in dados and dados["convite_boss"]:
                convite_boss_ativo = True
                convite_boss_recebido = True
                convite_boss_tempo = pygame.time.get_ticks()

            # --- Host mandou iniciar o boss ---
            if "iniciar_boss" in dados and dados["iniciar_boss"]:
                iniciar_boss = True
                convite_boss_ativo = False
            if "boss" in dados:
                boss_data = dados["boss"]
                pos_x_chefe = boss_data["x"]
                pos_y_chefe = boss_data["y"]
                vida_boss = boss_data["vida"]
                vida_maxima_boss1 = boss_data["vida_max"]
                boss_vivo1 = True

                # Define a sprite conforme a fase
                porcentagem_vida_boss = (vida_boss / vida_maxima_boss1) * 100
                if porcentagem_vida_boss >= 90:
                    frame_porcentagem = frames_chefe1_1
                elif 60 <= porcentagem_vida_boss < 90:
                    frame_porcentagem = frames_chefe1_2
                elif 40 <= porcentagem_vida_boss < 60:
                    frame_porcentagem = frames_chefe1_3
                else:
                    frame_porcentagem = frames_chefe1_4
            if "boss_morto" in dados and dados["boss_morto"]:
                boss_vivo1 = False
            if "crescimento_local" in dados:
                aplicar_crescimento_personalizado()
            if "drop_moeda" in dados:
                posicao_inimigo = dados["drop_moeda"]
                soltar_moeda(posicao_inimigo)

            if "p1" in dados:
                pos_x_player2 = dados["p1"]["x"]
                pos_y_player2 = dados["p1"]["y"]
                direcao_player2 = dados["p1"].get("direcao", "down")
                host_ativo = True  # Se o host enviou dados, o host está ativo
                if "morto" in dados["p1"]:
                    jogador_remoto_morto = dados["p1"]["morto"]
            # --- Recebe e sincroniza inimigos ---
            if "inimigos" in dados:
                inimigos_recebidos = dados["inimigos"]

                with lock_inimigos:
                    # Ajusta o tamanho da lista conforme o host
                    if len(inimigos_comum) < len(inimigos_recebidos):
                        # adiciona os que faltam
                        for i in range(len(inimigos_comum), len(inimigos_recebidos)):
                            novo = criar_inimigo(
                                inimigos_recebidos[i]["x"],
                                inimigos_recebidos[i]["y"]
                            )
                            novo["vida"] = inimigos_recebidos[i]["vida"]
                            novo["vida_maxima"] = inimigos_recebidos[i]["vida_max"]
                            inimigos_comum.append(novo)

                    elif len(inimigos_comum) > len(inimigos_recebidos):
                        # remove os que sobraram
                        inimigos_comum = inimigos_comum[:len(inimigos_recebidos)]

                    # Atualiza todos os inimigos existentes
                    for i, info in enumerate(inimigos_recebidos):
                        inimigos_comum[i]["rect"].x = info["x"]
                        inimigos_comum[i]["rect"].y = info["y"]
                        inimigos_comum[i]["vida"] = info["vida"]
                        inimigos_comum[i]["vida_maxima"] = info["vida_max"]



        except queue.Empty:
            continue
        except Exception as e:
            print("Erro ao processar pacote:", e)

if modo == "join":
    
    threading.Thread(target=thread_processar_pacotes, daemon=True).start()


inimigos_comum = []
#inicializa a Threading
if modo == "host" :
    tempo_anterior = pygame.time.get_ticks()
    tempo_movimento = random.randint(2000, 7000)
    tempo_parado = random.randint(500, 700) 
    movendo = True 
    threading.Thread(target=thread_atualizar_inimigos, daemon=True).start()


def gerar_posicao_aleatoria(largura_mapa, altura_mapa, largura_personagem, altura_personagem):
    largura_mapa_int, altura_mapa_int, largura_personagem_int, altura_personagem_int=map(int,(largura_mapa, altura_mapa, largura_personagem, altura_personagem))
    x = random.randint(0, largura_mapa_int - largura_personagem_int)
    y = random.randint(0, altura_mapa_int - altura_personagem_int)
    return x, y
    
def solicitar_boss(tela, fila_envio, modo):
    global convite_boss_recebido, convite_boss_ativo, convite_boss_aceitou, convite_boss_tempo
    fonte = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Se o jogador for host, ele inicia o convite com R
    if modo == "host":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            convite_boss_recebido = False
            convite_boss_ativo = True
            convite_boss_tempo = pygame.time.get_ticks()
            fila_envio.put({"convite_boss": True})
            

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if convite_boss_recebido and convite_boss_ativo:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        fila_envio.put({"resposta_boss": True})
                        convite_boss_aceitou = True
                        convite_boss_ativo = False
                    elif event.key == pygame.K_n:
                        fila_envio.put({"resposta_boss": False})
                        convite_boss_aceitou = False
                        convite_boss_ativo = False

        tela.fill((0, 0, 0))

        # --- Exibir status ---
        tela_rect = tela.get_rect()
        if convite_boss_ativo and not convite_boss_recebido:
            texto = fonte.render("Convite enviado: aguardando resposta...", True, (255, 255, 0))
            tela.blit(texto, (tela_rect.width - texto.get_width() - 30, 30))

        elif convite_boss_recebido and convite_boss_ativo:
            restante = 5 - int((pygame.time.get_ticks() - convite_boss_tempo) / 1000)
            texto = fonte.render(f"Boss solicitado! Aceitar? (Y/N) {restante}s", True, (255, 255, 255))
            tela.blit(texto, (tela_rect.width - texto.get_width() - 30, 30))
            if restante <= 0:
                fila_envio.put({"resposta_boss": False})
                convite_boss_aceitou = False
                convite_boss_ativo = False

        elif convite_boss_aceitou is True:
            return True
        elif convite_boss_aceitou is False:
            return False

        pygame.display.flip()
        clock.tick(30)


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
direcao_player2 = None
movimento_pressionado = False
#as seguintes variáveis para controle do tempo de hit do inimigo
tempo_ultimo_hit_inimigo = pygame.time.get_ticks()

piscando_vida = False
vida_inimigo_maxima=30
vida_inimigo= vida_inimigo_maxima


def tela_de_espera_host(tela, fila_envio, fila_recebimento):
    global esperando_host
    fonte = pygame.font.Font(None, 60)
    clock = pygame.time.Clock()
    esperando_host = True

    while esperando_host:
        tela.fill((15, 15, 15))
        texto = fonte.render("Aguardando o jogador entrar...", True, (255, 255, 255))
        sub = fonte.render("O jogo começará quando o cliente estiver pronto.", True, (180, 180, 180))
        tela.blit(texto, (tela.get_width()//2 - texto.get_width()//2, tela.get_height()//2 - 30))
        tela.blit(sub, (tela.get_width()//2 - sub.get_width()//2, tela.get_height()//2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # host envia o próprio estado de pronto
        fila_envio.put({"host_ready": True})

        # verifica se recebeu o join_ready do cliente
        try:
            while not fila_recebimento.empty():
                dados = fila_recebimento.get_nowait()
                if "join_ready" in dados and dados["join_ready"]:
                    
                    esperando_host = False
        except:
            pass

        clock.tick(30)

def tela_de_espera_client(tela, fila_envio, fila_recebimento):
    global esperando_client
    fonte = pygame.font.Font(None, 60)
    clock = pygame.time.Clock()
    esperando_client = True

    # o cliente envia uma única vez que está pronto
    fila_envio.put({"join_ready": True})

    while esperando_client:
        tela.fill((15, 15, 15))
        texto = fonte.render("Esperando o host iniciar...", True, (255, 255, 255))
        sub = fonte.render("O jogo começará em breve.", True, (180, 180, 180))
        tela.blit(texto, (tela.get_width()//2 - texto.get_width()//2, tela.get_height()//2 - 30))
        tela.blit(sub, (tela.get_width()//2 - sub.get_width()//2, tela.get_height()//2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # A thread processar_pacotes() vai alterar esperando_client = False
        clock.tick(30)




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

        if pygame.time.get_ticks() - tempo_ultimo_dash >= teleporte_duration // 2:
            teleporte_index = (teleporte_index + 1) % len(teleporte_sprites)
            tempo_ultimo_dash = pygame.time.get_ticks()

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
        if pygame.time.get_ticks() - tempo_ultimo_dash >= teleporte_duration // 2:
            teleporte_index = (teleporte_index + 1) % len(teleporte_sprites)
            tempo_ultimo_dash = pygame.time.get_ticks()

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

# aplica os escalonamento do jogo ao eliminar os inimigos
def aplicar_crescimento_personalizado():
    global vida_inimigo_maxima, Resistencia_petro, dano_inimigo_perto, dano_person_hit
    global vida_maxima_petro, dano_petro, dano_inimigo_longe, dano_boss
    global Dano_Boss_Habilit, Velocidade_Inimigos_1, inimigos_eliminados
    global max_inimigos, tempo_revive

    # Crescimento dos atributos do inimigo
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

    # ---- Crescimento balanceado do número máximo de inimigos ----
    # A cada 30 eliminações aumenta o número de inimigos até o limite de 12
    if inimigos_eliminados % 30 == 0 and max_inimigos < 12:
        max_inimigos += 1

    # ---- Incrementa o tempo de reviver baseado em inimigos eliminados ----
    tempo_revive += inimigos_eliminados // 30  # A cada 30 inimigos mortos, aumenta 1 segundo no tempo de reviver



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
    chance = 0.05 # Chance da moeda dropar 10%
    if random.random() < chance:
        tamanho_moeda = (36, 36)  # Novo tamanho desejado
        sprite_redimensionada = pygame.transform.scale(sprite_moeda, tamanho_moeda)
        rect = sprite_redimensionada.get_rect(center=posicao)
        moedas_soltadas.append({
            "rect": rect,
            "image": sprite_redimensionada
        })
        

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


    #################################### Conexão Host ou cliente
    if modo == "host" :
        # --- Atualiza e envia estado completo para o cliente ---
        estado = {
            "p1": {
                "x": pos_x_personagem,
                "y": pos_y_personagem,
                "direcao": direcao_atual,
                "morto": jogador_morto
            },
            "inimigos": [
                {
                    "x": inimigo["rect"].x,
                    "y": inimigo["rect"].y,
                    "vida": inimigo["vida"],
                    "vida_max": inimigo["vida_maxima"]
                }
                for inimigo in inimigos_comum
            ]
        }
        fila_envio.put(estado)
        if boss_vivo1:
            estado["boss"] = {
                "x": pos_x_chefe,
                "y": pos_y_chefe,
                "vida": vida_boss,
                "vida_max": vida_maxima_boss1
            }
        while not fila_recebimento.empty():
            dados = fila_recebimento.get()
            if dados:
                if "game_over" in dados and dados["game_over"]:
                    estado_jogo = "game_over"
                
                if "ping" in dados:
                    try:
                        fila_envio.put({"pong": dados["ping"]})  # devolve o mesmo tempo
                    except:
                        pass
                if "p2" in dados:  # Recebe dados do cliente (jogador 2)
                    pos_x_player2 = dados["p2"]["x"]
                    pos_y_player2 = dados["p2"]["y"]
                    direcao_player2 = dados["p2"].get("direcao", "down")
                    cliente_ativo = True  # O cliente está ativo
                    if "morto" in dados["p2"]:
                        jogador_remoto_morto = dados["p2"]["morto"]


                # Cliente avisou que acertou um inimigo
                if "hit" in dados:
                    
                    idx = dados["hit"]
                    if 0 <= idx < len(inimigos_comum):
                        inimigo = inimigos_comum[idx]

                        # aplica o dano
                        inimigo["vida"] -= dano_person_hit

                        # verifica se morreu
                        if inimigo["vida"] <= 0:
                            # Guarda posição antes de remover
                            posicao_inimigo = inimigo["rect"].center
                            inimigos_comum.pop(idx)
                            ganho = int(75 + math.log2(inimigos_eliminados + 1) * 4)
                            # soma pontos
                            pontuacao_exib += ganho  # ou o valor real do inimigo
                            # envia pontuação atualizada para o cliente
                            
                            fila_envio.put({"pontuacao_atual": pontuacao_exib})
                            aplicar_crescimento_personalizado()
                            fila_envio.put({"crescimento_local": True})
                            
                            # Host também avisa o client para soltar moeda no local certo
                            try:
                                fila_envio.put({"drop_moeda": posicao_inimigo})
                            except:
                                pass


                # Cliente avisou que acertou com ataque especial
                # HOST
                if "hit_especial" in dados:
                    rect_onda = pygame.Rect(
                        dados["hit_especial"]["x"],
                        dados["hit_especial"]["y"],
                        dados["hit_especial"]["w"],
                        dados["hit_especial"]["h"]
                    )
                    for inimigo in inimigos_comum[:]:
                        if rect_onda.colliderect(inimigo["rect"]):
                            inimigo["vida"] -= dano_person_hit * 2
                            if inimigo["vida"] <= 0:
                                inimigos_comum.remove(inimigo)
                                fila_envio.put({"pontuacao_atual": pontuacao_exib})
                                aplicar_crescimento_personalizado()
                                fila_envio.put({"crescimento_local": True})

                 # --- Cliente sugeriu o boss ---
                if "convite_boss" in dados and dados["convite_boss"]:
                    convite_boss_ativo = True
                    convite_boss_recebido = True
                    convite_boss_tempo = pygame.time.get_ticks()

                # --- Cliente respondeu ---
                if "resposta_boss" in dados:
                    if dados["resposta_boss"]:
                        iniciar_boss = True
                        fila_envio.put({"iniciar_boss": True})  # avisa cliente
                    else:
                        convite_boss_ativo = False

                # --- Cliente recebeu confirmação de iniciar ---
                if "iniciar_boss" in dados and dados["iniciar_boss"]:
                    iniciar_boss = True
                # --- CLIENTE ACERTOU O BOSS (DANO NORMAL) ---
                if "hit_boss" in dados:
                    if boss_vivo1 and vida_boss > 0:
                        dano = dano_person_hit
                        if random.random() <= chance_critico:
                            dano *= 3
                        vida_boss -= dano
                        if vida_boss <= 0:
                            boss_vivo1 = False
                            fila_envio.put({"boss_morto": True})

                # --- CLIENTE ACERTOU O BOSS (HIT ESPECIAL) ---
                if "hit_boss_especial" in dados:
                    if boss_vivo1 and vida_boss > 0:
                        dano = dano_person_hit * 2
                        vida_boss -= dano
                        if vida_boss <= 0:
                            boss_vivo1 = False
                            fila_envio.put({"boss_morto": True})
                if "vida_cliente" in dados:
                    vida_remota = dados["vida_cliente"]


            # --- Host aperta R para sugerir o boss ---
        if not convite_boss_ativo and not r_press and pygame.key.get_pressed()[pygame.K_r]:
            convite_boss_ativo = True
            convite_boss_enviado = True
            convite_boss_tempo = pygame.time.get_ticks()
            fila_envio.put({"convite_boss": True})

        # --- Tempo limite do convite ---
        if convite_boss_ativo and pygame.time.get_ticks() - convite_boss_tempo > 5000:  
            convite_boss_ativo = False
            convite_boss_enviado = False
            convite_boss_recebido = False
        outro_jogador_morto = jogador_remoto_morto  # cliente remoto
                



    elif modo == "join":
        # Medir ping: envia um pacote de teste e mede o tempo de resposta
        if pygame.time.get_ticks() - tempo_envio_ping > 1000:
            tempo_envio_ping = pygame.time.get_ticks()
            try:
                fila_envio.put({"ping": tempo_envio_ping})  # envia o tempo de envio
            except:
                pass

        
        fila_envio.put({
            "p2": {
                "x": pos_x_personagem,
                "y": pos_y_personagem,
                "direcao": direcao_atual_p2,
                "morto": jogador_morto
            }
        })
        # Se a vida mudou, envia ao host
        if vida != ultima_vida_enviada:
            fila_envio.put({"vida_cliente": vida})
            ultima_vida_enviada = vida

        if loja_aberta:
            loja_aberta = False

        
            ret = tela_de_pausa(velocidade_personagem, intervalo_disparo, vida, largura_disparo, altura_disparo,
                        trembo, dano_person_hit, chance_critico, roubo_de_vida, quantidade_roubo_vida,
                        tempo_cooldown_dash, vida_maxima, Petro_active, Resistencia, vida_petro,
                        vida_maxima_petro, dano_petro, xp_petro, petro_evolucao, Resistencia_petro,
                        Chance_Sorte, Poison_Active, Dano_Veneno_Acumulado, Executa_inimigo, Ultimo_Estalo,
                        mostrar_info, Mercenaria_Active, Valor_Bonus, dispositivo_ativo, Tempo_cura,
                        porcentagem_cura, cartas_compradas, pontuacao_exib,
                        max_cartas_compraveis=quantidade_cartas)
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
            tela_de_espera_client(tela, fila_envio, fila_recebimento)
            fila_envio.put({"pontuacao_atual": pontuacao_exib})
        # --- Cliente pode sugerir o boss ---
        if not convite_boss_ativo and not r_press and pygame.key.get_pressed()[pygame.K_r]:
            fila_envio.put({"convite_boss": True})
            convite_boss_ativo = True
            convite_boss_enviado = True
            convite_boss_tempo = pygame.time.get_ticks()

        # --- Cliente responde a convite ativo ---
        if convite_boss_ativo and convite_boss_recebido:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y]:
                fila_envio.put({"resposta_boss": True})
                convite_boss_ativo = False
            elif keys[pygame.K_n]:
                fila_envio.put({"resposta_boss": False})
                convite_boss_ativo = False 
        outro_jogador_morto = jogador_remoto_morto  # host remoto
                   




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
            pygame.quit()
            sys.exit()

        if not jogador_morto:  # Só permite se estiver vivo
            if botao_mouse[0] and tempo_atual - tempo_ultimo_disparo >= intervalo_disparo:  # Botão esquerdo do mouse
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
    if not jogador_morto:
        if modo == "host" :
            direcao_atual = atualizar_posicao_personagem(keys, joystick)
        elif modo == "join":
            direcao_atual_p2 = atualizar_posicao_personagem(keys, joystick)
    else:
        # Jogador morto não pode se mover
        direcao_atual = "down"


    

    novos_inimigos = []
    novos_disparos = []
    inimig_atin=[]

    tempo_passado += relogio.get_rawtime()
    relogio.tick()

     # Adicionar inimigos a cada 10 segundos
    tempo_atual = pygame.time.get_ticks()
    if modo == "host" :  # Apenas o host pode gerar inimigos
        if mostrar_tutorial:
            if (
                tempo_atual > 23000
                and apertou_q
                and tempo_atual - tempo_ultimo_inimigo >= 1000
                and len(inimigos_comum) < max_inimigos
                and not boss_vivo1
            ):
                gerar_inimigo()
                tempo_ultimo_inimigo = tempo_atual  # Atualiza o tempo do último inimigo adicionado
        else:
            if (
                tempo_atual - tempo_ultimo_inimigo >= 1000
                and len(inimigos_comum) < max_inimigos
                and not boss_vivo1
            ):
                gerar_inimigo()
                tempo_ultimo_inimigo = tempo_atual  # Atualiza o tempo do último inimigo adicionado

    
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



    if modo == "join":
        novas_ondas = []
        for onda in ondas:
            onda["rect"].x += velocidade_onda * math.cos(onda["angulo"])
            onda["rect"].y += velocidade_onda * math.sin(onda["angulo"])
            tempo_decorrido_onda = pygame.time.get_ticks() - onda["tempo_inicio"]
            onda["frame_atual"] = (tempo_decorrido_onda // duracao_frame_onda) % len(onda["frames"])
            tela.blit(onda["frames"][onda["frame_atual"]], onda["rect"])

            if 0 <= onda["rect"].x < largura_mapa and 0 <= onda["rect"].y < altura_mapa:
                novas_ondas.append(onda)

            # detecta colisão, só avisa
            for idx, inimigo in enumerate(inimigos_comum):
                if onda["rect"].colliderect(inimigo["rect"]):
                    try:
                        # CLIENTE
                        for onda in ondas:
                            fila_envio.put({
                                "hit_especial": {
                                    "x": onda["rect"].x,
                                    "y": onda["rect"].y,
                                    "w": onda["rect"].w,
                                    "h": onda["rect"].h
                                }
                            })

                    except:
                        pass

        ondas = novas_ondas

        

    if modo == "host" :
        novas_ondas = []
        for onda in ondas:
            onda["rect"].x += velocidade_onda * math.cos(onda["angulo"])
            onda["rect"].y += velocidade_onda * math.sin(onda["angulo"])
            tempo_decorrido_onda = pygame.time.get_ticks() - onda["tempo_inicio"]
            onda["frame_atual"] = (tempo_decorrido_onda // duracao_frame_onda) % len(onda["frames"])
            tela.blit(onda["frames"][onda["frame_atual"]], onda["rect"])

            if 0 <= onda["rect"].x < largura_mapa and 0 <= onda["rect"].y < altura_mapa:
                novas_ondas.append(onda)

        ondas = novas_ondas

        # Aplica dano real
        for onda in ondas:
            for inimigo in inimigos_comum[:]:  # [:] evita erro ao remover
                inimigo_id = id(inimigo["rect"])
                if onda["rect"].colliderect(inimigo["rect"]) and \
                (inimigo_id not in inimigos_atingidos_por_onda or tempo_atual - inimigos_atingidos_por_onda[inimigo_id] >= 500):
                    inimigo["vida"] -= dano_person_hit * 2
                    inimigos_atingidos_por_onda[inimigo_id] = tempo_atual

                    if inimigo["vida"] <= 0:
                        inimigos_comum.remove(inimigo)
                        # Pontuação escalada
                        ganho = int(75 + math.log2(inimigos_eliminados + 1) * 4)
                        pontuacao += ganho
                        pontuacao_exib += ganho
                        aplicar_crescimento_personalizado()
                        fila_envio.put({"pontuacao_atual": pontuacao_exib})
                        fila_envio.put({"crescimento_local": True})
            
                        

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
                        fila_envio.put({"boss_morto": True})
                        vida_maxima_boss1 = 0
                        # Aplique os efeitos ou recompensas ao derrotar o boss aqui            

        # Depois do cálculo, envia sincronização pro cliente
        try:
            fila_envio.put({"inimigos": [{"x": i["x"], "y": i["y"], "vida": i["vida"], "vida_max": i["vida_maxima"]} for i in inimigos_comum],
                            "pontuacao_atual": pontuacao_exib})
            
        except:
            pass
    
    if modo == "host" :
        for inimigo in inimigos_comum:
            # Se o alvo atual morreu, força troca imediata
            if alvo_atual == "host" and jogador_morto and not jogador_remoto_morto:
                alvo_atual = "cliente"
                tempo_ultima_troca_alvo = tempo_atual

            elif alvo_atual == "cliente" and jogador_remoto_morto and not jogador_morto:
                alvo_atual = "host"
                tempo_ultima_troca_alvo = tempo_atual

            else:
                # Avalia se está na hora de reconsiderar o alvo
                if tempo_atual - tempo_ultima_troca_alvo >= intervalo_troca_alvo:

                    # Calcula distância até cada jogador
                    for inimigo in inimigos_comum:  # Aqui a variável inimigo está sendo iterada de uma lista de inimigos
                        dist_host = math.hypot(pos_x_personagem - inimigo["rect"].x, pos_y_personagem - inimigo["rect"].y)
                        dist_cliente = math.hypot(pos_x_player2 - inimigo["rect"].x, pos_y_player2 - inimigo["rect"].y)

                    # Atribui pontuação de prioridade para cada alvo
                    prioridade_host = 0
                    prioridade_cliente = 0

                    if not jogador_morto:
                        prioridade_host += max(0, 1000 - dist_host)
                    if not jogador_remoto_morto:
                        prioridade_cliente += max(0, 1000 - dist_cliente)

                    # Bônus por vulnerabilidade: quanto menor a vida, mais atraente
                    prioridade_host += max(0, (vida_maxima - vida) * 0.3)
                    prioridade_cliente += max(0, (vida_maxima - vida_remota) * 0.3)

                    # Chance aleatória leve para variação de comportamento
                    prioridade_host *= random.uniform(0.8, 1.2)
                    prioridade_cliente *= random.uniform(0.8, 1.2)

                    # Define novo alvo se diferença for significativa
                    if abs(prioridade_host - prioridade_cliente) > 150:
                        novo_alvo = "host" if prioridade_host > prioridade_cliente else "cliente"
                        if novo_alvo != alvo_atual:
                            alvo_atual = novo_alvo
                            tempo_ultima_troca_alvo = tempo_atual

            # Define coordenadas do alvo com base na escolha
            if alvo_atual == "host":
                alvo_x, alvo_y = pos_x_personagem, pos_y_personagem
                direcao_alvo = ultima_tecla_movimento
            else:
                alvo_x, alvo_y = pos_x_player2, pos_y_player2
                direcao_alvo = direcao_player2

    
            

    
    # Desenhe os inimigos na tela
    with lock_inimigos: # Evita ler enqaunto a threading escreve
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

    if not jogador_morto:  # Só pode tomar dano se estiver vivo 
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
    else:
        # Morto = não sofre dano
        pass
    
        
    # --- SISTEMA DE MORTE E REVIVAL ---

    # Jogador morre
    if vida <= 0 and not jogador_morto:
        if trembo:
            vida = vida_maxima  # Recupera a vida total
            trembo = False  # Consome o "trembo"
            imune_tempo_restante = 10000
            teleportado = True  # Ativa o teleporte aleatório
            porcentagem_cura = 0.02
            Tempo_cura = 2500
            pos_x_personagem, pos_y_personagem = gerar_posicao_aleatoria(
                largura_mapa, altura_mapa, largura_personagem, altura_personagem
            )
        else:
            # Marca jogador como morto (revival temporário)
            jogador_morto = True
            tempo_morte = pygame.time.get_ticks()
            vida = 0
            sprite_atual = sprite_morto

    # Se estiver morto, controla o revival
    if jogador_morto:
        tempo_passado_morte = pygame.time.get_ticks() - tempo_morte

        # Desenha sprite de caído
        tela.blit(sprite_morto, (pos_x_personagem, pos_y_personagem))

        
        # Calcula o tempo restante para reviver em segundos
        segundos_restantes = max(0, (tempo_revive - (tempo_passado_morte // 1000)))  # tempo_revive é em segundos
        texto_timer = fonte_mensagem.render(f"Revive em {segundos_restantes}s", True, (255, 80, 80))
        tela.blit(texto_timer, (pos_x_personagem - 20, pos_y_personagem - 40))

        # ⚙️ 1️⃣ Se o tempo de revival acabou e o outro jogador está morto → Game Over
        if jogador_morto:
            # Calcula o tempo passado desde a morte do jogador
            tempo_passado_morte = pygame.time.get_ticks() - tempo_morte

            # Desenha a sprite do jogador morto
            tela.blit(sprite_morto, (pos_x_personagem, pos_y_personagem))

            # Calcula o tempo restante para reviver em segundos
            segundos_restantes = max(0, (tempo_revive - (tempo_passado_morte // 1000)))  # tempo_revive é em segundos
            texto_timer = fonte_mensagem.render(f"Revive em {segundos_restantes}s", True, (255, 80, 80))
            tela.blit(texto_timer, (pos_x_personagem - 20, pos_y_personagem - 40))

            # ⚙️ 1️⃣ Se o tempo de revival acabou e o outro jogador também está morto → Game Over
            if modo == "join" and jogador_remoto_morto:
                fila_envio.put({"game_over": True})
                mostrar_tutorial = False
                pygame.time.delay(2000)
                Musica_tema_fases.stop()
                Som_tema_fases.stop()
                tela_upgrade_aureas(tela, fonte, moedas_coletadas)
                pygame.quit()
                limpar_salvamento()
                subprocess.run([python, "Game_Over.py"])
                sys.exit()

            # ⚙️ 2️⃣ Se o tempo de revival acabou, mas o outro jogador está vivo → revive
            elif tempo_passado_morte >= tempo_revive * 1000 and not jogador_remoto_morto:
                vida = vida_maxima // 2  # O jogador revive com metade da vida máxima
                jogador_morto = False  # O jogador revive
                sprite_atual = frames_animacao["down"][0]  # Restaura o sprite original do jogador

                # Enviar para o host que o jogador reviveu
                if modo == "join":
                    fila_envio.put({"reviver": True})
        if modo == "host" :
            if estado_jogo == "game_over" or not running:
                mostrar_tutorial = False
                pygame.time.delay(2000)
                Musica_tema_fases.stop()
                Som_tema_fases.stop()
                tela_upgrade_aureas(tela, fonte, moedas_coletadas)
                pygame.quit()
                limpar_salvamento()
                subprocess.run([python, "Game_Over.py"])
                sys.exit()
        # No lado do host, quando o jogador renasce
        if modo == "host" :
            if jogador_morto and tempo_passado_morte >= tempo_revive * 1000:
                jogador_morto = False  # O jogador revive
                # Definir a posição e outras variáveis, se necessário
                pos_x_personagem = largura_mapa // 2
                pos_y_personagem = altura_mapa // 2
                vida = vida_maxima // 2  # O jogador renasce com metade da vida
                sprite_atual = frames_animacao["down"][0]  # Restabelece o sprite
        


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
    

    ###############################################
    #   DESENHA OS PERSONAGENS NA TELA
    ###############################################

    # HOST (jogador 1 local)
    if modo == "host" :
        # --- Desenha o próprio personagem ---
        if jogador_morto:
            tela.blit(sprite_morto, (pos_x_personagem, pos_y_personagem))
        else:
            tela.blit(frames_animacao[direcao_atual][frame_atual], (pos_x_personagem, pos_y_personagem))

        # --- Desenha o segundo jogador (cliente) ---
        if cliente_ativo:
            try:
                if jogador_remoto_morto:
                    tela.blit(sprite_morto, (pos_x_player2, pos_y_player2))
                else:
                    tela.blit(frames_animacao2[direcao_player2][frame_atual], (pos_x_player2, pos_y_player2))
            except KeyError:
                tela.blit(frames_animacao2["down"][frame_atual], (pos_x_player2, pos_y_player2))

    # JOIN (jogador 2 local)
    elif modo == "join":
        # --- Desenha o próprio personagem ---
        if jogador_morto:
            tela.blit(sprite_morto, (pos_x_personagem, pos_y_personagem))
        else:
            tela.blit(frames_animacao2[direcao_atual_p2][frame_atual], (pos_x_personagem, pos_y_personagem))

        # --- Desenha o host (jogador 1 remoto) ---
        if host_ativo:
            try:
                if jogador_remoto_morto:
                    tela.blit(sprite_morto, (pos_x_player2, pos_y_player2))
                else:
                    tela.blit(frames_animacao[direcao_player2][frame_atual], (pos_x_player2, pos_y_player2))
            except KeyError:
                tela.blit(frames_animacao["down"][frame_atual], (pos_x_player2, pos_y_player2))




    

    for moeda in moedas_soltadas[:]:  # cópia da lista para evitar erro ao remover
        if personagem_rect.colliderect(moeda["rect"]):
            moedas_coletadas+=1
            moedas_soltadas.remove(moeda)
            
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
                    tempo_anterior_petro = tempo_atual_petro

        if comando_direção_petro:
            direcao_atual_petro="left_petro"
            comando_direção_petro=False
            
        desenhar_barra_de_vida_petro(tela, vida_petro, pos_x_petro, pos_y_petro - 20,vida_maxima_petro)  
        tela.blit(petro_nivel[direcao_atual_petro][frame_atual], (pos_x_petro, pos_y_petro))


    #AQUI GERAMOS O BOSS:
        # --- ATIVAÇÃO DO BOSS ---
    if iniciar_boss and not r_press:
        r_press = True
        iniciar_boss = False
        boss_vivo1 = True
        Musica_tema_fases.stop()
        Musica_tema_Boss1.play(loops=-1)
        tempo_inicio_boss = pygame.time.get_ticks()
        tempo_ultima_mudanca_direcao_boss = tempo_inicio_boss
        vida_boss = vida_maxima_boss1
        boss_envenenado = False
        frame_atual_chefe = 0
        tempo_passado_animacao_chefe = 0

    # --- LÓGICA DO BOSS (somente host controla) ---
    if modo == "host"  and boss_vivo1:
        tempo_passado_animacao_chefe += relogio.get_rawtime()
        if tempo_passado_animacao_chefe >= tempo_animacao_chefe:
            tempo_passado_animacao_chefe = 0
            frame_atual_chefe = (frame_atual_chefe + 1) % 2

        # Mudar direção aleatoriamente
        tempo_atual = pygame.time.get_ticks()
        intervalo_mudanca_direcao_boss = random.randint(1000, 3000)
        if tempo_atual - tempo_ultima_mudanca_direcao_boss >= intervalo_mudanca_direcao_boss:
            direcoes_possiveis = ['up', 'down', 'left', 'right']
            direcoes_possiveis.remove(ultima_direcao_boss)
            ultima_direcao_boss = random.choice(direcoes_possiveis)
            tempo_ultima_mudanca_direcao_boss = tempo_atual

        # Movimento do boss
        inimigos_comum = []  # limpa inimigos comuns durante o boss
        if ultima_direcao_boss == 'up':
            pos_y_chefe = max(0, pos_y_chefe - Velocidade_boss)
        elif ultima_direcao_boss == 'down':
            pos_y_chefe = min(altura_mapa - chefe_altura, pos_y_chefe + Velocidade_boss)
        elif ultima_direcao_boss == 'left':
            pos_x_chefe = max(0, pos_x_chefe - Velocidade_boss)
        elif ultima_direcao_boss == 'right':
            pos_x_chefe = min(largura_mapa - chefe_largura, pos_x_chefe + Velocidade_boss)

        # Muda direção se tocar na borda
        if pos_x_chefe <= 0 or pos_x_chefe >= largura_mapa - chefe_largura or pos_y_chefe <= 0 or pos_y_chefe >= altura_mapa - chefe_altura:
            if ultima_direcao_boss == 'up': ultima_direcao_boss = 'down'
            elif ultima_direcao_boss == 'down': ultima_direcao_boss = 'up'
            elif ultima_direcao_boss == 'left': ultima_direcao_boss = 'right'
            elif ultima_direcao_boss == 'right': ultima_direcao_boss = 'left'

        # --- Colisão com disparos do jogador ---
        for disparo in disparos[:]:
            rect_disparo = disparo["rect"]
            rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, chefe_largura, chefe_altura)
            if rect_disparo.colliderect(rect_boss):
                if vida_boss > 0:
                    if random.random() <= chance_critico:
                        dano = dano_person_hit * 3
                        cor = (255, 255, 0)
                        fonte_dano = fonte_dano_critico
                    else:
                        dano = dano_person_hit
                        cor = (255, 0, 0)
                        fonte_dano = fonte_dano_normal

                # Efeito de veneno
                if not boss_envenenado and Poison_Active:
                    boss_envenenado = True
                    dano_por_tick_veneno_boss = vida_boss * (Dano_Veneno_Acumulado / 100)
                    tempo_inicio_veneno_boss = pygame.time.get_ticks()
                    ultimo_tick_veneno_boss = pygame.time.get_ticks()

                # Aplica dano e roubo de vida
                texto_dano = fonte_dano.render(f"-{int(dano)}", True, cor)
                tela.blit(texto_dano, (pos_x_chefe + chefe_largura // 2, pos_y_chefe - 20))
                vida_boss -= dano
                disparos.remove(disparo)
                if random.random() < roubo_de_vida:
                    vida += (vida_maxima - vida) * quantidade_roubo_vida

        # --- Colisão com jogador ---
        rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, 200, 100)
        rect_personagem = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
        if rect_boss.colliderect(rect_personagem):
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_ataque >= 2500:
                dano_boss_total = int((vida_maxima * 0.10) + 150 + dano_boss)
                if not escudo_devota_ativo:
                    vida -= max(0, dano_boss_total - Resistencia)
                Dano_person.play()
                piscando_vida = True
                tempo_ultimo_ataque = tempo_atual

        # --- Atualiza frame de acordo com a vida ---
        porcentagem_vida_boss = (vida_boss / vida_maxima_boss1) * 100
        if porcentagem_vida_boss >= 90:
            frame_porcentagem = frames_chefe1_1
        elif 60 <= porcentagem_vida_boss < 90:
            frame_porcentagem = frames_chefe1_2
        elif 40 <= porcentagem_vida_boss < 60:
            frame_porcentagem = frames_chefe1_3
        else:
            frame_porcentagem = frames_chefe1_4

        # --- Renderizar ---
        tela.blit(frame_porcentagem[frame_atual_chefe], (pos_x_chefe, pos_y_chefe))
        desenhar_barra_de_vida(tela, pos_x_chefe, pos_y_chefe - 20, chefe_largura, 10, vida_boss, vida_maxima_boss1)

        fila_envio.put({
            "boss": {
                "x": pos_x_chefe,
                "y": pos_y_chefe,
                "vida": vida_boss,
                "vida_max": vida_maxima_boss1,
                "fase": porcentagem_vida_boss  # ou use porcentagem_vida_boss
            }
        })
    if modo == "join" and boss_vivo1:
        for idx, disparo in enumerate(disparos[:]):
            rect_disparo = disparo["rect"]
            rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, chefe_largura, chefe_altura)
            # Se o disparo colidir com o boss
            if rect_disparo.colliderect(rect_boss):
                try:
                    fila_envio.put({"hit_boss": True})
                except:
                    pass
                disparos.remove(disparo)
    if modo == "join" and boss_vivo1:
        for idx, onda in enumerate(ondas[:]):
            rect_onda = onda["rect"]
            rect_boss = pygame.Rect(pos_x_chefe, pos_y_chefe, chefe_largura, chefe_altura)

            if rect_onda.colliderect(rect_boss):
                try:
                    fila_envio.put({"hit_boss_especial": True})
                except:
                    pass
                ondas.remove(onda)
    # --- DESENHAR NO CLIENT ---
    if modo == "join" and boss_vivo1:
        tela.blit(frame_porcentagem[frame_atual_chefe], (pos_x_chefe, pos_y_chefe))
        desenhar_barra_de_vida(
            tela,
            pos_x_chefe,
            pos_y_chefe - 20,
            chefe_largura,
            10,
            vida_boss,
            vida_maxima_boss1
        )

    if modo == "host" :
        for inimigo in inimigos_comum:
            inimigo_rect = inimigo["rect"]
            inimigo_image = inimigo["image"]

            inimigo_atingido = False

            for disparo in disparos:
                
                if verificar_colisao_disparo_inimigo(
                    disparo,
                    (inimigo["rect"].x, inimigo["rect"].y),
                    largura_disparo,
                    altura_disparo,
                    largura_inimigo,
                    altura_inimigo,
                    inimigos_eliminados
                ):
                    if random.random() <= chance_critico:  # chance de dano crítico
                        dano = dano_person_hit * 3  # Valor do dano crítico é 3 vezes o dano normal
                        cor = (255, 255, 0)  # Amarelo (RGB)
                        fonte_dano = fonte_dano_critico
                    else:
                        dano = dano_person_hit
                        cor = (255, 0, 0)  # Vermelho (RGB)
                        fonte_dano = fonte_dano_normal

                    if Petro_active:
                        if vida_petro < vida_maxima_petro:
                            vida_petro += (vida_maxima_petro - vida_petro) * 0.25

                    # Renderize o texto do dano
                    texto_dano = fonte_dano.render("-" + str(int(dano)), True, cor)
                    # Desenhe o texto na tela perto do chefe
                    pos_texto = (
                        inimigo["rect"].x + largura_inimigo // 2 - texto_dano.get_width() // 2,
                        inimigo["rect"].y - 20
                    )
                    # Rastreie o tempo de exibição do texto
                    tempo_texto_dano = pygame.time.get_ticks()

                    inimigo["vida"] -= dano
                    disparos.remove(disparo)  # Remover o disparo após colisão

                    
                    
                    if inimigo["vida"] <= 0:
                        posicao_inimigo = inimigo["rect"].center
                        soltar_moeda(posicao_inimigo)
                        # envia pro client desenhar a moeda também
                        try:
                            fila_envio.put({"drop_moeda": posicao_inimigo})
                        except:
                            pass
                        inimigos_comum.remove(inimigo)
                        
                        # Crescimento proporcional por nível de ameaça
                        aplicar_crescimento_personalizado()
                        
                        ganho = int(75 + math.log2(inimigos_eliminados + 1) * 4)
                        pontuacao += ganho
                        eliminacoes_consecutivas_impulsiva += 1
                        
                        pontuacao_exib += ganho
                        fila_envio.put({"pontuacao_atual": pontuacao_exib})
                        fila_envio.put({"crescimento_local": True})

                        # Boss: aumento escalonado
                        if not boss_vivo1:
                            if vida_boss > 0:
                                vida_boss += 15 + nivel_ameaca * 10
                                vida_maxima_boss1 = vida_boss

                    if random.random() < roubo_de_vida:
                        vida += (vida_maxima - vida) * quantidade_roubo_vida

                    

            if inimigo_atingido:
                break  # Sair do loop externo se um inimigo foi atingido
        

        
            if pontuacao_exib > pontuacao_magia:
                pontuacao_magia = min(pontuacao_exib, maxima_pontuacao_magia)
    
    if modo == "join":
        for inimigo in inimigos_comum:
            inimigo_rect = inimigo["rect"]
            inimigo_image = inimigo["image"]

            inimigo_atingido = False

            for disparo in disparos:
                
                if verificar_colisao_disparo_inimigo(
                    disparo,
                    (inimigo["rect"].x, inimigo["rect"].y),
                    largura_disparo,
                    altura_disparo,
                    largura_inimigo,
                    altura_inimigo,
                    inimigos_eliminados
                ):
                    if random.random() <= chance_critico:  # chance de dano crítico
                        dano = dano_person_hit * 3  # Valor do dano crítico é 3 vezes o dano normal
                        cor = (255, 255, 0)  # Amarelo (RGB)
                        fonte_dano = fonte_dano_critico
                    else:
                        dano = dano_person_hit
                        cor = (255, 0, 0)  # Vermelho (RGB)
                        fonte_dano = fonte_dano_normal

                    if Petro_active:
                        if vida_petro < vida_maxima_petro:
                            vida_petro += (vida_maxima_petro - vida_petro) * 0.25

                    # Renderize o texto do dano
                    texto_dano = fonte_dano.render("-" + str(int(dano)), True, cor)
                    # Desenhe o texto na tela perto do chefe
                    pos_texto = (
                        inimigo["rect"].x + largura_inimigo // 2 - texto_dano.get_width() // 2,
                        inimigo["rect"].y - 20
                    )
                    # Rastreie o tempo de exibição do texto
                    tempo_texto_dano = pygame.time.get_ticks()
                    disparos.remove(disparo)  # Remover o disparo após colisão
                    # Notifica o host se for client
                    if modo == "join":
                        try:
                            idx = inimigos_comum.index(inimigo)
                            fila_envio.put({"hit": idx})
                        except:
                            pass
                    
                    
                
                        
                    if random.random() < roubo_de_vida:
                        vida += (vida_maxima - vida) * quantidade_roubo_vida

                    

            if inimigo_atingido:
                break  # Sair do loop externo se um inimigo foi atingido
        

        
            if pontuacao_exib > pontuacao_magia:
                pontuacao_magia = min(pontuacao_exib, maxima_pontuacao_magia)
    
                    
    

        
    total_cartas_compradas = sum(cartas_compradas.values())
    custo_carta_atual = custo_base_carta + (total_cartas_compradas * custo_por_carta)
    # Verifica se a pontuação atingiu 1500 e se o jogador pressionou 'Q'
    if modo == "host" :
        if (not jogador_remoto_morto) and (pontuacao_exib >= custo_carta_atual) and (keys[config_teclas["Comprar na loja"]] or (joystick and joystick.get_button(3))):
            # Calcula quantas cartas o jogador pode comprar
            max_cartas = pontuacao_exib // custo_carta_atual
            if max_cartas <= 0:
                continue  # segurança

            # Debita tudo de uma vez
            total_custo = custo_carta_atual * max_cartas
            pontuacao_exib -= total_custo
            pontuacao_magia -= total_custo
            apertou_q = True

            # Envia pro client abrir loja também
            fila_envio.put({"abrir_loja": True, "quantidade_cartas": max_cartas})
    
            ret = tela_de_pausa(velocidade_personagem, intervalo_disparo, vida, largura_disparo, altura_disparo,
                                trembo, dano_person_hit, chance_critico, roubo_de_vida, quantidade_roubo_vida,
                                tempo_cooldown_dash, vida_maxima, Petro_active, Resistencia, vida_petro,
                                vida_maxima_petro, dano_petro, xp_petro, petro_evolucao, Resistencia_petro,
                                Chance_Sorte, Poison_Active, Dano_Veneno_Acumulado, Executa_inimigo, Ultimo_Estalo,
                                mostrar_info, Mercenaria_Active, Valor_Bonus, dispositivo_ativo, Tempo_cura,
                                porcentagem_cura, cartas_compradas, pontuacao_exib,max_cartas_compraveis=max_cartas, inimigos_eliminados=inimigos_eliminados)
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

            # após sair da loja, avisa o outro lado
            fila_envio.put({"abrir_loja": False})
            tela_de_espera_host(tela, fila_envio, fila_recebimento)

        

        
        

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
    # Exibir ping no canto superior direito
    if modo == "join":  # apenas o cliente precisa ver o ping
        fonte_ping = pygame.font.Font(None, 32)
        texto_ping = fonte_ping.render(f"Ping: {ping_atual} ms", True, cor_ping)
        tela.blit(texto_ping, (largura_mapa - texto_ping.get_width() - 20, 40))
    # --- Popup Boss ---
    if convite_boss_ativo:
        fonte_popup = pygame.font.Font(None, 32)
        rect_popup = pygame.Rect(tela.get_width() - 320, 20, 300, 60)
        pygame.draw.rect(tela, (30, 30, 30), rect_popup, border_radius=8)
        pygame.draw.rect(tela, (200, 200, 0), rect_popup, 2, border_radius=8)

        if convite_boss_enviado:
            texto = fonte_popup.render("Convite enviado...", True, (255, 255, 0))
        elif convite_boss_recebido:
            restante = 5 - (pygame.time.get_ticks() - convite_boss_tempo) // 1000
            texto = fonte_popup.render("Aperte Y para aceitar o Boss", True, (255, 255, 255))
        else:
            texto = fonte_popup.render("Esperando confirmação...", True, (255, 255, 255))

        tela.blit(texto, (rect_popup.x + 15, rect_popup.y + 20))
    



    tela.blit(cursor_imagem, (mouse_x, mouse_y))
    exibir_cronometro(tela)
    pygame.display.flip()
    FPS.tick(100)  # Limita a 100 FPS


# Encerrar o Pygame
pygame.quit()
