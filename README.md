# Capacitated Vehicle Routing Problem (CVRP)

This repository contains solutions for the Capacitated Vehicle Routing Problem (CVRP), a classic optimization problem in logistics and transportation. The CVRP involves determining the optimal set of routes for a fleet of vehicles to deliver goods to a set of customers, starting and ending at a depot. Each vehicle has a maximum capacity, and the goal is to minimize the total distance traveled while ensuring that the demand of each customer is met without exceeding the vehicle capacities.

## Implemented Algorithms

### Random Search

Generates random solutions to the CVRP by randomly selecting customers for the routes, ensuring the capacity constraint is respected. It evaluates multiple random solutions and selects the best one.

### Greedy Search

Constructs a solution incrementally by always selecting the nearest customer that doesn't violate the capacity constraint.

There are 2 implemented versions:

- Standard: Constructs a solution incrementally by always selecting the nearest customer that doesn't violate the capacity constraint.
- Randomized Greedy Search: Adds randomness by sometimes selecting one of the k-nearest customers instead of the nearest, to explore different potential solutions.

### Tabu Search

An iterative optimization method for the CVRP that explores neighboring solutions by making local changes, such as swapping customers between routes. It uses a tabu list to avoid revisiting recently explored solutions, enhancing the search for a global optimum. The best solution found during the process is selected.

### Genetic Algorithm

An evolutionary algorithm inspired by natural selection.

#### Initial Population:

The initial population consists of solutions where 80% are generated using a greedy heuristic approach, and 20% are randomly generated solutions.

#### Selection (Tournament Selection):

Tournament selection is used to choose parent solutions based on their fitness scores. Each tournament selects a subset of solutions randomly and picks the best-performing solution among them.

#### Crossover (Ordered Crossover - OX):

Ordered crossover combines genetic material from two parent solutions to create new offspring.

##### Steps

1. Flattening Parents: Parents are flattened into linear lists of nodes.

2. Crossover Points: Two points are randomly chosen within these lists.

3. Creating Offspring: Offspring inherit a segment from one parent and fill the rest with nodes from the other parent, ensuring all nodes are included while respecting vehicle capacity constraints.

#### Mutation (Swap Mutation):

Swap mutation randomly exchanges positions of nodes within routes in offspring solutions.

## Fitness Criteria

Fitness is computed using the formula:

```
fitness = alpha * total_distance + beta * number_of_vehicles
```

where `total_distance` represents the total travel distance of all vehicles in the solution, and `number_of_vehicles` is the count of vehicles used.
`Alpha (𝛼)` and `Beta (𝛽)` are coefficients that balance the importance between minimizing total distance and minimizing the number of vehicles, respectively. Lower fitness values indicate better solutions.

## Customizing Experiments

### Running All Algorithms

To run all algorithms, use the `run_all` function. This function executes all algorithms on the specified problem instance and reports the best, worst, and average fitness across multiple executions. You have the flexibility to adjust all algorithm parameters dynamically by providing them as arguments when invoking the `.run()` method.

### Running Experiments for the different parameters

You can customize the parameters (population_size, crossover_rate, mutation_rate) by modifying the respective arrays in the main script and using the `run_experiment` function. This function iterates over the specified parameter values, runs the GA with each value, and records the best, worst, and average fitness in separate CSV files for analysis.
