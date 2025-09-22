import pgzrun
import math
import random
from pygame import Rect
import pygame.mixer

# ===================================================================
# MINI SPACEK - JOGO DE PLATAFORMA ESPACIAL SIMPLIFICADO
# ===================================================================
# Versão reduzida do SpaceK, focada na mecânica essencial.
# Máximo de 500 linhas.
# ===================================================================

# Configuração da tela
WIDTH = 800
HEIGHT = 600

# Variáveis do jogo
game_state = "menu"
sounds_enabled = True
score = 0
high_score = 0

# Variáveis do jogador
player_x = 100
player_y = 500
player_vx = 0
player_vy = 0
player_on_ground = False
player_lives = 3
player_facing = 1
player_invulnerable = 0
player_move_left = False
player_move_right = False

# Listas de elementos
platforms = []
enemies = []
lasers = []
particles = []
stars = []
coins = []
menu_buttons = []

# ===================================================================
# SISTEMA DE ÁUDIO SIMPLIFICADO
# ===================================================================
pygame.mixer.init()
loaded_sounds = {}
sound_files = {
    "jump": "sounds/jump.mp3",
    "click": "sounds/button_click.mp3",
    "explosion": "sounds/explode.mp3",
    "hurt": "sounds/impact.mp3",
    "laser_shoot": "sounds/laser_shoot.mp3",
    "laser_hit": "sounds/laser_hit.mp3",
    "collect": "sounds/jump.mp3"
}
for key, path in sound_files.items():
    try:
        loaded_sounds[key] = pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Erro ao carregar som {path}: {e}")

def play_spacek_sound(sound_type):
    if sounds_enabled and sound_type in loaded_sounds:
        loaded_sounds[sound_type].play()

def safe_color(color):
    return tuple(max(0, min(255, int(c))) for c in color)

# ===================================================================
# CLASSES SIMPLIFICADAS
# ===================================================================

class SpaceKButton:
    def __init__(self, x, y, w, h, text, action, color=(100, 100, 200)):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.color = color
        self.hovered = False
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    def draw(self):
        color = safe_color((self.color[0] + 60, self.color[1] + 60, self.color[2] + 60)) if self.hovered else self.color
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=16, color="white")
    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            play_spacek_sound("click")
            return True
        return False

