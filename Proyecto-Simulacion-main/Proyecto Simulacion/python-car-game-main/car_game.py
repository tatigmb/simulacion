import pygame
import sys
import random
import subprocess
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación STEAM")

# Definir la ruta base de las imágenes
base_path = os.path.join("C:", os.sep, "Users", "Dell-Latitude", "Downloads", "Proyecto-Simulacion-main", "Proyecto Simulacion", "python-car-game-main", "images")

# Cargar la imagen de fondo del menú
menu_background_image = pygame.image.load(os.path.join(base_path, "vectors.jpg"))
menu_background_image = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))

# Cargar la imagen de fondo de la simulación
background_image = pygame.image.load(os.path.join(base_path, "vector.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Cargar la imagen del vehículo
player_car_image = pygame.image.load(os.path.join(base_path, "car1.png"))
player_car_image = pygame.transform.scale(player_car_image, (400, 300))

# Cargar las imágenes de las señales de tránsito
stop_sign_image = pygame.image.load(os.path.join(base_path, "stop1.png"))
stop_sign_image = pygame.transform.scale(stop_sign_image, (300, 200))

contra_sign_image = pygame.image.load(os.path.join(base_path, "contramano.png"))
contra_sign_image = pygame.transform.scale(contra_sign_image, (100, 200))

cruz_sign_image = pygame.image.load(os.path.join(base_path, "cruz.png"))
cruz_sign_image = pygame.transform.scale(cruz_sign_image, (300, 200))

t_sign_image = pygame.image.load(os.path.join(base_path, "t.png"))
t_sign_image = pygame.transform.scale(t_sign_image, (300, 200))

triangulo_sign_image = pygame.image.load(os.path.join(base_path, "triangulo.png"))
triangulo_sign_image = pygame.transform.scale(triangulo_sign_image, (100, 200))

verde_sign_image = pygame.image.load(os.path.join(base_path, "verde.png"))
verde_sign_image = pygame.transform.scale(verde_sign_image, (100, 200))

zona_sign_image = pygame.image.load(os.path.join(base_path, "zona_escolar.png"))
zona_sign_image = pygame.transform.scale(zona_sign_image, (300, 200))

giro_sign_image = pygame.image.load(os.path.join(base_path, "giroi.png"))
giro_sign_image = pygame.transform.scale(giro_sign_image, (300, 200))

# Variables de la simulación
player_car_x = WIDTH // 2 - 300
player_car_y = 200
background_speed = 4
background_x = 0
obstacles = []
obstacle_timer = 0
obstacle_spawn_rate = random.randint(300, 400)
alert_message = None

# Colores y fuente
WHITE = (230, 235, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 200)
font = pygame.font.Font(None, 48)
bold_font = pygame.font.Font(None, 60)

# Variables para el parpadeo del texto
blink_timer = 0
blink_state = True

# Función para mostrar el menú
def mostrar_menu():
    global blink_timer, blink_state
    menu_running = True
    modo_seleccionado = None
    while menu_running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_peaton_rect.collidepoint(mouse_x, mouse_y):
                    print("Modo Peatón seleccionado")
                    ruta_peaton = os.path.join("C:", os.sep, "Users", "Dell-Latitude", "Downloads", "Proyecto-Simulacion-main", "Proyecto Simulacion", "python-car-game-main", "peaton.py")
                    subprocess.run(['python', ruta_peaton])
                elif boton_conductor_rect.collidepoint(mouse_x, mouse_y):
                    print("Modo Conductor seleccionado")
                    modo_seleccionado = "conductor"
                    menu_running = False  # Salir del menú
                elif boton_salir_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # Salir del juego

        # Dibujar el fondo del menú
        screen.blit(menu_background_image, (0, 0))

        # Controlar el parpadeo del texto
        blink_timer += 1
        if blink_timer > 200:  # Cambiar el estado cada 30 fotogramas
            blink_state = not blink_state
            blink_timer = 0

        # Dibujar el título del menú con efecto de parpadeo
        if blink_state:
            titulo_texto = bold_font.render("Elegir Modo de Juego", True, BLACK)
            titulo_rect = titulo_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
            screen.blit(titulo_texto, titulo_rect)

        # Dibujar los botones
        boton_peaton_texto = font.render("Jugar como Peatón", True, BLACK)
        boton_peaton_rect = boton_peaton_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        if boton_peaton_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, boton_peaton_rect.inflate(20, 20))
        else:
            pygame.draw.rect(screen, WHITE, boton_peaton_rect.inflate(20, 20))
        screen.blit(boton_peaton_texto, boton_peaton_rect)

        boton_conductor_texto = font.render("Jugar como Conductor", True, BLACK)
        boton_conductor_rect = boton_conductor_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        if boton_conductor_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, boton_conductor_rect.inflate(20, 20))
        else:
            pygame.draw.rect(screen, WHITE, boton_conductor_rect.inflate(20, 20))
        screen.blit(boton_conductor_texto, boton_conductor_rect)

        # Agregar el botón "Salir"
        boton_salir_texto = font.render("Salir", True, BLACK)
        boton_salir_rect = boton_salir_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170))
        if boton_salir_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, boton_salir_rect.inflate(20, 20))
        else:
            pygame.draw.rect(screen, WHITE, boton_salir_rect.inflate(20, 20))
        screen.blit(boton_salir_texto, boton_salir_rect)

        # Actualizar la pantalla
        pygame.display.flip()

    return modo_seleccionado

# Función para dibujar el cruce peatonal
def draw_crosswalk(x, y):
    line_width = 10    # Grosor de cada línea
    line_length = 45   # Largo de cada línea
    line_spacing = 22  # Espaciado entre cada línea

    num_lines = 6  # Número de líneas del cruce peatonal
    for i in range(num_lines):
        pygame.draw.line(screen, (255, 255, 255), 
                         (x, y + i * line_spacing),  # Posición inicial (x, y)
                         (x + line_length, y + i * line_spacing), 
                         line_width)

