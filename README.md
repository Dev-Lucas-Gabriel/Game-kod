🕹️ Pixel Runner 
Bem-vindo ao Pixel Runner, um jogo simples em Python usando Pygame / Pygame Zero, onde você controla um personagem e precisa desviar ou enfrentar inimigos espalhados pelo cenário.
Este projeto é ideal para quem gosta de jogos retrô, programação ou quer estudar lógica de games em Python.

---

🎮 Gameplay

- O mapa é uma grade (grid) de paredes `#` e chão `.`
- O herói se move suavemente de célula em célula, com animação de sprite para `idle` e `walk`
- Existem múltiplos inimigos (slimes) com animação, que se movem aleatoriamente **apenas dentro de seus territórios**
- Se o herói colidir com um inimigo:
  - Toca som de dano
  - O herói muda para estado hurt por um instante
  - Em seguida ele é resetado para o ponto inicial
- Ao chegar na porta (tile verde com maçaneta), você vence e aparece a tela de vitória

---

🎮 Como Jogar
Você controla o personagem na tela.
Controles Tecla	Ação:
⬅️ Seta Esquerda	Mover para a esquerda
➡️ Seta Direita	Mover para a direita
⬆️ Seta Cima	Mover para cima
⬇️ Seta Baixo	Mover para baixo
O jogo possui vários inimigos (verdes) que se movimentam automaticamente.
Seu objetivo é sobreviver, explorar a fase e desviar dos inimigos.
- M: alterna música (Musica ON/OFF)  
- N: alterna efeitos sonoros (Sons ON/OFF)  
- ESC: volta ao menu principal  

Tela de vitória (STATE_WIN):
- **ENTER** ou **ESPAÇO**: volta ao **menu**

Menu principal:
- Botões clicáveis: Iniciar, Audio ON/OFF (liga/desliga música e efeitos juntos), **Sair do jogo**  
- Dentro do jogo há botões pequenos (HUD) para **Musica ON/OFF**, **Sons ON/OFF** e **Voltar ao início**.

---

👾 O que o jogo tem
✔️ Sistema de Player com movimento livre
✔️ Inimigos com vida, velocidade e área (Rect)
✔️ Movimentação automática dos inimigos
✔️ Loop de jogo estável
✔️ Código simples e fácil de modificar
✔️ Feito especialmente para rodar em Pygame Zero
✔️ Fase 1 com vários inimigos pré-definidos

---

📦 Requisitos
Você precisa ter instalado:
Python 3
Pygame
Pygame Zero (pgzero)
Instalação (caso precise):
pip install pygame pgzero

--- 

▶️ Como rodar o jogo
Dentro do diretório do projeto, execute:
**python3 -m pgzero game.py**
Se estiver no Windows:
**py -m pgzero game.py**
Isso abre a janela do jogo imediatamente.
🛠️ Como clonar o jogo pelo GitHub
1. Abra o terminal (cmd, PowerShell, bash, etc.)
2. Vá até a pasta onde quer salvar
Exemplo:
**cd Documentos**
3. Clone o repositório:
**git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git**
Troque SEU_USUARIO e SEU_REPOSITORIO pelo nome correto do seu GitHub.
4. Entre na pasta do projeto:
cd SEU_REPOSITORIO
5. Rode o jogo:
**python3 -m pgzero game.py**
Pronto! O jogo funciona igual em qualquer computador.
🧩 Estrutura do Projeto
/game.py        → arquivo principal do jogo
README.md       → este arquivo
/assets/        → imagens, sons (se houver)


