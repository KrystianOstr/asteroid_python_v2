from asyncio import events
import pygame
import sys


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))


# basic setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
clock = pygame.time.Clock()

# background

background_surface = pygame.image.load("./graphics/background.png").convert()

# sprite groups

spaceship_group = pygame.sprite.Group()


# sprite creation

ship = Ship(spaceship_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # delta
    dt = clock.tick() / 1000

    # background
    screen.blit(background_surface, (0, 0))

    # graphics
    spaceship_group.draw(screen)

    pygame.display.update()

    clock.tick(60)
