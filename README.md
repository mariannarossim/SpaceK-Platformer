# SpaceK-Platformer

![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-green)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pygame Zero](https://img.shields.io/badge/Pygame%20Zero-1.2+-006400)

Jogo de plataforma 2D com temática espacial, inspirado em Mario, desenvolvido em **Python** com a biblioteca **Pygame Zero**. O jogador controla um astronauta que precisa atravessar plataformas e desviar de inimigos alienígenas para concluir as fases.

O repositório contém o jogo principal e uma versão reduzida (mini-jogo), além de um plano de aula completo que utiliza o projeto como base para o ensino de desenvolvimento de jogos em Python.

---

## Sobre o projeto

O SpaceK foi concebido para unir um produto final jogável a um material didático completo. A escolha do **Pygame Zero** se justifica por oferecer uma API simplificada sobre o Pygame, reduzindo a verbosidade do código de inicialização e permitindo que o foco recaia sobre os conceitos centrais do desenvolvimento de jogos: o ciclo de atualização, a renderização, a física básica e a detecção de colisões.

---

## Versões do jogo

O repositório disponibiliza duas versões:

| Versão | Descrição |
|--------|-----------|
| **SpaceK (completo)** | Jogo principal, com menu, múltiplas fases, inimigos, sistema de pontuação e progressão. |
| **SpaceK Mini** | Versão simplificada, ideal para introdução aos conceitos básicos do Pygame Zero e como ponto de partida para iniciantes. |

---

## Bibliotecas utilizadas

| Biblioteca | Descrição |
|------------|-----------|
| [Pygame Zero](https://pygame-zero.readthedocs.io/) | Framework simplificado para desenvolvimento de jogos 2D em Python |
| [Pygame](https://www.pygame.org/) | Biblioteca base utilizada internamente pelo Pygame Zero, usada para `pygame.Rect` |
| `random` | Módulo padrão do Python para geração de valores aleatórios |

---

## Funcionalidades implementadas

- Menu principal com botões clicáveis (Iniciar Jogo, Sair)
- Duas fases jogáveis com complexidade progressiva
- Personagem com movimentação, pulo e gravidade
- Inimigos com comportamento de patrulha em territórios definidos
- Sistema de colisão entre jogador, plataformas e inimigos
- Estrutura orientada a objetos para jogador e inimigos
- Código modularizado e organizado por responsabilidades

---

## Controles e jogabilidade

**Movimentação**

- `A` ou `Seta Esquerda` — mover para a esquerda
- `D` ou `Seta Direita` — mover para a direita
- `Barra de Espaço` — pular

**Objetivo**

- Alcançar o lado direito da tela para concluir a fase
- Desviar dos inimigos e evitar quedas no vazio

---

## Requisitos

- **Python 3.10 ou superior**
- Bibliotecas: `pygame` e `pgzero`

### Instalação das dependências

```bash
python -m pip install --upgrade pip
pip install pygame pgzero
```

Recomenda-se o uso de um ambiente virtual (`venv`) para isolar as dependências:

```bash
python -m venv venv
# Ativação no Windows
venv\Scripts\activate
# Ativação no Linux/macOS
source venv/bin/activate
```

---

## Como executar

No terminal, acesse o diretório do projeto e execute:

```bash
# Jogo principal
pgzrun spaceK.py

# Versão mini
pgzrun spaceK_mini.py
```

---

## Estrutura do repositório

```
SpaceK-Platformer/
├── README.md
├── spaceK.py              # Jogo principal
├── spaceK_mini.py         # Versão simplificada
├── images/                # Sprites e elementos visuais
└── sounds/                # Efeitos sonoros e trilhas
```

---

## Plano de aula

O projeto SpaceK foi estruturado também como **material didático** para o desenvolvimento de jogos 2D em Python com Pygame Zero. O plano abaixo organiza o conteúdo em módulos progressivos.

**Duração sugerida:** 4 a 6 módulos
**Ferramentas:** Python 3, Pygame Zero, VS Code ou Thonny
**Pré-requisitos:** noções básicas de Python (variáveis, laços, condicionais, funções)

### Objetivos de aprendizagem

- Compreender a estrutura de um jogo (`update()`, `draw()`, estados de jogo)
- Implementar física simples: gravidade, pulo e detecção de colisão
- Construir interatividade por meio do teclado
- Trabalhar com múltiplos objetos (inimigos, plataformas, power-ups)
- Integrar efeitos visuais e sonoros
- Organizar o código em funções e classes
- Realizar testes, depuração e refinamento

---

### Módulo 1 — Primeiros passos com Pygame Zero

**Conceitos:** funções `update()` e `draw()`, variáveis globais, ciclo do jogo

**Atividades:**

- Instalação das dependências
- Execução do arquivo `spaceK.py`
- Alteração das constantes `WIDTH` e `HEIGHT`
- Criação de um sprite simples em movimento

---

### Módulo 2 — O astronauta em ação

**Conceitos:** posição, velocidade, gravidade, detecção de colisão

**Atividades:**

- Implementação do mecanismo de pulo
- Limitação da velocidade de queda
- Ajuste da câmera do jogo

---

### Módulo 3 — Inimigos e power-ups

**Conceitos:** programação orientada a objetos, métodos `__init__`, `update` e `draw`

**Atividades:**

- Modificação dos atributos dos inimigos
- Criação de um power-up personalizado

---

### Módulo 4 — Lasers, partículas e sons

**Conceitos:** projéteis, sistemas de partículas, integração de áudio

**Atividades:**

- Alteração de velocidade e cor dos lasers
- Adição de efeitos de partículas
- Integração de sons ao jogo

---

### Módulo 5 — Interface e estados do jogo

**Conceitos:** menus, HUD, pontuação, transições entre telas

**Atividades:**

- Personalização de cores e textos dos botões
- Adição de novos itens ao menu
- Customização da HUD (interface durante o jogo)

---

### Módulo 6 — Refinamento e desafios finais

**Conceitos:** desenho de níveis, balanceamento, otimização

**Atividades:**

- Edição e criação de novas fases
- Implementação de um novo tipo de inimigo
- Criação de um sistema de vidas extras
- Implementação de um chefe (boss) simples

---

## Conceitos aplicados

| Área | O que o projeto demonstra |
|------|---------------------------|
| **Python** | Programação orientada a objetos, modularização, escopo de variáveis |
| **Pygame Zero** | Ciclo de atualização e renderização, manipulação de sprites, captura de eventos |
| **Física de jogos** | Gravidade, velocidade, detecção de colisão por retângulos |
| **Arquitetura de jogos** | Estados de jogo, separação entre lógica e renderização |
| **Design de níveis** | Posicionamento de plataformas, inimigos e elementos interativos |

---

## Recursos complementares

- [Documentação oficial do Pygame Zero](https://pygame-zero.readthedocs.io/)
- [Documentação do Pygame](https://www.pygame.org/docs/)
- Repositório original: [SpaceK-Platformer](https://github.com/mariannarossim/SpaceK-Platformer)

---

## Sobre o material

Todo o conteúdo deste repositório é de autoria própria, podendo ser utilizado tanto como referência para projetos de jogos quanto como base para o ensino de desenvolvimento de jogos em Python. O material pode ser utilizado, adaptado e compartilhado, desde que mantidos os devidos créditos.

---

## Autora

**Marianna Rossi**

[GitHub](https://github.com/mariannarossim)

---

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
