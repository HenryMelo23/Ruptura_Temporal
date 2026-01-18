import pygame
import math
import random
from Variaveis import espacamento, largura_mapa, altura_mapa
import json
import os

class MemoriaEvolutivaUmbra:
    def __init__(self, arquivo="memoria_umbra.json"):
        self.arquivo = arquivo
        self.aprendizado = 0.1
        self.desconto = 0.9
        self.exploracao = 0.2
        self.q_table = self._carregar()
        self.ultimo_estado = None
        self.ultima_acao = None

    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as f:
                return json.load(f)
        return {}

    def salvar(self):
        with open(self.arquivo, 'w') as f:
            json.dump(self.q_table, f)

    def discretizar_estado(self, vida_perc, dist_player, sob_fogo):
        v = "crit" if vida_perc < 0.35 else "estavel"
        d = "perto" if dist_player < 350 else "longe"
        f = "perigo" if sob_fogo else "calmo"
        return f"{v}_{d}_{f}"

    def decidir(self, estado, acoes):
        if estado not in self.q_table:
            self.q_table[estado] = {a: 0.0 for a in acoes}
        
        if random.random() < self.exploracao:
            self.ultima_acao = random.choice(acoes)
        else:
            self.ultima_acao = max(self.q_table[estado], key=self.q_table[estado].get)
        
        self.ultimo_estado = estado
        return self.ultima_acao

    def treinar(self, recompensa):
        if self.ultimo_estado and self.ultima_acao:
            v_antigo = self.q_table[self.ultimo_estado][self.ultima_acao]
            # Algoritmo de Bellman: $Q(s,a) = Q(s,a) + \alpha \cdot (r - Q(s,a))$
            self.q_table[self.ultimo_estado][self.ultima_acao] = v_antigo + self.aprendizado * (recompensa - v_antigo)

def calcular_distancia(p1, p2):
    r"""
    Calcula a distância euclidiana: $d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$
    """
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def calcular_poh(player_pos, boss_pos, historico_player, confianca_ia):
    if len(historico_player) < 60: return 0
    # Vetores de estabilidade
    p_ini, p_mid, p_end = historico_player[0], historico_player[30], historico_player[-1]
    v1 = (p_mid[0] - p_ini[0], p_mid[1] - p_ini[1])
    v2 = (p_end[0] - p_mid[0], p_end[1] - p_mid[1])
    
    estabilidade = 1.0 if (abs(v1[0]-v2[0]) < 5 and abs(v1[1]-v2[1]) < 5) else 0.5
    fator_dist = max(0.3, 1.0 - (calcular_distancia(player_pos, boss_pos) / 1500))
    
    return confianca_ia * estabilidade * fator_dist

def node_ataque_direcionado(agora, estado_ia, bx, by, px, py, historico_player, memoria):
    """
    Nódulo de Ofensiva Visionária: Integra predição física com aprendizado generativo.
    """
    # 1. VALIDAÇÃO DE CADÊNCIA (COOLDOWN)
    if agora - estado_ia.get('ultimo_attack', 0) >= estado_ia.get('intervalo', 1900):
        
        # 2. CÁLCULO FÍSICO DO TEMPO DE VOO
        distancia = math.hypot(px - bx, py - by)
        vel_projetil = 7  # Mantendo sua variável de contexto
        
        # Tempo (em frames) que o tiro levará para chegar: $t = d / v$
        tempo_voo = distancia / vel_projetil
        
        # 3. CONSULTA À MEMÓRIA GENERATIVA (O PESO DA EXPERIÊNCIA)
        # A IA discretiza a situação para decidir o quão agressiva será a mira
        vida_perc = estado_ia.get('vida_atual', 1) / estado_ia.get('vida_max', 1)
        estado_disc = memoria.discretizar_estado(vida_perc, distancia, True)
        
        # O 'fator_lead' deixa de ser fixo (0.8) e passa a ser influenciado pela Q-Table
        # Se a IA errou muito recentemente, ela aprenderá a reduzir ou aumentar este peso
        fator_aprendido = estado_ia.get('lead', 0.8)
        
        # 4. EXTRAPOLAÇÃO DINÂMICA
        if len(historico_player) >= 2:
            v_px = px - historico_player[-2][0]
            v_py = py - historico_player[-2][1]
            
            # O alvo agora é projetado exatamente para onde o player estará no momento do impacto
            alvo_x = px + (v_px * tempo_voo * fator_aprendido)
            alvo_y = py + (v_py * tempo_voo * fator_aprendido)
        else:
            alvo_x, alvo_y = px, py

        # 5. EXECUÇÃO DO DISPARO
        angulo = math.atan2(alvo_y - by, alvo_x - bx)
        estado_ia['projeteis'].append({
            "rect": pygame.Rect(bx + 20, by + 20, 12, 12),
            "angulo": angulo,
            "velocidade": vel_projetil,
            "tipo": "comum",
            "cor": (255, 50, 50)
        })

        estado_ia['ultimo_attack'] = agora

