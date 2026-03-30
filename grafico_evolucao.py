import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

arquivo_historico = "historico_batalhas.json"

fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.manager.set_window_title('Evolução Neural: Umbra vs Apolo')

def atualizar_grafico(frame):
    if os.path.exists(arquivo_historico):
        try:
            with open(arquivo_historico, "r") as f:
                dados = json.load(f)
        except:
            return
            
        geracoes = [d["geracao"] for d in dados]
        duracoes = [d["duracao"] for d in dados]
        vencedores = [d["vencedor"] for d in dados]

        ax.clear()
        
        cores = ['blue' if v == 'Apolo' else 'purple' for v in vencedores]
        
        ax.scatter(geracoes, duracoes, c=cores, s=50, alpha=0.7)
        ax.plot(geracoes, duracoes, color='gray', linestyle='--', alpha=0.5)

        if len(duracoes) >= 5:
            medias_moveis = [sum(duracoes[i-5:i])/5 for i in range(5, len(duracoes)+1)]
            ax.plot(geracoes[4:], medias_moveis, color='red', linewidth=2, label='Média Móvel (5 ger)')

        ax.set_title("Tempo de Sobrevivência por Geração", fontsize=14, fontweight='bold')
        ax.set_xlabel("Gerações", fontsize=12)
        ax.set_ylabel("Duração do Combate (Segundos)", fontsize=12)
        ax.grid(True, linestyle=':', alpha=0.6)
        
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Apolo Venceu'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10, label='Umbra Venceu')
        ]
        if len(duracoes) >= 5:
            legend_elements.append(Line2D([0], [0], color='red', lw=2, label='Tendência (Média)'))
        ax.legend(handles=legend_elements, loc='upper left')

ani = FuncAnimation(fig, atualizar_grafico, interval=2000)
plt.tight_layout()
plt.show()