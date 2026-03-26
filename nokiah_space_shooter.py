# Nokiah Space-Shooter [Game] (mobile-friendly)



import pygame, random, sys, os

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 750
GAME_HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nokiah Space-Shooter")

clock = pygame.time.Clock()

# Grid
GRID_SIZE = 50
COLS = WIDTH // GRID_SIZE

# Fonts
font = pygame.font.SysFont("arial", 26)
big_font = pygame.font.SysFont("arial", 45)

# High score file
HS_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HS_FILE):
        return int(open(HS_FILE).read())
    return 0

def save_high_score(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))

# Themes
THEMES = {
    "Dark": {"bg": (0,0,0), "player": (0,255,0), "enemy": (255,0,0), "bullet": (255,255,0), "button": (0,100,255)},
    "Neon": {"bg": (10,10,30), "player": (0,255,255), "enemy": (255,0,255), "bullet": (255,255,0), "button": (255,255,0)},
    "Retro": {"bg": (230,230,180), "player": (0,100,0), "enemy": (200,0,0), "bullet": (0,0,0), "button": (100,50,0)}
}

# Buttons
BTN_PLAY = pygame.Rect(200,300,200,60)
BTN_QUIT = pygame.Rect(200,400,200,60)
BTN_LEFT = pygame.Rect(100,650,100,60)
BTN_RIGHT = pygame.Rect(400,650,100,60)
BTN_FIRE = pygame.Rect(250,650,100,60)
BTN_RESTART = pygame.Rect(200,350,200,60)