# Mostrar el menú
modo = mostrar_menu()

# Solo iniciar la simulación si se seleccionó el modo "conductor"
if modo == "conductor":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if boton_volver_menu_rect.collidepoint(mouse_x, mouse_y):
                    modo = mostrar_menu()
                    if modo != "conductor":
                        running = False

        # Dibujar el botón "Volver al Menú" en la esquina superior izquierda
        boton_volver_menu_texto = font.render("Menú", True, BLACK)
        boton_volver_menu_rect = boton_volver_menu_texto.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, WHITE, boton_volver_menu_rect.inflate(20, 20))
        screen.blit(boton_volver_menu_texto, boton_volver_menu_rect)

        # Control del auto del jugador
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_RIGHT]:
            background_x -= background_speed
            for i in range(len(obstacles)):
                type_, x, y = obstacles[i]
                x -= background_speed
                obstacles[i] = (type_, x, y)
            moved = True

        if keys[pygame.K_LEFT]:
            background_x += background_speed
            for i in range(len(obstacles)):
                type_, x, y = obstacles[i]
                x += background_speed
                obstacles[i] = (type_, x, y)
            moved = True

        # Reiniciar la posición del fondo
        if background_x <= -WIDTH:
            background_x = 0
        elif background_x >= 0:
            background_x = -WIDTH

        # Generar obstáculos a intervalos
        if moved:
            obstacle_timer += 1
            if obstacle_timer > obstacle_spawn_rate:
                obstacle_type = random.choice(['crosswalk', 'stop_sign', 'contra_sign', 'cruz_sign', 't_sign', 'triangulo_sign', 'verde_sign', 'zona_sign', 'giro_sign'])
                if obstacle_type == 'crosswalk':
                    obstacles.append(('crosswalk', WIDTH, HEIGHT - 215))
                elif obstacle_type == 'stop_sign':
                    obstacles.append(('stop_sign', WIDTH, HEIGHT - 400))
                elif obstacle_type == 'contra_sign':
                    obstacles.append (('contra_sign', WIDTH, HEIGHT - 400))
                elif obstacle_type == 'cruz_sign':
                    obstacles.append (('cruz_sign', WIDTH, HEIGHT - 400))
                elif obstacle_type == 'triangulo_sign':
                    obstacles.append (('triangulo_sign', WIDTH, HEIGHT - 400))
                elif obstacle_type == 'verde_sign':
                    obstacles.append (('verde_sign', WIDTH, HEIGHT - 400))  
                elif obstacle_type == 'zona_sign':
                    obstacles.append (('zona_sign', WIDTH, HEIGHT - 400))
                elif obstacle_type == 'giro_sign':
                    obstacles.append (('giro_sign', WIDTH, HEIGHT - 400))  
                else:
                    obstacles.append (('t_sign', WIDTH, HEIGHT - 400))
                obstacle_timer = 0

        # Comprobar colisión con obstáculos
        for type_, x, y in obstacles:
            if type_ == 'crosswalk' and player_car_x + 400 > x:
                alert_message = "ATENCIÓN - cruce peatonal"
            elif type_ == 'stop_sign' and player_car_x + 400 > x:
                alert_message = "Detente - Señal de PARE"
            elif type_ == 'contra_sign' and player_car_x + 400 > x:
                alert_message = "Detente - CONTRAMANO"
            elif type_ == 'cruz_sign' and player_car_x + 400 > x:
                alert_message = "ATENCIÓN - cruce de vías"
            elif type_ == 't_sign' and player_car_x + 400 > x:
                alert_message = "ATENCIÓN - bifurcación de la vía"
            elif type_ == 'triangulo_sign' and player_car_x + 400 > x:
                alert_message = "PARE - ceda el paso"
            elif type_ == 'verde_sign' and player_car_x + 400 > x:
                alert_message = "CONTINUE - semáforo en verde"
            elif type_ == 'zona_sign' and player_car_x + 400 > x:
                alert_message = "ATENCIÓN - reduce la marcha - zona escolar"
            elif type_ == 'giro_sign' and player_car_x + 400 > x:
                alert_message = "puede girar a la izquierda"
            if player_car_x + 100 > x + 70:
                alert_message = None

        # Dibujar el fondo
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + WIDTH, 0))

        # Dibujar los obstáculos
        for type_, x, y in obstacles:
            if type_ == 'crosswalk':
                draw_crosswalk(x, y)
            elif type_ == 'stop_sign':
                screen.blit(stop_sign_image, (x, y))
            elif type_ == 'contra_sign':
                screen.blit(contra_sign_image, (x, y))
            elif type_ == 'cruz_sign':
                screen.blit(cruz_sign_image, (x, y))
            elif type_ == 't_sign':
                screen.blit(t_sign_image, (x, y))
            elif type_ == 'triangulo_sign':
                screen.blit(triangulo_sign_image, (x, y))
            elif type_ == 'verde_sign':
                screen.blit(verde_sign_image, (x, y))
            elif type_ == 'zona_sign':
                screen.blit(zona_sign_image, (x, y))
            elif type_ == 'giro_sign':
                screen.blit(giro_sign_image, (x, y))

        # Mostrar la alerta si existe
        if alert_message:
            alert_surface = font.render(alert_message, True, WHITE)
            alert_rect = alert_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(screen, (0, 0, 0), alert_rect.inflate(20, 20))
            screen.blit(alert_surface, alert_rect)

        # Dibujar el auto del jugador
        screen.blit(player_car_image, (player_car_x, player_car_y))

        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()