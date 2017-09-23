import pygame_textinput
import pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInput()

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

paused = True

while True:
    screen.fill((225, 225, 225))
    if paused == False:
        pygame.draw.rect(screen, (0,0,0), (20, 20, 10, 10))
    if paused == True:
        # Feed it with events every frame
        textinput.update(pygame.event.get())
        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (10, 10))
    
    pygame.display.update()
    clock.tick(30)
