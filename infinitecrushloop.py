import pygame
import time
import random
import sys
import math

# Inicializar pygame
pygame.init()

# Configuracion de la pantalla
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Codigo de Amor")

# Colores
BACKGROUND = (15, 15, 20)
WHITE = (255, 255, 255)
BLUE = (65, 105, 225)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
PINK = (219, 112, 147)
GRAY = (52, 73, 94)
ACCENT = (241, 196, 15)
HEART_COLOR = (255, 105, 180)

# Fuentes
title_font = pygame.font.SysFont('Arial', 42)
code_font = pygame.font.SysFont('Consolas', 24)
days_font = pygame.font.SysFont('Arial', 32)
button_font = pygame.font.SysFont('Arial', 28)

# Variables para la animacion
days = 0
max_days = 200  # Ajustado para que dure aproximadamente 13 segundos
code_written = ["def codigo_para_ella():"]
animation_started = False
hearts = []  # Para almacenar los corazones que flotan
thought_index = 0  # Para controlar qué pensamiento mostrar
thought_timer = 0  # Contador para controlar cuánto tiempo mostrar cada pensamiento
thought_change_rate = 25  # Cambiar pensamiento cada X frames (más alto = más lento)

thoughts = [
    # Pensamientos románticos
    "No puedo dejar de pensar en ella...",
    "Su sonrisa es como mi mejor codigo",
    "Quisiera ser tan valiente como para hablarle",
    "Me pregunto si le gustan los programadores",
    "Cada linea de codigo me recuerda a ella",
    "Si fuera una variable, seria mi constante",
    "Ella es como un bug en mi cerebro que no quiero arreglar",
    "Deberia invitarla a salir en vez de programar",
    "Su nombre seria el mejor nombre de variable",
    "Cuando la veo, mi sistema colapsa",
    "Es mas bonita que un codigo bien indentado",
    "Mi corazon hace print(te_amo) cada vez que la veo",
    "Si fuera CSS, seria mi !important",
    "Es como un bucle infinito en mi mente",
    "Quisiera escribirle, pero me da miedo que me deje en null",
    "Mi vida ejecutaba bien hasta que la conoci",
    "Seria capaz de programar mil dias solo por verla",
    "Es la excepcion que nunca quiero capturar",
    "Ella no sabe que existe en cada linea que escribo",
    "Si la vida fuera codigo, ella seria mi funcion principal",
    "Me pregunto si ella pensara en mi tambien",
    "Podria documentar cada detalle de su rostro",
    "Mi corazon hace commit cada vez que la recuerdo",
    "Ojala pudiera debuggear mis sentimientos",
    "Su recuerdo tiene mas prioridad que cualquier tarea",
    "Ella es mi error favorito",
    "Quisiera tener el valor de decirle lo que siento",
    "Si fuera un algoritmo, seria el mas complejo",
    "Me quede en un while(amor) sin break",
    "Su recuerdo nunca hace timeout",
    "Me gustaria ser su repositorio favorito",
    "Cada dia sin ella es como un codigo sin ejecutar",
    "Ella transforma mi mundo binario en algo magico",
    "No existe IDE que compile lo que siento por ella",
    "Podria refactorizar todo mi codigo pero no mis sentimientos",
    "Ella es mi unico pensamiento sin comentarios",
    "Ni Stack Overflow tiene respuesta para lo que siento",
    "Sueno con crear un futuro donde nuestro codigo se una",
    "Si la vida fuera un commit, ella seria mi mensaje",
    "Su voz es como el sonido de una compilacion exitosa",
]

# Clase para el corazón flotante
class Heart:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(HEIGHT + 10, HEIGHT + 100)
        self.speed = random.uniform(1.0, 3.0)
        self.size = random.randint(5, 15)
        self.alpha = random.randint(100, 200)
        self.wobble = random.uniform(0.5, 1.5)
        self.wobble_speed = random.uniform(0.05, 0.1)
        self.wobble_offset = random.uniform(0, 2 * math.pi)
        
    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.wobble_offset + time.time() * self.wobble_speed) * self.wobble
        if self.y < -20:
            self.y = random.randint(HEIGHT + 10, HEIGHT + 100)
            self.x = random.randint(50, WIDTH - 50)
            
    def draw(self):
        heart_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.polygon(heart_surface, (*HEART_COLOR, self.alpha), [
            (self.size, 0),
            (self.size * 0.5, self.size * 0.5),
            (0, 0),
            (0, self.size * 0.5),
            (self.size, self.size * 1.5),
            (self.size * 2, self.size * 0.5),
            (self.size * 2, 0),
            (self.size * 1.5, self.size * 0.5),
        ])
        screen.blit(heart_surface, (self.x - self.size, self.y - self.size))

# Clase para el boton
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self):
        pygame.draw.rect(screen, self.current_color, self.rect, 0, 10)
        text_surface = button_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False

# Crear el boton de inicio
start_button = Button(
    "COMENZAR", 
    WIDTH//2 - 100, 
    HEIGHT//2 + 50, 
    200, 
    60, 
    PINK, 
    (255, 150, 180), 
    WHITE
)

# Inicializar algunos corazones
for _ in range(15):
    hearts.append(Heart())

def draw_terminal_background():
    # Dibujar fondo tipo terminal
    terminal_rect = pygame.Rect(40, 220, WIDTH - 80, 280)  # Reducida altura para dejar espacio abajo
    pygame.draw.rect(screen, (30, 30, 35), terminal_rect, 0, 8)
    pygame.draw.rect(screen, (50, 50, 55), terminal_rect, 2, 8)
    
    # Dibujar los círculos de control de la ventana de terminal
    pygame.draw.circle(screen, RED, (60, 240), 8)
    pygame.draw.circle(screen, ACCENT, (85, 240), 8)
    pygame.draw.circle(screen, GREEN, (110, 240), 8)

