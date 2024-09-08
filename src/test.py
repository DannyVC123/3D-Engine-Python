import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 800
window_height = 600

# Create the window
window = pygame.display.set_mode((window_width, window_height))

# Set window title
pygame.display.set_caption("Simple Pygame Window")

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the window with a color (RGB)
    window.fill((0, 128, 255))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