class SpaceKAlien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.vx = random.choice([-2, 2])
        self.vy = 0
        self.health = 1
        self.alive = True
        self.facing = 1 if self.vx > 0 else -1
        self.start_x = x
        self.territory_size = 80
    def update(self, platforms):
        if not self.alive: return
        self.vy += 0.5
        alien_rect = Rect(self.x, self.y, self.width, self.height)
        for plat in platforms:
            if alien_rect.colliderect(plat) and self.vy > 0:
                self.y = plat.top - self.height
                self.vy = 0
        if abs(self.x - self.start_x) > self.territory_size:
            self.vx *= -1
        self.x += self.vx
        self.y += self.vy
        self.facing = 1 if self.vx > 0 else -1
    def take_damage(self):
        global score
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            play_spacek_sound("explosion")
            create_spacek_particles(self.x + self.width//2, self.y + self.height//2, (255, 100, 100), 10)
            score += 100
        else:
            play_spacek_sound("hurt")
            create_spacek_particles(self.x + self.width//2, self.y + self.height//2, (255, 255, 0), 5)
            score += 20
    def draw(self):
        draw_x = self.x - camera_x
        if -50 < draw_x < WIDTH + 50:
            screen.draw.filled_rect(Rect(draw_x, self.y, self.width, self.height), (255, 100, 100))
            screen.draw.filled_circle((draw_x + self.width//2, self.y + 10), 10, (255, 255, 0)) # Olho

class SpaceKCoin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.collected = False
        self.rotation = 0
        self.original_y = y
    def update(self):
        if not self.collected:
            self.rotation += 8
            self.y = self.original_y + math.sin(self.rotation * 0.05) * 6
    def draw(self):
        if not self.collected:
            draw_x = self.x - camera_x
            if -25 < draw_x < WIDTH + 25:
                scale = abs(math.cos(self.rotation * 0.08))
                width = max(4, int(16 * scale))
                screen.draw.filled_rect(Rect(draw_x + 8 - width//2, self.y + 4, width, 8), (255, 215, 0))
                if width > 8:
                    screen.draw.text("K", (draw_x + 6, self.y + 2), fontsize=14, color="orange")

class SpaceKLaser:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 18
        self.width = 14
        self.height = 6
        self.alive = True
    def update(self):
        self.x += self.speed * self.direction
        if self.x < camera_x - 150 or self.x > camera_x + WIDTH + 150:
            self.alive = False
    def draw(self):
        if self.alive:
            draw_x = self.x - camera_x
            screen.draw.filled_rect(Rect(draw_x, self.y, self.width, self.height), (0, 255, 255))

class SpaceKParticle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = safe_color(color)
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 7)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.lifetime -= 1
        alpha = max(0, self.lifetime / self.max_lifetime)
        self.size = max(1, int(7 * alpha))
    def draw(self):
        if self.lifetime > 0:
            draw_x = self.x - camera_x
            final_color = safe_color((self.color[0] * alpha, self.color[1] * alpha, self.color[2] * alpha))
            screen.draw.filled_circle((int(draw_x), int(self.y)), self.size, final_color)

# ===================================================================
# FUNÇÕES AUXILIARES
# ===================================================================

def create_spacek_particles(x, y, color, count=8):
    for _ in range(count):
        velocity = (random.uniform(-6, 6), random.uniform(-8, -3))
        particles.append(SpaceKParticle(x, y, safe_color(color), velocity, random.randint(50, 100)))

def create_spacek_menu():
    global menu_buttons
    menu_buttons = [
        SpaceKButton(WIDTH//2 - 100, 250, 200, 50, "INICIAR", "start"),
        SpaceKButton(WIDTH//2 - 100, 320, 200, 50, f"ÁUDIO: {'ON' if sounds_enabled else 'OFF'}", "audio"),
        SpaceKButton(WIDTH//2 - 100, 390, 200, 50, "SAIR", "quit")
    ]

def setup_spacek():
    global platforms, enemies, coins, stars
    global player_x, player_y, player_vx, player_vy, player_lives, score
    global camera_x, player_invulnerable, player_move_left, player_move_right

    player_x, player_y = 100, 500
    player_vx, player_vy = 0, 0
    player_lives = 3
    score = 0
    camera_x = 0
    player_invulnerable = 0
    player_move_left, player_move_right = False, False

    platforms.clear()
    enemies.clear()
    coins.clear()
    stars.clear()

    platforms.extend([
        Rect(0, 540, WIDTH * 2, 60),
        Rect(200, 450, 120, 20),
        Rect(400, 400, 140, 20),
        Rect(600, 350, 120, 20),
        Rect(800, 380, 160, 20),
        Rect(1000, 320, 120, 20)
    ])
    enemies.extend([
        SpaceKAlien(250, 430),
        SpaceKAlien(450, 380),
        SpaceKAlien(850, 360)
    ])
    coins.extend([
        SpaceKCoin(280, 410),
        SpaceKCoin(520, 300),
        SpaceKCoin(920, 340)
    ])
    for _ in range(60):
        stars.append({'x': random.randint(0, WIDTH * 2), 'y': random.randint(0, HEIGHT), 'size': random.randint(1, 3)})

def take_spacek_damage():
    global player_lives, player_invulnerable, player_x, player_y, player_vx, player_vy
    if player_invulnerable > 0: return
    player_lives -= 1
    player_invulnerable = 120 # 2 segundos
    play_spacek_sound("hurt")
    create_spacek_particles(player_x + 15, player_y + 20, (255, 100, 100), 15)
    if player_lives > 0:
        player_x = max(100, camera_x + 100)
        player_y = 500
        player_vx, player_vy = 0, 0

def start_spacek():
    global game_state
    game_state = "playing"
    setup_spacek()

def toggle_spacek_audio():
    global sounds_enabled
    sounds_enabled = not sounds_enabled
    menu_buttons[1].text = f"ÁUDIO: {'ON' if sounds_enabled else 'OFF'}"
    if sounds_enabled: play_spacek_sound("click")

# ===================================================================
# FUNÇÕES PRINCIPAIS DO JOGO
# ===================================================================

def update():
    global player_x, player_y, player_vx, player_vy, player_on_ground, player_invulnerable
    global game_state, camera_x, score, high_score

    if game_state == "menu":
        for star in stars: star['x'] -= 0.5; star['x'] = star['x'] % (WIDTH * 2)
        return
    if game_state != "playing": return

    # Movimento do jogador
    if player_move_left: player_vx = -6
    elif player_move_right: player_vx = 6
    else: player_vx *= 0.85 # Atrito

    if not player_on_ground: player_vy += 0.6
    if player_vy > 15: player_vy = 15

    old_player_x = player_x
    player_x += player_vx
    player_y += player_vy

    if player_x < 0: player_x = 0

    # Colisão com plataformas
    player_on_ground = False
    player_rect = Rect(player_x, player_y, 30, 40)
    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_vy > 0 and old_player_x + 15 > plat.left and old_player_x + 15 < plat.right:
                player_y = plat.top - 40
                player_vy = 0
                player_on_ground = True
                break

    # Câmera
    target_camera = max(0, player_x - WIDTH // 2.5)
    camera_x += (target_camera - camera_x) * 0.05

    # Atualizar elementos
    for enemy in enemies: enemy.update(platforms)
    for coin in coins: coin.update()
    for laser in lasers[:]:
        laser.update()
        if not laser.alive: lasers.remove(laser)
        else:
            laser_rect = Rect(laser.x, laser.y, laser.width, laser.height)
            for enemy in enemies:
                if enemy.alive and laser_rect.colliderect(Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                    play_spacek_sound("laser_hit")
                    enemy.take_damage()
                    laser.alive = False
                    break
    for particle in particles[:]:
        particle.update()
        if particle.lifetime <= 0: particles.remove(particle)

    # Colisão jogador-inimigo
    if player_invulnerable <= 0:
        for enemy in enemies:
            if enemy.alive and player_rect.colliderect(Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                take_spacek_damage()
                break
    else: player_invulnerable -= 1

    # Coleta de moedas
    for coin in coins:
        if not coin.collected and player_rect.colliderect(Rect(coin.x, coin.y, coin.width, coin.height)):
            coin.collected = True
            score += 50
            play_spacek_sound("collect")
            create_spacek_particles(coin.x + 8, coin.y + 8, (255, 215, 0), 10)

    # Queda
    if player_y > HEIGHT + 100: take_spacek_damage()

    # Fim do nível (simplificado)
    if player_x > 1100: # Perto do final do mundo
        game_state = "victory"
        if score > high_score: high_score = score

    if player_lives <= 0:
        game_state = "gameover"
        if score > high_score: high_score = score

def draw():
    screen.clear()
    if game_state == "menu": draw_spacek_menu()
    elif game_state == "playing": draw_spacek_game()
    elif game_state == "gameover": draw_spacek_gameover()
    elif game_state == "victory": draw_spacek_victory()

def draw_spacek_menu():
    screen.fill((1, 1, 25))
    for star in stars: screen.draw.filled_circle((int(star['x']), int(star['y'])), star['size'], (255, 255, 255))
    screen.draw.text("MINI SPACEK", center=(WIDTH//2, 100), fontsize=60, color="cyan")
    screen.draw.text("Derrote os aliens!", center=(WIDTH//2, 160), fontsize=24, color="white")
    if high_score > 0: screen.draw.text(f"RECORDE: {high_score}", center=(WIDTH//2, 200), fontsize=18, color="gold")
    for button in menu_buttons: button.draw()

def draw_spacek_game():
    screen.fill((3, 3, 45))
    for star in stars: screen.draw.filled_circle((int(star['x'] - camera_x * 0.1), int(star['y'])), star['size'], (255, 255, 255))
    for plat in platforms:
        draw_x = plat.x - camera_x
        if draw_x + plat.width > -50 and draw_x < WIDTH + 50:
            screen.draw.filled_rect(Rect(draw_x, plat.y, plat.width, plat.height), (70, 90, 130))
    for coin in coins: coin.draw()
    for enemy in enemies: enemy.draw()
    for laser in lasers: laser.draw()
    for particle in particles: particle.draw()

    # Desenhar jogador
    draw_x = player_x - camera_x
    if player_invulnerable == 0 or (player_invulnerable // 6) % 2 == 0:
        screen.draw.filled_rect(Rect(draw_x, player_y, 30, 40), (60, 130, 255))
        screen.draw.filled_circle((draw_x + 15, player_y + 12), 14, (180, 200, 255)) # Capacete
        screen.draw.text("^_^", (draw_x + 8, player_y + 6), fontsize=12, color="black") # Rosto

    # HUD
    screen.draw.text(f"SCORE: {score}", (10, 10), fontsize=20, color="cyan")
    screen.draw.text(f"VIDAS: {player_lives} ❤️", (10, 40), fontsize=20, color="red")

def draw_spacek_gameover():
    screen.fill((60, 0, 0))
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color="red")
    screen.draw.text(f"SCORE: {score}", center=(WIDTH//2, HEIGHT//2 + 10), fontsize=30, color="white")
    if score == high_score and score > 0: screen.draw.text("NOVO RECORDE!", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=20, color="gold")
    screen.draw.text("ENTER - REINICIAR | ESC - MENU", center=(WIDTH//2, HEIGHT//2 + 100), fontsize=16, color="gray")

def draw_spacek_victory():
    screen.fill((0, 60, 0))
    screen.draw.text("VITÓRIA!", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color="yellow")
    screen.draw.text(f"SCORE FINAL: {score}", center=(WIDTH//2, HEIGHT//2 + 10), fontsize=30, color="white")
    if score == high_score: screen.draw.text("RECORDE!", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=20, color="gold")
    screen.draw.text("ESC - MENU", center=(WIDTH//2, HEIGHT//2 + 100), fontsize=16, color="gray")

# ===================================================================
# CONTROLES
# ===================================================================

def on_key_down(key):
    global player_vy, game_state, player_facing, player_move_left, player_move_right
    if game_state == "menu":
        if key == keys.RETURN: start_spacek()
        elif key == keys.AUDIO: toggle_spacek_audio() # Usar keys.AUDIO para o toggle
        elif key == keys.ESCAPE: exit()
    elif game_state == "playing":
        if key == keys.A or key == keys.LEFT: player_move_left = True; player_facing = -1
        elif key == keys.D or key == keys.RIGHT: player_move_right = True; player_facing = 1
        elif key == keys.SPACE or key == keys.W or key == keys.UP:
            if player_on_ground:
                player_vy = -12 # Pulo mais baixo
                play_spacek_sound("jump")
        elif key == keys.X and len(lasers) < 3: # Menos lasers na tela
            lasers.append(SpaceKLaser(player_x + (45 if player_facing == 1 else -20), player_y + 20, player_facing))
            play_spacek_sound("laser_shoot")
        elif key == keys.ESCAPE: game_state = "menu"
    elif game_state == "gameover":
        if key == keys.RETURN: start_spacek()
        elif key == keys.ESCAPE: game_state = "menu"
    elif game_state == "victory":
        if key == keys.ESCAPE: game_state = "menu"

def on_key_up(key):
    global player_move_left, player_move_right
    if game_state == "playing":
        if key == keys.A or key == keys.LEFT: player_move_left = False
        elif key == keys.D or key == keys.RIGHT: player_move_right = False

def on_mouse_down(pos):
    if game_state == "menu":
        for button in menu_buttons:
            if button.is_clicked(pos):
                if button.action == "start": start_spacek()
                elif button.action == "audio": toggle_spacek_audio()
                elif button.action == "quit": exit()

def on_mouse_move(pos):
    if game_state == "menu":
        for button in menu_buttons: button.update(pos)

# Inicialização
create_spacek_menu()
setup_spacek()

pgzrun.go()