# --- MENUS ---
def start_menu():
    while True:
        screen.fill((20,20,20))
        title = big_font.render("Nokiah Space-Shooter", True, (255,255,255))
        screen.blit(title, ((WIDTH-title.get_width())//2,150))

        pygame.draw.rect(screen,(0,200,0),BTN_PLAY)
        pygame.draw.rect(screen,(200,0,0),BTN_QUIT)

        screen.blit(font.render("PLAY",True,(0,0,0)),(270,315))
        screen.blit(font.render("QUIT",True,(0,0,0)),(270,415))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                if BTN_PLAY.collidepoint(e.pos): return
                if BTN_QUIT.collidepoint(e.pos): sys.exit()

def select_theme():
    while True:
        screen.fill((20,20,20))
        title = big_font.render("Nokiah Space-Shooter", True, (255,255,255))
        screen.blit(title, ((WIDTH-title.get_width())//2,80))

        screen.blit(big_font.render("Theme",True,(255,255,255)),(220,160))

        dark = pygame.Rect(100,300,120,60)
        neon = pygame.Rect(240,300,120,60)
        retro = pygame.Rect(380,300,120,60)

        pygame.draw.rect(screen,(50,50,50),dark)
        pygame.draw.rect(screen,(0,255,255),neon)
        pygame.draw.rect(screen,(255,128,0),retro)

        screen.blit(font.render("DARK",True,(255,255,255)),(120,315))
        screen.blit(font.render("NEON",True,(0,0,0)),(260,315))
        screen.blit(font.render("RETRO",True,(0,0,0)),(400,315))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                if dark.collidepoint(e.pos): return THEMES["Dark"]
                if neon.collidepoint(e.pos): return THEMES["Neon"]
                if retro.collidepoint(e.pos): return THEMES["Retro"]

def select_difficulty():
    while True:
        screen.fill((20,20,20))
        title = big_font.render("Nokiah Space-Shooter", True, (255,255,255))
        screen.blit(title, ((WIDTH-title.get_width())//2,80))

        screen.blit(big_font.render("Difficulty",True,(255,255,255)),(180,160))

        easy = pygame.Rect(200,300,200,60)
        medium = pygame.Rect(200,400,200,60)
        hard = pygame.Rect(200,500,200,60)

        pygame.draw.rect(screen,(0,255,0),easy)
        pygame.draw.rect(screen,(255,255,0),medium)
        pygame.draw.rect(screen,(255,0,0),hard)

        screen.blit(font.render("EASY",True,(0,0,0)),(260,315))
        screen.blit(font.render("MEDIUM",True,(0,0,0)),(240,415))
        screen.blit(font.render("HARD",True,(0,0,0)),(260,515))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                if easy.collidepoint(e.pos): return 40
                if medium.collidepoint(e.pos): return 25
                if hard.collidepoint(e.pos): return 12

# --- START FLOW ---
start_menu()
theme = select_theme()
base_delay = select_difficulty()

# Game variables
player_x = (WIDTH//2)//GRID_SIZE * GRID_SIZE
player_y = GAME_HEIGHT - GRID_SIZE
enemy_x = random.randint(0,COLS-1)*GRID_SIZE
enemy_y = 40

bullets = []
explosions = []
score = 0
level = 1
game_over = False
move_timer = 0

high_score = load_high_score()

# Explosion
def create_explosion(x,y):
    particles = []
    for _ in range(15):
        particles.append([x,y,random.randint(-5,5),random.randint(-5,5)])
    explosions.append({"p":particles,"t":10})

# Draw player
def draw_player(x,y):
    pygame.draw.polygon(screen, theme["player"], [
        (x+GRID_SIZE//2,y),
        (x,y+GRID_SIZE),
        (x+GRID_SIZE,y+GRID_SIZE)
    ])

# Draw enemy with wings
def draw_enemy(x,y):
    pygame.draw.polygon(screen, theme["enemy"], [
        (x+GRID_SIZE//2,y),
        (x,y+GRID_SIZE),
        (x+GRID_SIZE,y+GRID_SIZE)
    ])
    pygame.draw.polygon(screen, theme["enemy"], [(x-10,y+25),(x,y),(x,y+50)])
    pygame.draw.polygon(screen, theme["enemy"], [(x+60,y+25),(x+50,y),(x+50,y+50)])

# --- MAIN LOOP ---
while True:
    screen.fill(theme["bg"])

    # GAME BOX
    pygame.draw.rect(screen,(255,255,255),(0,40,WIDTH,GAME_HEIGHT),2)

    # UI (outside box)
    screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(20,10))
    screen.blit(font.render(f"High: {high_score}",True,(0,200,255)),(400,10))
    screen.blit(font.render(f"Level: {level}",True,(255,255,255)),(250,10))

    # Player
    draw_player(player_x, player_y)

    # Enemy
    if enemy_y >= 40:
        draw_enemy(enemy_x, enemy_y)

    # Bullets
    for b in bullets:
        pygame.draw.rect(screen, theme["bullet"], (b[0],b[1],6,20))

    # Explosions
    for exp in explosions[:]:
        for p in exp["p"]:
            pygame.draw.circle(screen, theme["bullet"], (p[0],p[1]), 3)
            p[0]+=p[2]; p[1]+=p[3]
        exp["t"]-=1
        if exp["t"]<=0:
            explosions.remove(exp)
            enemy_x = random.randint(0,COLS-1)*GRID_SIZE
            enemy_y = 40

    # Level system
    level = 1 + score//5
    move_delay = max(5, base_delay - level*2)

    # Movement
    move_timer+=1
    if move_timer>move_delay and not game_over:
        move_timer=0

        enemy_y += GRID_SIZE
        if enemy_y >= GAME_HEIGHT:
            game_over = True

        for b in bullets[:]:
            b[1]-=GRID_SIZE
            if b[1]<40: bullets.remove(b)

        for b in bullets[:]:
            if (b[0]//GRID_SIZE == enemy_x//GRID_SIZE and abs(b[1]-enemy_y)<GRID_SIZE):
                bullets.remove(b)
                score+=1
                if score>high_score:
                    high_score=score
                    save_high_score(score)
                create_explosion(enemy_x+25,enemy_y+25)
                enemy_y = -100
                break

    # Buttons
    pygame.draw.rect(screen, theme["button"], BTN_LEFT)
    pygame.draw.rect(screen, theme["button"], BTN_RIGHT)
    pygame.draw.rect(screen, theme["button"], BTN_FIRE)

    screen.blit(font.render("LEFT",True,(255,255,255)),(130,665))
    screen.blit(font.render("RIGHT",True,(255,255,255)),(425,665))
    screen.blit(font.render("FIRE",True,(255,255,255)),(280,665))

    # Game Over
    if game_over:
        screen.blit(big_font.render("GAME OVER",True,theme["enemy"]),(150,250))
        pygame.draw.rect(screen, theme["button"], BTN_RESTART)
        screen.blit(font.render("RESTART",True,(255,255,255)),(240,370))

    pygame.display.update()
    clock.tick(60)

    # Events
    for e in pygame.event.get():
        if e.type==pygame.QUIT: sys.exit()
        if e.type==pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if BTN_LEFT.collidepoint(e.pos): player_x-=GRID_SIZE
                if BTN_RIGHT.collidepoint(e.pos): player_x+=GRID_SIZE
                if BTN_FIRE.collidepoint(e.pos): bullets.append([player_x+25,player_y])
            else:
                if BTN_RESTART.collidepoint(e.pos):
                    player_x = (WIDTH//2)//GRID_SIZE*GRID_SIZE
                    enemy_x = random.randint(0,COLS-1)*GRID_SIZE
                    enemy_y = 40
                    bullets.clear()
                    score = 0
                    level = 1
                    game_over = False

    # Bounds
    player_x = max(0, min(WIDTH-GRID_SIZE, player_x))