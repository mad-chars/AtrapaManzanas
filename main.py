import pygame
import random
import math

# --------------------------
# Configuración inicial
# --------------------------
pygame.init()
ANCHO, ALTO = 900, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa Manzanas 🍎 - ISB Prepa Área I")

clock = pygame.time.Clock()
FPS = 60

# Colores
BG_CLARO = (240, 244, 248)
NEGRO = (20, 20, 20)
ROJO = (220, 60, 60)
AZUL = (60, 120, 220)
BLANCO = (255, 255, 255)

# Fuentes
font_h1 = pygame.font.Font(None, 64)
font_p = pygame.font.Font(None, 36)

# Jugador (cuadrado)
J_SIZE = 50
VEL = 8
jugador = pygame.Rect(ANCHO //2 - J_SIZE // 2, ALTO - 120, J_SIZE, J_SIZE)

# Manzana (círculo)
R = 18 # Radio

def pos_manzana_alaeatoria():
    #Evitar aparecer encimada en los bordes
    x = random.randint(R + 20, ANCHO - (R + 20))
    y = random.randint(R + 80, ALTO - (R + 20))
    return x, y

manzana_x, manzana_y = pos_manzana_alaeatoria()

# Puntaje y estado de juego 
puntaje = 0 
META = 15
ganaste = False

pygame.mixer.init()
snd_eat = pygame.mixer.Sound("eat.wav")
snd_eat.set_volume(0.6)

# Música de fondo 
pygame.mixer.music.load("fondo.wav")
pygame.mixer.music.set_volume(0.3)           
pygame.mixer.music.play(-1)
    
def comer_manzana():
    snd_eat.play()
    pass

def clamp_jugador(rect):
    if rect.left < 0: rect.left = 0
    if rect.right > ANCHO: rect.right = ANCHO
    if rect.top < 0: rect.top = 0
    if rect.bottom > ALTO: rect.bottom = ALTO
    
def hay_colision_cuadro_circulo(rect, cx, cy, r):
    px = max(rect.left, min(cx, rect.right))
    py = max(rect.top, min(cy, rect.bottom))
    dx = cx - px
    dy = cy - py
    return (dx * dx + dy * dy) <= (r * r)

def dibujar_hud():
    barra = pygame.Rect(0, 0, ANCHO, 64)
    pygame.draw.rect(PANTALLA, BLANCO, barra)
    pygame.draw.line(PANTALLA, (220, 220, 200), (0, 64), (ANCHO, 64), 2)
    t1 = font_p.render(f"Puntaje: {puntaje}/{META}", True, NEGRO)
    PANTALLA.blit(t1, (20, 20))
    t2 = font_p.render("Flechas: mover | R: reiniciar | Esc: salir", True, (80, 80, 80))
    PANTALLA.blit(t2, (ANCHO - t2.get_width() - 20, 20))
    
def dibujar_escena():
    PANTALLA.fill(BG_CLARO)
    
    # HUD
    dibujar_hud()
    
    # Jugador (cuadrado)
    pygame.draw.rect(PANTALLA, AZUL, jugador, border_radius=6)
    
    # Manzana (círculo rojo con brillo)
    pygame.draw.circle(PANTALLA, ROJO, (manzana_x, manzana_y), R)
    pygame.draw.circle(PANTALLA, (255,120, 120), (manzana_x - 5, manzana_y - 5), max(6, R // 3))
    
    if ganaste: 
        msg = font_h1.render("¡GG!", True, ROJO)
        sub = font_p.render("Pulsa R para jugar de nuevo o Esc para salir", True, NEGRO)
        PANTALLA.blit(msg, ((ANCHO - msg.get_width()) // 2, ALTO // 2 - 50))
        PANTALLA.blit(sub, ((ANCHO - sub.get_width()) // 2, ALTO // 2 + 50))
        
# ----------------------
# Loop principal
# ----------------------
ejecutando = True
while ejecutando:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            ejecutando = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                ejecutando = False
            if e.key == pygame.K_r:
                # Reiniciar
                puntaje = 0
                ganaste = False
                jugador.x = ANCHO // 2 - J_SIZE // 2
                jugador.y = ALTO - 120
                manzana_x, manzana_y = pos_manzana_alaeatoria()
                
    teclas = pygame.key.get_pressed()
    if not ganaste:
        if teclas[pygame.K_LEFT]:
            jugador.x -= VEL
        if teclas[pygame.K_RIGHT]:
            jugador.x += VEL
        if teclas[pygame.K_UP]:
            jugador.y -= VEL
        if teclas[pygame.K_DOWN]:
            jugador.y += VEL
            
        clamp_jugador(jugador)
        
        # Colisión con la manzana 
        if hay_colision_cuadro_circulo(jugador, manzana_x, manzana_y, R):
            puntaje += 1
            comer_manzana()
            if puntaje >= META:
                ganaste = True
            else: 
                manzana_x, manzana_y = pos_manzana_alaeatoria()
                
    # DIBUJO 
    dibujar_escena()
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()