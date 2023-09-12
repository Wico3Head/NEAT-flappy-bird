import pygame, random
from setting import *
from pipe import Pipe
from bird import Bird

class Game:
    def __init__(self, window, player_count):
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(LOCAL_DIR, 'Assets/background.png')), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.window = window
        self.backgrounds = [[0, 0]]
        self.pipes = [Pipe(self.window, random.randint(PIPE_GAP_MAX_HEIGHT, PIPE_GAP_MIN_HEIGHT))]
        self.birds = [Bird(window) for i in range(player_count)]
        self.alive_birds = self.birds
        self.pipe_creation_time = pygame.time.get_ticks()
        self.game_over = False

        self.alive_label = None
        self.alive_rect = None
        self.score_label = None
        self.score_rect = None

    def createPipe(self):
        self.pipes.append(Pipe(self.window, random.randint(PIPE_GAP_MAX_HEIGHT, PIPE_GAP_MIN_HEIGHT)))
        self.pipe_creation_time = pygame.time.get_ticks()

    def draw(self):
        for background_coordinates in self.backgrounds:
            self.window.blit(self.background, background_coordinates)

        for pipes in self.pipes:
            pipes.draw()

        for bird in self.birds:
            if bird.alive:
                bird.draw()

        self.alive_label = FONT.render(f"Alive: {len(self.alive_birds)}", False, "black")
        self.alive_rect = self.alive_label.get_rect(topright=(580, 100))
        if not self.game_over:
            self.score_label = FONT.render(f"Score: {len(self.alive_birds[0].passed_pipes)}", False, "black")
            self.score_rect = self.score_label.get_rect(topleft=(20, 20))
        self.window.blit(self.score_label, self.score_rect)
        self.window.blit(self.alive_label, self.alive_rect)

    def update(self, deltaTime):
        current_time = pygame.time.get_ticks()
        if current_time - self.pipe_creation_time >= PIPE_SPAWN_TIME:
            self.createPipe()

        if len(self.backgrounds) == 1 and self.backgrounds[0][0] < 0:
            self.backgrounds.append([self.backgrounds[0][0] + SCREEN_WIDTH, 0])

        for background_coordinates in self.backgrounds:
            background_coordinates[0] -= BACKGROUND_MOVE_SPEED * deltaTime         
            if background_coordinates[0] < -SCREEN_WIDTH:
                self.backgrounds.remove(background_coordinates)

        for bird in self.birds:
            if bird.alive:
                bird.update(deltaTime)

                for pipes in self.pipes:
                    if pygame.Rect.colliderect(bird.rect, pipes.uppipe_rect) or pygame.Rect.colliderect(bird.rect, pipes.downpipe_rect):
                        bird.alive = False
                        break
                    elif bird.height < 40 or bird.height > SCREEN_HEIGHT - 40:
                        bird.alive = False
                        break

                    if pipes not in bird.passed_pipes and pipes.x_position < BIRD_X_POS - 10:
                        bird.passed_pipes.append(pipes)

        self.alive_birds = list(filter(lambda x: x.alive, self.birds))

        if len(self.alive_birds) == 0:
            self.game_over = True
            return

        for pipes in self.pipes:
            pipes.x_position -= PIPE_MOVE_SPEED * deltaTime