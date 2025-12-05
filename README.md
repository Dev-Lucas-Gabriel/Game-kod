🎮 PixelRunner 
Bem-vindo ao PixelRunner, um jogo estilo mini-roguelike, simples, leve e rápido, criado usando PgZero.
O objetivo é avançar pelas 5 fases, evitando inimigos e chegando até a porta de saída.
Um jogo perfeito para aprender lógica de programação, mapas baseados em grid e movimentação suave por interpolação.

📌 📜 História
Você é um pequeno aventureiro preso em uma série de salas misteriosas.
Cada sala possui inimigos patrulhando áreas aleatórias.
Seu objetivo é chegar até a porta verde em cada fase para fugir e avançar para a próxima.
Na quinta fase, ao escapar… você vence o jogo! 🎉

🎮 Como Jogar
🕹 Movimentação
Use qualquer um:
Tecla	Função
W / ↑	Mover para cima
S / ↓	Mover para baixo
A / ←	Mover para esquerda
D / →	Mover para direita
A movimentação acontece em grid, com animação suave.
🔊 Áudio
No jogo, você pode ligar ou desligar:
Tecla	Função
M	Liga/desliga música
N	Liga/desliga efeitos sonoros (SFX)
Também existem botões na interface para isso.
⏪ Voltar ao menu
Tecla	Função
ESC	Volta imediatamente ao menu
📋 Estrutura do Jogo
✔ 5 Fases jogáveis
Cada fase possui:
um mapa próprio
cores próprias
número crescente de inimigos
velocidade maior dos inimigos
✔ Menu inicial
Com os botões:
Iniciar
Áudio ON/OFF
Sair do jogo
✔ Tela de vitória
Após terminar a fase 5, aparece uma tela especial, e você pode retornar ao menu com:
ENTER
SPACE
clique do mouse
✔ Inimigos
Movem-se aleatoriamente dentro de um território específico.
Velocidade aumenta em cada fase.
Se encostarem no herói, ele sofre dano (animação “hurt”) e volta ao início da fase.
✔ Herói
Animações: idle, walk, hurt
Sistema de interpolação para movimento suave
Reinicia automaticamente ao tomar dano
🛠 Como Instalar e Rodar
1️⃣ Instale o Python 3 (caso não tenha)
Baixe em:
https://www.python.org/downloads/
2️⃣ Instale o PgZero
Abra o terminal e execute:
python3 -m pip install pgzero
3️⃣ Coloque o arquivo roguelike.py e as pastas images/ e sounds/ no mesmo diretório
Seu projeto deve ficar assim:
/PixelRunner
 ├─ game.py
 ├─ images/
 ├─ music/
 ├─ sounds/
 └─ README.md
4️⃣ Rode o jogo
No terminal, dentro da pasta do projeto:
pgzrun roguelike.py
💻 Como Clonar este Jogo pelo GitHub
Se o projeto estiver no GitHub, qualquer usuário pode clonar assim:
git clone https://github.com/Dev-Lucas-Gabriel/Game-kod.git
Entre na pasta:
cd PixelRunner
Rode o jogo:
pgzrun game.py

