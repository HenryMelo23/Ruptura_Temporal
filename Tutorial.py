
import pygame
import sys
import random
import math
import importlib
import subprocess
from Tela_Cartas import tela_de_pausa
from Variaveis import *

velocidade_personagem = 1.5
intervalo_disparo = 800
dano_person_hit=10
chance_critico=0.05
roubo_de_vida=0
quantidade_roubo_vida=0.10

# Inicializar o Pygame
pygame.init()
speed_inimigo=0.70
dano_inimigo=25
# Configurações da tela
 
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Renderizando Mapa com Personagem")

# Variáveis para a barra de magia
pontuacao_inimigos=0
maxima_pontuacao_magia = 750
piscar_magia = False
spawn_inimigo=True


nivel_ameaca = inimigos_eliminados // 10
tempo_ultimo_inimigo_apos_morte = pygame.time.get_ticks()
tempo_ultimo_disparo_inimigo = pygame.time.get_ticks()

# Carregar a imagem do mapa
mapa = pygame.image.load(mapa_path2).convert()
mapa = pygame.transform.scale(mapa, (largura_tela, altura_tela))


###################################################                                             JOYSTICK FUNCION                                   ##########################################################################
# Verifica se um joystick está conectado
joystick_conectado = pygame.joystick.get_count() > 0

# Define o texto a ser exibido com base na presença do joystick
if joystick_conectado:
    texto_botao = "RB para sair"
    texto1 = "Use o Joystick para se mover"
    texto2 = "Aperte A para teleportar, o ícone azul no canto direito indica sua disponibilidade"
    texto3 = "X para disparar"
    texto4 = "Junte 900 pontos e aperte Y para ir à loja de cartas"
else:
    texto_botao = "ESC para voltar"
    texto1 = "Aperte A,W,S,D para se mover"
    texto2 = "Aperte SHIFT para teleportar, o ícone azul no canto direito indica sua disponibilidade"
    texto3 = "ESPAÇO para disparar"
    texto4 = "Junte 900 pontos e aperte Q para ir à loja de cartas"
    



disparos_inimigos = []

fonte_hit= "Texto/breakaway.ttf"
#Fonte para tipos de dano
fonte_dano = pygame.font.Font(fonte_hit, 36)
fonte_dano_critico = pygame.font.Font(fonte_hit, 23)

# Variáveis para rastrear o texto de dano
texto_dano = None
tempo_texto_dano = 0

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
intervalo_hit_inimigo = 1000  # Intervalo de 1 segundo (ajuste conforme necessário)

# esta variável global para controlar o piscar da barra de vida
piscando_vida = False

# Adicione esses frames aos frames_inimigo existentes
frames_inimigo = frames_inimigo_esquerda2 + frames_inimigo_direita2


vida_inimigo_maxima=30
vida_inimigo= vida_inimigo_maxima
# Função para desenhar uma barra de vida
def gerar_posicao_aleatoria(largura_mapa, altura_mapa, largura_personagem, altura_personagem):
    largura_mapa_int, altura_mapa_int, largura_personagem_int, altura_personagem_int=map(int,(largura_mapa, altura_mapa, largura_personagem, altura_personagem))
    x = random.randint(0, largura_mapa_int - largura_personagem_int)
    y = random.randint(0, altura_mapa_int - altura_personagem_int)
    return x, y
def desenhar_barra_de_vida(surface, x, y, largura_total, altura, vida_atual, vida_maxima):
    largura_vida = int(largura_total * (vida_atual / vida_maxima))
    borda = pygame.Rect(x, y, largura_total, altura)
    barra = pygame.Rect(x, y, largura_vida, altura)
    pygame.draw.rect(surface, (255, 0, 0), borda, 1)
    pygame.draw.rect(surface, (0, 255, 0), barra)


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
    if posicao_petro[0] < posicao_inimigo[0]: 
        return 'right_petro'
    elif posicao_petro[0] > posicao_inimigo[0]: 
        return 'left_petro'
    elif posicao_petro[1] < posicao_inimigo[1]:  
        return 'down_petro'
    elif posicao_petro[1] > posicao_inimigo[1]:  
        return 'up_petro'
    else:
        return 'stop_petro'  # Petro está na mesma posição do inimigo



