import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")           

# Load images
bird_up = pygame.image.load("bird_wing_up.png")
bird_down = pygame.image.load("bird_wing_down.png")
background = pygame.image.load("background.png")
ground = pygame.image.load("ground.png")
pipe = pygame.image.load("pipe.png")

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_up
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.gravity = 0.5
        self.lift = -10
        self.velocity = 0
        self.is_flapping = False

    def update(self):
        if self.is_flapping:
            self.velocity = self.lift
            self.is_flapping = False
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def flap(self):
        self.is_flapping = True
        self.image = bird_up

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.image = pygame.transform.flip(pipe, False, flipped)
        self.rect = self.image.get_rect()
        if flipped:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Main game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    all_sprites = pygame.sprite.Group(bird)
    pipes = pygame.sprite.Group()

    ADDPIPE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDPIPE, 1500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
            elif event.type == ADDPIPE:
                pipe_height = random.randint(150, 450)
                top_pipe = Pipe(SCREEN_WIDTH, pipe_height - 600, flipped=True)
                bottom_pipe = Pipe(SCREEN_WIDTH, pipe_height + 150)
                all_sprites.add(top_pipe, bottom_pipe)
                pipes.add(top_pipe, bottom_pipe)

        all_sprites.update()

        if pygame.sprite.spritecollide(bird, pipes, False):
            running = False

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        screen.blit(ground, (0, SCREEN_HEIGHT - ground.get_height()))
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