# --- NÓDULOS DE PENSAMENTO (AÇÕES DO GRAFO) ---

def node_furia(agora, estado_ia, hitbox_centro, centro_mapa, boss_pos):
    """Nódulo de ataque em espiral 360."""
    dist_ao_centro = calcular_distancia(centro_mapa, (boss_pos['x'], boss_pos['y']))
    
    if estado_ia['furia_fase'] == "caminhando":
        if dist_ao_centro > 15:
            estado_ia['f_fuga_x'] = (centro_mapa[0] - boss_pos['x']) / dist_ao_centro * 5
            estado_ia['f_fuga_y'] = (centro_mapa[1] - boss_pos['y']) / dist_ao_centro * 5
        else:
            estado_ia['furia_fase'] = "espiral"
            estado_ia['angulo_furia'] = 0
    elif estado_ia['furia_fase'] == "espiral":
        estado_ia['projeteis'].append({
            "rect": pygame.Rect(hitbox_centro[0], hitbox_centro[1], 35, 35),
            "angulo": estado_ia['angulo_furia'], "velocidade": 4.0, "tipo": "furia"
        })
        estado_ia['angulo_furia'] += 0.15
        if estado_ia['angulo_furia'] >= 2 * math.pi:
            estado_ia['furia_fase'] = "espera"
            estado_ia['ultimo_furia'] = agora

def node_sifon(agora, estado_ia, boss_pos, centro_mapa):
    """
    Nódulo de Estase e Cura: O Boss torna-se o epicentro do mapa.
    """
    # 1. CÁLCULO DE DESLOCAMENTO AO CENTRO
    dx = centro_mapa[0] - boss_pos['x']
    dy = centro_mapa[1] - boss_pos['y']
    dist_ao_centro = math.hypot(dx, dy)

    # Se ainda não chegou ao centro, move-se rapidamente para lá
    if dist_ao_centro > 5:
        estado_ia['f_fuga_x'] = (dx / dist_ao_centro) * 8
        estado_ia['f_fuga_y'] = (dy / dist_ao_centro) * 8
    else:
        # Chegou ao centro: Ancoragem absoluta
        estado_ia['f_fuga_x'], estado_ia['f_fuga_y'] = 0, 0
        
    # 2. GESTÃO DO TEMPO DE ATIVAÇÃO (4 SEGUNDOS)
    # Verificamos se o tempo de duração expirou
    if agora - estado_ia.get('ultimo_parede', 0) > 4000:
        estado_ia['parede_ativa'] = False
        # O SEGREDO: O cooldown começa a contar AGORA
        estado_ia['ultimo_sifon_fim'] = agora

