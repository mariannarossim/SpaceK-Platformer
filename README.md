# SpaceK-Platformer
2D space platformer developed in Python using Pygame Zero.


🚀 SpaceK

Um jogo de plataforma espacial, inspirado em Mario, desenvolvido em Python com Pygame Zero.
O jogador controla um astronauta que precisa atravessar plataformas e evitar inimigos alienígenas para chegar ao final das fases.

📌 Requisitos Atendidos
📚 Bibliotecas utilizadas

pgzero

pygame.Rect

random

🎮 Gênero

Platformer

⚙️ Funcionalidades implementadas

Menu principal com botões clicáveis:

Iniciar Jogo

Sair

Duas fases jogáveis

Jogador com movimento, pulo e gravidade

Inimigos que patrulham seus territórios

Colisão entre jogador, plataformas e inimigos
🎮 Como Jogar

Mover:

Tecla A ou Seta Esquerda → Esquerda

Tecla D ou Seta Direita → Direita

Pular:

Barra de Espaço

Objetivo:

Alcance o lado direito da tela para passar de fase

Evite inimigos e não caia no vazio

💻 Como Executar
Pré-requisitos

Python 3.10 ou superior

Instalar dependências:
python -m pip install --upgrade pip
pip install pygame pgzero

Rodar o jogo

No terminal (CMD ou PowerShell), vá até a pasta onde está o código e execute:
python -m pgzero spaceK.py

📂 Estrutura do Projeto
SpaceK/
│── spaceK.py       # Código principal do jogo
│── README.md       # Documentação do projeto
│── sounds/         # Pasta reservada para efeitos sonoros e músicas

# 🚀 Plano de Aula – SpaceK

📝 **Tema:** Desenvolvimento de um jogo de plataforma 2D em Python com Pygame Zero  

⏱ **Duração sugerida:** 4 a 6 módulos   
🛠 **Ferramentas:** Python 3, Pygame Zero, VS Code / Thonny  
📌 **Pré-requisitos:** Noções básicas de Python (variáveis, loops, condicionais, funções)  

---

## 🎯 Objetivos de Aprendizagem
- Entender a estrutura de um jogo (`update()`, `draw()`, estados de jogo).  
- Implementar física simples: gravidade, pulo e colisão.  
- Criar interatividade com teclado.  
- Trabalhar com múltiplos objetos (inimigos, plataformas, power-ups).  
- Adicionar efeitos visuais e sonoros.  
- Organizar o código em funções e classes.  
- Realizar testes e depuração.  

---

## 📚 Estrutura de Módulos

### 📘 Módulo 1 – Primeiros Passos com Pygame Zero
- **Conceitos:** `update()`, `draw()`, variáveis globais.  
- **Atividades:**  
  - Instalar dependências  
  - Rodar `spaceK.py`  
  - Alterar `WIDTH` e `HEIGHT`  
  - Criar sprite simples em movimento  

---

### 🚀 Módulo 2 – O Astronauta em Ação
- **Conceitos:** posição, velocidade, gravidade, colisão.  
- **Atividades:**  
  - Implementar pulo  
  - Limitar velocidade de queda  
  - Ajustar a câmera do jogo  

---

### 👾 Módulo 3 – Inimigos e Power-ups
- **Conceitos:** uso de classes, métodos (`__init__`, `update`, `draw`).  
- **Atividades:**  
  - Alterar atributos de inimigos  
  - Criar power-up personalizado  

---

### 💥 Módulo 4 – Lasers, Partículas e Sons
- **Conceitos:** projéteis, partículas, integração de áudio.  
- **Atividades:**  
  - Modificar velocidade/cor de lasers  
  - Adicionar partículas  
  - Testar sons do jogo  

---

### 🖥️ Módulo 5 – Interface e Estados do Jogo
- **Conceitos:** menus, HUD, pontuação, transições.  
- **Atividades:**  
  - Alterar cores/textos de botões  
  - Adicionar botão ao menu  
  - Personalizar HUD  

---

### 🎮 Módulo 6 – Refinamento e Desafios Finais
- **Conceitos:** níveis, balanceamento, otimização.  
- **Atividades:**  
  - Editar fases  
  - Criar inimigo novo  
  - Implementar sistema de vidas extras  
  - Criar boss simples  

---

## 📂 Recursos Disponíveis
- **Código-fonte:** `spaceK.py`  
- **Documentação:** [Pygame Zero Docs](https://pygame-zero.readthedocs.io/)  
- **Sprites e sons:** disponíveis na pasta `sounds/`  
- **Guia prático:** este README serve como trilha de aprendizado  




Estrutura em classes para jogador e inimigos

Código organizado e independente