def atualizar_posicao_personagem(keys, joystick):
    global pos_x_personagem, pos_y_personagem, direcao_atual, ultima_tecla_movimento
    global movimento_pressionado, cooldown_dash, distancia_dash, tempo_ultimo_dash, teleporte_timer, teleporte_duration, teleporte_index

    direcao_atual = 'stop'

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
        teleporte_timer += velocidade_personagem
        if teleporte_timer >= teleporte_duration:
            teleporte_index = (teleporte_index + 1) % len(teleporte_sprites)
            teleporte_timer = 0

        # Desenhe a sprite de teletransporte
        tela.blit(teleporte_sprites[teleporte_index], (pos_x_personagem, pos_y_personagem))

        # Atualize a tela
        pygame.display.flip()
        pygame.time.delay(teleporte_duration // 5)  # Tempo de espera entre cada quadro (metade da duração)

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
intervalo_criacao_gelo = 2000  # 10 segundos


def criar_inimigo(x, y):
    image = pygame.transform.scale(pygame.image.load("Sprites/inimig1.png"), (largura_inimigo, altura_inimigo))
    return {"rect": pygame.Rect(x, y, largura_inimigo, altura_inimigo), "image": image, "vida": vida_inimigo_maxima, "vida_maxima": vida_inimigo_maxima}

def gerar_inimigo():
    global inimigos_comum

    if len(inimigos_comum) < max_inimigos2:
        # Adicione uma chance de 40% de gerar o inimigo na borda esquerda
        if random.random() <= 0.4:
            novo_inimigo = criar_inimigo(0, random.randint(10, altura_mapa))
        else:
            novo_inimigo = criar_inimigo(largura_mapa, random.randint(10, altura_mapa))

        # Verifique se o novo inimigo está muito próximo de algum inimigo existente
        distancia_minima_alcancada = any(
            math.sqrt((novo_inimigo["rect"].x - inimigo["rect"].x) ** 2 + (novo_inimigo["rect"].y - inimigo["rect"].y) ** 2) < distancia_minima_inimigos
            for inimigo in inimigos_comum
        )

        # Se estiver muito próximo, ajuste a posição do novo inimigo
        while distancia_minima_alcancada:
            if random.random() <= 0.4:
                novo_inimigo = criar_inimigo(0, random.randint(10, altura_mapa))
            else:
                novo_inimigo = criar_inimigo(largura_mapa, random.randint(10, altura_mapa))
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
        

# Configurações para controlar a criação de inimigos
dobro_pontuacao = 15  # Quantidade de pontos necessários para dobrar a pontuação e adicionar mais inimigos
pontuacao_dobro = dobro_pontuacao  # Inicializa a pontuação necessária para dobrar a pontuação



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


###################################################################################################PRINCIPAL#################################################################################################################
#LOOP PRINCIPAL
running = True
mensagem1_exibida = False
mensagem2_exibida = False
mensagem3_exibida = False
mensagem4_exibida = False
mensagem5_exibida = False
mensagem6_exibida = False
tempo_inicial_mensagem1 = pygame.time.get_ticks()

FPS=pygame.time.Clock()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                subprocess.run([python, "Ruptura_Temporal.py"])
                sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 5:  # Botão RB do controle do Xbox
                pygame.quit()
                subprocess.run([python, "Ruptura_Temporal.py"])
                sys.exit()

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

    

    novos_disparos = []
    inimig_atin=[]

    for inimigo in inimigos_comum:
        inimigo_rect = inimigo["rect"]
        inimigo_image = inimigo["image"]

        inimigo_atingido = False

        for disparo in disparos:
            
            if verificar_colisao_disparo_inimigo(disparo, (inimigo["rect"].x, inimigo["rect"].y), largura_disparo, altura_disparo, largura_inimigo, altura_inimigo,inimigos_eliminados):
                
                if random.random() <= chance_critico:  # 10% de chance de dano crítico
                    dano = dano_person_hit * 2  # Valor do dano crítico é 3 vezes o dano normal
                    cor = (255, 255, 0)  # Amarelo (RGB)
                else:
                    dano = dano_person_hit
                    cor = (255, 0, 0)  # Vermelho (RGB)
                    
                # Renderize o texto do dano
                texto_dano = fonte_dano_critico.render("-" + str(int(dano)), True, cor)
                    
                # Desenhe o texto na tela perto do chefe
                pos_texto = (inimigo["rect"].x + largura_inimigo // 2 - texto_dano.get_width() // 2,  inimigo["rect"].y - 20)
                            
                # Rastreie o tempo de exibição do texto
                tempo_texto_dano = pygame.time.get_ticks()
                inimigo["vida"] -= dano_person_hit*2
                disparos.remove(disparo)  # Remover o disparo após colisão
                # Adicionar uma chance de 50% de aumentar a vida em 20 pontos

                if random.random() < roubo_de_vida:
                    vida += (vida_maxima-vida)*quantidade_roubo_vida

                if inimigo["vida"] <= 0:
                    # Se a vida do inimigo é menor ou igual a zero, remover o inimigo
                    inimigos_comum.remove(inimigo)
                    vida_inimigo_maxima+=15
                    Resistencia_petro+=24.5
                    dano_inimigo+=25
                    dano_person_hit+=5
                    vida_maxima_petro+=35
                    dano_petro+=5
                    if speed_inimigo <2.5:
                        speed_inimigo+=0.002
                    dano_inimigo+= 5

                    inimigos_eliminados += 1
                    pontuacao += 100
                    pontuacao_exib+=100
                    if vida_petro < (vida_maxima_petro*0.6):
                            vida_petro+=(vida_maxima_petro*0.4)
                    break  # Sai do loop interno para evitar problemas ao modificar a lista enquanto iteramos sobre elad

        



                
                

        if inimigo_atingido:
            break  # Sair do loop externo se um inimigo foi atingido
    

    
        if pontuacao_exib > pontuacao_magia:
            pontuacao_magia = min(pontuacao_exib, maxima_pontuacao_magia)

        

    def criar_disparo():
        return {"rect": pygame.Rect(pos_x_personagem, pos_y_personagem, largura_disparo, altura_disparo),"direcao": ultima_tecla_movimento }

    # Adicionar um novo disparo quando a tecla de espaço é pressionada
    tempo_atual = pygame.time.get_ticks()
    if (keys[pygame.K_SPACE] or (joystick and joystick.get_button(2))) and movimento_pressionado and tempo_atual - tempo_ultimo_disparo >= intervalo_disparo:
        if ultima_tecla_movimento is not None:
            
            pos_x_disparo = pos_x_personagem + largura_personagem // 1 - largura_disparo // 1
            pos_y_disparo = pos_y_personagem + altura_personagem // 1 - altura_disparo // 1
            disparos.append((pos_x_disparo, pos_y_disparo, ultima_tecla_movimento))
            tempo_ultimo_disparo = tempo_atual  # Atualizar o tempo do último disparo
            

    tempo_passado += relogio.get_rawtime()
    relogio.tick()

     # Adicionar inimigos a cada 10 segundos
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_ultimo_inimigo >= 1000 and len(inimigos_comum) < max_inimigos2 and spawn_inimigo:
        gerar_inimigo()
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
    tela.blit(frames_animacao[direcao_atual][frame_atual], (pos_x_personagem, pos_y_personagem))

    if trembo:
        # Desenhar o segundo personagem ao lado do personagem original
        pos_x_segundo_personagem = pos_x_personagem + largura_personagem + 4
        pos_y_segundo_personagem = pos_y_personagem
        tela.blit(frames_animacao_trembo[direcao_atual][frame_atual], (pos_x_segundo_personagem, pos_y_segundo_personagem))

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
                    
                    
                    inimigo_mais_proximo["vida"] -= int(dano_person_hit * 0.25)+ dano_petro
                    tempo_anterior_petro = tempo_atual_petro
                    
                    # Verifica se o inimigo foi derrotado
                    if inimigo_mais_proximo["vida"] <= 0:
                        vida_inimigo_maxima+=23
                        pontuacao += 100
                        pontuacao_exib+=100
                        Resistencia_petro+=24.5
                        vida_maxima_petro+=35
                        dano_inimigo+=28
                        dano_person_hit+=8
                        inimigos_eliminados += 1
                        dano_petro+=5
                        
                        # Remove o inimigo da lista de inimigos comuns
                        inimigos_comum.remove(inimigo_mais_proximo)
                        
                        if vida_petro < (vida_maxima_petro*0.6):
                            vida_petro+=(vida_maxima_petro*0.4)
                            
                             
                        
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

    frame_atual_disparo = (frame_atual_disparo + 1) % len(frames_disparo)

    

    # loop principal, onde o inimigo é desenhado:
    for inimigo in inimigos_comum:
        dx = pos_x_personagem - inimigo["rect"].x
        dy = pos_y_personagem - inimigo["rect"].y
        dist = max(40, abs(dx) + abs(dy))
        inimigo["rect"].x += (dx / dist) * speed_inimigo
        inimigo["rect"].y += (dy / dist) * speed_inimigo

        # Atualize os frames do inimigo com base na direção
        if dx > 0:  # Mova para a direita
            inimigo["image"] = frames_inimigo_direita2[frame_atual % len(frames_inimigo_direita2)]
        else:  # Mova para a esquerda
            inimigo["image"] = frames_inimigo_esquerda2[frame_atual % len(frames_inimigo_esquerda2)]

        tela.blit(inimigo["image"], inimigo["rect"])

        desenhar_barra_de_vida(tela, inimigo["rect"].x, inimigo["rect"].y - 10, largura_inimigo, 5, inimigo["vida"], inimigo["vida_maxima"])


    


    personagem_rect = pygame.Rect(pos_x_personagem, pos_y_personagem, largura_personagem, altura_personagem)
    inimigos_rects = [inimigo["rect"] for inimigo in inimigos_comum]

    if verificar_colisao_personagem_inimigo(personagem_rect, inimigos_rects):

        
        if tempo_atual - tempo_ultimo_hit_inimigo >= intervalo_hit_inimigo:
            vida -= 25
            tempo_ultimo_hit_inimigo = tempo_atual  # Atualize o tempo do último hit do inimigo
            # esta parte para iniciar o piscar da barra de vida
            piscando_vida = True




    

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

    

    # Verifica se a pontuação atingiu 1500 e se o jogador pressionou 'Q'
    if pontuacao_exib >= 700 and (keys[pygame.K_q] or (joystick and joystick.get_button(3))):
        pontuacao_exib-=700
        pontuacao_magia-=700
        
        
        ret = tela_de_pausa(velocidade_personagem, intervalo_disparo,vida,largura_disparo, altura_disparo,trembo,dano_person_hit,chance_critico,roubo_de_vida,
                            quantidade_roubo_vida,tempo_cooldown_dash,vida_maxima,Petro_active,Resistencia,vida_petro,vida_maxima_petro,dano_petro,xp_petro,petro_evolucao,Resistencia_petro,
                            Chance_Sorte,Poison_Active,Dano_Veneno_Acumulado,Executa_inimigo,Ultimo_Estalo)
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
    


    

    posicao_barra_vida = (20, altura_mapa - (altura_mapa - 30))
    posicao_barra_magia = (20, altura_mapa * 0.09)
    # Desenha a barra de magia
    largura_barra_magia = (pontuacao_magia / maxima_pontuacao_magia) * int(largura_mapa * 0.215)
    pygame.draw.rect(tela, (53, 239, 252), (posicao_barra_magia[0], posicao_barra_magia[1], largura_barra_magia, altura_mapa - (altura_mapa - 20)))

    # Desenha o placar pontos
    fonte = pygame.font.Font(None, int(altura_barra_vida*0.9))
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao_exib}', True, (250, 255,255))
    tela.blit(texto_pontuacao, (largura_mapa*0.025, altura_mapa*0.096))

    if vida > vida_maxima:
        vida_maxima=vida

    
    pygame.draw.rect(tela, verde, (posicao_barra_vida[0], posicao_barra_vida[1], (vida / vida_maxima) * largura_barra_vida, altura_barra_vida))
    pygame.draw.rect(tela, (255, 255, 255), (posicao_barra_vida[0], posicao_barra_vida[1], largura_barra_vida, altura_barra_vida), 2)

    pygame.draw.rect(tela, (255, 255, 255), (posicao_barra_vida[0], posicao_barra_vida[1], largura_barra_vida, altura_barra_vida), 2)
    # Desenha a quantidade total de vida e a vida atual sobre a barra
    fonte_vida = pygame.font.Font(None, int(altura_barra_vida*0.9))
    texto_vida = fonte_vida.render(f'Vida: {int(vida)}/{int(vida_maxima)}', True, (255, 255, 255))
    tela.blit(texto_vida, (posicao_barra_vida[0]*2, posicao_barra_vida[1]+5, (vida / vida_maxima) * largura_barra_vida, altura_barra_vida))

    # Se o cooldown estiver ativo, mostre-o na tela
    if cooldown_dash:
        tela.blit(cooldown_ativo_img, (largura_mapa - largura_cooldown_img - 10, altura_mapa - altura_cooldown_img - 10))
    else:
        tela.blit(cooldown_concluido_img, (largura_mapa - largura_cooldown_img - 10, altura_mapa - altura_cooldown_img - 10))

    



    # Verifica se já se passaram 4 segundos desde o início da exibição da primeira mensagem
    tempo_atual = pygame.time.get_ticks()
    if not mensagem1_exibida and tempo_atual - tempo_inicial_mensagem1 >= 7000:
        mensagem1_exibida = True  # Marca a mensagem 1 como exibida
        tempo_inicial_mensagem2 = pygame.time.get_ticks()  # Inicia o tempo para a segunda mensagem

    # Verifica se já se passaram 5 segundos desde o início da exibição da segunda mensagem
    if mensagem1_exibida and not mensagem2_exibida and tempo_atual - tempo_inicial_mensagem2 >= 7000:
        mensagem2_exibida = True  # Marca a mensagem 2 como exibida
        tempo_inicial_mensagem3 = pygame.time.get_ticks()  # Inicia o tempo para a segunda mensagem

    # Verifica se já se passaram 7 segundos desde o início da exibição da terceira mensagem
    if mensagem2_exibida and not mensagem3_exibida and tempo_atual - tempo_inicial_mensagem3 >= 7000:
        mensagem3_exibida = True  # Marca a mensagem 3 como exibida
        tempo_inicial_mensagem4 = pygame.time.get_ticks()  # Inicia o tempo para a quarta mensagem

    # Verifica se já se passaram 7 segundos desde o início da exibição da quarta mensagem
    if mensagem3_exibida and not mensagem4_exibida and tempo_atual - tempo_inicial_mensagem4 >= 7000:
        mensagem4_exibida = True  # Marca a mensagem 4 como exibida
        tempo_inicial_mensagem5 = pygame.time.get_ticks()  # Inicia o tempo para a quarta mensagem

    if mensagem4_exibida and not mensagem5_exibida and tempo_atual - tempo_inicial_mensagem5 >= 7000:
        mensagem5_exibida = True  # Marca a mensagem 5 como exibida
        tempo_inicial_mensagem6 = pygame.time.get_ticks()  # Inicia o tempo para a quarta mensagem

    if mensagem5_exibida and not mensagem6_exibida and tempo_atual - tempo_inicial_mensagem6 >= 7000:
        mensagem6_exibida = True  # Marca a mensagem 6 como exibida


    
    # Desenha a mensagem 1 na tela se ainda não foi exibida
    if not mensagem1_exibida:
        fonte1 = pygame.font.Font(None, 36)
        
        cor_texto = (255, 0, 0)  # Cor do texto (vermelho)
        largura_texto, altura_texto = fonte1.size(texto1)  # Obtém as dimensões do texto
        # Calcula a posição para centralizar o texto horizontalmente e mantê-lo na parte inferior da tela
        pos_x_texto = (largura_tela - largura_texto) // 2
        pos_y_texto = altura_tela - altura_texto - 10  # Distância de 10 pixels da borda inferior
        # Desenha o fundo branco do tamanho do texto
        pygame.draw.rect(tela, (255, 255, 255,128), (pos_x_texto - 10, pos_y_texto - 10, largura_texto + 20, altura_texto + 20))
        # Desenha o texto centralizado na tela
        tela.blit(fonte1.render(texto1, True, cor_texto), (pos_x_texto, pos_y_texto))


    if mensagem1_exibida and not mensagem2_exibida:
        fonte2 = pygame.font.Font(None, 36)
        cor_texto = (255, 0, 0)  # Cor do texto (vermelho)
        largura_texto, altura_texto = fonte2.size(texto2)  # Obtém as dimensões do texto
        # Calcula a posição para centralizar o texto horizontalmente e mantê-lo na parte inferior da tela
        pos_x_texto = (largura_tela - largura_texto) // 2
        pos_y_texto = altura_tela - altura_texto - 10  # Distância de 10 pixels da borda inferior
        # Desenha o fundo branco do tamanho do texto
        pygame.draw.rect(tela, (255, 255, 255,128), (pos_x_texto - 10, pos_y_texto - 10, largura_texto + 20, altura_texto + 20))
        # Desenha o texto centralizado na tela
        tela.blit(fonte2.render(texto2, True, cor_texto), (pos_x_texto, pos_y_texto))
    
        # Desenha a mensagem 3 na tela se a mensagem 2 já foi exibida e a mensagem 3 ainda não foi exibida
    if mensagem2_exibida and not mensagem3_exibida:
        fonte3 = pygame.font.Font(None, 36)
        cor_texto = (255, 0, 0)  # Cor do texto (vermelho)
        largura_texto, altura_texto = fonte3.size(texto3)  # Obtém as dimensões do texto
        # Calcula a posição para centralizar o texto horizontalmente e mantê-lo na parte inferior da tela
        pos_x_texto = (largura_tela - largura_texto) // 2
        pos_y_texto = altura_tela - altura_texto - 10  # Distância de 10 pixels da borda inferior
        # Desenha o fundo branco do tamanho do texto
        pygame.draw.rect(tela, (255, 255, 255,128), (pos_x_texto - 10, pos_y_texto - 10, largura_texto + 20, altura_texto + 20))
        # Desenha o texto centralizado na tela
        tela.blit(fonte3.render(texto3, True, cor_texto), (pos_x_texto, pos_y_texto))


        # Desenha a mensagem 4 na tela se a mensagem 3 já foi exibida e a mensagem 4 ainda não foi exibida
    if mensagem3_exibida and not mensagem4_exibida:
        fonte4 = pygame.font.Font(None, 36)
        cor_texto = (255, 0, 0)  # Cor do texto (vermelho)
        largura_texto, altura_texto = fonte4.size(texto4)  # Obtém as dimensões do texto
        # Calcula a posição para centralizar o texto horizontalmente e mantê-lo na parte inferior da tela
        pos_x_texto = (largura_tela - largura_texto) // 2
        pos_y_texto = altura_tela - altura_texto - 10  # Distância de 10 pixels da borda inferior
        # Desenha o fundo branco do tamanho do texto
        pygame.draw.rect(tela, (255, 255, 255,128), (pos_x_texto - 10, pos_y_texto - 10, largura_texto + 20, altura_texto + 20))
        # Desenha o texto centralizado na tela
        tela.blit(fonte4.render(texto4, True, cor_texto), (pos_x_texto, pos_y_texto))

    
        # Desenha a mensagem 5 na tela se a mensagem 4 já foi exibida e a mensagem 5 ainda não foi exibida
    if mensagem4_exibida and not mensagem5_exibida:
        fonte5 = pygame.font.Font(None, 36)
        texto5 = "Cada carta tem seus atributos. Aprenda a entendê-los."
        cor_texto = (255, 0, 0)  # Cor do texto (vermelho)
        largura_texto, altura_texto = fonte5.size(texto5)  # Obtém as dimensões do texto
        # Calcula a posição para centralizar o texto horizontalmente e mantê-lo na parte inferior da tela
        pos_x_texto = (largura_tela - largura_texto) // 2
        pos_y_texto = altura_tela - altura_texto - 10  # Distância de 10 pixels da borda inferior
        # Desenha o fundo branco do tamanho do texto
        pygame.draw.rect(tela, (255, 255, 255,128), (pos_x_texto - 10, pos_y_texto - 10, largura_texto + 20, altura_texto + 20))
        # Desenha o texto centralizado na tela
        tela.blit(fonte5.render(texto5, True, cor_texto), (pos_x_texto, pos_y_texto))

   

        # Renderiza o texto do botão
    fonte_botao = pygame.font.Font(None, 28)
    texto_renderizado = fonte_botao.render(texto_botao, True, (0, 0, 0))

    # Calcula as dimensões do botão com base no texto renderizado
    largura_texto, altura_texto = fonte_botao.size(texto_botao)
    largura_botao = largura_texto + 20  # Largura do botão
    altura_botao = altura_texto + 10  # Altura do botão

    # Posiciona o botão no canto superior direito da tela
    posicao_botao = (largura_tela - largura_botao - 10, 10)

    # Desenha o fundo branco do botão
    pygame.draw.rect(tela, (255, 255, 255, 128), (posicao_botao[0], posicao_botao[1], largura_botao, altura_botao))

    # Desenha o texto do botão
    tela.blit(texto_renderizado, (posicao_botao[0] + 10, posicao_botao[1] + 5))

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