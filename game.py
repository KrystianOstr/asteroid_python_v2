import pygame
import sys
from random import randint, uniform


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

        self.can_shoot = True
        self.shoot_time = 0

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(laser_group, ship.rect.midtop)
            laser_sound.play()

    def laser_timer(self, duration=500):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > duration:
                self.can_shoot = True

    def meteor_collision(self):
        if pygame.sprite.spritecollide(
            self, meteor_group, False, pygame.sprite.collide_mask
        ):
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()

    def update(self):
        self.input_position()
        self.laser_shoot()
        self.laser_timer()

        self.meteor_collision()


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 800

    def meteor_collision(self):
        if pygame.sprite.spritecollide(
            self, meteor_group, True, pygame.sprite.collide_mask
        ):
            explosion_sound.play()
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.meteor_collision()

        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        meteor_surface = pygame.image.load("./graphics/meteor.png").convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surface.get_size()) * uniform(0.5, 1.5)
        self.scaled_surface = pygame.transform.scale(meteor_surface, meteor_size)
        self.image = self.scaled_surface
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1).normalize()
        self.speed = randint(400, 600)

        self.rotation = 0
        self.rotation_speed = randint(20, 50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotate_surface = pygame.transform.rotozoom(
            self.scaled_surface, self.rotation, 1
        )
        self.image = rotate_surface
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()

        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()


class Score:
    def __init__(self):
        self.font = pygame.font.Font("./graphics/subatomic.ttf", 50)

    def display(self):
        score_text = f"Score: {pygame.time.get_ticks() // 1000}"
        text_surf = self.font.render(score_text, True, "white")
        text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        screen.blit(text_surf, text_rect)
        pygame.draw.rect(
            screen, "white", text_rect.inflate(30, 30), width=8, border_radius=5
        )


# basic setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
clock = pygame.time.Clock()

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 800)

# background

background_surface = pygame.image.load("./graphics/background.png").convert()

# sounds

explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
laser_sound = pygame.mixer.Sound("./sounds/laser.ogg")
background_music = pygame.mixer.music.load("./sounds/background_music.mp3")
pygame.mixer_music.play(-1)
pygame.mixer_music.set_volume(0.2)

# sprite groups

spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()


# sprite creation

ship = Ship(spaceship_group)
score = Score()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == meteor_timer:
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            meteor_y_pos = randint(-100, -50)
            # y_pos = 300
            Meteor(meteor_group, (meteor_x_pos, meteor_y_pos))

    # delta
    dt = clock.tick(60) / 1000

    # background
    screen.blit(background_surface, (0, 0))

    # update

    spaceship_group.update()
    laser_group.update()
    meteor_group.update()
    score.display()

    # graphics
    laser_group.draw(screen)
    meteor_group.draw(screen)
    spaceship_group.draw(screen)

    pygame.display.update()

    clock.tick(60)
