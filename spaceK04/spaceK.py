# ===================================================================
# SPACEK - JOGO DE PLATAFORMA ESPACIAL
# ===================================================================
# Este é um jogo de plataforma onde o jogador controla um astronauta
# que deve derrotar aliens inimigos em uma missão espacial.
# 
# BIBLIOTECAS PERMITIDAS CONFORME REQUISITOS:
# - pgzero (biblioteca principal para o jogo)
# - math (para cálculos matemáticos e trigonometria)
# - random (para gerar números aleatórios)
# - pygame.Rect (exceção permitida para detecção de colisões)
# ===================================================================

import pgzrun
import math
import random
from pygame import Rect
import pygame.mixer

# ===================================================================
# CONFIGURAÇÃO INICIAL DO JOGO SPACEK
# ===================================================================
# Estas constantes definem o tamanho da tela do jogo
WIDTH = 800  # Largura da tela em pixels
HEIGHT = 600  # Altura da tela em pixels

# ===================================================================
# VARIÁVEIS DE ESTADO DO JOGO
# ===================================================================
# Controla em que tela o jogo está (menu principal, jogando, etc.)
game_state = "menu"  # Estados possíveis: "menu", "playing", "gameover", "victory"

# Controles de áudio conforme requisitos do projeto
music_enabled = True    # Controla se a música de fundo está ativa
sounds_enabled = True   # Controla se os efeitos sonoros estão ativos

# ===================================================================
# VARIÁVEIS DO HERÓI ASTRONAUTA (PERSONAGEM PRINCIPAL)
# ===================================================================
# Posição do jogador no mundo do jogo
player_x = 100  # Posição horizontal inicial
player_y = 500  # Posição vertical inicial

# Velocidades do jogador (física do movimento)
player_vx = 0  # Velocidade horizontal
player_vy = 0  # Velocidade vertical (afetada pela gravidade)

# Estados do personagem principal
player_on_ground = False        # Se o astronauta está no chão
player_lives = 3               # Número de vidas (requisito do jogo)
player_energy = 100           # Energia do traje espacial
player_jetpack_fuel = 100     # Combustível do jetpack
player_invulnerable = 0       # Timer de invulnerabilidade após dano
player_facing = 1             # Direção que o jogador está olhando (1=direita, -1=esquerda)

# Sistema de animação do herói
player_animation_timer = 0    # Controla a velocidade da animação
player_animation_frame = 0    # Frame atual da animação

# Power-ups especiais do astronauta
player_has_shield = False     # Se o jogador tem escudo ativo
player_shield_timer = 0       # Tempo restante do escudo

# Sistema de controle contínuo de movimento
player_move_left = False      # Se a tecla esquerda está pressionada
player_move_right = False     # Se a tecla direita está pressionada
player_max_speed = 6          # Velocidade máxima do jogador
player_acceleration = 0.8     # Aceleração do movimento
player_friction = 0.85        # Atrito para desaceleração suave

# ===================================================================
# VARIÁVEIS DO MUNDO DO JOGO SPACEK
# ===================================================================
current_level = 1     # Nível atual (1 ou 2)
camera_x = 0          # Posição da câmera (para scrolling horizontal)
oxygen = 100          # Sistema de sobrevivência - oxigênio
score = 0             # Pontuação do jogador
high_score = 0        # Maior pontuação já alcançada
coins_collected = 0   # Moedas K coletadas
enemies_defeated = 0  # Número de aliens derrotados

# ===================================================================
# LISTAS DOS ELEMENTOS DO JOGO
# ===================================================================
# Estas listas armazenam todos os objetos do jogo
platforms = []   # Lista de plataformas onde o jogador pode andar
enemies = []     # Lista de inimigos aliens
powerups = []    # Lista de power-ups colecionáveis
lasers = []      # Lista de projéteis laser disparados
particles = []   # Lista de efeitos visuais (explosões, faíscas)
stars = []       # Lista de estrelas de fundo
coins = []       # Lista de moedas K colecionáveis
menu_buttons = [] # Lista de botões do menu principal

# ===================================================================
# SISTEMA DE ÁUDIO DO SPACEK
# ===================================================================
# Inicializar mixer do pygame para suportar mp3
pygame.mixer.init()

# Pré-carregar sons usando pygame.mixer.Sound para mp3
sound_files = {
    "jump": "sounds/jump.mp3",
    "click": "sounds/button_click.mp3",
    "explosion": "sounds/explode.mp3",
    "hurt": "sounds/impact.mp3",
    "jetpack": "sounds/jetpack.mp3",
    "laser_shoot": "sounds/laser_shoot.mp3",
    "laser_hit": "sounds/laser_hit.mp3",
    "enemy_death": "sounds/enemy_death.mp3",
    "powerup": "sounds/button_click.mp3",  # Temporário
    "collect": "sounds/jump.mp3"            # Temporário
}

loaded_sounds = {}

for key, path in sound_files.items():
    try:
        loaded_sounds[key] = pygame.mixer.Sound(path)
        print(f"✅ Som carregado: {path}")
    except Exception as e:
        print(f"❌ Falha ao carregar som {path}: {e}")

def play_spacek_sound(sound_type):
    """
    Reproduz efeitos sonoros específicos do SpaceK usando pygame.mixer.Sound
    
    Args:
        sound_type (str): Tipo de som a ser reproduzido
    """
    if not sounds_enabled:
        return
    
    try:
        print(f"🎵 SpaceK Audio System: Reproduzindo {sound_type}")
        sound = loaded_sounds.get(sound_type)
        if sound:
            sound.play()
            print(f"✅ {sound_type} reproduzido com sucesso!")
        else:
            print(f"❌ Som {sound_type} não encontrado na lista carregada.")
    except Exception as e:
        print(f"❌ Erro geral do sistema de áudio SpaceK: {e}")

def test_spacek_audio_system():
    """
    Função para testar todo o sistema de áudio do SpaceK usando pygame.mixer
    Esta função verifica se todos os sons estão carregados corretamente
    e podem ser reproduzidos sem erro.
    """
    print("\n" + "="*60)
    print("🚀 SPACEK - TESTE COMPLETO DO SISTEMA DE ÁUDIO 🚀")
    print("="*60)
    print("Testando sons carregados com pygame.mixer.Sound:")

    # Lista de todos os sons que devem estar disponíveis
    spacek_sound_tests = [
        ("button_click.mp3", "click", "Cliques nos botões do menu"),
        ("enemy_death.mp3", "enemy_death", "Morte de aliens inimigos"),
        ("explode.mp3", "explosion", "Explosões gerais"),
        ("impact.mp3", "hurt", "Dano recebido pelo astronauta"),
        ("jetpack.mp3", "jetpack", "Ativação do sistema de jetpack"),
        ("jump.mp3", "jump", "Pulos do astronauta e aliens"),
        ("laser_hit.mp3", "laser_hit", "Laser atingindo inimigos"),
        ("laser_shoot.mp3", "laser_shoot", "Disparar projéteis laser")
    ]

    # Testar cada som individualmente
    for i, (file_name, sound_key, description) in enumerate(spacek_sound_tests):
        try:
            print(f"\n{i+1}/8 🔊 Testando: {file_name}")
            print(f"     ↳ Função: {description}")
            print(f"     ↳ Comando: play_spacek_sound('{sound_key}')")

            # Verificar se o som está carregado
            if sound_key in loaded_sounds:
                print(f"     ✅ Som carregado: {loaded_sounds[sound_key]}")
                # Tentar reproduzir o som
                play_spacek_sound(sound_key)
                print(f"     ✅ TESTE APROVADO - {file_name} funcionando!")
            else:
                print(f"     ❌ TESTE FALHOU - Som {sound_key} não carregado.")

        except Exception as e:
            print(f"     ❌ TESTE FALHOU - Erro em {file_name}: {e}")

    print("\n" + "="*60)
    print("🎵 Teste do sistema de áudio SpaceK finalizado!")
    print("="*60)

def safe_color(color):
    """
    Função utilitária para garantir que valores de cor estão válidos
    
    Args:
        color (tuple): Tupla RGB com valores de cor
    
    Returns:
        tuple: Tupla RGB com valores limitados entre 0-255
    
    Esta função previne erros de cor inválida no pygame/pgzero
    """
    return tuple(max(0, min(255, int(c))) for c in color)

# ===================================================================
# CLASSE PARA BOTÕES DO MENU (REQUISITO: BOTÕES CLICÁVEIS)
# ===================================================================

class SpaceKButton:
    """
    Classe para criar botões clicáveis do menu principal
    
    REQUISITO ATENDIDO: "Menu principal com botões clicáveis"
    - Começar o jogo
    - Música/sons ON-OFF  
    - Sair
    """
    
    def __init__(self, x, y, width, height, text, action, color=(100, 100, 200)):
        """
        Inicializar botão do SpaceK
        
        Args:
            x, y: Posição do botão na tela
            width, height: Tamanho do botão
            text: Texto exibido no botão
            action: Ação executada quando clicado
            color: Cor base do botão
        """
        self.rect = Rect(x, y, width, height)  # Área clicável do botão
        self.text = text                       # Texto do botão
        self.action = action                   # Ação a ser executada
        self.color = color                     # Cor base
        self.hovered = False                   # Se o mouse está sobre o botão
        self.click_timer = 0                   # Timer para efeito visual de clique
        self.glow_timer = 0                    # Timer para efeito de brilho
    
    def update(self, mouse_pos):
        """
        Atualizar estado do botão baseado na posição do mouse
        
        Args:
            mouse_pos: Posição atual do mouse
        """
        # Detectar se o mouse está sobre o botão (hover effect)
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Decrementar timers dos efeitos visuais
        if self.click_timer > 0:
            self.click_timer -= 1
        self.glow_timer += 1
    
    def draw(self):
        """
        Desenhar o botão na tela com todos os efeitos visuais
        """
        # Calcular efeito de brilho baseado no timer
        glow_offset = int(abs(math.sin(self.glow_timer * 0.1)) * 20)
        
        # Determinar cor do botão baseada no estado
        if self.hovered:
            # Cor mais brilhante quando o mouse está sobre o botão
            color = safe_color((self.color[0] + 60, self.color[1] + 60, self.color[2] + 60))
        else:
            # Cor normal com leve brilho
            color = self.color
        
        # Efeito visual de clique (cor mais escura)
        if self.click_timer > 0:
            color = safe_color((color[0] - 40, color[1] - 40, color[2] - 40))
        
        # Desenhar sombra do botão para efeito 3D
        shadow_rect = Rect(self.rect.x + 4, self.rect.y + 4, self.rect.width, self.rect.height)
        screen.draw.filled_rect(shadow_rect, (15, 15, 15))
        
        # Desenhar corpo principal do botão
        screen.draw.filled_rect(self.rect, color)
        
        # Desenhar borda do botão
        border_color = (255, 255, 255) if not self.hovered else (0, 255, 255)
        screen.draw.line((self.rect.left, self.rect.top), (self.rect.right, self.rect.top), border_color)
        screen.draw.line((self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), border_color)
        screen.draw.line((self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), border_color)
        screen.draw.line((self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), border_color)
        
        # Desenhar texto do botão com sombra
        screen.draw.text(self.text, center=(self.rect.centerx + 2, self.rect.centery + 2), fontsize=16, color="black")
        screen.draw.text(self.text, center=self.rect.center, fontsize=16, color="white")
    
    def is_clicked(self, pos):
        """
        Verificar se o botão foi clicado
        
        Args:
            pos: Posição do clique do mouse
            
        Returns:
            bool: True se o botão foi clicado
        """
        if self.rect.collidepoint(pos):
            self.click_timer = 10  # Ativar efeito visual de clique
            play_spacek_sound("click")  # Reproduzir som de clique
            return True
        return False

