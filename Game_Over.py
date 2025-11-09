import pygame
import time
import random  

# Inicializar Pygame
pygame.init()

# Inicializa o controle Xbox (definir a variável joystick fora da verificação)
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Função para desenhar botões
def draw_buttons(surface, buttons, selected):
    font = pygame.font.Font(None, 40)
    for i, button in enumerate(buttons):
        color = (255, 0, 0) if i == selected else (255, 255, 255)
        text_surface = font.render(button, True, color)
        x = surface.get_width() // 2 - text_surface.get_width() // 2
        y = surface.get_height() // 2 - text_surface.get_height() // 2 + i * 50
        surface.blit(text_surface, (x, y))

# Lista de botões
buttons = ["Voltar para o Menu", "Tentar Novamente", "Sair"]
selected_button = 0

# Definição do atraso entre as mudanças de botão (em milissegundos)
DELAY_ENTRE_BOTOES = 200  # Por exemplo, 200 milissegundos
ultima_mudanca_de_botao = pygame.time.get_ticks()  # Controle do tempo da última mudança

# Som do jogo
som_game = pygame.mixer.Sound("Sounds/Game_Over.mp3")
som_game.set_volume(0.8)  # Defina o volume do som
som_game.play()

# Criar a janela
window = pygame.display.set_mode((1360 * 0.8, 768 * 1))

# Escolher e exibir a imagem de fundo
background_image = pygame.image.load(
    'Sprites/Game_over2.png' if random.randint(1, 100) <= 2 else 'Sprites/Game_over1.png'
)
background_image = pygame.transform.scale(background_image, window.get_size())
window.blit(background_image, (0, 0))

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                if pygame.time.get_ticks() - ultima_mudanca_de_botao >= DELAY_ENTRE_BOTOES:
                    selected_button = (selected_button - 1) % len(buttons)
                    ultima_mudanca_de_botao = pygame.time.get_ticks()
            elif event.key == pygame.K_s:
                if pygame.time.get_ticks() - ultima_mudanca_de_botao >= DELAY_ENTRE_BOTOES:
                    selected_button = (selected_button + 1) % len(buttons)
                    ultima_mudanca_de_botao = pygame.time.get_ticks()
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                som_game.stop()
                if buttons[selected_button] == "Sair":
                    running = False
                elif buttons[selected_button] == "Voltar para o Menu":
                    import Ruptura_Temporal
                elif buttons[selected_button] == "Tentar Novamente":
                    import GAMERE

        # Detecta entrada do controle Xbox, apenas se o joystick estiver inicializado
        if joystick and joystick.get_init():
            eixo_vertical = joystick.get_axis(1)  # Analógico esquerdo, eixo vertical
            if eixo_vertical < -0.5 and pygame.time.get_ticks() - ultima_mudanca_de_botao >= DELAY_ENTRE_BOTOES:
                selected_button = (selected_button - 1) % len(buttons)
                ultima_mudanca_de_botao = pygame.time.get_ticks()
            elif eixo_vertical > 0.5 and pygame.time.get_ticks() - ultima_mudanca_de_botao >= DELAY_ENTRE_BOTOES:
                selected_button = (selected_button + 1) % len(buttons)
                ultima_mudanca_de_botao = pygame.time.get_ticks()

            # Botão A para selecionar
            if joystick.get_button(0):  # Botão A
                som_game.stop()
                if buttons[selected_button] == "Sair":
                    running = False
                elif buttons[selected_button] == "Voltar para o Menu":
                    import Ruptura_Temporal
                elif buttons[selected_button] == "Tentar Novamente":
                    import json
                    from rede import iniciar_host, conectar_ao_host

                    # Lê o modo e IP salvos
                    with open("modo_jogo.json", "r") as f:
                        dados = json.load(f)

                    modo = dados["modo"]
                    ip = dados["ip"]

                    # Recria a conexão conforme o modo
                    if modo == "host":
                        conn = iniciar_host()
                    elif modo == "join" and ip:
                        conn = conectar_ao_host(ip)

                    # Quando conectado, inicia o jogo novamente
                    import GAMERE
                    GAMERE.modo = modo
                    if modo == "join":
                        GAMERE.ip_host = ip
                    GAMERE.conn = conn


    # Desenha botões
    window.blit(background_image, (0, 0))  # Redesenha o fundo
    draw_buttons(window, buttons, selected_button)
    pygame.display.flip()

# Encerrar Pygame
pygame.quit()