def node_teleporte(agora, estado_ia, boss_pos, player_pos, historico_player, tipo="fuga"):
    """
    Nódulo de Translocação Visionário: Substitui o acaso por intenção tática.
    """
    bx, by = boss_pos['x'], boss_pos['y']
    px, py = player_pos[0], player_pos[1]
    
    if tipo == "fuga":
        # ESTRATÉGIA DE MAXIMIZAÇÃO DE DISTÂNCIA
        # Identifica os cantos da arena e seleciona o que está mais longe do Senhor
        cantos = [(150, 150), (1150, 150), (150, 620), (1150, 620)]
        alvo_x, alvo_y = max(cantos, key=lambda c: math.hypot(c[0] - px, c[1] - py))
    else:
        # ESTRATÉGIA DE INTERCEPTAÇÃO PREDITIVA
        # Se houver histórico, projeta o salto à frente do seu vetor de movimento
        if len(historico_player) >= 2:
            vx = px - historico_player[-2][0]
            vy = py - historico_player[-2][1]
            alvo_x = px + (vx * 25) # Intercepta 25 frames à frente
            alvo_y = py + (vy * 25)
        else:
            # Flanqueamento Lateral em caso de alvo estático
            alvo_x = px + (350 if bx < px else -350)
            alvo_y = py

    # CONTENÇÃO FÍSICA (Limites fornecidos pelo Senhor)
    alvo_x = max(150, min(1150, alvo_x))
    alvo_y = max(150, min(620, alvo_y))
    
    # Materialização do Projétil Sinalizador
    estado_ia['proj_tele'] = {
        "rect": pygame.Rect(bx, by, 30, 30),
        "angulo": math.atan2(alvo_y - by, alvo_x - bx),
        "tipo": tipo, 
        "alvo_pos": (alvo_x, alvo_y), 
        "velocidade": 12 # Velocidade calibrada para resposta tática
    }
    
    estado_ia['ultimo_teleporte'] = agora
    estado_ia['fase_tele'] = "disparando"

def node_teleporte_sinalizador(agora, estado_ia, boss_pos, alvo_pos):
    """
    Cria o 'Sinalizador de Translocação' (Círculo Azul).
    Ele viajará da posição atual até o alvo_pos.
    """
    # Nota: boss_pos deve ser passado como {'x': ..., 'y': ...}
    start_x, start_y = boss_pos['x'], boss_pos['y']
    target_x, target_y = alvo_pos
    
    dx = target_x - start_x
    dy = target_y - start_y
    dist_total = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)
    
    # Define o projétil sinalizador na memória da IA
    estado_ia['proj_tele'] = {
        'x': start_x, 'y': start_y,       # Posição atual do projétil
        'start_pos': (start_x, start_y),  # Origem
        'target_pos': (target_x, target_y), # Destino final
        'angulo': ang,
        'velocidade': 17,                 # Aumentado para maior fluidez
        'dist_total': dist_total,
        'dist_percorrida': 0,
        'cor_sinal': (0, 120, 255),       # Azul Neon
        'raio': 15 
    }
    
    estado_ia['ultimo_teleporte'] = agora
    estado_ia['fase_tele'] = "projetil_viajando"

# --- MOTOR DE DECISÃO (O GRAFO) ---

