import numpy as np

NUM_PARTICLES = 10
NUM_PARAMETERS = 49
NUM_GENERATIONS = 50
w = 0.5
c1 = 2.0
c2 = 2.0


# Initialize particle position
positions = np.random.randn(NUM_PARTICLES,NUM_PARAMETERS)

# Initialize particle Velocity
velocities = np.random.randn(NUM_PARTICLES,NUM_PARAMETERS)

# Initialize personal best positions
pbest_positions = positions.copy()

#Initialize personal best best fitness
pbest_fitness = np.full(NUM_PARTICLES,-np.inf)


# Initialize global best position
gbest_position = None
gbest_fitness = -np.inf

# partical temporary fitness score

fitness = np.array([5,10,3,8,6,2,9,4,7,1])

# Compare each particle with its personal best score
for i in range (NUM_PARTICLES):
    if  fitness[i]> pbest_fitness[i]:
        pbest_fitness[i] = fitness[i]
        pbest_positions[i] = positions[i].copy()

best_score = pbest_fitness.max()
print(best_score)

partical_best_score = pbest_fitness.argmax()
print(partical_best_score)

gbest_fitness = best_score

gbest_position = pbest_positions[partical_best_score].copy()


for generation in range(NUM_GENERATIONS):
    for i in range(NUM_PARTICLES):
        # 1. Calculate inertia
        inertia_value = w*velocities[i]
        # 2. Random values r1 and r2
        r1 = np.random.rand()
        r2 = np.random.rand()
        #3.calcualte the cognitive component 
        cogitive_component = c1*r1*(pbest_positions[i]-positions[i])

        #4.calcualte the social component
        social_component = c2*r2*(gbest_position-positions[i])

        #5.finding new velocity vlaue 
        new_velocity = inertia_value+cogitive_component+social_component
    
        #6.Updating new velocity 
        velocities[i] = new_velocity.copy()
    
        #7.Updating new position
        new_position = positions[i] + new_velocity
        positions[i] = new_position.copy()

        new_fitness = fitness[i]

        #8.  
        if new_fitness > pbest_fitness[i]:
            pbest_fitness[i] = new_fitness
            pbest_positions[i] = positions[i].copy()
        
        
        fitness[i] = new_fitness

    # 9. Update global best
    best_score = pbest_fitness.max()
    partical_best_score = pbest_fitness.argmax()

    if best_score > gbest_fitness:
        gbest_fitness = best_score
        gbest_position = pbest_positions[partical_best_score].copy()

