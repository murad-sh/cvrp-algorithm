import random
from utils import calculate_distance_matrix, calculate_fitness


class RandomSearch:
    def __init__(self, dimension, capacity, node_coords, demands, depot):
        self.dimension = dimension
        self.capacity = capacity
        self.node_coords = node_coords
        self.demands = demands
        self.depot = depot
        self.distance_matrix = calculate_distance_matrix(self.node_coords)

    def generate_random_solution(self):
        remaining_customers = list(range(1, self.dimension + 1))
        remaining_customers.remove(self.depot)

        routes = []
        current_route = []
        current_load = 0

        current_route.append(self.depot)

        while remaining_customers:
            customer = random.choice(remaining_customers)
            demand = self.demands[customer - 1][1]

            if current_load + demand <= self.capacity:
                current_route.append(customer)
                current_load += demand
                remaining_customers.remove(customer)
            else:
                current_route.append(self.depot)
                routes.append(current_route)
                current_route = [self.depot]
                current_load = 0

        current_route.append(self.depot)
        routes.append(current_route)

        return routes

    def run(self, iterations=100, alpha=1.0, beta=100.0):
        best_solution = None
        best_fitness = float("inf")
        best_total_distance = None
        best_number_of_vehicles = None

        worst_fitness = float("-inf")
        total_fitness_sum = 0

        for _ in range(iterations):
            solution = self.generate_random_solution()
            fitness, total_distance, number_of_vehicles = calculate_fitness(
                solution, self.distance_matrix, alpha, beta
            )

            total_fitness_sum += fitness
            if fitness > worst_fitness:
                worst_fitness = fitness

            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = solution
                best_total_distance = total_distance
                best_number_of_vehicles = number_of_vehicles

        average_fitness = total_fitness_sum / iterations

        return (
            best_solution,
            best_fitness,
            worst_fitness,
            average_fitness,
            best_total_distance,
            best_number_of_vehicles,
        )
