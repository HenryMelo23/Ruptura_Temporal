
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
import habilidade_boss as hb

pygame.init()
memoria_umbra = hb.MemoriaEvolutivaUmbra()

estalos = pygame.mixer.Sound("Sounds/Estalo.mp3")
estalos.set_volume(0.07) 

som_ataque_boss = pygame.mixer.Sound("Sounds/Hit_Boss1.mp3")
som_ataque_boss.set_volume(0.04) 


Disparo_Geo = pygame.mixer.Sound("Sounds/Disparo_Geo.wav")
Disparo_Geo.set_volume(0.04) 

Musica_tema_Boss1 = pygame.mixer.Sound("Sounds/Fase1_Boss.mp3")
Musica_tema_Boss1.set_volume(0.00) 

Musica_tema_fases = pygame.mixer.Sound("Sounds/Fase_boas.mp3")
Musica_tema_fases.set_volume(0.00) 

Som_tema_fases = pygame.mixer.Sound("Sounds/Praia.wav")
Som_tema_fases.set_volume(0.00) 

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


tempo_mostrando_mensagem = 0  
imune_tempo_restante = 0  # Tempo restante de imunidade (em milissegundos)
teleportado = False  # Controle de teleporte

direcao_atual_petro="left_petro"
carregar_atributos_na_fase=True
nivel_ameaca = inimigos_eliminados // 10
fonte_mensagem = pygame.font.Font(None, 48)  # Tamanho da fonte
mensagens_exibidas = set()
mensagem_ativa = None
tempo_fim_mensagem = 0





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
        "vida_maxima_personagem": vida_maxima,
        "vida_maxima_petro": vida_maxima_petro,
        "vida_atual_personagem": vida,
        "nivel_Petro": xp_petro,
        "existencia_petro": Petro_active,
        "existencia_trembo": trembo,
        "dano_petro": dano_petro,
        "resistencia_personagem": Resistencia,
        "resistencia_petro": Resistencia_petro,
        "dano_inimigo_longe": dano_inimigo_longe,
        "dano_inimigo_perto": dano_inimigo_perto,
        "Poison_Active": Poison_Active,
        "Ultimo_Estalo": Ultimo_Estalo,
        "Executa_inimigo": Executa_inimigo,
        "Mercenaria_Active": Mercenaria_Active,
        "Valor_Bonus": Valor_Bonus,
        "tempo_cooldown_dash": tempo_cooldown_dash,
        "petro_evolucao": petro_evolucao,
        "Dano_Veneno_Acumulado": Dano_Veneno_Acumulado,
        "Tempo_cura": Tempo_cura,
        "porcentagem_cura": porcentagem_cura,
        # 🪙 novo campo
        "moedas_totais": moedas_totais,
    }

    with open('atributos.json', 'w') as file:
        json.dump(atributos, file)

def carregar_atributos():
    global velocidade_personagem, intervalo_disparo, dano_person_hit, chance_critico, roubo_de_vida, quantidade_roubo_vida,vida_maxima,vida_maxima_petro,vida,xp_petro,Petro_active,trembo,dano_petro,Resistencia,Resistencia_petro,dano_inimigo_longe,dano_inimigo_perto,direcao_atual,Poison_Active,Ultimo_Estalo,Executa_inimigo,Valor_Bonus,Mercenaria_Active,tempo_cooldown_dash,vida_petro,petro_evolucao,Dano_Veneno_Acumulado, Tempo_cura,porcentagem_cura, moedas_totais
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
        moedas_totais = atributos["moedas_totais"]

        
with open("aurea_selecionada.json", "r") as file:
    aurea = json.load(file)["aurea"]

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
# Carregar a imagem do mapa
mapa = pygame.image.load(mapa_path5).convert()
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


