import pygame
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import json
import random
import os

DIMENSAO_EMBEDDING = 64
CABECAS_ATENCAO = 4
CAMADAS_TRANSFORMER = 2
MAX_SEQ_LEN = 30

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class UmbraLLM(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, DIMENSAO_EMBEDDING)
        self.pos_encoder = PositionalEncoding(DIMENSAO_EMBEDDING, MAX_SEQ_LEN)
        encoder_layers = nn.TransformerEncoderLayer(
            d_model=DIMENSAO_EMBEDDING, nhead=CABECAS_ATENCAO, dim_feedforward=128, dropout=0.1, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layers, num_layers=CAMADAS_TRANSFORMER)
        self.decoder = nn.Linear(DIMENSAO_EMBEDDING, vocab_size)

    def forward(self, x, mask=None):
        x = self.embedding(x) * math.sqrt(DIMENSAO_EMBEDDING)
        x = self.pos_encoder(x)
        output = self.transformer(x, mask=mask)
        return self.decoder(output)

class OratoriaUmbra:
    def __init__(self):
        with open("umbra_vocab.json", "r", encoding="utf-8") as f:
            self.vocabulario = json.load(f)
        self.inv_vocabulario = {v: k for k, v in self.vocabulario.items()}
        
        self.modelo = UmbraLLM(len(self.vocabulario))
        try:
            self.modelo.load_state_dict(torch.load("umbra_brain.pth", weights_only=True))
        except:
            self.modelo.load_state_dict(torch.load("umbra_brain.pth"))
        self.modelo.eval()

        self.fala_atual = ""
        self.tempo_fala_fim = 0
        self.tempo_silencio_fim = 0  # Período obrigatório onde ela fica calada
        self.historico_falas = []    # Memória de curto prazo para não repetir falas
        
        try:
            self.fonte = pygame.font.Font("Texto/World.otf", 16)
        except:
            self.fonte = pygame.font.SysFont("Courier New", 16, bold=True)
            
        self.memorias = self._carregar_memorias()

    def _carregar_memorias(self):
        if os.path.exists("umbra_memorias_fatais.json"):
            with open("umbra_memorias_fatais.json", "r") as f:
                return json.load(f)
        return {"mortes_jogador": 0, "mortes_umbra": 0}

    def registrar_morte_jogador(self):
        self.memorias["mortes_jogador"] += 1
        with open("umbra_memorias_fatais.json", "w") as f:
            json.dump(self.memorias, f)

    def avaliar_contexto(self, cartas, estado):
        pesos = {
            "MORTE_ALTA": self.memorias["mortes_jogador"] * 10,
            "CURA": (cartas.get("Cura", 0) + cartas.get("Porção", 0)) * 15,
            "SPEED BOOST": cartas.get("Speed Boost", 0) * 15,
            "LONGE": 25 if "longe" in estado else 0,
            "ERRATICO": 30 if "erratico" in estado else 0,
            "PETRO": cartas.get("Petro", 0) * 20,
            "TREMBO": cartas.get("Trembo", 0) * 20
        }
        
        # Filtra apenas os contextos que estão acontecendo
        pesos_validos = {k: v for k, v in pesos.items() if v > 0}
        
        if not pesos_validos:
            return "[CONTEXTO: CURA]" 

        # Sistema de Roleta (Sorteio ponderado para diversificar os assuntos)
        total_pesos = sum(pesos_validos.values())
        sorteio = random.uniform(0, total_pesos)
        acumulado = 0
        
        for contexto, peso in pesos_validos.items():
            acumulado += peso
            if sorteio <= acumulado:
                return f"[CONTEXTO: {contexto}]"
                
        return f"[CONTEXTO: {list(pesos_validos.keys())[0]}]"

    def invocar_fala(self, agora, cartas_compradas, estado_composto, temperatura=0.90):
        # Impede a Umbra de falar se o balão estiver visível ou no período de silêncio
        if agora < self.tempo_fala_fim or agora < self.tempo_silencio_fim:
            return

        contexto_input = self.avaliar_contexto(cartas_compradas, estado_composto)
        palavras_input = contexto_input.replace("]", "] ").replace("[", " [").split()
        
        tokens = [self.vocabulario["<BOS>"]]
        for p in palavras_input:
            tokens.append(self.vocabulario.get(p, self.vocabulario["<PAD>"]))
            
        tamanho_prompt = len(tokens)
        
        with torch.no_grad():
            for _ in range(MAX_SEQ_LEN):
                x = torch.tensor([tokens], dtype=torch.long)
                sz = x.size(1)
                mask = torch.triu(torch.ones(sz, sz) * float('-inf'), diagonal=1)
                predicao = self.modelo(x, mask=mask)
                
                logits = predicao[0, -1, :]
                probabilidades = F.softmax(logits / temperatura, dim=-1)
                proximo_token = torch.multinomial(probabilidades, num_samples=1).item()
                
                if proximo_token == self.vocabulario["<EOS>"]:
                    break
                tokens.append(proximo_token)
                
        nova_fala = " ".join([self.inv_vocabulario.get(t, "") for t in tokens[tamanho_prompt:]])
        
        # Filtro Absoluto Anti-Repetição
        if nova_fala in self.historico_falas or len(nova_fala) < 5:
            # Se for repetida, penaliza com silêncio curto e tenta outro assunto depois
            self.tempo_silencio_fim = agora + 2000
            return
            
        # Grava na memória para não repetir
        self.historico_falas.append(nova_fala)
        if len(self.historico_falas) > 3:
            self.historico_falas.pop(0)

        self.fala_atual = nova_fala
        
        # O tempo de leitura dinâmico (mais tempo para ler)
        tempo_leitura = len(self.fala_atual) * 80  
        self.tempo_fala_fim = agora + max(3000, tempo_leitura)
        
        # Define o Silêncio Obrigatório (A Umbra fica quieta de 8 a 15 segundos após a frase sumir)
        self.tempo_silencio_fim = self.tempo_fala_fim + random.randint(8000, 15000)

    def desenhar_balao(self, tela, boss_rect, agora):
        # Desintegra o balão no exato milissegundo correto
        if agora > self.tempo_fala_fim:
            self.fala_atual = ""
            return

        if self.fala_atual == "":
            return

        texto_render = self.fonte.render(self.fala_atual, True, (0, 255, 204))
        largura_texto = texto_render.get_width()
        altura_texto = texto_render.get_height()

        margem = 12
        balao_rect = pygame.Rect(0, 0, largura_texto + margem*2, altura_texto + margem*2)
        balao_rect.centerx = boss_rect.centerx
        balao_rect.bottom = boss_rect.top - 20

        if balao_rect.top < 10:
            balao_rect.top = 10

        s = pygame.Surface((balao_rect.width, balao_rect.height), pygame.SRCALPHA)
        s.fill((0, 10, 20, 210))
        tela.blit(s, balao_rect.topleft)
        pygame.draw.rect(tela, (138, 43, 226), balao_rect, 2)

        p1 = (balao_rect.centerx - 10, balao_rect.bottom)
        p2 = (balao_rect.centerx + 10, balao_rect.bottom)
        p3 = (boss_rect.centerx, balao_rect.bottom + 15)
        pygame.draw.polygon(tela, (138, 43, 226), [p1, p2, p3], 2)
        pygame.draw.polygon(tela, (0, 10, 20), [p1, p2, p3])

        tela.blit(texto_render, (balao_rect.x + margem, balao_rect.y + margem))