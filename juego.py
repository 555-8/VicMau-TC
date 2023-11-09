import pygame
import random

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

# Bucle principal del juego
running = True
guess = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Verificar la suposición del jugador
                if guess == number_to_guess:
                    print("¡Correcto! Has adivinado el número.")
                    running = False
                elif guess < number_to_guess:
                    print("Demasiado bajo. Intenta de nuevo.")
                else:
                    print("Demasiado alto. Intenta de nuevo.")
                guess = 0
            elif event.key == pygame.K_BACKSPACE:
                # Eliminar el último dígito de la suposición
                guess = guess // 10
            elif pygame.K_0 <= event.key <= pygame.K_9:
                # Agregar dígito a la suposición
                guess = guess * 10 + int(pygame.key.name(event.key))

    # Dibujar la pantalla
    screen.fill(white)
    text = font.render(f"Adivina el número: {guess}", True, black)
    screen.blit(text, (10, 10))
    pygame.display.flip()

# Salir del juego
pygame.quit()
