import pygame
import game
import neural_network
import pso

print("Game imported:", game.Bird)
print("Neural network imported:", neural_network.predict)
print("Particles:", pso.positions.shape)

birds = []

for i in range(pso.NUM_PARTICLES):
    bird = game.bird(230,350)
    birds.append(bird)

print("Number of birds:", len(birds))

pipes = [game.Pipe(700)]