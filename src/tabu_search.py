import random
from utils import calculate_distance_matrix, calculate_fitness
from file_handler import read_file
from random_search import RandomSearch


class TabuSearch:
    def __init__(self, dimension, capacity, node_coords, demands, depot, tabu_tenure=10):
        self.dimension = dimension
        self.capacity = capacity
        self.node_coords = node_coords
        self.demands = demands
        self.depot = depot
        self.distance_matrix = calculate_distance_matrix(self.node_coords)
        self.tabu_list = []
        self.tabu_tenure = tabu_tenure
        self.best_solution = None
        self.best_cost = float('inf')

    def generate_initial_solution(self):
        initial_solution = RandomSearch(
            self.dimension, self.capacity, self.node_coords, self.demands, self.depot
        ).generate_random_solution()
        return initial_solution

    def get_neighbors(self, solution):
        neighbors = []
        for route_idx, route in enumerate(solution):
            for i in range(1, len(route) - 1):
                for j in range(i + 1, len(route) - 1):
                    if route[i] != self.depot and route[j] != self.depot:
                        new_route = route[:]
                        new_route[i], new_route[j] = new_route[j], new_route[i]
                        new_solution = solution[:]
                        new_solution[route_idx] = new_route
                        neighbors.append(new_solution)
        return neighbors

    def is_tabu(self, move):
        return move in self.tabu_list

    def add_to_tabu_list(self, move):
        self.tabu_list.append(move)
        if len(self.tabu_list) > self.tabu_tenure:
            self.tabu_list.pop(0)

    def run(self, iterations=1000):
        current_solution = self.generate_initial_solution()
        current_cost = calculate_fitness(current_solution, self.distance_matrix)[0]
        self.best_solution = current_solution
        self.best_cost = current_cost

        best_fitness = float("inf")
        worst_fitness = float("-inf")
        total_fitness_sum = 0

        for iteration in range(iterations):
            neighbors = self.get_neighbors(current_solution)
            best_neighbor = None
            best_neighbor_cost = float('inf')

            for neighbor in neighbors:
                neighbor_cost = calculate_fitness(neighbor, self.distance_matrix)[0]
                move = (current_solution, neighbor)
                if not self.is_tabu(move) and neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost

            if best_neighbor and best_neighbor_cost < self.best_cost:
                self.best_solution = best_neighbor
                self.best_cost = best_neighbor_cost

            current_solution = best_neighbor
            current_cost = best_neighbor_cost
            self.add_to_tabu_list((current_solution, best_neighbor))

            total_fitness_sum += current_cost

            if current_cost < best_fitness:
                best_fitness = current_cost
            if current_cost > worst_fitness:
                worst_fitness = current_cost

        average_fitness = total_fitness_sum / iterations

        best_individual = self.best_solution
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
