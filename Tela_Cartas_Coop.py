import pygame
import sys
import random
from Variaveis import *
import time




def tela_de_pausa(velocidade_personagem, intervalo_disparo,vida,largura_disparo, altura_disparo,trembo,dano_person_hit,chance_critico,roubo_de_vida,quantidade_roubo_vida,
                  tempo_cooldown_dash,vida_maxima,Petro_active,Resistencia,vida_petro,vida_maxima_petro,dano_petro,xp_petro,petro_evolucao,Resistencia_petro,Chance_Sorte,Poison_Active,Dano_Veneno_Acumulado,Executa_inimigo,Ultimo_Estalo,mostrar_info,Mercenaria_Active,Valor_Bonus,dispositivo_ativo,Tempo_cura,
                    porcentagem_cura,cartas_compradas,pontuacao_exib,max_cartas_compraveis=1,inimigos_eliminados=inimigos_eliminados):
    Rolagens_possiveis = 3
    Rolagens_Dadas = 0
    compras_restantes = max_cartas_compraveis
    DELAY_ENTRE_CARTAS = 200
    ultima_mudanca_de_carta = pygame.time.get_ticks()
    
    pygame.init()
    icone_q = pygame.image.load('Sprites/Q.png')
    icone_q = pygame.transform.scale(icone_q, (50, 50))  # Redimensiona para o tamanho desejado

    icone_rolagem = pygame.image.load('Sprites/Rolagem.png')
    icone_rolagem = pygame.transform.scale(icone_rolagem, (50, 50))  # Redimensiona para o tamanho desejado

    # Posição dos ícones no canto superior esquerdo
    posicao_icone_q = (10, 10)
    posicao_icone_rolagem = (70, 10)
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Tela de Pausa')
    valor_rolagem=250
    
    # Carregar a imagem de fundo e redimensioná-la para ajustar-se à tela
    background = pygame.image.load("Sprites/Cartas_back.png").convert()
    background = pygame.transform.scale(background, (largura_tela, altura_tela))
    # Define os atributos de cada carta em um dicionário
    # Definir cores
    cor_fundo = (30, 30, 30)
    cor_texto = (255, 255, 255)
    cor_contorno = (0, 0, 0)

    # Definir fontes
    fonte_titulo = pygame.font.Font(None, 38)
    fonte_texto = pygame.font.Font(None, 26)
    fonte_pequena = pygame.font.Font(None, 17)
    def render_texto_com_contorno(fonte, texto, cor_texto, cor_contorno, x, y, deslocamento=2):
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
     

    

    atributos_cartas = [
        {"nome": "Speed Boost", "Nick": "Vento Celeste", "velocidade": 10, 
        "descricao": "Aumente sua velocidade em +10%. Corra como o vento e fuja de qualquer situação perigosa. (Aumento acumulativo)"},
        
        {"nome": "Porção", "Nick": "Elixir Vital", "vida_maxima": 50, 
        "descricao": "Recupere 25% da sua vida máxima e ganhe mais vida máxima permanentemente. Excedente vira vida máxima."},
        
        {"nome": "Disparo crescente", "Nick": "Impacto Escalante", "ataque": 20, 
        "descricao": "Ganhe +27 de dano e deixe os inimigos temendo seus tiros poderosos. (Acumulativo com mais cartas)."},
        
        {"nome": "Tempestade", "Nick": "Tempestade Crescente", "Dano e chance critica": 5, 
        "descricao": "Aumente sua chance crítica em 2% e triplique o dano causado. Transforme cada acerto em uma tempestade!"},

        {"nome": "Cura", "Nick": "Mordida Sombria", "Roubo de Vida": 10, 
        "descricao": "Restaure 3% da sua vida a cada hit e 4% a cada ativação. Recupere sua saúde enquanto luta!"},

        {"nome": "Trembo", "Nick": "Reversão Temporal", "segunda_vida": True, 
        "descricao": "Quando a morte se aproxima, o tempo volta. Recupere toda a sua saúde e reapareça em outro local!"},

        {"nome": "Speed Atack", "Nick": "Fluidez Letal", "Velocidade de Ataque": 5, 
        "descricao": "Aumente a velocidade de ataque em 5%, tornando seus tiros rápidos e letais. (Aumento acumulativo)"},
        
        {"nome": "Teleporte", "Nick": "Salto Espacial", "cooldown": 5, 
        "descricao": "Reduza o cooldown do teleporte em 3%, permitindo que você se mova rapidamente entre os campos de batalha."},

        {"nome": "Petro", "Nick": "Sentinela Leal", "Amigo": True, 
        "descricao": "Desencadeie o poder de um pequeno guardião. Alimente-o para ver seu poder crescer e proteger você!"},

        {"nome": "Defesa", "Nick": "Escudo Fásico", "Resistencia": 5, 
        "descricao": "Aumente sua resistência em +5 e mitigue os danos dos inimigos. Uma defesa imbatível para cada desafio."},

        {"nome": "Sorte", "Nick": "Anomalia Favorável", "Sorte": 2, 
        "descricao": "Aumente suas chances de obter cartas raras com 2% de sorte adicional. A sorte agora está ao seu favor!"}
    ]


    # Carrega as imagens das seis cartas disponíveis
    cartas_disponiveis = [
        pygame.image.load('Sprites/Deck/Speed_boost1.png'),  # Dar velocidade
        pygame.image.load('Sprites/Deck/carta_por1.png'),  # Dar mais vida máxima
        pygame.image.load('Sprites/Deck/carta_odio1.png'),  # Dar mais velocidade de ataque
        pygame.image.load('Sprites/Deck/Carta_tempestade_crescente1.png'),  # Dar mais velocidade de movimento
        pygame.image.load('Sprites/Deck/Carta_roubo_vida1.png'),  # Dar um efeito de invisível
        pygame.image.load('Sprites/Deck/carta_trem1.png'),  # Dá uma segunda vida
        pygame.image.load('Sprites/Deck/carta_onda.png'),  # Mais atack speed
        pygame.image.load('Sprites/Deck/carta_teleporte1.png'),# Menos cooldown telporte
        pygame.image.load('Sprites/Deck/carta_petro1.png'),# Um amigo para lhe ajudar na run
        pygame.image.load('Sprites/Deck/carta_defesa1.png'),# Um amigo para lhe ajudar na run
        pygame.image.load('Sprites/Deck/carta_sorte1.png')#Uma sorte cairia bem
         
    ]

    # Carrega os frames da animação das cartas
    frames_cartas = [
        [
            pygame.image.load('Sprites/Deck/Speed_boost1.png'),
            pygame.image.load('Sprites/Deck/Speed_boost2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_por1.png'),
            pygame.image.load('Sprites/Deck/carta_por2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_odio1.png'),
            pygame.image.load('Sprites/Deck/carta_odio2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/Carta_tempestade_crescente1.png'),
            pygame.image.load('Sprites/Deck/Carta_tempestade_crescente2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/Carta_roubo_vida1.png'),
            pygame.image.load('Sprites/Deck/Carta_roubo_vida2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_trem1.png'),
            pygame.image.load('Sprites/Deck/carta_trem2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_onda.png'),
            pygame.image.load('Sprites/Deck/carta_onda2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_teleporte1.png'),
            pygame.image.load('Sprites/Deck/carta_teleporte2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_petro1.png'),
            pygame.image.load('Sprites/Deck/carta_petro2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_defesa1.png'),
            pygame.image.load('Sprites/Deck/carta_defesa2.png')
        ],
        [
            pygame.image.load('Sprites/Deck/carta_sorte1.png'),
            pygame.image.load('Sprites/Deck/carta_sorte2.png')
        ],

    ]


    # Ajusta o tamanho das cartas (opcional)
    largura_carta = 150
    altura_carta = 200
    cartas_disponiveis = [pygame.transform.scale(carta, (largura_carta, altura_carta)) for carta in cartas_disponiveis]
    frames_cartas = [[pygame.transform.scale(frame, (largura_carta, altura_carta)) for frame in frames] for frames in frames_cartas]

    # Associa cada carta a seus atributos e frames de animação
    cartas = []
    for i, carta_img in enumerate(cartas_disponiveis):
        carta = {"imagem": carta_img, "frames_animacao": frames_cartas[i], "frame_atual": 0}
        carta.update(atributos_cartas[i])
        cartas.append(carta)

    # Select three cards randomly from the combined list
    cartas_selecionadas = random.sample(cartas, 3)

    # Variável para rastrear a carta selecionada
    carta_selecionada_index = 0

    # Distância entre as cartas
    distancia_entre_cartas = 100

    # Contador para controlar a animação das cartas
    contador_animacao = 0
    fps_animacao = 140  # Ajuste a velocidade da animação conforme necessário

    # Define a fonte e tamanho do texto
    fonte = pygame.font.Font(None, 20)

    pygame.display.set_caption("Cartas")

    while compras_restantes > 0:
        pos_x = largura_tela // 2 - (len(cartas_compradas) * 100) // 2  # centraliza as cartas
        pos_y = altura_tela - 90  
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  # Tecla A pressionada, seleciona a carta anterior
                    carta_selecionada_index = (carta_selecionada_index - 1) % 3
                elif evento.key == pygame.K_d:  # Tecla D pressionada, seleciona a próxima carta
                    carta_selecionada_index = (carta_selecionada_index + 1) % 3
                elif evento.key == pygame.K_SPACE:  # Tecla ESPAÇO pressionada, confirma a seleção da carta
                    carta_selecionada = cartas_selecionadas[carta_selecionada_index]
                    valor_rolagem=250
                    if carta_selecionada["nome"] == "Speed Boost":  # Se a carta selecionada for "Speed Boost"
                        velocidade_personagem += 0.035 + (inimigos_eliminados // 50) * 0.005  # Aumenta a cada 50 inimigos
                        cartas_compradas["Speed Boost"] += 1

                    elif carta_selecionada["nome"] == "Porção":
                        vida += int(vida_maxima * 0.45 + (inimigos_eliminados // 30) * 0.05)  # Aumenta conforme inimigos eliminados
                        vida_petro += int(vida_maxima_petro * 0.30 + (inimigos_eliminados // 40) * 0.03)  # Aumenta conforme inimigos eliminados
                        if vida_petro > vida_maxima_petro:
                            vida_maxima_petro = vida_petro
                        

                    elif carta_selecionada["nome"] == "Disparo crescente":
                        dano_person_hit += 27 + (inimigos_eliminados // 50) * 10  # Aumenta o dano conforme inimigos são eliminados
                        cartas_compradas["Disparo crescente"] += 1

                    elif carta_selecionada["nome"] == "Trembo":
                        trembo = True
                        Tempo_cura -= Tempo_cura * 0.05
                        porcentagem_cura += 0.001 + (inimigos_eliminados // 100) * 0.0005  # Aumenta a cura gradualmente
                        

                    elif carta_selecionada["nome"] == "Tempestade":
                        dano_person_hit += 10 + (inimigos_eliminados // 50) * 4  # Aumenta o dano conforme inimigos são eliminados
                        chance_critico += 0.02 + (inimigos_eliminados // 100) * 0.005  # Aumenta a chance crítica
                        cartas_compradas["Tempestade"] += 1

                    elif carta_selecionada["nome"] == "Cura":
                        roubo_de_vida += 0.04 + (inimigos_eliminados // 80) * 0.01  # Aumenta o roubo de vida conforme inimigos eliminados
                        quantidade_roubo_vida += 0.03 + (inimigos_eliminados // 80) * 0.005  # Aumenta a quantidade de roubo de vida
                        cartas_compradas["Cura"] += 1

                    elif carta_selecionada["nome"] == "Speed Atack":
                        intervalo_disparo -= 20 + (inimigos_eliminados // 100) * 5  # A cada 100 inimigos, diminui 5 de intervalo
                        if intervalo_disparo < 50:
                            intervalo_disparo = 50  # Limita o intervalo de disparo
                        cartas_compradas["Speed Atack"] += 1

                    elif carta_selecionada["nome"] == "Teleporte":
                        tempo_cooldown_dash -= tempo_cooldown_dash * 0.003 + (inimigos_eliminados // 50) * 0.0005  # A cada 50 inimigos, diminui mais o tempo de cooldown
                        if tempo_cooldown_dash < 0.5:
                            tempo_cooldown_dash = 0.5  # Limita o cooldown do teleporte
                        cartas_compradas["Teleporte"] += 1

                    elif carta_selecionada["nome"] == "Petro":
                        Petro_active = True
                        dano_petro += 2 + (inimigos_eliminados // 30) * 1  # Aumenta o dano do petro conforme inimigos eliminados
                        if petro_evolucao > 0 and petro_evolucao <= 8:
                            xp_petro = "nivel_1"
                            petro_evolucao += 4
                        elif petro_evolucao > 8 and petro_evolucao <= 16:
                            xp_petro = "nivel_2"
                            vida_maxima_petro += 1000
                            petro_evolucao += 4
                        elif petro_evolucao > 16:
                            xp_petro = "nivel_3"
                            vida_maxima_petro += 2000
                            Resistencia_petro += 18
                            dano_petro += 250
                        if vida_petro < vida_maxima_petro:
                            vida_petro += int(vida_maxima_petro * 0.45)
                        if vida_petro > vida_maxima_petro:
                            vida_maxima_petro = vida_petro
                        cartas_compradas["Petro"] += 1

                    elif carta_selecionada["nome"] == "Defesa":
                        Resistencia += 3.5 + (inimigos_eliminados // 50) * 0.5  # Aumenta a resistência conforme inimigos eliminados
                        if Resistencia > 50:
                            Resistencia = 50  # Limita a resistência
                        cartas_compradas["Defesa"] += 1

                    elif carta_selecionada["nome"] == "Sorte":
                        Chance_Sorte += 0.01 + (inimigos_eliminados // 100) * 0.002  # Aumenta a sorte conforme inimigos eliminados
                        cartas_compradas["Sorte"] += 1


                    compras_restantes -= 1  # diminui o contador
                    if compras_restantes > 0:
                        cartas_selecionadas = cartas_selecionadas = random.sample(cartas, 3)
                elif evento.key == pygame.K_w:  # Exibe informações da carta
                    mostrar_info = True
                elif Rolagens_possiveis > Rolagens_Dadas  and evento.key == pygame.K_q:
                    Rolagens_Dadas+=1
                    cartas_selecionadas = random.sample(cartas, 3)

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_w:  # Para de exibir informações da carta ao soltar "W"
                    mostrar_info = False    
                     
            elif evento.type == pygame.JOYAXISMOTION:
                if evento.axis == 0:  # Eixo X do joystick (analógico esquerdo/direito)
                    if pygame.time.get_ticks() - ultima_mudanca_de_carta >= DELAY_ENTRE_CARTAS:
                        if evento.value < -0.5:  # Movimento para a esquerda
                            carta_selecionada_index = (carta_selecionada_index - 1) % 3
                            ultima_mudanca_de_carta = pygame.time.get_ticks()
                        elif evento.value > 0.5:  # Movimento para a direita
                            carta_selecionada_index = (carta_selecionada_index + 1) % 3
                            ultima_mudanca_de_carta = pygame.time.get_ticks()
            elif evento.type == pygame.JOYBUTTONDOWN or evento.type == pygame.KEYDOWN:
                if evento.button == 0:  # Botão X do controle do Xbox pressionado
                    carta_selecionada = cartas_selecionadas[carta_selecionada_index]
                    # Coloque aqui a lógica relacionada à seleção da carta usando o botão do joystick

                    
    
                    if carta_selecionada["nome"] == "Speed Boost":  # Se a carta selecionada for "Speed Boost"
                        velocidade_personagem += 0.065  # Aumenta a velocidade do personagem em 2
                        cartas_compradas["Speed Boost"] += 1
                    elif carta_selecionada["nome"] == "Porção":
                        vida+=int(vida_maxima*0.45)
                        vida_petro+=int(vida_maxima_petro*0.30)
                        if vida_petro > vida_maxima_petro:
                            vida_maxima_petro= vida_petro
                    elif carta_selecionada["nome"] == "Disparo crescente":
                        dano_person_hit+=27
                        cartas_compradas["Disparo crescente"] += 1
                    elif carta_selecionada["nome"] == "Trembo":
                        trembo=True
                        Tempo_cura-= Tempo_cura*0.05
                        porcentagem_cura+= 0.001
                    elif carta_selecionada["nome"] == "Tempestade":
                        dano_person_hit+= 10
                        chance_critico+= 0.02
                        cartas_compradas["Tempestade"] += 1
                    elif carta_selecionada["nome"] == "Cura":
                        roubo_de_vida+=0.04
                        quantidade_roubo_vida+=0.03
                        cartas_compradas["Cura"] += 1
                    elif carta_selecionada["nome"] == "Speed Atack":
                        intervalo_disparo-=20
                        cartas_compradas["Speed Atack"] += 1
                    elif carta_selecionada["nome"] == "Teleporte":
                        tempo_cooldown_dash-= tempo_cooldown_dash*0.003
                        cartas_compradas["Teleporte"] += 1
                    elif carta_selecionada["nome"] == "Petro":
                        Petro_active=True
                        dano_petro+=2
                        
                        #Usado para verificar os niveis do petro para trocar a skin dele
                        if petro_evolucao>0 and petro_evolucao<=8:
                            xp_petro = "nivel_1"
                            petro_evolucao+=4     
                        elif petro_evolucao>8 and petro_evolucao<=16:
                            xp_petro = "nivel_2"
                            vida_maxima_petro+=1000
                            petro_evolucao+=4   
                        elif petro_evolucao>16  :
                            xp_petro = "nivel_3"
                            vida_maxima_petro+=2000
                            Resistencia_petro+=18
                            dano_petro+=250
                            
                                
                        if vida_petro < vida_maxima_petro:
                            vida_petro+=int(vida_maxima_petro*0.45)
                            if vida_petro > vida_maxima_petro:
                                vida_maxima_petro= vida_petro
                        cartas_compradas["Petro"] += 1
                    elif carta_selecionada["nome"] == "Defesa":
                        Resistencia+=3.5
                        cartas_compradas["Defesa"] += 1
                    elif carta_selecionada["nome"] == "Sorte":
                        Chance_Sorte+=0.01
                        cartas_compradas["Sorte"] += 1
                    elif carta_selecionada["nome"] == "Poison":
                        Poison_Active=True
                        Dano_Veneno_Acumulado+=0.05
                        cartas_compradas["Poison"] += 1
                    elif carta_selecionada["nome"] == "Coletora":
                        Executa_inimigo+=0.005
                        Ultimo_Estalo= True
                        cartas_compradas["Coletora"] += 1   
                    elif carta_selecionada["nome"] == "Mercenaria":
                        Mercenaria_Active=True
                        Valor_Bonus+=25
                        cartas_compradas["Coletora"] += 1   
                if evento.type == pygame.JOYBUTTONDOWN:
                    if evento.button == 2:  # Botão X do controle do Xbox
                        mostrar_info = True
            elif evento.type == pygame.JOYBUTTONUP:
                if evento.button == 2:  # Solta o botão X do controle
                    mostrar_info = False
        # Blit do background primeiro
        tela.blit(background, (0, 0))
        # Calcula as posições das cartas para que elas fiquem centralizadas
        total_largura_cartas = 3 * largura_carta + 2 * distancia_entre_cartas
        posicao_inicial = (largura_mapa - total_largura_cartas) // 2
        posicao_y = (altura_mapa - altura_carta) // 2

        for i, carta in enumerate(cartas_selecionadas):
            # Aumenta ligeiramente a escala da carta selecionada
            escala = 1.1 if i == carta_selecionada_index else 1.0
            largura_carta_scaled = int(largura_carta * escala)
            altura_carta_scaled = int(altura_carta * escala)
            carta_scaled = pygame.transform.scale(carta["frames_animacao"][carta["frame_atual"]],
                                              (largura_carta_scaled, altura_carta_scaled))
            # Calcula a posição de desenho considerando a escala e a distância entre as cartas
            pos_x_escala = posicao_inicial + i * (largura_carta + distancia_entre_cartas) - (largura_carta_scaled - largura_carta) // 2
            tela.blit(carta_scaled, (pos_x_escala, posicao_y))
            if i == carta_selecionada_index:
                if dispositivo_ativo == "teclado":
                    tela.blit(icone_w, (pos_x_escala + largura_carta // 2 - 25, posicao_y - 70))
                else:
                    tela.blit(icone_x, (pos_x_escala + largura_carta // 2 - 25, posicao_y - 70))


            # Desenha o texto explicativo no centro da carta
            texto = fonte.render(carta["Nick"], True, (0, 0, 0))  # Renderiza o texto
            texto_rect = texto.get_rect(
            center=(pos_x_escala + largura_carta_scaled // 2, posicao_y + altura_carta_scaled // 1.5))  # Obtém o retângulo do texto
            tela.blit(texto, texto_rect)  # Desenha o texto na tela usando o retângulo
        
        # Atualiza a animação das cartas
        contador_animacao += 1
        if contador_animacao >= fps_animacao:
            contador_animacao = 0
            for carta in cartas_selecionadas:
                carta["frame_atual"] = (carta["frame_atual"] + 1) % 2


        for nome, quantidade in cartas_compradas.items():
            if quantidade > 0:  # Apenas renderiza cartas compradas
                # Renderiza a imagem da carta
                imagem_carta = cartas_imagens[nome]
                tela.blit(imagem_carta, (pos_x, pos_y))
                
                # Renderiza a quantidade de cartas compradas
                fonte = pygame.font.SysFont('Texto/Doctor Glitch.otf', 20)
                texto = fonte.render(str(quantidade), True, (0, 0, 0))  # Cor do texto em branco
                tela.blit(texto, (pos_x + 30, pos_y + 70))  
                
                # Atualiza a posição X para a próxima carta
                pos_x += 50  # Espaço entre as cartas  
        # Reroll principal (centralizado)
        texto_reroll = f"Reroll: {Rolagens_possiveis}"
        largura_texto = fonte_titulo.render(texto_reroll, True, cor_texto).get_width()
        render_texto_com_contorno(
            fonte_titulo,
            texto_reroll,
            cor_texto,
            cor_contorno,
            (largura_tela - largura_texto) // 2,
            50
        )

        # Compras restantes (centralizado)
        texto_compras = f"Compras restantes: {compras_restantes}"
        largura_texto = fonte_titulo.render(texto_compras, True, cor_texto).get_width()
        render_texto_com_contorno(
            fonte_titulo,
            texto_compras,
            cor_texto,
            cor_contorno,
            (largura_tela - largura_texto) // 2,
            130
        )

        # Reroll restantes (centralizado e menor)
        texto_restantes = f"Reroll restantes ({Rolagens_possiveis - Rolagens_Dadas})"
        fonte_reroll_restante = pygame.font.Font(None, 42)
        largura_texto = fonte_reroll_restante.render(texto_restantes, True, cor_texto).get_width()
        render_texto_com_contorno(
            fonte_reroll_restante,
            texto_restantes,
            cor_texto,
            cor_contorno,
            (largura_tela - largura_texto) // 2,
            200
        )


        if mostrar_info:
            carta_selecionada = cartas_selecionadas[carta_selecionada_index]
            pos_x_info = posicao_inicial + carta_selecionada_index * (largura_carta + distancia_entre_cartas) + posicao_info_x
            pos_y_info = posicao_y + posicao_info_y  # Ajusta a posição com o deslocamento vertical

            # Desenha o quadrado branco com altura ajustada
            largura_quadrado = largura_carta
            altura_quadrado = 210
            pygame.draw.rect(tela, (255, 255, 255), (pos_x_info, pos_y_info, largura_quadrado, altura_quadrado))
            
            # Divide o texto em múltiplas linhas se for muito longo
            fonte_pequena = pygame.font.Font(None, 18)  # Fonte menor
            texto_descricao = carta_selecionada["descricao"]
            linhas = []
            largura_maxima_texto = largura_quadrado - 20  # Margem de 10px em cada lado

            # Quebra o texto em múltiplas linhas
            palavras = texto_descricao.split()
            linha_atual = ""
            for palavra in palavras:
                if fonte_pequena.size(linha_atual + palavra)[0] > largura_maxima_texto:
                    linhas.append(linha_atual)
                    linha_atual = palavra + " "
                else:
                    linha_atual += palavra + " "
            linhas.append(linha_atual)

            # Renderiza o nome da carta
            texto_nome = fonte.render(carta_selecionada["nome"], True, (0, 0, 0))
            tela.blit(texto_nome, (pos_x_info + 10, pos_y_info + 10))

            # Renderiza as linhas do texto de descrição
            for i, linha in enumerate(linhas):
                texto_linha = fonte_pequena.render(linha.strip(), True, (0, 0, 0))
                tela.blit(texto_linha, (pos_x_info + 10, pos_y_info + 35 + i * 18))

        
        tela.blit(icone_q, posicao_icone_q)
        tela.blit(icone_rolagem, posicao_icone_rolagem)
        pygame.display.flip()

        
    return [velocidade_personagem, intervalo_disparo,vida,largura_disparo, altura_disparo,trembo,dano_person_hit,chance_critico,roubo_de_vida,
            quantidade_roubo_vida,tempo_cooldown_dash,vida_maxima,Petro_active,Resistencia,vida_petro,vida_maxima_petro,dano_petro,xp_petro,petro_evolucao,Resistencia_petro,
            Chance_Sorte,Poison_Active,Dano_Veneno_Acumulado,Executa_inimigo,Ultimo_Estalo,Mercenaria_Active,Valor_Bonus,dispositivo_ativo,Tempo_cura,porcentagem_cura,cartas_compradas,pontuacao_exib]