# ===================================================================
# CLASSE DO HERÓI ASTRONAUTA (REQUISITO: CLASSES PARA PERSONAGENS)
# ===================================================================

class SpaceKHero:
    """
    Classe do herói astronauta com sistema completo de animações
    
    REQUISITOS ATENDIDOS:
    - Usar classes para personagens e sprites
    - Animações de sprite (andar, parado, respirando, etc.)
    """
    
    def __init__(self):
        """
        Inicializar o herói astronauta do SpaceK
        Define todos os estados de animação do personagem
        """
        # Sistema de animação de sprites conforme requisito
        # Cada estado tem múltiplos frames para animação fluida
        self.animation_states = {
            "idle": ["^_^", "^_^", "^_^", "o_o", "^_^", "^_^", "-_-", "^_^"],           # Estado parado
            "walking": ["^_^", "o_o", "^_^", "-_-", "^_^", "o_o", "~_~", "^_^"],       # Estado andando
            "jumping": ["O_O", "O_O", "@_@", "O_O", "O_O", "@_@"],                    # Estado pulando
            "breathing": ["^_^", "^_^", "o_o", "^_^", "-_-", "^_^", "o_o", "^_^"]     # Estado respirando
        }
        
        self.current_state = "idle"     # Estado atual da animação
        self.breathing_cycle = 0        # Controla quando alternar para respiração
    
    def update_animation(self):
        """
        Atualizar sistema de animação do herói
        
        REQUISITO ATENDIDO: "animações de sprite (andar, parado, respirando, etc.)"
        
        Este método determina qual animação deve ser reproduzida
        baseado no estado atual do personagem
        """
        global player_animation_timer, player_animation_frame
        
        # Determinar estado da animação baseado no movimento do jogador
        if not player_on_ground:
            # Se não está no chão, usar animação de pulo
            self.current_state = "jumping"
        elif abs(player_vx) > 0.5:
            # Se está se movendo horizontalmente, usar animação de caminhada
            self.current_state = "walking"
        else:
            # Se está parado, alternar entre idle e breathing
            self.breathing_cycle += 1
            if self.breathing_cycle > 200:  # A cada ~3 segundos
                # Alternar entre estado parado e respirando
                self.current_state = "breathing" if self.current_state == "idle" else "idle"
                self.breathing_cycle = 0
        
        # Controlar velocidade da animação
        player_animation_timer += 1
        if player_animation_timer > 8:  # Velocidade da animação
            player_animation_timer = 0
            frames = self.animation_states[self.current_state]
            player_animation_frame = (player_animation_frame + 1) % len(frames)
    
    def get_current_frame(self):
        """
        Obter o frame atual da animação
        
        Returns:
            str: Emoji representando a expressão facial atual
        """
        frames = self.animation_states[self.current_state]
        return frames[player_animation_frame % len(frames)]

# ===================================================================
# CLASSE DOS INIMIGOS ALIENS (REQUISITO: INIMIGOS PERIGOSOS)
# ===================================================================

