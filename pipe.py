import pygame
from setting import *

class Pipe:
    def __init__(self, window, height):
        self.window = window
        self.pipe = pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/pipe.png'))
        self.height = height
        self.x_position = SCREEN_WIDTH
        self.uppipe_rect = self.pipe.get_rect(bottomleft=(self.x_position, self.height-GAP_SIZE))
        self.downpipe_rect = self.pipe.get_rect(topleft=(self.x_position, self.height))

    def draw(self):
        self.uppipe_rect = self.pipe.get_rect(bottomleft=(self.x_position, self.height-GAP_SIZE))
        self.downpipe_rect = self.pipe.get_rect(topleft=(self.x_position, self.height))
        self.window.blit(self.pipe, self.downpipe_rect)
        self.window.blit(pygame.transform.flip(self.pipe, False, True), self.uppipe_rect)