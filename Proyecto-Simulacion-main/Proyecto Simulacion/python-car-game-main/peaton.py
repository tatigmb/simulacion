import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla principal
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación con Clase Personaje")

# Cargar la imagen de fondo
background_image = pygame.image.load("C:/Users/Dell-Latitude/Downloads/Proyecto-Simulacion-main/Proyecto Simulacion/python-car-game-main/images/urbano.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Función para escalar la imagen
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

# Cargar las animaciones del jugador
animaciones = []
scale = 0.3  # Valor de escala
for i in range(5):
    img = pygame.image.load(f"C:/Users/Dell-Latitude/Downloads/Proyecto-Simulacion-main/Proyecto Simulacion/python-car-game-main/images/player_{i}.png")
    img = escalar_img(img, scale)
    animaciones.append(img)

# Definición de la clase Personaje
class Personaje:
    def __init__(self, x, y, animaciones, velocidad=1):
        self.x = x
        self.y = y
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.velocidad = velocidad
        self.flip = False

    def mover(self, keys):
        delta_x = 0  # Inicializamos delta_x

        if keys[pygame.K_RIGHT]:
            self.x += self.velocidad
            delta_x = self.velocidad  # Movimiento hacia la derecha
        if keys[pygame.K_LEFT]:
            self.x -= self.velocidad
            delta_x = -self.velocidad  # Movimiento hacia la izquierda
        if keys[pygame.K_UP]:
            self.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.y += self.velocidad

        # Actualizar el valor de flip según el movimiento en el eje X
        if delta_x < 0:
            self.flip = True  # Voltear la imagen si se mueve a la izquierda
        if delta_x > 0:
            self.flip = False  # No voltear la imagen si se mueve a la derecha

        return delta_x  # Retornar delta_x para saber si hay movimiento

    def dibujar(self, screen):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(imagen_flip, (self.x, self.y))

    def update(self, animar=True):
        if animar:  # Solo actualiza si `animar` es True
            cooldown_animacion = 100  # Tiempo entre cambios de frames
            self.image = self.animaciones[self.frame_index]
            if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                self.frame_index = (self.frame_index + 1) % len(self.animaciones)
                self.update_time = pygame.time.get_ticks()

# Crear instancia del personaje
jugador = Personaje(100, HEIGHT - 190, animaciones)

# Variables de desplazamiento del fondo
background_x = 0
background_speed = 4

# Preguntas y respuestas
preguntas = [
    {
        "texto": "¿Qué significa una señal de alto?",
        "imagen": "C:/Users/Dell-Latitude/Downloads/Proyecto-Simulacion-main/Proyecto Simulacion/python-car-game-main/images/stop1.png",
        "opciones": ["A) Detenerse", "B) Continuar"],
        "respuesta_correcta": "A) Detenerse"
    },
    {
        "texto": "¿Qué significa esta señal de tránsito?",
        "imagen": "C:/Users/Dell-Latitude/Downloads/Proyecto-Simulacion-main/Proyecto Simulacion/python-car-game-main/images/peatonesr.png",
        "opciones": ["A) cruzar", "B) detenerse"],
        "respuesta_correcta": "B) detenerse"
    },
    {
        "texto": "¿Dónde es más seguro cruzar la calle?",
        "imagen": "C:/Users/Dell-Latitude/Downloads/Proyecto-Simulacion-main/Proyecto Simulacion/python-car-game-main/images/calle.png",
        "opciones": ["A) En cualquier lugar", "B) En un cruce peatonal", "C) Entre autos estacionados"],
        "respuesta_correcta": "B) En un cruce peatonal"
    },
    {
        "texto": "¿Qué debes hacer si ves una señal de 'Puente peatonal' cerca de una carretera?",
        "imagen": "C:/Users/Dell-Latitude/Downloads/Proyecto-Simulacion-main/Proyecto Simulacion/python-car-game-main/images/pasarela.png",
        "opciones": ["A) Cruzar por la carretera si parece seguro", "B) Solo cruzar si hay semáforo peatonal", "C) Usar el puente peatonal para cruzar de forma segura"],
        "respuesta_correcta": "C) Usar el puente peatonal para cruzar de forma segura"
    }
    # Puedes agregar más preguntas aquí
]

# Función para mostrar preguntas en una ventana emergente usando Tkinter en un hilo separado
def mostrar_pregunta():
    global show_question  # Para controlar la animación
    show_question = True

    pregunta = random.choice(preguntas)
    ventana = tk.Tk()
    ventana.title("Pregunta de Educación Vial")
    ventana.geometry("400x400")
    x_offset = 520  # Posición a la derecha
    y_offset = 100  # Posición hacia abajo
    ventana.geometry(f"400x400+{x_offset}+{y_offset}")
    ventana.resizable(False, False)

    pregunta_label = tk.Label(ventana, text=pregunta["texto"], font=("Arial", 14), wraplength=300)
    pregunta_label.pack(pady=10)

    img = Image.open(pregunta["imagen"])
    img = img.resize((300, 200))
    img = ImageTk.PhotoImage(img)
    imagen_label = tk.Label(ventana, image=img)
    imagen_label.image = img
    imagen_label.pack()

    def verificar_respuesta(opcion):
        global running, show_question, question_timer
        if opcion == pregunta["respuesta_correcta"]:
            messagebox.showinfo("Correcto", "¡Respuesta correcta! Continúa jugando.")
        else:
            messagebox.showerror("Incorrecto", "Respuesta incorrecta. ¡Juego terminado!")
            running = False
        ventana.destroy()
        show_question = False
        question_timer = pygame.time.get_ticks()  # Resetea el temporizador al cerrar la pregunta

    for opcion in pregunta["opciones"]:
        tk.Button(ventana, text=opcion, command=lambda opcion=opcion: verificar_respuesta(opcion)).pack(pady=5)

    ventana.mainloop()

# Bucle principal
running = True
question_timer = 0
question_interval = 10000  # Mostrar pregunta cada 10 segundos
show_question = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Solo mover fondo si el personaje se mueve y no hay pregunta
    movimiento = jugador.mover(keys)
    if not show_question:
        jugador.update(animar=movimiento != 0)

    if movimiento != 0 and not show_question:
        background_x -= background_speed if movimiento > 0 else -background_speed

    # Mostrar una pregunta cada cierto tiempo solo si no hay una pregunta activa
    if not show_question and pygame.time.get_ticks() - question_timer >= question_interval:
        show_question = True  # Indicar que hay una pregunta activa
        threading.Thread(target=mostrar_pregunta).start()

    # Ajustar la posición del fondo para un bucle continuo
    if background_x <= -WIDTH:
        background_x = 0
    elif background_x >= 0:
        background_x = -WIDTH

    # Dibujar el fondo
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + WIDTH, 0))

    # Dibujar el personaje
    jugador.dibujar(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