def draw_welcome_screen():
    screen.fill(BACKGROUND)
    
    # Actualizar y dibujar corazones
    for heart in hearts:
        heart.update()
        heart.draw()
    
    # Título
    title = title_font.render("CÓDIGO PARA ELLA", True, PINK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    
    # Subtítulo
    subtitle = code_font.render("Una historia de amor y programacion", True, GRAY)
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 40))
    
    # Dibujar botón
    start_button.draw()
    
    pygame.display.flip()

def draw_animation_screen():
    global thought_timer, thought_index
    
    screen.fill(BACKGROUND)
    
    # Actualizar y dibujar corazones al fondo
    for heart in hearts:
        heart.update()
        heart.draw()
    
    # Dibujar título
    title = title_font.render("ESCRIBIRÉ UNA LÍNEA DE CÓDIGO", True, WHITE)
    subtitle = title_font.render("CADA VEZ QUE DEJE DE PENSAR EN ELLA", True, PINK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 110))
    
    # Dibujar contador de días
    days_text = days_font.render(f"Día {days}", True, RED)
    screen.blit(days_text, (WIDTH//2 - days_text.get_width()//2, 170))
    
    # Dibujar fondo tipo terminal
    draw_terminal_background()
    
    # Dibujar código
    for i, line in enumerate(code_written):
        code_line = code_font.render(line, True, GREEN)
        screen.blit(code_line, (70, 280 + i * 30))
    
    # Dibujar cursor parpadeante si solo hay una línea
    if len(code_written) == 1 and days % 10 < 5:
        cursor_pos = (70 + code_font.size(code_written[0])[0], 280)
        pygame.draw.rect(screen, GREEN, (cursor_pos[0], cursor_pos[1], 10, 24))
    
    # Actualizar pensamiento más lentamente
    thought_timer += 1
    if thought_timer >= thought_change_rate:
        thought_timer = 0
        thought_index = (thought_index + 1) % len(thoughts)
    
    # Dibujar pensamiento DEBAJO de la terminal
    if days > 0:
        thought = code_font.render(thoughts[thought_index], True, ACCENT)
        thought_bubble = pygame.Rect(WIDTH//2 - thought.get_width()//2 - 10, 520, thought.get_width() + 20, 40)
        pygame.draw.rect(screen, (40, 40, 45), thought_bubble, 0, 10)
        pygame.draw.rect(screen, (60, 60, 65), thought_bubble, 2, 10)
        screen.blit(thought, (WIDTH//2 - thought.get_width()//2, 530))
        
        # Dibujar un pequeño corazón junto al pensamiento
        heart_size = 8
        heart_pos = (WIDTH//2 - thought.get_width()//2 - 20, 530 + thought.get_height()//2)
        pygame.draw.polygon(screen, HEART_COLOR, [
            (heart_pos[0], heart_pos[1] - heart_size//2),
            (heart_pos[0] - heart_size//2, heart_pos[1]),
            (heart_pos[0] - heart_size, heart_pos[1] - heart_size//2),
            (heart_pos[0] - heart_size, heart_pos[1] - heart_size),
            (heart_pos[0], heart_pos[1] - heart_size//2 - heart_size),
            (heart_pos[0] + heart_size, heart_pos[1] - heart_size),
            (heart_pos[0] + heart_size, heart_pos[1] - heart_size//2),
            (heart_pos[0] + heart_size//2, heart_pos[1]),
        ])
    
    pygame.display.flip()

def handle_ending():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BACKGROUND)
    
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        draw_animation_screen()
        screen.blit(fade_surface, (0, 0))
        
        ending_text = title_font.render("Nunca pudo escribir la segunda línea...", True, WHITE)
        ending_text.set_alpha(alpha)
        screen.blit(ending_text, (WIDTH//2 - ending_text.get_width()//2, HEIGHT//2))
        
        sub_text = code_font.render("...porque nunca dejó de pensar en ella", True, PINK)
        sub_text.set_alpha(alpha)
        screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 60))
        
        # Dibujar corazón grande
        if alpha > 50:
            heart_size = 30
            heart_pos = (WIDTH//2, HEIGHT//2 + 120)
            heart_alpha = min(255, alpha * 2)
            heart_surface = pygame.Surface((heart_size * 2, heart_size * 2), pygame.SRCALPHA)
            pygame.draw.polygon(heart_surface, (*HEART_COLOR, heart_alpha), [
                (heart_size, 0),
                (heart_size * 0.5, heart_size * 0.5),
                (0, 0),
                (0, heart_size * 0.5),
                (heart_size, heart_size * 1.5),
                (heart_size * 2, heart_size * 0.5),
                (heart_size * 2, 0),
                (heart_size * 1.5, heart_size * 0.5),
            ])
            screen.blit(heart_surface, (heart_pos[0] - heart_size, heart_pos[1] - heart_size))
        
        pygame.display.flip()
        time.sleep(0.05)
    
    time.sleep(5)

def run_game():
    global days, animation_started
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not animation_started:
                if event.type == pygame.MOUSEMOTION:
                    start_button.is_hovered(mouse_pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_hovered(mouse_pos):
                        animation_started = True
                        time.sleep(0.5)
            
        if not animation_started:
            draw_welcome_screen()
        else:
            draw_animation_screen()
            
            if days == 0:
                time.sleep(2)  # Pausa inicial
                days = 1
            else:
                time.sleep(0.08)
                days += 1
                
                # Final de la animación
                if days >= max_days:
                    handle_ending()
                    running = False
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()