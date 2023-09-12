import pygame, sys, neat
from setting import *
from game import Game
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         os.path.join(LOCAL_DIR, 'config.txt'))

generations = 0

def main(genomes, config):
    global generations
    generations += 1

    game = Game(screen, len(genomes))
    prev_time = pygame.time.get_ticks()
    networks = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append([network, genome])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        alive_bird = list(filter(lambda x: x.alive, game.birds))[0]
        for pipes in game.pipes:
            if pipes not in alive_bird.passed_pipes:
                closest_pipe = pipes

        for index, [network, genome] in enumerate(networks):
            bird = game.birds[index]
            if bird.alive:
                output = network.activate((closest_pipe.x_position, closest_pipe.height, bird.height))
                if output[0] > 0.5:
                    bird.jump()
                genome.fitness += 1

        current_time = pygame.time.get_ticks()
        deltaTime = current_time - prev_time
        game.update(deltaTime)

        if game.game_over:
            return

        game.draw()
        pygame.display.update()
        prev_time = current_time

if __name__ == "__main__":
    p = neat.Population(config)
    p.run(main)