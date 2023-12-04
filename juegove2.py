import pygame
import random
import sqlite3
import threading
import time

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de Adivinanzas")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Número aleatorio para adivinar
number_to_guess = random.randint(1, 100)

# Obtener nombre del jugador (cambiar "Jugador" por el nombre que prefieras)
player_name = input("Ingresa tu nombre: ") or "Jugador"

# Bucle principal del juego
running = True
attempts = 0  # Nuevo: contador de intentos
guess = 0  # Nuevo: variable para almacenar la suposición del jugador
guess_lock = threading.Lock()  # Nuevo: cerrojo para sincronización

# Función para dibujar la pantalla
def draw_screen():
    global attempts, guess
    while running:
        screen.fill(white)
        text = font.render(f"Adivina el número: {guess} - Intentos: {attempts}", True, black)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        time.sleep(0.1)

# Función para verificar la suposición del jugador
def check_guess():
    global running, guess, attempts
    while running:
        user_guess = input("Ingresa tu suposición: ")
        if user_guess.isdigit():
            with guess_lock:
                attempts += 1
                guess = int(user_guess)
        else:
            print("Por favor, ingresa un número válido.")
        time.sleep(0.1)
        check_guess_logic()

# Lógica de verificación de la suposición
def check_guess_logic():
    global guess, attempts, running
    with guess_lock:
        if guess == number_to_guess:
            print(f"¡Correcto, {player_name}! Has adivinado el número en {attempts} intentos.")
            running = False
        elif guess < number_to_guess:
            print("Demasiado bajo. Intenta de nuevo.")
        else:
            print("Demasiado alto. Intenta de nuevo.")

# Iniciar hilos
draw_thread = threading.Thread(target=draw_screen)
check_guess_thread = threading.Thread(target=check_guess)

draw_thread.start()
check_guess_thread.start()

# Esperar a que terminen los hilos
draw_thread.join()
check_guess_thread.join()

# Guardar puntuación en la base de datos solo si se adivina correctamente
if guess == number_to_guess:
    conn = sqlite3.connect("puntuaciones.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO puntuaciones VALUES (?, ?)", (player_name, attempts))
    conn.commit()
    conn.close()

# Mostrar las mejores puntuaciones
conn = sqlite3.connect("puntuaciones.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM puntuaciones ORDER BY puntuacion ASC LIMIT 5")

print("\nMejores puntuaciones:")
for row in cursor.fetchall():
    print(f"{row[0]} - {row[1]} intentos")

# Cerrar la conexión
conn.close()

# Salir del juego
pygame.quit()