def processar_ia_umbra(agora, boss_pos, player_pos, historico_player, disparos_player, estado_ia, config_boss, memoria):
    bx, by = boss_pos['x'], boss_pos['y']
    px, py = player_pos[0], player_pos[1]
    centro_mapa = estado_ia['centro_mapa']
    
    # --- 1. HIERARQUIA DE ESTADO ATIVO ---
    if estado_ia.get('parede_ativa'):
        node_sifon(agora, estado_ia, boss_pos, centro_mapa)
        return estado_ia

    if estado_ia.get('fase_tele') != "espera":
        return estado_ia

    # --- 2. CÁLCULO DE PESOS (O PENSAMENTO) ---
    pesos = { 
        "TELEPORTE": 0.0, 
        "SIFON": 0.0,
        "ATAQUE": 1.0 
    }

    # Lógica de Teleporte: Apenas define o peso estratégico
    if agora - estado_ia.get('ultimo_teleporte', 0) >= 10000:
        pesos["TELEPORTE"] = 1.8
        if estado_ia.get('dano_recente', 0) > 400:
            pesos["TELEPORTE"] = 4.0

    # Lógica de Sifon (Gatilhos de Saúde e Dano)
    # Garante que o cooldown de 20s seja respeitado após o FIM da última ativação
    tempo_pos_sifon = agora - estado_ia.get('ultimo_sifon_fim', 0)
    if tempo_pos_sifon >= 25000 or estado_ia.get('ultimo_sifon_fim') == 0:
        vida_perc = config_boss.get('vida_atual', 1600) / config_boss.get('vida_max', 1600)
        dano_acumulado = estado_ia.get('dano_recente', 0)

        # Gatilhos de Prioridade
        if vida_perc < 0.15:
            pesos["SIFON"] = 20.0
        elif dano_acumulado >= 400:
            pesos["SIFON"] = 999.0 # Prioridade absoluta para teste e sobrevivência
        elif vida_perc < 0.50:
            pesos["SIFON"] = 1.5

    # --- 3. RESOLUÇÃO E EXECUÇÃO ---
    decisao = max(pesos, key=pesos.get)

    if decisao == "SIFON":
        # Ativação do Sifão e Reset de Telemetria de Dano
        estado_ia['parede_ativa'] = True
        estado_ia['ultimo_parede'] = agora
        estado_ia['dano_recente'] = 0 
        node_sifon(agora, estado_ia, boss_pos, centro_mapa)

    elif decisao == "TELEPORTE":
        # Execução do Teleporte apenas se vencer os outros pesos
        if estado_ia.get('dano_recente', 0) > 400:
            vec_x, vec_y = bx - px, by - py
            mag = math.hypot(vec_x, vec_y)
            alvo_x, alvo_y = (bx + (vec_x/mag)*600, by + (vec_y/mag)*600) if mag > 0 else (bx+400, by+400)
        else:
            ang_player = math.atan2(py - by, px - bx)
            ang_flanco = ang_player + random.choice([math.pi/2, -math.pi/2])
            alvo_x = px + math.cos(ang_flanco) * 450
            alvo_y = py + math.sin(ang_flanco) * 450

        alvo_x_f = max(espacamento, min(largura_mapa - 100, alvo_x))
        alvo_y_f = max(espacamento, min(altura_mapa - 150, alvo_y))
        
        if math.hypot(alvo_x_f - bx, alvo_y_f - by) > 200:
            node_teleporte_sinalizador(agora, estado_ia, boss_pos, (alvo_x_f, alvo_y_f))
    elif decisao == "ATAQUE":
        # Executa o disparo direcionado se não houver outras prioridades
        node_ataque_direcionado(agora, estado_ia, bx, by, px, py, historico_player, memoria)
    return estado_ia