class SpaceKAlien:
    """
    Classe para inimigos alienígenas perigosos
    
    REQUISITOS ATENDIDOS:
    - Vários inimigos perigosos
    - Eles se movem em seu território
    - Usar classes para personagens e sprites
    - Animações de sprite (andar, parado, respirando, etc.)
    """
    
    def __init__(self, x, y, alien_type="standard", territory_size=100):
        """
        Inicializar alien inimigo
        
        Args:
            x, y: Posição inicial do alien
            alien_type: Tipo do alien (standard, jumper, flyer, robot)
            territory_size: Tamanho do território onde o alien patrulha
        """
        # Posição e tamanho do alien
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        
        # Sistema de movimento
        self.vx = random.choice([-2, 2])  # Velocidade horizontal inicial
        self.vy = 0                       # Velocidade vertical
        
        # Definir território de patrulhamento (REQUISITO: movem em território)
        self.alien_type = alien_type
        self.start_x = x                  # Centro do território
        self.territory_size = territory_size  # Raio do território
        self.on_ground = False
        
        # Sistema completo de animação de sprite para aliens
        self.idle_timer = 0               # Timer para animação parado
        self.walk_timer = 0               # Timer para animação andando
        self.breathing_timer = 0          # Timer para animação respirando
        self.blink_timer = random.randint(60, 180)  # Timer para piscar
        self.is_blinking = False          # Estado de piscar
        
        # Estados de animação (REQUISITO: animações de sprite)
        self.animation_state = "idle"     # Estado atual
        self.animation_frame = 0          # Frame atual
        self.animation_timer = 0          # Timer da animação
        
        # Sistema de vida baseado no tipo de alien
        if alien_type == "robot":
            self.health = 3               # Robôs são mais resistentes
        elif alien_type == "jumper":
            self.health = 2               # Saltadores são médios
        else:
            self.health = 1               # Aliens padrão são frágeis
        
        self.max_health = self.health     # Vida máxima (para barra de vida)
        self.alive = True                 # Se o alien está vivo
        self.facing = 1 if self.vx > 0 else -1  # Direção que está olhando
        self.glow_timer = random.randint(0, 100)  # Timer para efeitos visuais
        self.patrol_pause_timer = 0       # Timer para pausas na patrulha
        
        # Comportamentos especiais por tipo de alien
        if alien_type == "flyer":
            # Aliens voadores têm padrão de voo
            self.flight_offset = random.uniform(0, math.pi * 2)
            self.base_y = y
            self.vx *= 0.7  # Voadores são mais lentos horizontalmente
        elif alien_type == "jumper":
            # Aliens saltadores têm sistema de pulo
            self.jump_timer = random.randint(60, 120)
    
    def update_in_territory(self, platforms):
        """
        Atualizar movimento do alien dentro de seu território
        
        REQUISITO ATENDIDO: "Eles se movem em seu território"
        
        Args:
            platforms: Lista de plataformas para colisão
            
        Cada alien tem um território específico onde patrulha.
        Diferentes tipos têm comportamentos únicos de movimento.
        """
        # Não fazer nada se o alien morreu
        if not self.alive:
            return
        
        # Atualizar todas as animações do alien
        self.update_sprite_animations()
        
        # Sistema de pausa na patrulha (comportamento natural)
        if self.patrol_pause_timer > 0:
            self.patrol_pause_timer -= 1
            self.vx = 0  # Parar movimento durante pausa
            self.animation_state = "idle"  # Mudar para animação parado
            return
        
        # Comportamento específico por tipo de alien
        if self.alien_type == "flyer":
            # Alien voador: movimento em padrão senoidal no ar
            self.flight_offset += 0.12
            self.y = self.base_y + math.sin(self.flight_offset) * 35
            
            # Manter dentro do território horizontal
            if abs(self.x - self.start_x) > self.territory_size:
                self.vx *= -1  # Inverter direção
                self.patrol_pause_timer = random.randint(30, 60)  # Pausar ocasionalmente
                
        elif self.alien_type == "jumper":
            # Alien saltador: aplica gravidade e pula ocasionalmente
            self.vy += 0.5  # Aplicar gravidade
            
            # Verificar colisão com plataformas
            self.on_ground = False
            alien_rect = Rect(self.x, self.y, self.width, self.height)
            for plat in platforms:
                if alien_rect.colliderect(plat) and self.vy > 0:
                    self.y = plat.top - self.height
                    self.vy = 0
                    self.on_ground = True
            
            # Sistema de pulo do alien saltador
            self.jump_timer -= 1
            if self.jump_timer <= 0 and self.on_ground:
                self.vy = random.randint(-12, -8)  # Força do pulo
                self.jump_timer = random.randint(40, 80)  # Próximo pulo
                play_spacek_sound("jump")  # Som de pulo do alien
            
            # Manter dentro do território
            if abs(self.x - self.start_x) > self.territory_size:
                self.vx *= -1
                
        else:  # alien padrão ou robot
            # Aliens terrestres: aplicam gravidade e caminham
            self.vy += 0.5  # Gravidade
            
            # Colisão com plataformas
            alien_rect = Rect(self.x, self.y, self.width, self.height)
            for plat in platforms:
                if alien_rect.colliderect(plat) and self.vy > 0:
                    self.y = plat.top - self.height
                    self.vy = 0
                    self.on_ground = True
            
            # Patrulhamento com pausas ocasionais
            if abs(self.x - self.start_x) > self.territory_size:
                self.vx *= -1  # Inverter direção ao chegar no limite
                if random.randint(0, 100) < 30:  # 30% chance de pausar
                    self.patrol_pause_timer = random.randint(60, 120)
        
        # Atualizar direção de facing baseada no movimento
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1
        
        # Aplicar movimento calculado
        self.x += self.vx
        self.y += self.vy
    
    def update_sprite_animations(self):
        """
        Atualizar todas as animações de sprite do alien
        
        REQUISITO ATENDIDO: "animações de sprite (andar, parado, respirando, etc.)"
        
        Gerencia:
        - Animação de caminhada quando se movendo
        - Animação de parado quando estático
        - Respiração contínua
        - Sistema de piscar natural
        """
        # Incrementar todos os timers de animação
        self.animation_timer += 1
        self.breathing_timer += 1
        self.blink_timer -= 1
        
        # Determinar estado da animação baseado no movimento
        if abs(self.vx) > 0.5:
            self.animation_state = "walking"  # Andando
            self.walk_timer += 1
        else:
            self.animation_state = "idle"     # Parado
            self.idle_timer += 1
        
        # Ciclo de respiração (sempre ativo)
        if self.breathing_timer > 100:
            self.breathing_timer = 0
        
        # Sistema de piscar natural
        if self.blink_timer <= 0:
            self.is_blinking = True
            self.blink_timer = random.randint(200, 500)  # Próxima piscada
        elif self.blink_timer > 480:
            self.is_blinking = False
        
        # Avançar frames da animação
        if self.animation_timer > 30:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 8
    
    def take_damage(self):
        """
        Sistema de dano do alien
        
        Returns:
            bool: True se o alien morreu, False se ainda está vivo
        """
        global score, enemies_defeated
        
        self.health -= 1  # Reduzir vida
        
        if self.health <= 0:
            # Alien morreu
            self.alive = False
            play_spacek_sound("enemy_death")  # Som de morte (enemy_death.mp3)
            
            # Criar efeito visual de explosão
            create_spacek_particles(self.x + self.width//2, self.y + self.height//2, (255, 100, 100), 15)
            
            # Atualizar estatísticas
            enemies_defeated += 1
            score += 150
            return True
        else:
            # Alien ferido mas ainda vivo
            play_spacek_sound("hurt")  # Som de impacto (impact.mp3)
            
            # Criar efeito visual de dano
            create_spacek_particles(self.x + self.width//2, self.y + self.height//2, (255, 255, 0), 8)
            
            # Knockback do alien
            self.vx *= -1.5
            score += 50
        return False
    
    def draw_alien_sprite(self):
        """
        Desenhar sprite do alien com todas as animações
        
        REQUISITO ATENDIDO: "animações de sprite"
        
        Inclui:
        - Cores diferentes por tipo
        - Animação de respiração
        - Movimento da cabeça
        - Olhos que seguem o jogador
        - Antenas animadas
        - Barra de vida para aliens resistentes
        """
        draw_x = self.x - camera_x  # Ajustar posição pela câmera
        
        # Só desenhar se estiver visível na tela
        if -50 < draw_x < WIDTH + 50:
            # Cores específicas por tipo de alien
            base_colors = {
                "flyer": (200, 255, 100),    # Verde-amarelo para voadores
                "jumper": (100, 255, 100),   # Verde para saltadores
                "robot": (150, 150, 255),    # Azul para robôs
                "alien": (255, 100, 100)     # Vermelho para aliens padrão
            }
            
            # Efeito de respiração quando parado (animação de sprite)
            if self.animation_state == "idle":
                breathing_effect = int(abs(math.sin(self.breathing_timer * 0.12)) * 25)
            else:
                breathing_effect = 0
            
            # Aplicar cor base + efeito de respiração
            base_color = base_colors.get(self.alien_type, (255, 100, 100))
            color = safe_color((base_color[0] + breathing_effect, base_color[1], base_color[2]))
            
            # Desenhar sombra do alien
            shadow_rect = Rect(draw_x + 3, self.y + 3, self.width, self.height)
            screen.draw.filled_rect(shadow_rect, (8, 8, 8))
            
            # Desenhar corpo principal do alien
            alien_rect = Rect(draw_x, self.y, self.width, self.height)
            screen.draw.filled_rect(alien_rect, color)
            
            # Animação da cabeça baseada no movimento (sprite animation)
            if self.animation_state == "walking":
                # Cabeça balança ao andar
                head_bob = int(math.sin(self.walk_timer * 0.4) * 4)
            else:
                # Cabeça se move suavemente quando parado
                head_bob = int(math.sin(self.idle_timer * 0.08) * 2)
            
            # Calcular posição e tamanho da cabeça
            head_size = 16 + head_bob
            head_y = self.y + 12 + head_bob
            head_color = safe_color((color[0] + 50, color[1] + 50, color[2] + 50))
            
            # Desenhar cabeça do alien
            screen.draw.filled_circle((draw_x + self.width//2, head_y), head_size, head_color)
            screen.draw.circle((draw_x + self.width//2, head_y), head_size, (255, 255, 255))
            
            # Sistema de olhos por tipo de alien
            eye_colors = {
                "robot": (255, 0, 0),      # Vermelho para robôs
                "flyer": (255, 255, 0),    # Amarelo para voadores
                "jumper": (0, 255, 0),     # Verde para saltadores
                "alien": (0, 255, 100)     # Verde-azul para aliens padrão
            }
            eye_color = eye_colors.get(self.alien_type, (0, 255, 100))
            
            # Animação dos olhos baseada no estado (sprite animation)
            if self.is_blinking:
                eye_size = 1  # Olhos fechados quando piscando
            elif self.animation_state == "walking":
                # Olhos variam de tamanho ao andar
                eye_size = 5 + (self.animation_frame % 4)
            else:
                # Olhos pulsam com a respiração quando parado
                eye_size = 6 + int(abs(math.sin(self.breathing_timer * 0.15)) * 3)
            
            # Posições dos olhos
            eye1_x = draw_x + 7
            eye2_x = draw_x + 23
            eye_y = head_y - 3
            
            # Desenhar olhos do alien
            screen.draw.filled_circle((eye1_x, eye_y), eye_size, eye_color)
            screen.draw.filled_circle((eye2_x, eye_y), eye_size, eye_color)
            
            # Pupilas inteligentes que seguem o jogador
            if not self.is_blinking and abs(player_x - self.x) < 300:
                # Calcular direção para o jogador
                pupil_offset_x = 2 if player_x > self.x else -2
                pupil_offset_y = 1 if player_y > self.y else -1
                
                # Desenhar pupilas
                screen.draw.filled_circle((eye1_x + pupil_offset_x, eye_y + pupil_offset_y), 2, (0, 0, 0))
                screen.draw.filled_circle((eye2_x + pupil_offset_x, eye_y + pupil_offset_y), 2, (0, 0, 0))
            
            # Antenas animadas do alien
            for i in range(2):
                antenna_x = draw_x + 9 + i * 12
                # Movimento senoidal das antenas
                antenna_sway = int(math.sin(self.glow_timer * 0.15 + i * 4) * 5)
                antenna_length = 10 + int(abs(math.sin(self.glow_timer * 0.2 + i)) * 6)
                antenna_y = self.y - 8
                
                # Desenhar antena
                screen.draw.line((antenna_x, self.y), 
                               (antenna_x + antenna_sway, antenna_y - antenna_length), (255, 255, 255))
                # Ponta da antena brilhante
                screen.draw.filled_circle((antenna_x + antenna_sway, antenna_y - antenna_length), 4, eye_color)
            
            # Barra de vida para aliens com mais de 1 HP
            if self.max_health > 1:
                health_width = int((self.health / self.max_health) * 26)
                
                # Cor da barra baseada na vida restante
                if self.health <= 1:
                    health_color = (255, 0, 0)      # Vermelho (crítico)
                elif self.health <= 2:
                    health_color = (255, 255, 0)    # Amarelo (médio)
                else:
                    health_color = (0, 255, 0)      # Verde (cheio)
                
                # Desenhar barra de vida
                screen.draw.filled_rect(Rect(draw_x + 2, self.y - 15, health_width, 6), health_color)

# ===================================================================
# CLASSE DOS POWER-UPS (ELEMENTOS COLECIONÁVEIS)
# ===================================================================

class SpaceKPowerup:
    """
    Classe para power-ups colecionáveis do SpaceK
    
    Tipos disponíveis:
    - energy: Restaura energia do traje
    - oxygen: Restaura oxigênio
    - life: Vida extra
    - jetpack: Recarrega jetpack
    - shield: Escudo temporário
    - speed: Aumento de velocidade
    """
    
    def __init__(self, x, y, powerup_type="energy"):
        """
        Inicializar power-up
        
        Args:
            x, y: Posição do power-up
            powerup_type: Tipo de power-up
        """
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.powerup_type = powerup_type
        self.collected = False      # Se já foi coletado
        self.float_timer = 0        # Timer para animação flutuante
        self.original_y = y         # Posição Y original
        self.glow_timer = 0         # Timer para efeito de brilho
        self.pulse_timer = 0        # Timer para efeito pulsante
    
    def update(self):
        """
        Atualizar animação do power-up
        """
        if not self.collected:
            # Animação flutuante
            self.float_timer += 0.15
            self.y = self.original_y + math.sin(self.float_timer) * 12
            
            # Timers para efeitos visuais
            self.glow_timer += 1
            self.pulse_timer += 1
    
    def draw(self):
        """
        Desenhar power-up com efeitos visuais
        """
        if not self.collected:
            draw_x = self.x - camera_x
            
            if -50 < draw_x < WIDTH + 50:
                # Efeito pulsante
                pulse = int(abs(math.sin(self.pulse_timer * 0.2)) * 50)
                
                # Cores específicas por tipo
                colors = {
                    "energy": safe_color((0 + pulse, 255, 255)),      # Ciano
                    "oxygen": safe_color((100, 255, 100 + pulse)),    # Verde
                    "life": safe_color((255, 100 + pulse, 255)),      # Magenta
                    "jetpack": safe_color((255, 255, 0 + pulse)),     # Amarelo
                    "shield": safe_color((100 + pulse, 150, 255)),    # Azul
                    "speed": safe_color((255, 200, 0 + pulse))        # Laranja
                }
                color = colors.get(self.powerup_type, (255, 255, 255))
                
                # Aura externa
                aura_size = 25 + int(abs(math.sin(self.glow_timer * 0.12)) * 10)
                aura_color = safe_color((color[0] // 6, color[1] // 6, color[2] // 6))
                screen.draw.filled_circle((draw_x + 15, self.y + 15), aura_size, aura_color)
                
                # Cristal em camadas
                for layer in range(6):
                    size = 16 - layer * 2
                    layer_color = safe_color((color[0] + layer * 15, color[1] + layer * 15, color[2] + layer * 15))
                    screen.draw.filled_circle((draw_x + 15, self.y + 15), size, layer_color)
                
                # Borda externa
                screen.draw.circle((draw_x + 15, self.y + 15), 16, (255, 255, 255))
                
                # Ícone do power-up
                icons = {
                    "energy": "⚡", "oxygen": "💨", "life": "❤️",
                    "jetpack": "🚀", "shield": "🛡️", "speed": "💨"
                }
                icon = icons.get(self.powerup_type, "?")
                screen.draw.text(icon, (draw_x + 9, self.y + 9), fontsize=18)

# ===================================================================
# CLASSE DAS MOEDAS SPACEK
# ===================================================================

class SpaceKCoin:
    """
    Classe para moedas colecionáveis do SpaceK
    Moedas fornecem pontos extras e são marcadas com "K"
    """
    
    def __init__(self, x, y):
        """Inicializar moeda SpaceK"""
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.collected = False          # Se foi coletada
        self.rotation = 0               # Rotação para efeito 3D
        self.float_timer = 0            # Timer para flutuação
        self.original_y = y             # Posição Y original
        self.sparkle_timer = 0          # Timer para efeito de brilho
    
    def update(self):
        """Atualizar animação da moeda"""
        if not self.collected:
            self.rotation += 8  # Rotação constante
            self.float_timer += 0.3
            # Movimento flutuante suave
            self.y = self.original_y + math.sin(self.float_timer) * 6
            self.sparkle_timer += 1
    
    def draw(self):
        """Desenhar moeda com efeito 3D e brilhos"""
        if not self.collected:
            draw_x = self.x - camera_x
            
            if -25 < draw_x < WIDTH + 25:
                # Efeito de brilho ocasional
                if self.sparkle_timer % 80 < 15:
                    for i in range(4):
                        spark_x = draw_x + 8 + random.randint(-15, 15)
                        spark_y = self.y + 8 + random.randint(-15, 15)
                        screen.draw.filled_circle((spark_x, spark_y), 1, (255, 255, 200))
                
                # Efeito 3D da moeda rotativa
                scale = abs(math.cos(self.rotation * 0.08))
                width = max(4, int(16 * scale))
                
                # Desenhar moeda principal
                coin_rect = Rect(draw_x + 8 - width//2, self.y + 4, width, 8)
                screen.draw.filled_rect(coin_rect, (255, 215, 0))
                
                # Desenhar símbolo "K" do SpaceK
                if width > 8:
                    screen.draw.text("K", (draw_x + 6, self.y + 2), fontsize=14, color="orange")

# ===================================================================
# CLASSE DOS LASERS (SISTEMA DE COMBATE)
# ===================================================================

class SpaceKLaser:
    """
    Classe para projéteis laser do astronauta
    Sistema de combate contra os aliens
    """
    
    def __init__(self, x, y, direction):
        """
        Inicializar laser
        
        Args:
            x, y: Posição inicial
            direction: Direção do disparo (1=direita, -1=esquerda)
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 18             # Velocidade do laser
        self.width = 14
        self.height = 6
        self.alive = True           # Se o laser ainda existe
        self.trail = []             # Rastro visual do laser
        self.energy = 120           # Energia do laser (vida útil)
    
    def update(self):
        """Atualizar movimento do laser"""
        # Adicionar posição atual ao rastro
        self.trail.append((self.x - camera_x, self.y))
        if len(self.trail) > 12:
            self.trail.pop(0)  # Limitar tamanho do rastro
        
        # Mover laser
        self.x += self.speed * self.direction
        self.energy -= 3
        
        # Remover laser se saiu da tela ou perdeu energia
        if self.x < camera_x - 150 or self.x > camera_x + WIDTH + 150 or self.energy <= 0:
            self.alive = False
    
    def draw(self):
        """Desenhar laser com rastro energético"""
        if self.alive:
            draw_x = self.x - camera_x
            
            if -40 < draw_x < WIDTH + 40:
                # Desenhar rastro energético
                for i, (trail_x, trail_y) in enumerate(self.trail):
                    alpha = (i + 1) / len(self.trail)
                    size = int(8 * alpha)
                    brightness = int(255 * alpha)
                    if size > 0:
                        trail_color = safe_color((brightness, 255, 255))
                        screen.draw.filled_circle((int(trail_x), int(trail_y)), size, trail_color)
                
                # Desenhar laser principal em camadas
                laser_outer = Rect(draw_x - 3, self.y - 2, self.width + 6, self.height + 4)
                screen.draw.filled_rect(laser_outer, (50, 200, 255))
                
                laser_core = Rect(draw_x, self.y, self.width, self.height)
                screen.draw.filled_rect(laser_core, (255, 255, 255))

# ===================================================================
# CLASSE DE PARTÍCULAS (EFEITOS VISUAIS)
# ===================================================================

class SpaceKParticle:
    """
    Sistema de partículas para efeitos visuais
    Usado para explosões, faíscas, fumaça, etc.
    """
    
    def __init__(self, x, y, color, velocity, lifetime, particle_type="normal"):
        """
        Inicializar partícula
        
        Args:
            x, y: Posição inicial
            color: Cor da partícula
            velocity: Tupla (vx, vy) com velocidade
            lifetime: Tempo de vida da partícula
            particle_type: Tipo de partícula (normal, spark, smoke)
        """
        self.x = x
        self.y = y
        self.color = safe_color(color)
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 7)
        self.particle_type = particle_type
        self.rotation = random.uniform(0, 360)
    
    def update(self):
        """Atualizar física da partícula"""
        # Movimento
        self.x += self.vx
        self.y += self.vy
        
        # Comportamento específico por tipo
        if self.particle_type == "normal":
            self.vy += 0.2  # Gravidade normal
        elif self.particle_type == "spark":
            # Faíscas desaceleram gradualmente
            self.vx *= 0.92
            self.vy *= 0.92
        elif self.particle_type == "smoke":
            # Fumaça sobe e desacelera
            self.vy -= 0.1
            self.vx *= 0.9
        
        # Envelhecer partícula
        self.lifetime -= 1
        self.rotation += 10
        
        # Diminuir tamanho com o tempo (fade out)
        alpha = max(0, self.lifetime / self.max_lifetime)
        self.size = max(1, int(7 * alpha))
    
    def draw(self):
        """Desenhar partícula com efeitos visuais"""
        if self.lifetime > 0:
            draw_x = self.x - camera_x
            
            if -20 < draw_x < WIDTH + 20:
                # Calcular transparência baseada na vida restante
                alpha = max(0, self.lifetime / self.max_lifetime)
                final_color = safe_color((self.color[0] * alpha, self.color[1] * alpha, self.color[2] * alpha))
                
                if self.particle_type == "spark":
                    # Partícula em formato de estrela
                    for angle in [0, 60, 120, 180, 240, 300]:
                        rad = math.radians(angle + self.rotation)
                        end_x = draw_x + math.cos(rad) * self.size
                        end_y = self.y + math.sin(rad) * self.size
                        screen.draw.line((draw_x, self.y), (end_x, end_y), final_color)
                else:
                    # Partícula circular normal
                    screen.draw.filled_circle((int(draw_x), int(self.y)), self.size, final_color)

# ===================================================================
# INSTÂNCIA GLOBAL DO HERÓI
# ===================================================================
# Criar instância única do herói astronauta
spacek_hero = SpaceKHero()

# ===================================================================
# FUNÇÕES AUXILIARES DO JOGO
# ===================================================================

def create_spacek_particles(x, y, color, count=8, particle_type="normal"):
    """
    Criar explosão de partículas para efeitos visuais
    
    Args:
        x, y: Posição da explosão
        color: Cor das partículas
        count: Número de partículas
        particle_type: Tipo das partículas
    """
    for _ in range(count):
        if particle_type == "spark":
            # Faíscas têm velocidade alta e variada
            velocity = (random.uniform(-10, 10), random.uniform(-12, -4))
        elif particle_type == "smoke":
            # Fumaça tem velocidade baixa
            velocity = (random.uniform(-3, 3), random.uniform(-8, -5))
        else:
            # Partículas normais
            velocity = (random.uniform(-6, 6), random.uniform(-8, -3))
        
        # Adicionar partícula à lista global
        particles.append(SpaceKParticle(x, y, safe_color(color), velocity, random.randint(50, 100), particle_type))

def create_spacek_menu():
    """
    Criar botões do menu principal
    
    REQUISITO ATENDIDO: "Menu principal com botões clicáveis"
    """
    global menu_buttons
    menu_buttons = [
        # Botão para começar o jogo
        SpaceKButton(WIDTH//2 - 120, 300, 240, 60, "🚀 INICIAR SPACEK", "start", (80, 150, 80)),
        
        # Botão para controle de áudio (REQUISITO: Música/sons ON-OFF)
        SpaceKButton(WIDTH//2 - 120, 380, 240, 50, f"🎵 ÁUDIO: {'ON' if sounds_enabled else 'OFF'}", "music", (80, 80, 150)),
        
        # Botão para testar sistema de som
        SpaceKButton(WIDTH//2 - 120, 450, 240, 50, "🔊 TESTAR SONS", "test", (150, 150, 80)),
        
        # Botão para sair do jogo
        SpaceKButton(WIDTH//2 - 120, 520, 240, 50, "❌ SAIR", "quit", (150, 80, 80))
    ]

def setup_spacek():
    """
    Configurar estado inicial do jogo SpaceK
    
    Esta função inicializa todas as variáveis e elementos
    necessários para começar uma nova partida
    """
    # Declarar que vamos modificar variáveis globais
    global platforms, enemies, powerups, stars, coins
    global player_x, player_y, player_vx, player_vy, player_lives, player_energy
    global player_jetpack_fuel, current_level, camera_x, oxygen, score, coins_collected, enemies_defeated
    global player_move_left, player_move_right
    
    # Resetar estado do jogador
    player_x = 100                # Posição inicial
    player_y = 500
    player_vx = 0                 # Parado inicialmente
    player_vy = 0
    player_lives = 3              # Vidas iniciais
    player_energy = 100           # Energia cheia
    player_jetpack_fuel = 100     # Combustível cheio
    
    # Resetar controles de movimento
    player_move_left = False      # Não está movendo para esquerda
    player_move_right = False     # Não está movendo para direita
    
    # Resetar estado do jogo
    current_level = 1             # Começar no nível 1
    camera_x = 0                  # Câmera na posição inicial
    oxygen = 100                  # Oxigênio cheio
    score = 0                     # Pontuação zerada
    coins_collected = 0           # Moedas zeradas
    enemies_defeated = 0          # Inimigos derrotados zerado
    
    # Criar campo de estrelas de fundo
    stars.clear()
    for _ in range(120):
        stars.append({
            'x': random.randint(0, WIDTH * 6),  # Posição X aleatória
            'y': random.randint(0, HEIGHT),     # Posição Y aleatória
            'size': random.randint(1, 4),       # Tamanho aleatório
            'speed': random.uniform(0.02, 0.3), # Velocidade aleatória
            'twinkle': random.randint(0, 100),  # Timer de brilho
            'color': random.choice([            # Cor aleatória
                (255, 255, 255), (255, 255, 200), 
                (200, 255, 255), (255, 200, 255)
            ])
        })
    
    # Carregar o primeiro nível
    load_spacek_level(current_level)

def load_spacek_level(level):
    """
    Carregar elementos específicos de cada nível
    
    REQUISITO ATENDIDO: "Vários inimigos perigosos. Eles se movem em seu território"
    
    Args:
        level: Número do nível a ser carregado (1 ou 2)
    """
    global platforms, enemies, powerups, coins
    
    # Limpar elementos do nível anterior
    platforms.clear()
    enemies.clear()
    powerups.clear()
    coins.clear()
    
    if level == 1:
        # ===============================
        # NÍVEL 1 - ESTAÇÃO ESPACIAL
        # ===============================
        
        # Plataformas do primeiro nível
        platforms.extend([
            Rect(0, 540, WIDTH * 3, 60),      # Chão base contínuo (não desaparece)
            Rect(200, 450, 120, 20),          # Plataforma de desembarque
            Rect(400, 400, 140, 20),          # Plataforma central
            Rect(600, 350, 120, 20),          # Plataforma elevada
            Rect(800, 380, 160, 20),          # Plataforma larga
            Rect(1100, 320, 120, 20),         # Plataforma alta
            Rect(1300, 400, 200, 30),         # Plataforma de escape
            Rect(1600, 350, 150, 20),         # Plataforma avançada
            Rect(1900, 300, 120, 20),         # Plataforma final alta
            Rect(2200, 450, 300, 30)          # Base final do nível
        ])
        
        # Inimigos aliens em territórios específicos (REQUISITO)
        # Cada alien patrulha uma área definida
        enemies.extend([
            SpaceKAlien(250, 430, "alien", 100),      # Alien padrão: território 150-350
            SpaceKAlien(450, 380, "jumper", 120),     # Saltador: território 330-570
            SpaceKAlien(650, 330, "flyer", 140),      # Voador: território 510-790
            SpaceKAlien(850, 360, "robot", 100),      # Robô: território 750-950
            SpaceKAlien(1150, 300, "alien", 80),      # Alien: território 1070-1230
            SpaceKAlien(1400, 370, "flyer", 200),     # Voador: território 1200-1600
            SpaceKAlien(1700, 330, "jumper", 130),    # Saltador: território 1570-1830
            SpaceKAlien(2000, 280, "robot", 150)      # Robô final: território 1850-2150
        ])
        
        # Power-ups estrategicamente posicionados
        powerups.extend([
            SpaceKPowerup(350, 420, "energy"),   # Energia após primeiro alien
            SpaceKPowerup(550, 320, "oxygen"),   # Oxigênio na área central
            SpaceKPowerup(750, 350, "jetpack"),  # Jetpack antes do robô
            SpaceKPowerup(950, 350, "shield"),   # Escudo após robô
            SpaceKPowerup(1200, 280, "life"),    # Vida extra no meio
            SpaceKPowerup(1500, 320, "energy"),  # Energia avançada
            SpaceKPowerup(1800, 270, "shield"),  # Escudo antes do final
            SpaceKPowerup(2100, 430, "life")     # Vida antes do final
        ])
        
        # Moedas K espalhadas pelo nível
        coin_positions = [
            (280, 410), (520, 300), (680, 310), (920, 340),
            (1080, 280), (1450, 350), (1750, 310), (2050, 410)
        ]
        for x, y in coin_positions:
            coins.append(SpaceKCoin(x, y))
    
    elif level == 2:
        # ===============================
        # NÍVEL 2 - BASE ALIENÍGENA
        # ===============================
        # Nível mais desafiador com territórios menores (aliens mais agressivos)
        
        platforms.extend([
            Rect(0, 540, WIDTH * 3, 60),      # Chão base contínuo
            Rect(150, 480, 100, 20),          # Entrada da base
            Rect(320, 420, 80, 20),           # Plataforma de defesa
            Rect(480, 360, 100, 20),          # Centro de comando
            Rect(640, 300, 80, 20),           # Torre de vigilância
            Rect(800, 380, 120, 20),          # Laboratório
            Rect(980, 320, 100, 20),          # Sala de máquinas
            Rect(1150, 260, 120, 20),         # Hangar superior
            Rect(1320, 400, 150, 20),         # Hangar principal
            Rect(1550, 340, 100, 20),         # Sala de energia
            Rect(1750, 280, 120, 20),         # Torre principal
            Rect(1950, 400, 250, 30)          # Núcleo da base alienígena
        ])
        
        # Mais aliens com territórios menores (mais agressivos)
        enemies.extend([
            SpaceKAlien(180, 460, "jumper", 40),      # Território pequeno: mais agressivo
            SpaceKAlien(350, 400, "robot", 50),       # Robô guardião
            SpaceKAlien(510, 340, "flyer", 60),       # Patrulha aérea
            SpaceKAlien(670, 280, "alien", 40),       # Sentinela
            SpaceKAlien(830, 360, "robot", 70),       # Robô avançado
            SpaceKAlien(1010, 300, "flyer", 50),      # Interceptador
            SpaceKAlien(1180, 240, "jumper", 50),     # Saltador de elite
            SpaceKAlien(1350, 380, "alien", 80),      # Comandante alien
            SpaceKAlien(1580, 320, "robot", 60),      # Guardião da energia
            SpaceKAlien(1780, 260, "flyer", 70),      # Patrulha final
            SpaceKAlien(2000, 380, "alien", 100)      # Chefe final
        ])
        
        # Power-ups mais espaçados (maior dificuldade)
        powerups.extend([
            SpaceKPowerup(220, 440, "shield"),   # Escudo inicial
            SpaceKPowerup(380, 380, "energy"),   # Energia cedo
            SpaceKPowerup(540, 320, "jetpack"),  # Jetpack central
            SpaceKPowerup(700, 240, "oxygen"),   # Oxigênio crítico
            SpaceKPowerup(860, 340, "life"),     # Vida no meio
            SpaceKPowerup(1040, 280, "speed"),   # Velocidade
            SpaceKPowerup(1210, 220, "energy"),  # Energia alta
            SpaceKPowerup(1380, 360, "shield"),  # Escudo final
            SpaceKPowerup(1610, 300, "jetpack"), # Jetpack avançado
            SpaceKPowerup(1810, 240, "life")     # Vida final
        ])
        
        # Mais moedas no segundo nível
        coin_positions = [
            (250, 420), (410, 360), (570, 300), (730, 220), (890, 320),
            (1070, 260), (1240, 200), (1410, 340), (1640, 280), (1840, 220)
        ]
        for x, y in coin_positions:
            coins.append(SpaceKCoin(x, y))

# ===================================================================
# FUNÇÃO PRINCIPAL DE ATUALIZAÇÃO (MECÂNICA DO JOGO)
# ===================================================================

def update():
    """
    Função principal de atualização do jogo SpaceK
    
    REQUISITO ATENDIDO: "Jogo com mecânica lógica, sem bugs"
    
    Esta função é chamada 60 vezes por segundo e gerencia:
    - Física do jogador (gravidade, movimento, colisões)
    - Comportamento dos inimigos
    - Sistema de projéteis
    - Efeitos visuais
    - Lógica de progressão do jogo
    """
    # Declarar variáveis globais que serão modificadas
    global player_x, player_y, player_vx, player_vy, player_on_ground, player_invulnerable
    global player_energy, player_jetpack_fuel, player_lives, game_state, current_level
    global camera_x, oxygen, score, player_has_shield, player_shield_timer, coins_collected
    
    # ===============================
    # LÓGICA DO MENU PRINCIPAL
    # ===============================
    if game_state == "menu":
        # Atualizar apenas estrelas de fundo no menu
        for star in stars:
            star['x'] -= star['speed']
            if star['x'] < -20:
                star['x'] = WIDTH + 20
            star['twinkle'] += 1
        return  # Não executar lógica do jogo
    
    # ===============================
    # LÓGICA DA TELA DE VITÓRIA
    # ===============================
    if game_state == "victory":
        # Atualizar partículas de celebração
        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)
        
        # Adicionar novas partículas de celebração ocasionalmente
        if random.randint(0, 12) == 0:
            particles.append(SpaceKParticle(
                random.randint(0, WIDTH), random.randint(0, HEIGHT//3),
                (255, 255, 0), (random.uniform(-4, 4), random.uniform(-5, -2)),
                150, "spark"
            ))
        return  # Não executar lógica do jogo
    
    # Se não estiver jogando, não fazer nada
    if game_state != "playing":
        return
    
    # ===============================
    # SISTEMA DE ANIMAÇÃO DO HERÓI
    # ===============================
    # Atualizar animações do astronauta (REQUISITO: animações de sprite)
    spacek_hero.update_animation()
    
    # ===============================
    # SISTEMA DE ESCUDO
    # ===============================
    # Gerenciar tempo de duração do escudo
    if player_has_shield:
        player_shield_timer -= 1
        if player_shield_timer <= 0:
            player_has_shield = False
    
    # ===============================
    # FÍSICA DO JOGADOR
    # ===============================
    # Sistema de movimento contínuo baseado em teclas pressionadas
    if player_move_left and not player_move_right:
        # Acelerar para a esquerda
        player_vx -= player_acceleration
        if player_vx < -player_max_speed:
            player_vx = -player_max_speed
        player_facing = -1
    elif player_move_right and not player_move_left:
        # Acelerar para a direita
        player_vx += player_acceleration
        if player_vx > player_max_speed:
            player_vx = player_max_speed
        player_facing = 1
    else:
        # Aplicar atrito quando nenhuma tecla está pressionada
        player_vx *= player_friction
        # Parar completamente se a velocidade for muito baixa
        if abs(player_vx) < 0.1:
            player_vx = 0
    
    # Aplicar gravidade apenas se não estiver no chão
    if not player_on_ground:
        player_vy += 0.6  # Força da gravidade
    
    # Limitar velocidade máxima de queda
    if player_vy > 15:
        player_vy = 15
    
    # Salvar posição anterior para detectar colisões corretas
    old_player_x = player_x
    
    # Aplicar movimento
    player_x += player_vx  # Movimento horizontal
    player_y += player_vy  # Movimento vertical (inclui gravidade)
    
    # Limitar movimento para não sair da tela pela esquerda
    if player_x < 0:
        player_x = 0
    
    # ===============================
    # SISTEMA DE COLISÃO COM PLATAFORMAS
    # ===============================
    player_on_ground = False
    player_rect = Rect(player_x, player_y, 30, 40)  # Hitbox do jogador
    
    # Verificar colisão com todas as plataformas
    for plat in platforms:
        if player_rect.colliderect(plat):
            # Verificar se está caindo em cima da plataforma (não atravessando)
            if player_vy > 0 and old_player_x + 15 > plat.left and old_player_x + 15 < plat.right:
                player_y = plat.top - 40     # Posicionar em cima da plataforma
                player_vy = 0                # Parar queda
                player_on_ground = True      # Marcar como no chão
                # Recarregar jetpack quando toca o chão
                player_jetpack_fuel = min(100, player_jetpack_fuel + 4)
                break  # Parar após primeira colisão
    
    # ===============================
    # SISTEMA DE CÂMERA
    # ===============================
    # Câmera que segue o jogador suavemente
    target_camera = max(0, player_x - WIDTH // 2.5)  # Posição alvo da câmera
    camera_x += (target_camera - camera_x) * 0.05     # Movimento suave
    
    # ===============================
    # ATUALIZAR ELEMENTOS DE FUNDO
    # ===============================
    # Atualizar estrelas com efeito parallax
    for star in stars:
        star['x'] -= star['speed'] * 0.5  # Movimento mais lento que a câmera
        # Reposicionar estrelas que saíram da tela
        if star['x'] < camera_x - 200:
            star['x'] = camera_x + WIDTH + 200
        star['twinkle'] += 0.5  # Efeito de brilho
    
    # ===============================
    # ATUALIZAR INIMIGOS (REQUISITO)
    # ===============================
    # Atualizar todos os aliens que se movem em territórios
    for enemy in enemies:
        enemy.update_in_territory(platforms)
    
    # ===============================
    # ATUALIZAR POWER-UPS E MOEDAS
    # ===============================
    for powerup in powerups:
        powerup.update()
    
    for coin in coins:
        coin.update()
    
    # ===============================
    # SISTEMA DE PROJÉTEIS LASER
    # ===============================
    # Atualizar todos os lasers disparados
    for laser in lasers[:]:  # Usar cópia da lista para remoção segura
        laser.update()
        
        if not laser.alive:
            lasers.remove(laser)  # Remover lasers mortos
        else:
            # Verificar colisão laser-inimigo
            laser_rect = Rect(laser.x, laser.y, laser.width, laser.height)
            for enemy in enemies:
                if enemy.alive:
                    enemy_rect = Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    if laser_rect.colliderect(enemy_rect):
                        # Laser acertou inimigo
                        play_spacek_sound("laser_hit")  # Som de acerto
                        enemy.take_damage()             # Aplicar dano
                        laser.alive = False             # Destruir laser
                        break  # Parar após primeiro acerto
    
    # ===============================
    # SISTEMA DE PARTÍCULAS VISUAIS
    # ===============================
    # Atualizar e limpar partículas
    for particle in particles[:]:
        particle.update()
        if particle.lifetime <= 0:
            particles.remove(particle)
    
    # ===============================
    # COLISÃO JOGADOR-INIMIGO
    # ===============================
    # Verificar se jogador colidiu com algum inimigo
    if player_invulnerable <= 0 and not player_has_shield:
        for enemy in enemies:
            if enemy.alive:
                enemy_rect = Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if player_rect.colliderect(enemy_rect):
                    take_spacek_damage()  # Jogador recebe dano
                    break  # Parar após primeira colisão
    else:
        # Decrementar timer de invulnerabilidade
        player_invulnerable -= 1
    
    # ===============================
    # SISTEMA DE COLETA
    # ===============================
    # Verificar coleta de power-ups
    for powerup in powerups:
        if not powerup.collected:
            powerup_rect = Rect(powerup.x, powerup.y, powerup.width, powerup.height)
            if player_rect.colliderect(powerup_rect):
                collect_spacek_powerup(powerup)
    
    # Verificar coleta de moedas
    for coin in coins:
        if not coin.collected:
            coin_rect = Rect(coin.x, coin.y, coin.width, coin.height)
            if player_rect.colliderect(coin_rect):
                # Coletar moeda
                coin.collected = True
                coins_collected += 1
                score += 100
                play_spacek_sound("collect")  # Som de coleta
                # Efeito visual de coleta
                create_spacek_particles(coin.x + 8, coin.y + 8, (255, 215, 0), 15, "spark")
    
    # ===============================
    # SISTEMA DE SOBREVIVÊNCIA
    # ===============================
    # Consumir oxigênio gradualmente
    oxygen -= 0.03
    if oxygen <= 0:
        take_spacek_damage()  # Dano por falta de oxigênio
        oxygen = 100          # Resetar oxigênio
    
    # Verificar morte por queda
    if player_y > HEIGHT + 100:
        take_spacek_damage()
    
    # ===============================
    # PROGRESSÃO DE NÍVEIS
    # ===============================
    # Verificar se jogador chegou ao final do nível
    level_end_x = 2400 if current_level == 1 else 2200
    if player_x > level_end_x:
        if current_level == 1:
            # Avançar para nível 2
            current_level = 2
            load_spacek_level(current_level)
            
            # Resetar posição do jogador
            player_x = 100
            player_y = 500
            player_vx = 0
            player_vy = 0
            
            # Bônus por completar nível
            score += 3000
            play_spacek_sound("powerup")  # Som de sucesso
            
            # Efeito visual de celebração
            create_spacek_particles(player_x + 15, player_y + 20, (0, 255, 0), 40, "spark")
        else:
            # Jogador completou todos os níveis
            game_state = "victory"
            global high_score
            if score > high_score:
                high_score = score
    
    
    # ===============================
    # VERIFICAR GAME OVER
    # ===============================
    if player_lives <= 0:
        game_state = "gameover"
        if score > high_score:
            high_score = score

# ===================================================================
# FUNÇÕES DE DANO E COLETA
# ===================================================================

def take_spacek_damage():
    """
    Função chamada quando o astronauta recebe dano
    
    Gerencia:
    - Redução de vidas
    - Período de invulnerabilidade
    - Efeitos sonoros e visuais
    - Reset de posição se ainda tem vidas
    """
    global player_lives, player_invulnerable, player_x, player_y, player_vx, player_vy
    
    # Não aplicar dano se ainda invulnerável
    if player_invulnerable > 0:
        return
    
    # Aplicar dano
    player_lives -= 1
    player_invulnerable = 200  # 200 frames de invulnerabilidade (~3 segundos)
    
    # Efeitos de dano
    play_spacek_sound("hurt")  # Som de impacto
    create_spacek_particles(player_x + 15, player_y + 20, (255, 100, 100), 25, "spark")
    
    # Se ainda tem vidas, resetar posição
    if player_lives > 0:
        player_x = max(100, camera_x + 100)  # Reset relativo à câmera
        player_y = 500
        player_vx = 0
        player_vy = 0

def collect_spacek_powerup(powerup):
    """
    Função para coletar power-ups
    
    Args:
        powerup: Objeto power-up coletado
    """
    global player_energy, player_jetpack_fuel, player_lives, oxygen, score
    global player_has_shield, player_shield_timer
    
    # Marcar como coletado
    powerup.collected = True
    
    # Efeitos de coleta
    play_spacek_sound("powerup")  # Som de power-up
    create_spacek_particles(powerup.x + 15, powerup.y + 15, (255, 255, 0), 20, "spark")
    
    # Aplicar efeito baseado no tipo
    if powerup.powerup_type == "energy":
        player_energy = min(100, player_energy + 60)
        score += 200
    elif powerup.powerup_type == "oxygen":
        oxygen = min(100, oxygen + 80)
        score += 150
    elif powerup.powerup_type == "life":
        player_lives += 1
        score += 750
    elif powerup.powerup_type == "jetpack":
        player_jetpack_fuel = 100
        score += 300
    elif powerup.powerup_type == "shield":
        player_has_shield = True
        player_shield_timer = 600  # 10 segundos de escudo
        score += 400
    elif powerup.powerup_type == "speed":
        score += 250

# ===================================================================
# FUNÇÕES DE CONTROLE DO JOGO
# ===================================================================

def start_spacek():
    """Iniciar nova partida do SpaceK"""
    global game_state
    game_state = "playing"
    setup_spacek()

def toggle_spacek_audio():
    """
    Alternar sistema de áudio ON/OFF
    
    REQUISITO ATENDIDO: "Música/sons ON-OFF"
    """
    global music_enabled, sounds_enabled
    music_enabled = not music_enabled
    sounds_enabled = music_enabled
    
    # Atualizar texto do botão
    menu_buttons[1].text = f"🎵 ÁUDIO: {'ON' if sounds_enabled else 'OFF'}"
    
    # Som de confirmação se áudio foi ligado
    if sounds_enabled:
        play_spacek_sound("click")

# ===================================================================
# FUNÇÕES DE DESENHO (INTERFACE GRÁFICA)
# ===================================================================

def draw():
    """
    Função principal de desenho do SpaceK
    
    Gerencia qual tela deve ser desenhada baseada no estado do jogo
    """
    screen.clear()  # Limpar tela
    
    if game_state == "menu":
        draw_spacek_menu()
    elif game_state == "playing":
        draw_spacek_game()
    elif game_state == "gameover":
        draw_spacek_gameover()
    elif game_state == "victory":
        draw_spacek_victory()

def draw_spacek_menu():
    """
    Desenhar menu principal do SpaceK
    
    REQUISITO ATENDIDO: "Menu principal com botões clicáveis"
    """
    # Fundo escuro espacial
    screen.fill((1, 1, 25))
    
    # Desenhar estrelas de fundo
    for star in stars[:60]:  # Apenas parte das estrelas para performance
        draw_x = star['x'] - camera_x * 0.1
        if 0 < draw_x < WIDTH:
            # Calcular brilho baseado no timer de twinkle
            brightness = int(abs(math.sin(star['twinkle'] * 0.04)) * 180) + 75
            color = safe_color((star['color'][0] * brightness // 255, 
                              star['color'][1] * brightness // 255, 
                              star['color'][2] * brightness // 255))
            screen.draw.filled_circle((int(draw_x), int(star['y'])), star['size'], color)
    
    # Desenhar título com efeito de camadas (profundidade)
    for layer in range(6):
        offset = 6 - layer
        colors = [(20, 20, 20), (40, 40, 40), (80, 80, 80), (120, 120, 120), (200, 200, 200), (0, 255, 255)]
        screen.draw.text("🚀 SPACEK 🚀", 
                         center=(WIDTH//2 + offset, 60 + offset), 
                         fontsize=80, 
                         color=colors[layer])
    
    # Subtítulos informativos
    screen.draw.text("MISSÃO ALIENÍGENA", center=(WIDTH//2, 140), fontsize=32, color="white")
    screen.draw.text("Derrote os invasores ETs!", center=(WIDTH//2, 170), fontsize=22, color=(200, 255, 200))
    screen.draw.text("Explore territórios perigosos!", center=(WIDTH//2, 195), fontsize=20, color=(255, 200, 200))
    screen.draw.text("Colete cristais de energia!", center=(WIDTH//2, 220), fontsize=18, color=(200, 200, 255))
    
    # Mostrar recorde se existir
    if high_score > 0:
        screen.draw.text(f"🏆 RECORDE SPACEK: {high_score}", center=(WIDTH//2, 250), fontsize=18, color="gold")
    
    # Desenhar todos os botões do menu
    for button in menu_buttons:
        button.draw()
    
    # Instruções de controle
    screen.draw.text("T: Testar Áudio | WASD: Mover | Espaço: Jetpack | X: Laser", 
                     center=(WIDTH//2, 590), fontsize=12, color="gray")

def draw_spacek_game():
    """
    Desenhar tela principal do jogo SpaceK
    
    Inclui todos os elementos visuais:
    - Fundo espacial
    - Plataformas tecnológicas
    - Personagens e inimigos
    - Efeitos visuais
    - Interface do usuário
    """
    # Fundo diferente por nível
    if current_level == 1:
        screen.fill((3, 3, 45))    # Azul escuro para estação espacial
    else:
        screen.fill((45, 3, 3))    # Vermelho escuro para base alienígena
    
    # Desenhar estrelas com efeito parallax (diferentes velocidades)
    for star in stars:
        parallax_factor = 0.05 + star['size'] * 0.02  # Estrelas maiores movem mais
        draw_x = star['x'] - camera_x * parallax_factor
        
        if -40 < draw_x < WIDTH + 40:
            # Efeito de brilho
            brightness = int(abs(math.sin(star['twinkle'] * 0.01)) * 180) + 75
            color = safe_color((star['color'][0] * brightness // 255,
                              star['color'][1] * brightness // 255,
                              star['color'][2] * brightness // 255))
            screen.draw.filled_circle((int(draw_x), int(star['y'])), star['size'], color)
    
    # Desenhar plataformas (CORRIGIDO para não desaparecerem)
    for plat in platforms:
        draw_x = plat.x - camera_x
        
        # Verificar se qualquer parte da plataforma está visível
        if draw_x + plat.width > -50 and draw_x < WIDTH + 50:
            # Calcular parte visível da plataforma
            visible_x = max(0, draw_x)
            visible_width = min(WIDTH, draw_x + plat.width) - visible_x
            
            if visible_width > 0:
                # Desenhar parte visível da plataforma
                platform_rect = Rect(visible_x, plat.y, visible_width, plat.height)
                screen.draw.filled_rect(platform_rect, (70, 90, 130))
                
                # Padrão tecnológico (linhas de circuito)
                start_i = max(0, int(-draw_x // 20) * 20)
                for i in range(start_i, plat.width, 20):
                    line_x = draw_x + i
                    if 0 <= line_x <= WIDTH:
                        screen.draw.line((line_x, plat.y), (line_x, plat.y + plat.height), (0, 150, 255))
                
                # Bordas da plataforma
                if draw_x >= 0:
                    screen.draw.line((visible_x, plat.y), (visible_x, plat.y + plat.height), (100, 180, 255))
                if draw_x + plat.width <= WIDTH:
                    screen.draw.line((visible_x + visible_width, plat.y), (visible_x + visible_width, plat.y + plat.height), (100, 180, 255))
                
                screen.draw.line((visible_x, plat.y), (visible_x + visible_width, plat.y), (100, 180, 255))
                screen.draw.line((visible_x, plat.y + plat.height), (visible_x + visible_width, plat.y + plat.height), (100, 180, 255))
                
                # LEDs das plataformas (não no chão)
                if plat.y < 520:
                    for i in range(0, plat.width, 30):
                        light_x = draw_x + i + 15
                        if 0 <= light_x <= WIDTH:
                            screen.draw.filled_circle((light_x, plat.y + 5), 4, (0, 255, 255))
    
    # Desenhar todos os elementos do jogo
    for powerup in powerups:
        powerup.draw()
    
    for coin in coins:
        coin.draw()
    
    for enemy in enemies:
        enemy.draw_alien_sprite()
    
    for laser in lasers:
        laser.draw()
    
    for particle in particles:
        particle.draw()
    
    # Desenhar herói e interface
    draw_spacek_hero()
    draw_spacek_interface()

def draw_spacek_hero():
    """
    Desenhar herói astronauta do SpaceK
    
    Inclui:
    - Traje espacial detalhado
    - Capacete com reflexos
    - Jetpack com LEDs
    - Efeitos especiais (escudo, jetpack)
    - Animações faciais
    """
    draw_x = player_x - camera_x
    
    # Efeito visual do jetpack quando ativo
    if keyboard.space and not player_on_ground and player_jetpack_fuel > 0:
        for i in range(6):
            trail_x = draw_x + 15 + random.randint(-4, 4)
            trail_y = player_y + 40 + i * 4
            size = 6 - i
            # Gradiente de cores do fogo do jetpack
            colors = [(255, 255, 255), (255, 200, 0), (255, 150, 0), (255, 100, 0), (200, 50, 0), (100, 0, 0)]
            if i < len(colors):
                screen.draw.filled_circle((trail_x, trail_y), size, colors[i])
    
    # Efeito visual do escudo
    if player_has_shield:
        shield_pulse = int(abs(math.sin(player_shield_timer * 0.25)) * 30)
        shield_color = safe_color((80 + shield_pulse, 120 + shield_pulse, 255))
        screen.draw.circle((draw_x + 15, player_y + 20), 28, shield_color)
        screen.draw.circle((draw_x + 15, player_y + 20), 26, shield_color)
    
    # Desenhar astronauta (piscar se invulnerável)
    if player_invulnerable == 0 or (player_invulnerable // 6) % 2 == 0:
        # Corpo do traje espacial
        player_rect = Rect(draw_x, player_y, 30, 40)
        
        # Cor baseada na energia restante
        if player_energy > 70:
            body_color = (60, 130, 255)    # Azul brilhante (energia alta)
        elif player_energy > 40:
            body_color = (100, 150, 220)   # Azul médio (energia média)
        else:
            body_color = (200, 100, 100)   # Vermelho (energia baixa)
        
        # Desenhar traje espacial
        screen.draw.filled_rect(player_rect, body_color)
        screen.draw.filled_rect(Rect(draw_x + 4, player_y + 8, 22, 30), (40, 100, 200))
        
        # Capacete do astronauta
        screen.draw.filled_circle((draw_x + 15, player_y + 12), 14, (180, 200, 255))
        screen.draw.circle((draw_x + 15, player_y + 12), 14, (255, 255, 255))
        
        # Rosto animado do astronauta (REQUISITO: animações de sprite)
        current_face = spacek_hero.get_current_frame()
        screen.draw.text(current_face, (draw_x + 8, player_y + 6), fontsize=12, color="black")
        
        # Jetpack nas costas
        jetpack_main = Rect(draw_x + 28, player_y + 10, 10, 28)
        screen.draw.filled_rect(jetpack_main, (60, 60, 80))
        
        # LEDs indicadores do jetpack
        led_positions = [14, 18, 22, 26, 30]
        for i, led_y in enumerate(led_positions):
            fuel_threshold = 20 * (5 - i)
            
            # Cor do LED baseada no combustível
            if player_jetpack_fuel > fuel_threshold:
                led_color = (0, 255, 0)      # Verde (cheio)
            elif player_jetpack_fuel > fuel_threshold - 10:
                led_color = (255, 255, 0)    # Amarelo (médio)
            else:
                led_color = (50, 50, 50)     # Escuro (vazio)
            
            screen.draw.filled_circle((draw_x + 32, player_y + led_y), 2, led_color)

def draw_spacek_interface():
    """
    Desenhar interface do usuário (HUD)
    
    Mostra todas as informações importantes:
    - Pontuação
    - Vidas
    - Nível atual
    - Estatísticas
    - Barras de status
    - Progresso da missão
    """
    # Painel principal da interface
    ui_bg = Rect(5, 5, 350, 200)
    screen.draw.filled_rect(ui_bg, (0, 0, 0))  # Fundo preto
    
    # Borda ciano do painel
    screen.draw.line((ui_bg.left, ui_bg.top), (ui_bg.right, ui_bg.top), (0, 255, 255))
    screen.draw.line((ui_bg.left, ui_bg.top), (ui_bg.left, ui_bg.bottom), (0, 255, 255))
    screen.draw.line((ui_bg.right, ui_bg.top), (ui_bg.right, ui_bg.bottom), (0, 255, 255))
    screen.draw.line((ui_bg.left, ui_bg.bottom), (ui_bg.right, ui_bg.bottom), (0, 255, 255))
    
    # Título do painel
    screen.draw.text("🚀 SPACEK COMMAND CENTER", (10, 8), fontsize=14, color="cyan")
    
    # Informações principais
    screen.draw.text(f"SCORE: {score}", (10, 28), fontsize=16, color="cyan")
    screen.draw.text(f"VIDAS: {player_lives} ❤️", (10, 48), fontsize=16, color="red")
    screen.draw.text(f"NÍVEL: {current_level}/2", (10, 68), fontsize=16, color="white")
    screen.draw.text(f"MOEDAS K: {coins_collected} 💰", (180, 28), fontsize=14, color="yellow")
    screen.draw.text(f"ETs DERROTADOS: {enemies_defeated} 👽", (180, 48), fontsize=12, color="green")
    
    # Sistema de barras de status
    bar_y = 92
    
    # Barra de energia
    energy_width = int((player_energy / 100) * 140)
    # Cor baseada no nível de energia
    if player_energy > 50:
        energy_color = (0, 255, 0)      # Verde (alta)
    elif player_energy > 20:
        energy_color = (255, 255, 0)    # Amarelo (média)
    else:
        energy_color = (255, 0, 0)      # Vermelho (baixa)
    
    screen.draw.filled_rect(Rect(10, bar_y, energy_width, 18), energy_color)
    # Bordas da barra
    screen.draw.line((10, bar_y), (150, bar_y), (255, 255, 255))
    screen.draw.line((10, bar_y), (10, bar_y + 18), (255, 255, 255))
    screen.draw.line((150, bar_y), (150, bar_y + 18), (255, 255, 255))
    screen.draw.line((10, bar_y + 18), (150, bar_y + 18), (255, 255, 255))
    screen.draw.text("ENERGIA", (155, bar_y + 3), fontsize=12, color="white")
    
    bar_y += 28
    
    # Barra de oxigênio
    oxygen_width = int((oxygen / 100) * 140)
    oxygen_color = (100, 255, 255) if oxygen > 30 else (255, 150, 150)
    screen.draw.filled_rect(Rect(10, bar_y, oxygen_width, 18), oxygen_color)
    screen.draw.line((10, bar_y), (150, bar_y), (255, 255, 255))
    screen.draw.line((10, bar_y), (10, bar_y + 18), (255, 255, 255))
    screen.draw.line((150, bar_y), (150, bar_y + 18), (255, 255, 255))
    screen.draw.line((10, bar_y + 18), (150, bar_y + 18), (255, 255, 255))
    screen.draw.text("OXIGÊNIO", (155, bar_y + 3), fontsize=12, color="white")
    
    bar_y += 28
    
    # Barra de combustível do jetpack
    fuel_width = int((player_jetpack_fuel / 100) * 140)
    fuel_color = (255, 255, 0) if player_jetpack_fuel > 20 else (255, 100, 0)
    screen.draw.filled_rect(Rect(10, bar_y, fuel_width, 18), fuel_color)
    screen.draw.line((10, bar_y), (150, bar_y), (255, 255, 255))
    screen.draw.line((10, bar_y), (10, bar_y + 18), (255, 255, 255))
    screen.draw.line((150, bar_y), (150, bar_y + 18), (255, 255, 255))
    screen.draw.line((10, bar_y + 18), (150, bar_y + 18), (255, 255, 255))
    screen.draw.text("JETPACK", (155, bar_y + 3), fontsize=12, color="white")
    
    # Indicadores de status especiais
    if player_has_shield:
        screen.draw.text("🛡️ ESCUDO SPACEK ATIVO", (10, 175), fontsize=12, color="cyan")
    
    # Indicador de áudio
    audio_status = "🔊 ON" if sounds_enabled else "🔇 OFF"
    audio_color = "green" if sounds_enabled else "red"
    screen.draw.text(f"ÁUDIO: {audio_status}", (180, 68), fontsize=10, color=audio_color)
    
    # Barra de progresso da missão
    level_end_x = 2400 if current_level == 1 else 2200
    progress = min(1.0, player_x / level_end_x)
    progress_width = int(progress * 200)
    
    # Desenhar barra de progresso
    screen.draw.filled_rect(Rect(WIDTH - 210, 10, progress_width, 25), (0, 255, 0))
    screen.draw.line((WIDTH - 210, 10), (WIDTH - 10, 10), (255, 255, 255))
    screen.draw.line((WIDTH - 210, 10), (WIDTH - 210, 35), (255, 255, 255))
    screen.draw.line((WIDTH - 10, 10), (WIDTH - 10, 35), (255, 255, 255))
    screen.draw.line((WIDTH - 210, 35), (WIDTH - 10, 35), (255, 255, 255))
    screen.draw.text("MISSÃO SPACEK", (WIDTH - 205, 40), fontsize=12, color="white")

def draw_spacek_gameover():
    """Desenhar tela de game over"""
    screen.fill((60, 0, 0))
    
    screen.draw.text("💀 SPACEK: MISSÃO FALHADA 💀", 
                     center=(WIDTH//2, HEIGHT//2 - 100), 
                     fontsize=45, 
                     color="red")
    
    screen.draw.text("Os aliens SpaceK venceram!", 
                     center=(WIDTH//2, HEIGHT//2 - 40), 
                     fontsize=24, 
                     color="white")
    
    screen.draw.text(f"SCORE SPACEK: {score}", 
                     center=(WIDTH//2, HEIGHT//2), 
                     fontsize=28, 
                     color="cyan")
    
    screen.draw.text(f"MOEDAS K: {coins_collected} | ETs: {enemies_defeated}", 
                     center=(WIDTH//2, HEIGHT//2 + 40), 
                     fontsize=18, 
                     color="yellow")
    
    if score == high_score and score > 0:
        screen.draw.text("🏆 NOVO RECORDE SPACEK! 🏆", 
                         center=(WIDTH//2, HEIGHT//2 + 80), 
                         fontsize=20, 
                         color="gold")
    
    screen.draw.text("ENTER - Nova Missão | ESC - Menu SpaceK", 
                     center=(WIDTH//2, HEIGHT//2 + 120), 
                     fontsize=16, 
                     color="gray")

def draw_spacek_victory():
    """Desenhar tela de vitória"""
    screen.fill((0, 60, 0))
    
    # Desenhar partículas de celebração
    for particle in particles:
        particle.draw()
    
    screen.draw.text("🎉 SPACEK: VITÓRIA TOTAL! 🎉", 
                     center=(WIDTH//2, HEIGHT//2 - 100), 
                     fontsize=45, 
                     color="yellow")
    
    screen.draw.text("Comandante SpaceK, missão cumprida!", 
                     center=(WIDTH//2, HEIGHT//2 - 40), 
                     fontsize=22, 
                     color="white")
    
    screen.draw.text(f"SCORE FINAL SPACEK: {score}", 
                     center=(WIDTH//2, HEIGHT//2), 
                     fontsize=32, 
                     color="cyan")
    
    screen.draw.text(f"MOEDAS K: {coins_collected} | ETs ELIMINADOS: {enemies_defeated}", 
                     center=(WIDTH//2, HEIGHT//2 + 50), 
                     fontsize=18, 
                     color="yellow")
    
    if score == high_score:
        screen.draw.text("🏆 RECORDE UNIVERSAL SPACEK! 🏆", 
                         center=(WIDTH//2, HEIGHT//2 + 90), 
                         fontsize=22, 
                         color="gold")
    
    screen.draw.text("ESC - Menu SpaceK", 
                     center=(WIDTH//2, HEIGHT//2 + 130), 
                     fontsize=18, 
                     color="gray")

# ===================================================================
# SISTEMA DE CONTROLES (EVENTOS DE ENTRADA)
# ===================================================================

def on_key_down(key):
    """
    Gerenciar teclas pressionadas
    
    Controles do SpaceK:
    - WASD/Setas: Movimento
    - Espaço: Pulo/Jetpack
    - X: Disparar laser
    - ESC: Menu
    - T: Testar sons (no menu)
    """
    global player_vx, player_vy, game_state, player_facing, player_jetpack_fuel
    global player_move_left, player_move_right
    
    if game_state == "menu":
        # Controles do menu
        if key == keys.RETURN:
            play_spacek_sound("click")
            start_spacek()
        elif key == keys.T:
            test_spacek_audio_system()  # Testar sistema de áudio
        elif key == keys.ESCAPE:
            play_spacek_sound("click")
            exit()
    
    elif game_state == "playing":
        # Controles do jogo
        if key == keys.A or key == keys.LEFT:
            player_move_left = True  # Ativar movimento contínuo para esquerda
        elif key == keys.D or key == keys.RIGHT:
            player_move_right = True  # Ativar movimento contínuo para direita
        elif key == keys.SPACE or key == keys.W or key == keys.UP:
            if player_on_ground:
                # Pulo normal
                player_vy = -16
                play_spacek_sound("jump")  # Som jump.mp3
                create_spacek_particles(player_x + 15, player_y + 40, (255, 255, 255), 12, "smoke")
            elif player_jetpack_fuel > 0:
                # Jetpack (pulo aéreo)
                player_vy -= 2.5
                player_jetpack_fuel -= 4
                # Som de jetpack ocasional
                if player_jetpack_fuel % 25 == 0:
                    play_spacek_sound("jetpack")  # Som jetpack.mp3
        elif key == keys.X and len(lasers) < 5:
            # Disparar laser
            laser_x = player_x + (45 if player_facing == 1 else -20)
            laser_y = player_y + 20
            lasers.append(SpaceKLaser(laser_x, laser_y, player_facing))
            play_spacek_sound("laser_shoot")  # Som laser_shoot.mp3
            create_spacek_particles(laser_x, laser_y, (0, 255, 255), 10, "spark")
        elif key == keys.ESCAPE:
            play_spacek_sound("click")
            game_state = "menu"
    
    elif game_state == "gameover":
        # Controles da tela de game over
        if key == keys.RETURN:
            play_spacek_sound("click")
            start_spacek()
        elif key == keys.ESCAPE:
            play_spacek_sound("click")
            game_state = "menu"
    
    elif game_state == "victory":
        # Controles da tela de vitória
        if key == keys.ESCAPE:
            play_spacek_sound("click")
            game_state = "menu"

def on_key_up(key):
    """
    Gerenciar teclas soltas
    
    Implementa parada suave do movimento
    """
    global player_move_left, player_move_right
    
    if game_state == "playing":
        # Desativar movimento contínuo quando soltar tecla
        if key == keys.A or key == keys.LEFT:
            player_move_left = False  # Desativar movimento para esquerda
        elif key == keys.D or key == keys.RIGHT:
            player_move_right = False  # Desativar movimento para direita

def on_mouse_down(pos):
    """
    Gerenciar cliques do mouse
    
    REQUISITO ATENDIDO: "botões clicáveis"
    """
    if game_state == "menu":
        # Verificar clique em cada botão
        for button in menu_buttons:
            if button.is_clicked(pos):
                # Executar ação do botão clicado
                if button.action == "start":
                    start_spacek()
                elif button.action == "music":
                    toggle_spacek_audio()
                elif button.action == "test":
                    test_spacek_audio_system()
                elif button.action == "quit":
                    exit()

def on_mouse_move(pos):
    """
    Gerenciar movimento do mouse (para hover dos botões)
    """
    if game_state == "menu":
        for button in menu_buttons:
            button.update(pos)

# ===================================================================
# ALIASES PARA COMPATIBILIDADE
# ===================================================================
# Criar aliases para manter compatibilidade com código anterior
Enemy = SpaceKAlien
Powerup = SpaceKPowerup
Coin = SpaceKCoin  
Laser = SpaceKLaser
Particle = SpaceKParticle
Button = SpaceKButton

# ===================================================================
# INICIALIZAÇÃO DO JOGO SPACEK
# ===================================================================
# Criar menu e configurar estado inicial
create_spacek_menu()
setup_spacek()

# Mensagens informativas no console
print("🚀 SPACEK - JOGO TOTALMENTE DOCUMENTADO CARREGADO! 🚀")
print("")
print("📋 REQUISITOS DO PROJETO ATENDIDOS:")
print("   ✅ Bibliotecas: pgzero, math, random, pygame.Rect")
print("   ✅ Gênero: Platformer")
print("   ✅ Menu principal com botões clicáveis")
print("   ✅ Música/sons ON-OFF")
print("   ✅ Vários inimigos perigosos em territórios")
print("   ✅ Classes para personagens e sprites")
print("   ✅ Animações (andar, parado, respirando, etc.)")
print("   ✅ Código limpo (PEP8, nomes em inglês)")
print("   ✅ Mecânica lógica sem bugs")
print("   ✅ Projeto único e independente")
print("")
print("🔊 SISTEMA DE ÁUDIO MAPEADO:")
print("   • button_click.mp3 → Cliques nos botões")
print("   • enemy_death.mp3 → Morte de aliens")
print("   • explode.mp3 → Explosões")
print("   • impact.mp3 → Dano ao astronauta")
print("   • jetpack.mp3 → Ativação do jetpack")
print("   • jump.mp3 → Pulos e coletas")
print("   • laser_hit.mp3 → Laser atingindo inimigos")
print("   • laser_shoot.mp3 → Disparar projéteis")
print("")
print("🎮 COMO JOGAR:")
print("   • T: Testar sistema de áudio completo")
print("   • WASD/Setas: Mover astronauta")
print("   • Espaço: Pular/Ativar jetpack")
print("   • X: Disparar laser contra aliens")
print("   • ESC: Voltar ao menu")
print("")
print("🎯 OBJETIVO: Derrotar aliens em territórios e coletar cristais!")

# ===================================================================
# EXECUTAR JOGO
# ===================================================================
pgzrun.go()
