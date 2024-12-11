import pygame
from moviepy.editor import VideoFileClip
from Variaveis import largura_mapa, altura_mapa
import subprocess
import sys

# Inicializa o Pygame
pygame.init()


# Configura a tela do Pygame
screen = pygame.display.set_mode((largura_mapa, altura_mapa))

# Função para reproduzir um vídeo
def play_video(filename):
    clip = VideoFileClip(filename)
    clip = clip.resize((largura_mapa, altura_mapa))  # Redimensiona o vídeo para caber na tela
    clip.preview(fullscreen=False)
    clip.close()

# Função para exibir uma imagem
def show_image(filename):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, (largura_mapa, altura_mapa))
    screen.blit(image, (0, 0))
    pygame.display.update()

play_video("Video/Cap1.mp4")

# Mostra a imagem inicial
show_image("Sprites/Hospital.png")

play_video("Video/Cap2.mp4")

show_image("Sprites/Cap1-explo-frame1.png")#É para ser um frame, porém so temos uma imagem. vou chamar de "Momento caotico"

play_video("Video/Cap2.5.mp4")

# Espera por um curto período (opcional)
pygame.time.wait(500)  # 2000 milissegundos = 2 segundos

executando = True
video_playing = True  # Flag para controlar se o vídeo está sendo reproduzido

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  # Verifica se a tecla pressionada é a tecla ESC
                import GAME
                
    if video_playing:
        # Atualiza a tela do Pygame
        pygame.display.update()
        # Coloque aqui o código para reproduzir o vídeo
    else:
        # Se o vídeo não estiver sendo reproduzido, saia do loop
        executando = False

# Fecha o Pygame após o loop terminar
pygame.quit()
