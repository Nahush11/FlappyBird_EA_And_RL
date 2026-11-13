import numpy as np
import game
import pso 
# Neural network architecture

INPUT = 4
HIDDEN = 8
OUTPUT = 1

def get_inputs(bird, pipe, previous_y):

    # 1. Bird height
    normalized_height = bird.y / game.WIN_HEIGHT

    # 2. Bird vertical movement
    bird_velocity = bird.y - previous_y
    normalized_velocity = bird_velocity / 18

    # 3. Distance to pipe
    pipe_distance = pipe.x - bird.x
    normalized_distance = pipe_distance / game.WIN_WIDTH

    # 4. Difference between bird and gap center
    gap_center = (pipe.height + pipe.bottom) / 2
    gap_difference = bird.y - gap_center
    normalized_gap_difference = gap_difference / game.WIN_HEIGHT

    inputs = np.array([
        normalized_height,
        normalized_velocity,
        normalized_distance,
        normalized_gap_difference
    ])
    return inputs
# Temporary test objects
bird = game.Bird(230, 300)
pipe = game.Pipe(380)

def predict(inputs,particle):
    # Extract weights and biases
    weights_input_hidden = particle[0:32].reshape(INPUT,HIDDEN)
    weights_hidden_output = particle[32:40].reshape(HIDDEN, OUTPUT)

    print("Input-Hidden:", weights_input_hidden.shape)
    print("Hidden-Output:", weights_hidden_output.shape)

    bias_hidden = particle[40:48].reshape(1, HIDDEN)
    bias_output = particle[48:49].reshape(1, OUTPUT)

    # Calculate hidden layer
    hidden_input = np.dot(inputs,weights_input_hidden)+ bias_hidden
    hidden_output = np.maximum(0, hidden_input)

    # Calculate output layer
    output_input = np.dot(hidden_output, weights_hidden_output)+bias_output
    output = 1 / (1 +np.exp(-output_input))
    print("Final Output:", output)

    return output

bird = game.Bird(230, 300)
pipe = game.Pipe(380)

previous_y = 295
inputs = get_inputs(bird, pipe, previous_y)

print("Neural Network Inputs:", inputs)
for i in range(pso.NUM_PARTICLES):

    particle = pso.positions[i]

    result = predict(inputs,particle)


    if result > 0.5:
        print("Particle:", i, "JUMP")
    else:
        print("Particle:", i, "DON'T JUMP")

    print("Particle:",i,"Prediction:",result)