def movimentacao_inteligente_umbra(agora, boss_pos, player_pos, disparos, estado_mov, dados_player, memoria):
    r"""
    Navegação de Fluxo Visionária Generativa.
    """
    # --- 1. PROTOCOLO DE ESTASE ---
    if estado_mov.get('parede_ativa'):
        estado_mov['vel_x'], estado_mov['vel_y'] = 0, 0
        return estado_mov.get('centro_mapa', (680, 384)), "SIFON_STASIS"

    bx, by = boss_pos[0], boss_pos[1]
    px, py = player_pos[0], player_pos[1]
    dist_p = math.hypot(bx - px, by - py)

    # --- 2. TOMADA DE DECISÃO GENERATIVA (ALVO) ---
    alvo = estado_mov.get('alvo_ia', (680, 384))
    dist_alvo = math.hypot(alvo[0] - bx, alvo[1] - by)

    if dist_alvo < 50 or agora - estado_mov.get('ultimo_alvo_tempo', 0) > 4000:
        vida_perc = dados_player['vida_atual'] / dados_player['vida_max']
        sob_fogo = len(disparos) > 0
        
        estado_atual = memoria.discretizar_estado(vida_perc, dist_p, sob_fogo)
        estrategias = ["FUGIR", "INTERCEPTAR", "ORBITAR", "CERCAR"]
        decisao = memoria.decidir(estado_atual, estrategias)
        
        if decisao == "FUGIR":
            cantos = [(150, 150), (1150, 150), (150, 620), (1150, 620)]
            alvo_x, alvo_y = max(cantos, key=lambda c: math.hypot(c[0] - px, c[1] - py))
        elif decisao == "INTERCEPTAR":
            alvo_x = px + (px - bx) * 0.3
            alvo_y = py + (py - by) * 0.3
        elif decisao == "ORBITAR":
            ang = math.atan2(by - py, bx - px) + 0.7
            alvo_x, alvo_y = px + math.cos(ang) * 450, py + math.sin(ang) * 450
        else: # CERCAR
            ang = math.atan2(by - py, bx - px)
            alvo_x, alvo_y = px + math.cos(ang) * 300, py + math.sin(ang) * 300

        estado_mov['alvo_ia'] = (max(100, min(1260, alvo_x)), max(100, min(660, alvo_y)))
        estado_mov['ultimo_alvo_tempo'] = agora

    # --- 3. CONFIGURAÇÃO DE FÍSICA E STEERING (ORIGINAL) ---
    VEL_MAX, AGILIDADE, RAIO_SEGURANCA = 1, 0.2, 340
    vx, vy = estado_mov.get('vel_x', 0), estado_mov.get('vel_y', 0)
    hitbox_centro = (bx, by)

    # --- 4. PROTOCOLO DE ESQUIVA MATEMÁTICA ---
    f_esquiva_y = 0
    tiro_ameaca = None
    for d in disparos:
        dx_tiro = hitbox_centro[0] - d["rect"].centerx
        vx_tiro = math.cos(d["angulo"])
        if (dx_tiro > 0 and vx_tiro > 0) or (dx_tiro < 0 and vx_tiro < 0):
            dist_h = math.hypot(d["rect"].centerx - hitbox_centro[0], d["rect"].centery - hitbox_centro[1])
            if dist_h < 450: 
                tiro_ameaca = d
                break
    if tiro_ameaca:
        tx, ty = tiro_ameaca["rect"].centerx, tiro_ameaca["rect"].centery
        ang = tiro_ameaca["angulo"]
        dist_x = hitbox_centro[0] - tx
        try:
            y_proj = ty + (dist_x * math.tan(ang))
            if abs(y_proj - hitbox_centro[1]) < 60:
                f_esquiva_y = 2.0 if y_proj < hitbox_centro[1] else -2.0
                estado_mov['ultimo_desvio'] = agora
        except ZeroDivisionError:
            f_esquiva_y = random.choice([-2, 2])

    # --- 5. CÁLCULO DE VETORES ---
    dx_a, dy_a = estado_mov['alvo_ia'][0] - bx, estado_mov['alvo_ia'][1] - by
    mag_a = math.hypot(dx_a, dy_a)
    vec_alvo_x = (dx_a / mag_a) if mag_a > 0 else 0
    vec_alvo_y = (dy_a / mag_a) if mag_a > 0 else 0

    rx, ry = bx - px, by - py
    dist_r = math.hypot(rx, ry)
    f_rep_x = f_rep_y = 0
    if dist_r < RAIO_SEGURANCA:
        f_rep_x, f_rep_y = (rx/dist_r) * 1.5, (ry/dist_r) * 1.5

    v_desejada_x = (vec_alvo_x + f_rep_x) * VEL_MAX
    v_desejada_y = (vec_alvo_y + f_rep_y + f_esquiva_y) * VEL_MAX
    vx += (v_desejada_x - vx) * AGILIDADE
    vy += (v_desejada_y - vy) * AGILIDADE
    estado_mov['vel_x'], estado_mov['vel_y'] = vx, vy

    nx = max(espacamento, min(largura_mapa - 100, bx + vx)) 
    ny = max(espacamento, min(altura_mapa - 150, by + vy))

    return (nx, ny), "GENERATIVE_MOVE"