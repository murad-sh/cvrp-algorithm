import random
from utils import calculate_distance_matrix, calculate_fitness
from random_search import RandomSearch
from greedy_search import GreedySearch
from file_handler import read_file


class GeneticAlgorithm:
    def __init__(self, dimension, capacity, node_coords, demands, depot):
        self.dimension = dimension
        self.capacity = capacity
        self.node_coords = node_coords
        self.demands = demands
        self.depot = depot
        self.distance_matrix = calculate_distance_matrix(self.node_coords)
        self.random_search = RandomSearch(
            dimension, capacity, node_coords, demands, depot
        )
        self.greedy_search = GreedySearch(
            dimension, capacity, node_coords, demands, depot
        )
        self.population = None

    def generate_initial_population(self, population_size=100):
        population = []
        greedy_population_size = int(population_size * 0.8)
        random_population_size = population_size - greedy_population_size

        for _ in range(greedy_population_size):
            population.append(self.greedy_search.generate_randomized_greedy_solution())

        for _ in range(random_population_size):
            population.append(self.random_search.generate_random_solution())

        return population

    def calculate_fitness_population(self, population):
        return [
            (individual, calculate_fitness(individual, self.distance_matrix))
            for individual in population
        ]

    def tournament_selection(self, population_fitness, tournament_size=5):
        tournament = random.sample(population_fitness, tournament_size)
        tournament.sort(key=lambda x: x[1][0])
        return tournament[0][0]

    def get_flattened_solution(self, solution):
        return [node for route in solution for node in route if node != self.depot]

    def crossover_ox(self, parent1, parent2):
        parent1_flat = self.get_flattened_solution(parent1)
        parent2_flat = self.get_flattened_solution(parent2)

        crossover_point1 = random.randint(0, len(parent1_flat) - 1)
        crossover_point2 = random.randint(0, len(parent1_flat) - 1)

        if crossover_point1 > crossover_point2:
            crossover_point1, crossover_point2 = crossover_point2, crossover_point1

        child_flat = [-1] * len(parent1_flat)
        child_flat[crossover_point1:crossover_point2] = parent1_flat[
            crossover_point1:crossover_point2
        ]

        p2_index = 0
        for i in range(len(child_flat)):
            if child_flat[i] == -1:
                while parent2_flat[p2_index] in child_flat:
                    p2_index += 1
                child_flat[i] = parent2_flat[p2_index]

        child = []
        current_route = [self.depot]
        current_demand = 0
        for node in child_flat:
            node_demand = self.demands[node - 1][1]
            if current_demand + node_demand <= self.capacity:
                current_route.append(node)
                current_demand += node_demand
            else:
                current_route.append(self.depot)
                child.append(current_route)
                current_route = [self.depot, node]
                current_demand = node_demand
        current_route.append(self.depot)
        child.append(current_route)

        return child

    def swap_mutation(self, individual, mutation_rate=0.05):
        for route in individual:
            if len(route) > 3 and random.random() < mutation_rate:
                idx1, idx2 = random.sample(range(1, len(route) - 1), 2)
                route[idx1], route[idx2] = route[idx2], route[idx1]
        return individual

    def run(
        self,
        generations=1000,
        population_size=100,
        crossover_rate=0.8,
        mutation_rate=0.05,
        tournament_size=5,
    ):
        self.population = self.generate_initial_population()

        best_fitness = float("inf")
        worst_fitness = float("-inf")
        total_fitness_sum = 0

        for generation in range(generations):
            new_population = []
            population_fitness = self.calculate_fitness_population(self.population)

            generation_best_fitness = float("inf")
            generation_worst_fitness = float("-inf")

            for individual, fitness in population_fitness:
                total_fitness_sum += fitness[0]
                if fitness[0] < generation_best_fitness:
                    generation_best_fitness = fitness[0]
                if fitness[0] > generation_worst_fitness:
                    generation_worst_fitness = fitness[0]

            # Update overall best and worst fitness
            if generation_best_fitness < best_fitness:
                best_fitness = generation_best_fitness
            if generation_worst_fitness > worst_fitness:
                worst_fitness = generation_worst_fitness

            for _ in range(population_size):
                # Selection
                parent1 = self.tournament_selection(population_fitness, tournament_size)
                parent2 = self.tournament_selection(population_fitness, tournament_size)

                # Crossover
                if random.random() < crossover_rate:
                    child = self.crossover_ox(parent1, parent2)
                else:
                    child = random.choice([parent1, parent2])

                # Mutation
                child = self.swap_mutation(child, mutation_rate)

                new_population.append(child)

            # Elitism
            self.population = sorted(
                self.population + new_population,
                key=lambda x: calculate_fitness(x, self.distance_matrix)[0],
            )[:population_size]

        average_fitness = total_fitness_sum / (generations * population_size)

        best_individual = self.population[0]
        best_fitness, best_total_distance, best_number_of_vehicles = calculate_fitness(
            best_individual, self.distance_matrix
        )

        return (
            best_individual,
            best_fitness,
            worst_fitness,
            average_fitness,
            best_total_distance,
            best_number_of_vehicles,
        )
