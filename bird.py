import pygame
from setting import *

class Bird:
    def __init__(self, window):
        self.bird_image = pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/Bird.png')), (80, 60))
        self.window = window
        self.height = 600
        self.acceleration = 0
        self.passed_pipes = []
        self.alive = True
        self.rect = self.bird_image.get_rect(topleft=(BIRD_X_POS, self.height))

    def update(self, deltaTime):
        self.height += self.acceleration
        self.acceleration += GRAVITATIONAL_CONSTANT * deltaTime

    def jump(self):
        self.acceleration = BIRD_JUMP_ACCELERATION

    def draw(self):
        self.rect = self.bird_image.get_rect(topleft=(BIRD_X_POS, self.height))
        self.window.blit(self.bird_image, self.rect)