def criar_disparo():
        return {"rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_disparo, altura_disparo),"direcao": ultima_tecla_movimento }



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


def soltar_moeda(posicao):
    chance = 0.05 # 5%
    if random.random() < chance:
        tamanho_moeda = (36, 36)  # Novo tamanho desejado
        sprite_redimensionada = pygame.transform.scale(sprite_moeda, tamanho_moeda)
        rect = sprite_redimensionada.get_rect(center=posicao)
        moedas_soltadas.append({
            "rect": rect,
            "image": sprite_redimensionada
        })


def tela_upgrade_aureas(tela, fonte, moedas_disponiveis):
    if not os.path.exists("aureas_upgrade.json"):
        dados_iniciais = {
            "Racional": 0,
            "Impulsiva": 0,
            "Devota": 0,
            "Vanguarda": 0
        }
        with open("aureas_upgrade.json", "w") as f:
            json.dump(dados_iniciais, f, indent=4)
    
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
                memoria_umbra.salvar() # Garante que a experiência seja gravada no JSON
                rodando = False
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


                            # 🪙 salva o novo total no arquivo de atributos
                            with open("atributos.json", "r") as f:
                                atributos = json.load(f)
                            atributos["moedas_totais"] = moedas_disponiveis
                            with open("atributos.json", "w") as f:
                                json.dump(atributos, f)

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
            memoria_umbra.salvar() # Garante que a experiência seja gravada no JSON
            rodando = False
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
    if keys[pygame.K_t] and estado_atual_ia['fase_tele'] == "espera":
            # Resetamos o cooldown e simulamos dano crítico para forçar o Grafo
            estado_atual_ia['ultimo_teleporte'] = 0
            estado_atual_ia['dano_recente'] = 500
            print(" [DEBUG] Induzindo Teleporte de Pânico...")
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
    


    tempo_passado += relogio.get_rawtime()
    relogio.tick()

     # Adicionar inimigos a cada 10 segundos
    tempo_atual = pygame.time.get_ticks()
    
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
    

    if imune_tempo_restante > 0:
        imune_tempo_restante -= relogio.get_time()  
    else:
        imune_tempo_restante = 0 

    
    
            
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
            memoria_umbra.salvar() # Garante que a experiência seja gravada no JSON
            rodando = False

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

        


    personagem_rect = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
        
    ###############################################   DESENHA O PERSONAGEM NA TELA ################################
    tela.blit(frames_animacao[direcao_atual][frame_atual], (pos_x_personagem, pos_y_personagem))
    ###############################################   DESENHA O BOSS NA TELA ################################
    if boss_final_ativo:
        agora = pygame.time.get_ticks()
        if 'tempo_start_boss' not in estado_atual_ia:
            estado_atual_ia['tempo_start_boss'] = agora
        
        luta_iniciada = (agora - estado_atual_ia['tempo_start_boss']) >= 10000

        # Criamos o dicionário que o 'processar_ia_umbra' espera
        boss_pos_ia = {
            'x': pos_x_umbra,
            'y': pos_y_umbra,
            'hitbox_centro': hitbox_boss5.center if 'hitbox_boss5' in locals() else (pos_x_umbra, pos_y_umbra)
        }
        player_pos_data = (pos_x_personagem, pos_y_personagem)
        dados_p = {
            'vida_atual': vida_umbra,
            'vida_max': vida_maxima_umbra,
            'erros': erros_player_contagem
        }
        # A cada segundo de sobrevivência, a IA recebe um pequeno incentivo
        if luta_iniciada:
            if agora - estado_atual_ia.get('ultimo_reforço_positivo', 0) >= 1000:
                memoria_umbra.treinar(0.1)
                estado_atual_ia['ultimo_reforço_positivo'] = agora
            # --- 2. CHAMADA DO CÉREBRO (O GRAFO) ---
            estado_atual_ia = hb.processar_ia_umbra(
                agora, boss_pos_ia, player_pos_data, 
                [], disparos, estado_atual_ia, dados_p,memoria_umbra
            )

            # --- 3. HIERARQUIA DE MOVIMENTAÇÃO (O IF CORRIGIDO) ---
            if estado_atual_ia.get('parede_ativa'):
                if agora - estado_atual_ia.get('ultimo_tick_cura', 0) >= 600:
                    # Reduzimos para 3% para permitir o counter-play tático
                    valor_cura = vida_maxima_umbra * 0.03 
                    
                    # A cura não pode ultrapassar o limite máximo
                    vida_umbra = min(vida_maxima_umbra, vida_umbra + valor_cura)
                    
                    efeitos_texto.append({
                        "texto": f"+{int(valor_cura)}",
                        "x": hitbox_boss5.centerx + random.randint(-30, 30),
                        "y": hitbox_boss5.top - 30,
                        "tempo_inicio": agora,
                        "cor": (0, 255, 150) # Esmeralda Visionário
                    })
                    estado_atual_ia['ultimo_tick_cura'] = agora

            if estado_atual_ia.get('fase_tele') == "projetil_viajando":
                sinal = estado_atual_ia.get('proj_tele')
                if sinal:
                    # A. Movimentação do Sinalizador Azul
                    dx_sinal = sinal['velocidade'] * math.cos(sinal['angulo'])
                    dy_sinal = sinal['velocidade'] * math.sin(sinal['angulo'])
                    sinal['x'] += dx_sinal
                    sinal['y'] += dy_sinal
                    sinal['dist_percorrida'] += math.hypot(dx_sinal, dy_sinal)
                    memoria_umbra.treinar(0.5)

                    # B. Renderização do Sinalizador (Brilho Neon)
                    pygame.draw.circle(tela, (200, 230, 255), (int(sinal['x']), int(sinal['y'])), 8)
                    pygame.draw.circle(tela, (0, 150, 255), (int(sinal['x']), int(sinal['y'])), 15, 2)


                    # C. O SALTO REAL (Quando o projétil chega ao destino)
                    if sinal['dist_percorrida'] >= sinal['dist_total']:
                        pos_x_umbra = sinal['target_pos'][0]
                        pos_y_umbra = sinal['target_pos'][1]
                        
                        # Reset dos estados para permitir o próximo ciclo
                        estado_atual_ia['fase_tele'] = "espera"
                        estado_atual_ia['proj_tele'] = None
                        estado_atual_ia['dano_recente'] = 0 
                        print(f" [TECNOLOGIA] Salto Dimensional concluído para {sinal['target_pos']}")
            
            else:
                # SÓ SE MOVE NORMALMENTE SE NÃO ESTIVER TELEPORTANDO
                # Isso impede que o movimento normal 'puxe' a boss de volta durante o salto
                nova_pos, estado_mental = hb.movimentacao_inteligente_umbra(
                    agora, 
                    (pos_x_umbra, pos_y_umbra),
                    player_pos_data, 
                    disparos, 
                    estado_atual_ia, 
                    dados_p,
                    memoria_umbra  # <--- O argumento de aprendizado que faltava
                )
                pos_x_umbra, pos_y_umbra = nova_pos[0], nova_pos[1]

            # --- 4. DINÂMICA VISUAL, ANIMAÇÃO E HITBOX ---
            offset_y_boss = math.sin(agora * 0.005) * 7
            direcao_boss = 'stop'
            
            tempo_passado_boss += relogio.get_time()
            if tempo_passado_boss >= tempo_animacao_stop:
                tempo_passado_boss = 0
                frame_boss = (frame_boss + 1) % len(frames_geo_umbra_paths[direcao_boss])
            
            img_atual_boss = frames_geo_umbra_paths[direcao_boss][frame_boss]

            # Inversão horizontal e ajuste de Hitbox
            if pos_x_personagem < pos_x_umbra:
                img_atual_boss = pygame.transform.flip(img_atual_boss, True, False)
                hitbox_x = pos_x_umbra
            else:
                hitbox_x = pos_x_umbra + 30

            hitbox_boss5 = pygame.Rect(hitbox_x, pos_y_umbra + offset_y_boss, largura_boss - 30, altura_boss)
            tela.blit(img_atual_boss, (pos_x_umbra, pos_y_umbra + offset_y_boss))
           

            # --- 5. BARRA DE VIDA ---
            largura_barra = largura_boss * 0.8
            barra_x = pos_x_umbra + (largura_boss - largura_barra) // 2
            barra_y = pos_y_umbra + offset_y_boss - 15
            vida_percent = max(0, vida_umbra) / vida_maxima_umbra
            projeteis_vivos = []
            for p in estado_atual_ia.get('projeteis', []):
                # Movimentação baseada no ângulo definido pela IA
                p["rect"].x += p["velocidade"] * math.cos(p["angulo"])
                p["rect"].y += p["velocidade"] * math.sin(p["angulo"])

                # Verificação de fronteiras (Limites do Mapa)
                if 0 < p["rect"].x < largura_mapa and 0 < p["rect"].y < altura_mapa:
                    projeteis_vivos.append(p)
                    
                    # --- 2. RENDERIZAÇÃO DOS PROJÉTEIS ---
                    # Definimos o visual com base no tipo (Comum ou Fúria)
                    if p.get("tipo") == "furia":
                        cor_tiro = (138, 43, 226) # Roxo Intenso
                        raio = 12
                    else:
                        cor_tiro = (255, 50, 50)  # Vermelho Alerta
                        raio = 6

                    # Desenho do núcleo e brilho externo
                    pygame.draw.circle(tela, cor_tiro, p["rect"].center, raio)
                    pygame.draw.circle(tela, (255, 255, 255), p["rect"].center, raio // 2)
                else:
                    memoria_umbra.treinar(-0.5)

            # Atualiza a lista oficial na memória da IA
            estado_atual_ia['projeteis'] = projeteis_vivos

            # --- 3. DETECÇÃO DE DANO NO JOGADOR ---
            hitbox_player = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
            for p in estado_atual_ia['projeteis']:
                if p["rect"].colliderect(hitbox_player):

                    vida -= 100
                    memoria_umbra.treinar(1.5) # Recompensa alta por acerto tático
                    estado_atual_ia['projeteis'].remove(p)
         # Renderização Final da Boss
            pygame.draw.rect(tela, (40, 40, 40), (barra_x, barra_y, largura_barra, 7))
            pygame.draw.rect(tela, (138, 43, 226), (barra_x, barra_y, largura_barra * vida_percent, 7))
            pygame.draw.rect(tela, (0, 255, 0), (barra_x, barra_y, largura_barra, 7), 1)
        else:
            img_atual_boss = frames_geo_umbra_paths[direcao_boss][frame_boss]
            offset_y_boss = math.sin(agora * 0.005) * 7
            img_atual_boss = pygame.transform.flip(img_atual_boss, True, False)
            tela.blit(img_atual_boss, (pos_x_umbra, pos_y_umbra + offset_y_boss))
            
    
    
    # Se a IA ainda não foi processada neste frame, garantimos que o estado exista
    if 'estado_atual_ia' not in locals() and 'estado_atual_ia' not in globals():
        estado_atual_ia = {'parede_ativa': False}

    novos_disparos = []

    for disparo in disparos:
        # 1. Movimentação do Projétil do Jogador
        disparo["rect"].x += velocidade_disparo * math.cos(disparo["angulo"])
        disparo["rect"].y += velocidade_disparo * math.sin(disparo["angulo"])
        
        atingiu_boss = False
        interceptado = False

        if disparo["rect"].colliderect(hitbox_boss5):

            if random.random() <= chance_critico:
                dano_final = dano_person_hit * 3
                cor_feedback = (255, 255, 0) # Amarelo Crítico
            else:
                dano_final = dano_person_hit
                cor_feedback = (255, 255, 255) # Branco Normal

            # Se o escudo (parede_ativa) estiver ligado, reduzimos o dano em 25%
            if estado_atual_ia.get('parede_ativa'):
                dano_final *= 0.75
                cor_feedback = (0, 200, 255) # Azul de Escudo

            # Aplicação de Dano e Treino
            if vida_umbra > 0:
                vida_umbra -= dano_final
                memoria_umbra.treinar(-1.0)
                
                # Ativação de Veneno Preditivo (Igual ao Boss 1)
                if not boss_envenenado and Poison_Active:
                    boss_envenenado = True
                    dano_por_tick_veneno_boss = vida_maxima_umbra * (Dano_Veneno_Acumulado / 100)
                    ultimo_tick_veneno_boss = agora

            # Feedback Visual e Limpeza
            efeitos_texto.append({
                "texto": f"-{int(dano_final)}",
                "x": hitbox_boss5.centerx + random.randint(-20, 20),
                "y": hitbox_boss5.top - 10,
                "tempo_inicio": agora,
                "cor": cor_feedback
            })
            atingiu_boss = True

        # 5. Manutenção de Projéteis no Mapa
        dentro_mapa = 0 <= disparo["rect"].x < largura_mapa and 0 <= disparo["rect"].y < altura_mapa
        if dentro_mapa and not atingiu_boss and not interceptado:
            novos_disparos.append(disparo)
        elif not atingiu_boss and not interceptado:
            erros_player_contagem += 1 

    disparos = novos_disparos

    # --- PROCESSAMENTO DE PROJÉTEIS DA BOSS 5 ---
    rect_personagem = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
    novos_projeteis_boss = []

    # Renderizar os disparos
    for disparo in disparos:
        tela.blit(frames_disparo[frame_atual_disparo], disparo["rect"].topleft)

    for moeda in moedas_soltadas[:]:
        if personagem_rect.colliderect(moeda["rect"]):
            moedas_coletadas += 1
            moedas_totais += 1   # acumula no total salvo
            moedas_soltadas.remove(moeda)
            salvar_atributos()   #salva imediatamente

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
    

    total_cartas_compradas = sum(cartas_compradas.values())
    custo_carta_atual = custo_base_carta + (total_cartas_compradas * custo_por_carta)
    # Verifica se a pontuação atingiu 1500 e se o jogador pressionou 'Q'
   
        

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

    tela.blit(cursor_imagem, (mouse_x, mouse_y))
    exibir_cronometro(tela)
    pygame.display.flip()
    FPS.tick(100)  # Limita a 60 FPS


# Encerrar o Pygame
pygame.quit()
sys.exit()