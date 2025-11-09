🧩 Ruptura Temporal – Versão R.E. (Redes e Comunicação)

Versão experimental do Ruptura Temporal, desenvolvida como projeto prático da disciplina de Redes de Computadores.
Esta edição demonstra comunicação em tempo real entre jogadores via sockets TCP, com sincronização de estado, controle de latência e lógica multiplayer integrados ao núcleo do jogo.

⚠️ Nota: Esta é uma versão protótipo, contendo apenas a primeira fase do Ruptura Temporal original.
A adaptação completa exigiria mais tempo de desenvolvimento e ajustes de balanceamento.

🚀 Objetivo

Implementar uma arquitetura cliente-servidor funcional dentro de um ambiente de jogo, aplicando conceitos como:

Conexão e troca de dados via sockets TCP;

Sincronização em tempo real entre instâncias do jogo;

Controle de latência, integridade e ordem das mensagens;

Integração da lógica de rede ao sistema base de jogabilidade.

⚙️ Estrutura do Projeto
Ruptura_Temporal-RE/
│
├── Ruptura_Temporal.py   # Menu inicial e seleção de modo (Host, Join, Offline)

├── GAMERE.py             # Lógica principal da partida e sincronização de rede

├── rede.py               # Camada de comunicação (cliente e servidor TCP)

├── Variaveis.py          # Configurações globais

├── utils.py              # Funções auxiliares

├── Sprites/              # Recursos visuais

├── Sounds/               # Efeitos sonoros

└── Texto/                # Fontes e textos da interface

🕹️ Como Executar
🖥️ Host (Servidor)

No computador que hospedará a partida:

python Ruptura_Temporal.py


Selecione “Host Game”. O servidor aguardará conexão na porta 5050.

💻 Cliente (Jogador Convidado)

Em outro computador:

python Ruptura_Temporal.py


Escolha “Join Game” e insira o IP do host.

🎮 Modo Offline

Permite jogar individualmente sem necessidade de rede.

💡 Principais Funcionalidades

Comunicação cliente-servidor via TCP;

Sincronização em tempo real das posições e ações dos jogadores;

Transmissão de dados sobre inimigos, tiros e eventos;

Modo tutorial e fase inicial jogável;

Modularização entre lógica de jogo, interface e rede.

🔬 Destaques Técnicos

Implementação manual de sockets TCP em Python;

Uso de threads para conexões simultâneas;

Serialização JSON para troca de pacotes;

Estrutura escalável, pronta para futuras fases e otimizações.

👨‍💻 Autor

Luis Henrique Bessa de Melo
Universidade de Brasília – Ciência da Computação
Projeto prático da disciplina Redes de Computadores e Comunicação de Dados

Licença: Creative Commons BY-NC-SA 4.0
Uso comercial proibido. Modificações e redistribuições permitidas sob os mesmos termos.
