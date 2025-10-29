import pygame
import sys
import time
from Variaveis import largura_tela, altura_tela

# Inicializar o Pygame
pygame.init()

# Criar a tela em modo de tela cheia
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Minha Tela Pygame")

# Carregar a imagem de fundo
imagem_fundo = pygame.image.load("Sprites/Mensagem.png")
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_tela, altura_tela))

fonte_path = "Texto/Machine.ttf"  # Substitua pelo caminho correto
fonte = pygame.font.Font(fonte_path, 20)

# Mensagem a ser exibida
mensagem = "Na fenda azul, encontrei uma civilização hostil de pinguins, que não hesitou em me atacar assim que pus os pés em seu território. Instintivamente, reagi, lutando com fúria para me defender. Cada golpe era uma defesa, um lembrete de que não permitiria que nada me detivesse em minha busca. Revidar era uma necessidade, uma garantia de que seguiria em frente sem impedimentos."

# Definir o tamanho e a posição do 'caderno'
largura_caderno = int(largura_tela / 2.95)  # Largura do caderno
altura_caderno = int(altura_tela / 2)  # Altura do caderno
posicao_x_caderno = int(largura_tela / 2.95)  # Posição X do caderno na tela
posicao_y_caderno = int(altura_tela / 4)

# Ajustar a largura da área de texto para caber dentro do quadrado branco
largura_texto = largura_caderno - 10  # 10 pixels de margem

# Renderizar o texto considerando a largura ajustada
texto = fonte.render(mensagem, True, (0, 255, 0))  # Verde: (0, 255, 0)

# Ajustar a altura da área de texto para caber dentro do quadrado branco
if texto.get_width() > largura_texto:
    linhas_texto = []
    palavras = mensagem.split()
    linha_atual = palavras[0]
    for palavra in palavras[1:]:
        teste_linha = linha_atual + ' ' + palavra
        if fonte.render(teste_linha, True, (0, 255, 0)).get_width() <= largura_texto:  # Verde: (0, 255, 0)
            linha_atual = teste_linha
        else:
            linhas_texto.append(linha_atual)
            linha_atual = palavra
    linhas_texto.append(linha_atual)

# Função para renderizar o texto com efeito de digitação
def renderizar_com_efeito_digitar(texto_completo, fonte, largura_texto):
    # Desenhar o fundo preto uma vez antes de começar a escrever
    tela.fill((0, 0, 0), (posicao_x_caderno + 5, posicao_y_caderno + 2, largura_texto, altura_caderno))  # Preto: (0, 0, 0)

    for linha_idx, linha in enumerate(linhas_texto):
        texto_linha = ""
        for char_idx, char in enumerate(linha):
            texto_linha += char
            texto_renderizado = fonte.render(texto_linha, True, (0, 255, 0))  # Verde: (0, 255, 0)
            tela.blit(texto_renderizado, (posicao_x_caderno + 5, posicao_y_caderno + 2 + (linha_idx * fonte.get_height())))
            pygame.display.flip()
            pygame.time.delay(50)  # Ajuste o tempo de atraso conforme necessário

            # Verifica se a linha ainda cabe na tela ou se precisa pular para a próxima
            if char_idx == len(linha) - 1 and linha_idx != len(linhas_texto) - 1:
                time.sleep(0.3)  # Adicione um pequeno atraso entre as linhas

# Segunda mensagem a ser exibida
segunda_mensagem = "Após um período de confronto intenso, o líder dos pinguins emergiu. Sua presença era marcada por uma nevasca gélida que congelava tudo ao seu redor. Com cada golpe, o calor da minha determinação dissipava o gelo que me ameaçava. Após eliminar o líder, consegui a peça da máquina. Sem hesitar, segui em frente em direção à próxima fenda, uma fenda amarela, emanando um odor repugnante."
# Renderizar o texto da segunda mensagem
segundo_texto = fonte.render(segunda_mensagem, True,(0, 255, 0))  # Verde: (0, 255, 0)

# Ajustar a altura da área de texto para caber dentro do quadrado branco
if segundo_texto.get_width() > largura_texto:
    linhas_segundo_texto = []
    palavras_segundo_texto = segunda_mensagem.split()
    linha_atual_segundo_texto = palavras_segundo_texto[0]
    for palavra_segundo_texto in palavras_segundo_texto[1:]:
        teste_linha_segundo_texto = linha_atual_segundo_texto + ' ' + palavra_segundo_texto
        if fonte.render(teste_linha_segundo_texto, True, (0, 255, 0)).get_width() <= largura_texto:  # Verde: (0, 255, 0)
            linha_atual_segundo_texto = teste_linha_segundo_texto
        else:
            linhas_segundo_texto.append(linha_atual_segundo_texto)
            linha_atual_segundo_texto = palavra_segundo_texto
    linhas_segundo_texto.append(linha_atual_segundo_texto)

# Função para renderizar o texto com efeito de digitação para a segunda mensagem
def renderizar_com_efeito_digitar_segundo_texto(segunda_texto_completo, fonte, largura_texto):
    # Desenhar o fundo preto uma vez antes de começar a escrever a segunda mensagem
    tela.fill((0, 0, 0), (posicao_x_caderno + 5, posicao_y_caderno + 2, largura_texto, altura_caderno))  # Preto: (0, 0, 0)

    for linha_idx, linha_segundo_texto in enumerate(linhas_segundo_texto):
        texto_segundo_linha = ""
        for char_idx, char_segundo_texto in enumerate(linha_segundo_texto):
            texto_segundo_linha += char_segundo_texto
            texto_renderizado_segundo_texto = fonte.render(texto_segundo_linha, True, (0, 255, 0))  # Verde: (0, 255, 0)
            tela.blit(texto_renderizado_segundo_texto, (posicao_x_caderno + 5, posicao_y_caderno + 2 + (linha_idx * fonte.get_height())))
            pygame.display.flip()
            pygame.time.delay(50)  # Ajuste o tempo de atraso conforme necessário

            # Verifica se a linha ainda cabe na tela ou se precisa pular para a próxima
            if char_idx == len(linha_segundo_texto) - 1 and linha_idx != len(linhas_segundo_texto) - 1:
                time.sleep(0.3)  # Adicione um pequeno atraso entre as linhas





# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Desenhar a imagem de fundo
    tela.blit(imagem_fundo, (0, 0))

    # Desenhar o quadrado preto para o fundo do texto
    pygame.draw.rect(tela, (0, 0, 0), (posicao_x_caderno, posicao_y_caderno, largura_caderno, altura_caderno))  # Preto: (0, 0, 0)

    # Atualizar a tela
    pygame.display.flip()

    # Aguardar por 5 segundos antes de começar a digitar a primeira mensagem
    pygame.time.delay(5000)

    # Chamar a função com efeito de digitação
    renderizar_com_efeito_digitar(mensagem, fonte, largura_texto)
    

    # Atualizar a tela
    pygame.display.flip()

    # Aguardar por 2 segundos antes de exibir a segunda mensagem
    pygame.time.delay(2000)

    # Exibir a segunda mensagem
    renderizar_com_efeito_digitar_segundo_texto(segunda_mensagem, fonte, largura_texto)

    # Aguardar por 5 segundos antes de fechar a tela
    pygame.time.delay(5000)  # 5000 milissegundos = 5 segundos

    # Fechar o Pygame
    pygame.quit()
    sys.exit()

    # Esperar por 5 segundos antes de fechar a tela
    pygame.time.delay(3000)  # 3000 milissegundos = 3 segundos

    # Fechar o Pygame
    pygame.quit()
    sys.exit()